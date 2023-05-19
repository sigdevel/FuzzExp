import Queue

import mscs_consts
import mscs_data_writer as mdw
import mscs_logger as logger
import mscs_storage_blob_dispatcher as msbd


class StorageBlobListDataCollector(object):
    TIMEOUT = 3

    def __init__(self, all_conf_contents, meta_config, task_config):
        self._all_conf_contents = all_conf_contents
        self._meta_config = meta_config
        self._task_config = task_config
        self._data_writer = mdw.DataWriter()
        self._logger = logger.logger_for(self._get_logger_prefix())

        self._storage_dispatcher = msbd.StorageBlobDispatcher(
            all_conf_contents, meta_config, task_config, self._data_writer, self._logger
        )
        self._checkpointer = self._storage_dispatcher.get_checkpointer()

    def collect_data(self):
        try:
            self._logger.info('Starting to collect data.')
            self._storage_dispatcher.start()

            self._logger.info('Starting to get data from data_writer.')

            need_get_data = False
            
            
            while True:
                try:
                    events, key, ckpt = self._data_writer.get_data(
                        timeout=self.TIMEOUT)
                    if key:
                        self._checkpointer.update(key, ckpt)
                    stop = yield events, None
                    if stop:
                        self._storage_dispatcher.cancel()
                        break

                    if not self._storage_dispatcher.is_alive():
                        need_get_data = True
                        break
                except Queue.Empty:
                    if not self._storage_dispatcher.is_alive():
                        need_get_data = True
                        break
                    else:
                        continue

            if not need_get_data:
                self._checkpointer.close()
                return

            self._logger.info('Retrieve the remain data from data_writer.')

            while True:
                try:
                    events, key, ckpt = self._data_writer.get_data(block=False)
                    if key:
                        self._checkpointer.update(key, ckpt)
                    yield events, None
                except Queue.Empty:
                    break

            self._checkpointer.close()
        except Exception:
            self._logger.exception('Error occurred in collecting data.')
            try:
                self._checkpointer.close()
            except Exception:
                self._logger.exception('Closing checkpointer failed')
            self._storage_dispatcher.cancel()

    def _get_task_info(self):
        self._table_list = self._task_config.get(mscs_consts.TABLE_LIST)

    def _get_logger_prefix(self):
        account_stanza_name = self._task_config[mscs_consts.ACCOUNT]
        account_info = self._all_conf_contents[mscs_consts.ACCOUNTS][
            account_stanza_name]
        account_name = account_info.get(mscs_consts.ACCOUNT_NAME)
        pairs = [
            '{}="{}"'.format(mscs_consts.STANZA_NAME,
                             self._task_config[mscs_consts.STANZA_NAME]),
            '{}="{}"'.format(mscs_consts.ACCOUNT_NAME, account_name),
            '{}="{}"'.format(mscs_consts.CONTAINER_NAME,
                             self._task_config[mscs_consts.CONTAINER_NAME]),
            '{}="{}"'.format(mscs_consts.BLOB_LIST,
                             self._task_config.get(mscs_consts.BLOB_LIST), '')
        ]
        return '[{}]'.format(' '.join(pairs))
