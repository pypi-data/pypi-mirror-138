from tgaflow.base import BaseTask
from tgautil.download_util import DownloadUtil
from tgautil.sql_format import SQLFormat


class DownloadTask(BaseTask):
    def __init__(self, flow_id, params):
        self.task_name = 'download'
        super().__init__(flow_id, params, ['check', 'refresh'])

    def process(self):
        try:
            sqlFormat = SQLFormat()
            du = DownloadUtil({
                'name': self.params['name'],
                'sql': sqlFormat.run(self.params)

            })
            result = None
            try_num = 0

            while (not result) and try_num <= 3:
                try:
                    result = du.run()
                except Exception as e:
                    try_num = try_num + 1
                    if try_num <= 3:
                        logger.info( ' DownloadTask flow_id: %s . exception: %s . try num: %s ', self.flow_id, e, try_num)
                        time.sleep(3)
                    else:
                        error_text = f' DownloadTask flow_id: {self.flow_id} . error: {e} . try num: {try_num - 1} '
                        logger.error(error_text)
                        return False, {'exception': error_text}

            self.task_result_dict['filepath'] = result['filepath']
            self.task_result_dict['download_count'] = result['rowCount']
            if result is None:
                return False, {'result':result}
            else:
                return True, self.task_result_dict
        except Exception as e:
            error_text = f'celry task {self.flow_id} {self.task.task_name} process Exception {e}'
            logger.info(error_text)
            return False, {'exception': error_text}
