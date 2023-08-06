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


# 任务类型映射字典
TASK_TYPE_MAP_DICT: dict = {
    '1': CONST.TYPE.PROJECT_TYPE_WEB,
    '2': CONST.TYPE.PROJECT_TYPE_API
}

# 模板目录名称
TASK_TEMPLATE_DIR_NAME: str = 'task_template'

# 模板文件名称
TASK_TEMPLATE_WEB_FILE_NAME: str = 'task_web_template.py'
TASK_TEMPLATE_API_FILE_NAME: str = 'task_api_template.py'


if len(sys.argv) >= 2:

    task_template_path: Path = Path(sys.argv[0]).parent.joinpath(TASK_TEMPLATE_DIR_NAME)
    if TASK_TYPE_MAP_DICT[sys.argv[1]] == CONST.TYPE.PROJECT_TYPE_WEB:
        task_template_path = task_template_path.joinpath(TASK_TEMPLATE_WEB_FILE_NAME)
    elif TASK_TYPE_MAP_DICT[sys.argv[1]] == CONST.TYPE.PROJECT_TYPE_API:
        task_template_path = task_template_path.joinpath(TASK_TEMPLATE_API_FILE_NAME)

    number: int = 1
    while True:
        path: Path = CONST.SYS.PATH_ROOT.joinpath(f'task_{ number }.py')
        if not path.exists():
            task_template_code = re.sub(r'class Task', f'class Task{ number }', task_template_path.read_text())
            path.touch(mode=0o777)
            path.write_bytes(bytes(task_template_code, encoding='UTF-8'))
            break

        number += 1
        continue

print('任务模板创建成功')
