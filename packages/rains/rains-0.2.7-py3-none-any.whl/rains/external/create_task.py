#!/usr/bin/env python3
# coding=UTF-8
#
# Copyright 2022. quinn.7@foxmail.com All rights reserved.
# Author :: cat7
# Email  :: quinn.7@foxmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, 
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""
[ 创建任务 ]

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import re
from pathlib import Path

from rains.baseic.const import CONST


# ----------------------------------
def function_create_task():
    """
    [ 创建任务 ]

    """

    if len(sys.argv) >= 4:
        # 获取任务类型与模板路径
        task_template_path: Path
        task_type: str = sys.argv[2]
        if task_type in ['web', 'Web', 'WEB', 'w', 'W']:
            task_template_path = Path(sys.argv[0]).parent.joinpath(TASK_TEMPLATE_WEB_FILE_PATH)
        elif task_type in ['api', 'Api', 'API', 'a', 'A']:
            task_template_path = Path(sys.argv[0]).parent.joinpath(TASK_TEMPLATE_API_FILE_PATH)
        else:
            print(_MESSAGE_ERROR)
            exit(0)

        print('--------------------------------------')
        for task_name in sys.argv[3:]:
            # 拼接合法的任务名称
            if len(task_name) < 5 or task_name[0:5] != TASK_NAMING_BASE_PREFIX:
                task_name = ''.join([TASK_NAMING_BASE_PREFIX, task_name])
            if '.py' not in task_name:
                task_name2 = ''.join([task_name, '.py'])
            print(f'任务 [{ task_name }] => ', end='')
            
            task_path: Path = CONST.SYS.PATH_ROOT.joinpath(task_name2)
            if not task_path.exists():
                # 拼接首字母大写的任务类名
                template_class_name = ''
                for i in task_name.split('_'):
                    template_class_name = ''.join([template_class_name, i.capitalize()]) 
                
                # 创建任务
                task_template_code = re.sub(r'class Task', f'class { template_class_name }', task_template_path.read_text(encoding='UTF-8'))
                task_path.touch(mode=0o777)
                task_path.write_bytes(bytes(task_template_code, encoding='UTF-8'))
                print(_MESSAGE_CREATING_SUCCESSFUL)
            else:
                print(_MESSAGE_CREATING_UNSUCCESSFUL)
        print('--------------------------------------')

    else:
        print(_MESSAGE_ERROR)


# 任务命名前缀
TASK_NAMING_BASE_PREFIX: str = 'task_'

# Web任务模板路径
TASK_TEMPLATE_WEB_FILE_PATH: str = 'task_template\\task_web_template.py'

# Api任务模板路径
TASK_TEMPLATE_API_FILE_PATH: str = 'task_template\\task_api_template.py'

# 任务创建成功文案
_MESSAGE_CREATING_SUCCESSFUL: str = '创建成功!'

# 任务创建失败文案
_MESSAGE_CREATING_UNSUCCESSFUL: str = '创建失败, 任务已经存在!'

# 任务创建异常文案
_MESSAGE_ERROR: str = \
"""
--------------------------------------

指令键入异常!

正确格式:
>> rains -task [task_type] [task_name]
>> rains -task [task_type] [task_name] [task_name] ...

示例:
>> rains -task task_t1
>> rains -task task_t1 task_t2

目前支持的任务类型:
web : Web功能测试任务
api : Api功能测试任务

--------------------------------------
"""
