import datetime
import gzip
import logging
import multiprocessing as mp
import os
import sys
import tempfile
import threading
import time
import zipfile
from abc import ABC, abstractmethod
from datetime import timedelta
from io import BytesIO
from itertools import islice
from shutil import copy

import requests
from dateutil.parser import parse as parse_datetime
from pymongo.errors import BulkWriteError
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
from urllib3 import Retry

from lib.DatabaseLayer import getInfo, setColUpdate
from lib.LogHandler import UpdateHandler
from lib.redis_q import RedisQueue
from lib.Config import Configuration

thread_local = threading.local()
logging.setLoggerClass(UpdateHandler)

logging.getLogger("urllib3").setLevel(logging.WARNING)


class DownloadHandler(ABC):
    """
    DownloadHandler is the base class for all downloads and subsequent processing of the downloaded content.
    Each download script has a derived class which handles specifics for that type of content / download.
    """

    def __init__(self, feed_type, prefix=None):
        self._end = None

        self.feed_type = feed_type

        self.prefix = prefix

        self.queue = RedisQueue(name=self.feed_type)

        self.file_queue = RedisQueue(name=f"{self.feed_type}:files")
        self.file_queue.clear()

        self.progress_bar = None

        self.last_modified = None

        self.do_process = True

        self.logger = logging.getLogger("DownloadHandler")

        self.config = Configuration()

    def __repr__(self):
        """return string representation of object"""
        return "<< DownloadHandler:{} >>".format(self.feed_type)

    def get_session(
        self,
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(429, 500, 502, 503, 504),
        session=None,
    ):
        """
        Method for returning a session object per every requesting thread
        """

        proxies = {"http": self.config.getProxy(), "https": self.config.getProxy()}

        if not hasattr(thread_local, "session"):
            session = session or requests.Session()
            retry = Retry(
                total=retries,
                read=retries,
                connect=retries,
                backoff_factor=backoff_factor,
                status_forcelist=status_forcelist,
            )

            session.proxies.update(proxies)

            adapter = HTTPAdapter(max_retries=retry)
            session.mount("http://", adapter)
            session.mount("https://", adapter)

            thread_local.session = session

        return thread_local.session

    def process_downloads(self, sites, collection):
        """
        Method to download and process files

        :param sites: List of file to download and process
        :type sites: list
        :param collection: Mongodb Collection name
        :type collection: str
        :return:
        :rtype:
        """

        worker_size = (
            int(os.getenv("WORKER_SIZE"))
            if os.getenv("WORKER_SIZE")
            else min(32, os.cpu_count() + 4)
        )

        start_time = time.time()

        thread_map(self.download_site, sites, desc="Downloading files")

        if self.do_process:
            thread_map(
                self.file_to_queue,
                self.file_queue.get_full_list(),
                desc="Processing downloaded files",
            )

            self._process_queue_to_db(worker_size, collection=collection)

            
            if "01-01-1970" != self.last_modified.strftime("%d-%m-%Y"):
                setColUpdate(self.feed_type.lower(), self.last_modified)

        self.logger.info(
            "Duration: {}".format(timedelta(seconds=time.time() - start_time))
        )

    def chunk_list(self, lst, number):
        """
        Yield successive n-sized chunks from lst.

        :param lst: List to be chunked
        :type lst: list
        :param number: Chunk size
        :type number: int
        :return: Chunked list
        :rtype: list
        """
        for i in range(0, len(lst), number):
            yield lst[i : i + number]

    def _handle_queue_progressbar(self, description):
        """
        Method for handling the progressbar during queue processing

        :param description: Description for tqdm progressbar
        :type description: str
        """
        max_len = self.queue.qsize()

        pbar = tqdm(total=max_len, desc=description)
        not_Done = True
        q_len = max_len
        dif_old = 0
        x = 0

        while not_Done:

            current_q_len = self.queue.qsize()

            if x % 10 == 0:
                
                self.logger.debug(
                    "Queue max_len: {}, current_q_len: {}, q_len: {}, dif_old: {}, cycle: {}".format(
                        max_len, current_q_len, q_len, dif_old, x
                    )
                )

            if current_q_len != 0:

                if current_q_len != q_len:
                    q_len = current_q_len
                    dif = max_len - q_len

                    pbar.update(int(dif - dif_old))

                    dif_old = dif
            else:
                pbar.update(int(max_len - dif_old))
                not_Done = False

            x += 1
            time.sleep(5)

        self.logger.debug(
            "Queue max_len: {}, q_len: {}, dif_old: {}, cycles: {}".format(
                max_len, q_len, dif_old, x
            )
        )

        pbar.close()

    def _process_queue_to_db(self, max_workers, collection):
        """
        Method to write the queued database transactions into the database given a Queue reference and Collection name

        :param max_workers: Max amount of worker processes to use; defaults to min(32, os.cpu_count() + 4)
        :type max_workers: int
        :param collection: Mongodb Collection name
        :type collection: str
        """

        pbar = mp.Process(
            target=self._handle_queue_progressbar,
            args=("Transferring queue to database",),
        )

        processes = [
            mp.Process(target=self._db_bulk_writer, args=(collection,))
            for _ in range(max_workers)
        ]
        for proc in processes:
            proc.start()
            
            self.queue.put(self._end)

        pbar.start()

        for proc in processes:
            proc.join()

        pbar.join()

    def _db_bulk_writer(self, collection, threshold=1000):
        """
        Method to act as worker for writing queued entries into the database

        :param collection: Mongodb Collection name
        :type collection: str
        :param threshold: Batch size threshold; defaults to 1000
        :type threshold: int
        """
        database = self.config.getMongoConnection()

        for batch in iter(lambda: list(islice(self.queue, threshold)), []):
            try:
                database[collection].bulk_write(batch, ordered=False)
            except BulkWriteError as err:
                self.logger.debug("Error during bulk write: {}".format(err))
                pass

    def store_file(self, response_content, content_type, url):
        """
        Method to store the download based on the headers content type

        :param response_content: Response content
        :type response_content: bytes
        :param content_type: Content type; e.g. 'application/zip'
        :type content_type: str
        :param url: Download url
        :type url: str
        :return: A working directory and a filename
        :rtype: str and str
        """
        wd = tempfile.mkdtemp()
        filename = None

        if (
            content_type == "application/zip"
            or content_type == "application/x-zip"
            or content_type == "application/x-zip-compressed"
            or content_type == "application/zip-compressed"
        ):
            filename = os.path.join(wd, url.split("/")[-1][:-4])
            self.logger.debug("Saving file to: {}".format(filename))

            with zipfile.ZipFile(BytesIO(response_content)) as zip_file:
                zip_file.extractall(wd)

        elif (
            content_type == "application/x-gzip"
            or content_type == "application/gzip"
            or content_type == "application/x-gzip-compressed"
            or content_type == "application/gzip-compressed"
        ):
            filename = os.path.join(wd, url.split("/")[-1][:-3])
            self.logger.debug("Saving file to: {}".format(filename))

            buf = BytesIO(response_content)
            with open(filename, "wb") as f:
                f.write(gzip.GzipFile(fileobj=buf).read())

        elif content_type == "application/json" or content_type == "application/xml":
            filename = os.path.join(wd, url.split("/")[-1])
            self.logger.debug("Saving file to: {}".format(filename))

            with open(filename, "wb") as output_file:
                output_file.write(response_content)

        elif content_type == "application/local":
            filename = os.path.join(wd, url.split("/")[-1])
            self.logger.debug("Saving file to: {}".format(filename))

            copy(url[7:], filename)

        else:
            self.logger.error(
                "Unhandled Content-Type encountered: {} from url".format(
                    content_type, url
                )
            )
            sys.exit(1)

        return wd, filename

    def download_site(self, url):
        if url[:4] == "file":
            self.logger.info("Scheduling local hosted file: {}".format(url))

            
            
            self.last_modified = datetime.datetime.now()

            self.logger.debug(
                "Last {} modified value: {} for URL: {}".format(
                    self.feed_type, self.last_modified, url
                )
            )

            wd, filename = self.store_file(
                response_content=b"local", content_type="application/local", url=url
            )

            if filename is not None:
                self.file_queue.put((wd, filename))
            else:
                self.logger.error(
                    "Unable to retrieve a filename; something went wrong when trying to save the file"
                )
                sys.exit(1)

        else:
            self.logger.debug("Downloading from url: {}".format(url))
            session = self.get_session()
            try:
                with session.get(url) as response:
                    try:
                        self.last_modified = parse_datetime(
                            response.headers["last-modified"], ignoretz=True
                        )
                    except KeyError:
                        self.logger.error(
                            "Did not receive last-modified header in the response; setting to default "
                            "(01-01-1970) and force update! Headers received: {}".format(
                                response.headers
                            )
                        )
                        
                        self.last_modified = parse_datetime("01-01-1970")

                    self.logger.debug(
                        "Last {} modified value: {} for URL: {}".format(
                            self.feed_type, self.last_modified, url
                        )
                    )

                    i = getInfo(self.feed_type.lower())

                    if i is not None:
                        if self.last_modified == i["last-modified"]:
                            self.logger.info(
                                "{}'s are not modified since the last update".format(
                                    self.feed_type
                                )
                            )
                            self.file_queue.get_full_list()
                            self.do_process = False
                    if self.do_process:
                        content_type = response.headers["content-type"]

                        self.logger.debug(
                            "URL: {} fetched Content-Type: {}".format(url, content_type)
                        )

                        wd, filename = self.store_file(
                            response_content=response.content,
                            content_type=content_type,
                            url=url,
                        )

                        if filename is not None:
                            self.file_queue.put((wd, filename))
                        else:
                            self.logger.error(
                                "Unable to retrieve a filename; something went wrong when trying to save the file"
                            )
                            sys.exit(1)
            except Exception as err:
                self.logger.info(
                    "Exception encountered during download from: {}. Please check the logs for more information!".format(
                        url
                    )
                )
                self.logger.error(
                    "Exception encountered during the download from: {}. Error encountered: {}".format(
                        url, err
                    )
                )
                self.do_process = False

    @abstractmethod
    def process_item(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def file_to_queue(self, *args):
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def populate(self, **kwargs):
        raise NotImplementedError
