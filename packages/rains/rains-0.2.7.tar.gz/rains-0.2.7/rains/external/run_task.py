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
[ 运行任务 ]

"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

import time
import shutil
import pathlib
import importlib
from pathlib import Path

from rains.baseic.const import CONST


def function_run_task():
    """  
    [ 执行任务 ]

    """

    task_list = []

    if len(sys.argv) >= 3:

        if not CONST.SYS.PATH_RAINS_INI_FILE.is_file():
            print(_MESSAGE_ERROR)
            exit(0)

        # importlib 解析路径
        imp_analysis_str = _TASK_CACHE_NAMING

        # 拼接任务文件缓存目录路径
        # 因为 importlib 导入 py文件 的特殊方式, 需要在当前空间中创建任务文件缓存目录.
        imp_analysis_str = _TASK_CACHE_NAMING
        task_cache_path: Path = Path(sys.argv[0]).parent.joinpath(_TASK_CACHE_NAMING)

        # 循环参数
        for task_arg in sys.argv[2:]:

            if task_arg in ['.', '/', './']:
                task_arg_path = CONST.SYS.PATH_ROOT
            else:
                # 拼接参数路径
                task_arg_path = CONST.SYS.PATH_ROOT.joinpath(task_arg)  

            # 如果参数路径指向目录
            if task_arg_path.is_dir():
                dir_parent_name = pathlib.WindowsPath(str(task_arg_path)).parts[-1]
                save_dir = task_cache_path.joinpath(dir_parent_name)
                save_dir.mkdir(parents=True, exist_ok=True)
                imp_analysis_str += f'.{ dir_parent_name }'
                py_list = task_arg_path.glob(f'{ _LEGITIMATE_TASK_FILE_PREFIX }*.py')
                for py_file in py_list:
                    cache_task = save_dir.joinpath(py_file.name)
                    cache_task.write_bytes(py_file.read_bytes())
                    task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ py_file.stem }')
    
            # 如果参数路径指向文件
            else:
                if task_arg_path.suffix != '.py':
                    task_arg_path = Path(f'{ str(task_arg_path) }.py')

                if task_arg_path.is_file():
                    dir_parent_name = pathlib.WindowsPath(str(task_arg_path)).parts[-2]
                    save_dir = task_cache_path.joinpath(dir_parent_name)
                    save_dir.mkdir(parents=True, exist_ok=True)
                    imp_analysis_str += f'.{ dir_parent_name }'
                    cache_task = save_dir.joinpath(task_arg_path.name)
                    cache_task.write_bytes(task_arg_path.read_bytes())
                    task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ task_arg_path.stem }')

        if len(task_list) < 1:
            print('暂无任务可供执行!')
            shutil.rmtree(task_cache_path)
            exit(0)

        # 多进程执行任务
        from rains.core.perform_pool import PerFormPool
        perform_pool = PerFormPool()
        
        number = 1
        print('\n--------------------------------------\n')
        print('解析任务清单 : \n')
        for task in task_list:
            print(f' { number } : { task.__name__ }')
            perform_pool.put_task(task)
            number += 1
        print('\n--------------------------------------\n')
        perform_pool.running()

        # 销毁任务缓存
        shutil.rmtree(task_cache_path)


def analysis_py_file_tasks(imp_analysis_str: str) -> list:
    """
    [ 从 importlib 路径中解析任务类 ]

    ---
    参数:
        imp_analysis_str { str } : importlib 路径.

    ---
    返回:
        list : 任务类列表.

    """

    time.sleep(0.5)
    tasks = []
    module = importlib.import_module(imp_analysis_str)
    for n in module.__dict__.keys():
        if _LEGITIMATE_TASK_CLASS_PREFIX in n[0:4]:
            tasks.append(module.__dict__[n])
    return tasks


# 任务缓存目录名称
_TASK_CACHE_NAMING = 'task_cache'

# 合法的任务文件前缀
_LEGITIMATE_TASK_FILE_PREFIX = 'task'

# 合法的任务类前缀
_LEGITIMATE_TASK_CLASS_PREFIX = 'Task'

# 任务执行异常文案
_MESSAGE_ERROR = \
"""
--------------------------------------

请在工程根目录执行 -run 命令

初始化工程将创建或补全项目执行依赖文件, 并在工程根目录中创建 <rains.ini> 文件。

<rains.ini> 文件 仅作为工程根目录标识之用, -run|-server 命令需要在工程根目录中才允许执行。

--------------------------------------
"""
