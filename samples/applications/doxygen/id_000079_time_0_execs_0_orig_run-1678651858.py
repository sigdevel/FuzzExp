#!/usr/bin/python3

from bottle import route, run, request, response, HTTPError, error, install, view, static_file, redirect
import string
import urllib3, logging
import random
import sys
import os
import json
import pyqrcode
import png
from pyqrcode import QRCode
import base64
from base64 import b64encode
from json import dumps
import boto3
import requests
from botocore.exceptions import ClientError

class out:

    INFO, WARN, ERROR = ((32, "INFO"), (33, "WARN"), (31, "ERROR"))

    @staticmethod
    def _output(message, type):
        sys.stdout.write("[\033[1;%im%s\033[0;0m] " % type + "%s\n" % message)

    @staticmethod
    def info(message):
        out._output(message, out.INFO)

    @staticmethod
    def warn(message):
        out._output(message, out.WARN)

    @staticmethod
    def error(message):
        out._output(message, out.ERROR)
        sys.exit(1)


@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static/')


@route("/", method="GET")
@view("index.tpl")
def index() :
    URL = os.environ.get('URL') # None
    try:

        response.status = 200

    except Exception as e:
        response.status = 500
        return {"status": "error", "error": str(e)}
    
    return {"URL": URL}


@route("/validation", method="GET")
@view("validation.tpl")
def index() :

    ACCESS_KEY = os.environ.get('ACCESS_KEY') # None
    SECRET_KEY = os.environ.get('SECRET_KEY') # None
    S3BUCKET_NAME = os.environ.get('S3BUCKET_NAME') # None
    S3BUCKET_URL = os.environ.get('S3BUCKET_URL') # None
    S3BUCKET_REGION = os.environ.get('S3BUCKET_REGION') # None
    URL = os.environ.get('URL') # None
    SECRET_KEY_SHORT = SECRET_KEY.split('-', 1)[0]
    try:

        response.status = 200

    except Exception as e:
        response.status = 500
        return {"status": "error", "error": str(e)}
    
    return {"ACCESS_KEY": ACCESS_KEY, "SECRET_KEY": SECRET_KEY_SHORT, "S3BUCKET_NAME": S3BUCKET_NAME,"S3BUCKET_URL":S3BUCKET_URL,"S3BUCKET_REGION":S3BUCKET_REGION, "URL": URL}



@route("/v1/qrcode", method="POST")
def getQrcode():

    try:
        postdata = request.body.read()
        ret = generatQrcode(postdata)
        print (ret)
        response.status = 200
        return {"status": "ok", "result": ret}
    except Exception as e:
        response.status = 500
        return {"status": "error", "error": str(e)}



@route("/checkhealth", method="GET")
def get_checkhealth():
    try:
        response.status = 200
        return {"status": "ok"}
    except Exception as e:
        response.status = 500
        return {"status": "error", "error": str(e)}

@route("/version", method="GET")
def get_version():
    try:
        response.status = 200
        return version
    except Exception as e:
        response.status = 500
        return {"status": "error", "error": str(e)}


@error(404)
def error404(error):
    return {"status": "error", "error": "not found"}


@route('/download/<filename:path>')
def download(filename):
    return static_file(filename, root='tmp', download=True)

##Code



def generatQrcode(postdata):
    ACCESS_KEY = os.environ.get('ACCESS_KEY') # None
    SECRET_KEY = os.environ.get('SECRET_KEY') # None
    S3BUCKET_NAME = os.environ.get('S3BUCKET_NAME') # None
    S3BUCKET_URL = os.environ.get('S3BUCKET_URL') # None
    S3BUCKET_REGION = os.environ.get('S3BUCKET_REGION') # None
    URL = os.environ.get('URL') # None
    ret = {}
    payload = json.loads(postdata)
    result = []
    text = payload["text"]
    result_format = payload["result_format"]
    size = int(payload["size"])
    IMAGE_NAME_RAND = id_generator(18)
    IMAGE_NAME = IMAGE_NAME_RAND +".png"
    IMAGE_PATH = "tmp/" + IMAGE_NAME
    ENCODING = 'utf-8'

    try:
        url = pyqrcode.create(text)
        url.png(IMAGE_NAME, scale = size)
        os.rename(IMAGE_NAME, IMAGE_PATH)

        if result_format == "base64":
            with open(IMAGE_PATH, 'rb') as open_file:
                byte_content = open_file.read()
                base64_bytes = b64encode(byte_content)
                result = base64_bytes.decode(ENCODING)
        elif result_format == "link":
            result = uploads3(ACCESS_KEY=ACCESS_KEY, SECRET_KEY=SECRET_KEY, S3BUCKET_NAME=S3BUCKET_NAME, S3BUCKET_URL=S3BUCKET_URL, S3BUCKET_REGION=S3BUCKET_REGION, IMAGE_NAME=IMAGE_NAME, IMAGE_PATH=IMAGE_PATH)

        elif result_format == "download":
            IMAGE_DL_PATH = URL + "download/" + IMAGE_NAME
            print (IMAGE_DL_PATH)
            #return redirect(IMAGE_DL_PATH) 
            result = "plop"

        else:
            result="wrong parameter for result_format: " + result_format + " is not a supported value."

        ret = result

    except Exception as e:
        raise Exception("Something Bad append generatQrcode - %s" % e)
    return ret


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def uploads3(ACCESS_KEY, SECRET_KEY, S3BUCKET_NAME, S3BUCKET_URL, S3BUCKET_REGION, IMAGE_NAME, IMAGE_PATH):

    ret = {}
    result = []
    IMAGE_FOLDER_S3 = id_generator(18)

    session = boto3.session.Session()

    s3_client = session.client(
        service_name='s3',
        region_name=S3BUCKET_REGION,
        use_ssl=True,
        endpoint_url=S3BUCKET_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
    )
##  S3_FILE_DESTINATION=IMAGE_FOLDER_S3 + "/" + IMAGE_NAME
    S3_FILE_DESTINATION=IMAGE_NAME

    with open(IMAGE_PATH, "rb") as f:
        s3_client.upload_fileobj(f, S3BUCKET_NAME, S3_FILE_DESTINATION, ExtraArgs={'ACL': 'public-read'})

        result = S3BUCKET_URL + "/" +S3BUCKET_NAME  + "/" + S3_FILE_DESTINATION
    return result

def main():
    out.info("Starting read conf")

    try:
        with open("conf.conf") as f:
            c = json.load(f)
    except IOError:
        out.error("Could not read conf.conf file (missing? permission?)")
    except ValueError:
        out.error("Could not parse conf.conf file (not valid json?)")

    try:
        global port
        port = c["http"]["port"]
    except Exception as e:
        out.error("Could not find %s on conf.conf (missing? out of scope ?)" % e)

    try:
        host = c["http"]["host"]
    except Exception as e:
        out.error("Could not find %s on conf.conf (missing? out of scope ?)" % e)

    try:
        global version
        version = c["server"]["version"]
    except Exception as e:
        out.error("Could not find %s on conf.conf (missing? out of scope ?)" % e)


    out.info("Configuration file loaded")

    out.info("Starting http server")

    logging.getLogger("wsgi").addHandler(logging.NullHandler())
    run(
        host=host,
        port=port,
        quiet=True,
        server="paste",
        use_threadpool=True,
        threadpool_workers=15,
        request_queue_size=5,
    )


if __name__ == "__main__":
    main()