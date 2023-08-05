# !/usr/bin/env python
# coding:utf-8

"""
Copyright (c) 2021. quinn.7@foxmail.com All rights reserved.
Based on the Apache License 2.0 open source protocol.

作者 cat7
邮箱 quinn.7@foxmail.com

"""


import random

from rains.common.i.i_task import ITask
from rains.baseic.consts import ConstTaskType

from rains.kit.mini.mini_plant import MiniPlant


class MiniTask(ITask):
    """
    [ 小程序任务集 ]
    * 无

    """

    _task_id: int = random.randint(10000, 99999)
    """ 任务编号 """

    _type: str = ConstTaskType.CODE
    """ 任务类型 """

    plant: MiniPlant
    """ 工厂对象 """

    def set_class_starting(self):
        pass

    def set_class_ending(self):
        pass

    def set_function_starting(self):
        pass

    def set_function_ending(self):
        pass
