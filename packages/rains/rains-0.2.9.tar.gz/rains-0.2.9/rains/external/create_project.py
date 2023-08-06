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
[ 创建项目 ]

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from rains.baseic.environment.make import create_project


# ----------------------------------
def function_create_project():
    """
    [ 创建项目 ]

    """
    
    if len(sys.argv) >= 3:

        print('\n--------------------------------------\n')
        for p in sys.argv[2:]:
            project_name = ''.join([PROJECT_NAMING_BASE_PREFIX, p])
            print(f'项目 [{ project_name }] => ', end='')
            result = create_project(project_name)
            if result:
                print(_MESSAGE_CREATING_SUCCESSFUL)
            else:
                print(_MESSAGE_CREATING_UNSUCCESSFUL)
        print('\n--------------------------------------\n')

    else:
        print(_MESSAGE_ERROR)


# 项目命名前缀
PROJECT_NAMING_BASE_PREFIX: str = 'p_'

# 项目创建成功文案
_MESSAGE_CREATING_SUCCESSFUL: str = '创建成功!'

# 项目创建失败文案
_MESSAGE_CREATING_UNSUCCESSFUL: str = '创建失败, 项目已经存在!'

# 项目创建异常文案
_MESSAGE_ERROR: str = \
"""
--------------------------------------

指令键入异常!

正确格式:
>> rains -make [project_name]
>> rains -make [project_name] [project_name] ...

示例:
>> rains -make Project
>> rains -make Project Project2

--------------------------------------
"""
