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
[ 初始化工程 ]

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

from rains.baseic.environment.make import create_runtime_environment
from rains.baseic.environment.make import init_engineering


_MESSAGE = \
"""
--------------------------------------

工程初始化成功。

初始化工程将创建或补全项目执行依赖文件, 并在工程根目录中创建 <rains.ini> 文件。

<rains.ini> 文件 仅作为工程根目录标识之用, -run|-server 命令需要在工程根目录中才允许执行。

--------------------------------------
"""


def function_init_engineering():
    """
    [ 初始化工程 ]

    """

    create_runtime_environment()
    init_engineering()
    print(_MESSAGE)
