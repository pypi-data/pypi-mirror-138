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
[ 命令行工具实现 ]

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


command: str = 'order'
if len(sys.argv) > 1:
    command: str = sys.argv[1]

# ------------------------------
if command in ['order', '-order', '-o']:
    from rains.external.order import function_order
    function_order()

# ------------------------------
elif command in ['init', '-init', '-i']:
    from rains.external.init_engineering import function_init_engineering
    function_init_engineering()

# ------------------------------
elif command in ['make', '-make', '-m']:
    from rains.external.create_project import function_create_project
    function_create_project()

# ------------------------------
elif command in ['task', '-task', '-t']:
    from rains.external.create_task import function_create_task
    function_create_task()

# ------------------------------
elif command in ['run', '-run', '-r']:
    from rains.external.run_task import function_run_task
    function_run_task()

# ------------------------------
elif command in ['server', '-server', '-s']:
    from rains.external.run_server import function_run_server
    function_run_server()

# ------------------------------
elif command in ['help', '-help', '-h']:
    from rains.external.help import function_help
    function_help()

# ------------------------------
elif command in ['version', '-version', '-v']:
    from rains.external.version import function_version
    function_version()

else:
    print('error:: rains不存在这样的指令!')
