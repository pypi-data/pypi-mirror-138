import json
import logging
import time
import datetime
from config.settings import TGA
from proj.models import CeleryTask
from tgautil.dingtalk import send_dingtalk_message

logger = logging.getLogger('raw_logger')

task_logger = logging.getLogger('task')


class BaseTask:
    def __init__(self, flow_id, params, depends=[]):
        # 接收参数
        self.flow_id = flow_id
        self.depends = depends
        self.task_result_dict = {
            'time_cost': 0,
        }

        self.task, create = CeleryTask.objects.get_or_create(flow_id=flow_id, task_name=self.task_name)

        if create:
            self.params = params
            self.task.params = params
            self.task.save(update_fields=['params', 'modified'])
        else:
            self.params = self.task.params

        if 'depends' in self.params:
            self.depends = self.params['depends']

        # 读取配置
        self.settings = TGA

    def handle(self):
        start_time = time.time()
        logger.info('handle task: flowid %s, task_name: %s, status %s', self.flow_id, self.task.task_name,
                    self.task.status)

        # injudge task should run or not
        if self.task.status == 2:
            return True
        elif self.task.status == 1:
            logger.info('celry task %s %s is running', self.flow_id, self.task.task_name)
            return False
        else:
            depend_success_count = CeleryTask.objects.filter(flow_id=self.flow_id, task_name__in=self.depends,
                                                             status=2).count()
            if depend_success_count < len(self.depends):
                logger.info('celry task %s %s prerequisite task not done', self.flow_id, self.task.task_name)
                return False

        # run task
        self.task.status = 1
        self.task.retry_time = self.task.retry_time + 1
        self.task.save(update_fields=['status', 'retry_time', 'modified'])

        # process 由子类继承，必须返回true or false
        success, result = self.process()

        end_time = time.time()
        result['time_cost'] = round(end_time - start_time, 4)

        if success:
            self.task.status = 2
            self.task.result = result
            self.task.save(update_fields=['status', 'result', 'modified'])
        else:
            send_dingtalk_message(json.dumps({'result': result, 'flow_id': self.flow_id, 'params': self.params}))
            self.task.status = 3
            self.task.result = result
            self.task.save(update_fields=['status', 'result', 'modified'])

        task_logger.info(
            json.dumps(
                {
                    'cerated': self.task.created,
                    'task_name': self.task.task_name,
                    'status': self.task.status,
                    'params': self.task.params,
                    'retry_time': self.task.retry_time,
                    'result': self.task.result,
                }, indent=4, sort_keys=True, default=str
            )
        )

    def process(self):
        pass
