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

from rains.core.perform_pool import PerFormPool


def analysis_py_file_tasks(imp_analysis_str: str) -> list:
    time.sleep(1)
    tasks = []
    module = importlib.import_module(imp_analysis_str)
    for n in module.__dict__.keys():
        if 'Task' in n[0:4]:
            tasks.append(module.__dict__[n])

    return tasks

task_list = []
if len(sys.argv) >= 2:

    for i in sys.argv[1:]:

        imp_analysis_str = 'task_cache'
        root_task_path: Path = Path(sys.argv[0]).parent.joinpath(imp_analysis_str)
        path = Path(i)

        # 参数是目录
        if path.is_dir():
            dir_parent_name = pathlib.WindowsPath(str(i)).parts[-1]
            save_dir = root_task_path.joinpath(dir_parent_name)
            save_dir.mkdir(parents=True, exist_ok=True)
            imp_analysis_str += f'.{ dir_parent_name }'

            py_list = path.glob('task*.py')
            for i in py_list:
                cache_task = save_dir.joinpath(i.name)
                cache_task.write_bytes(i.read_bytes())
                task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ i.stem }')

        # 参数是文件
        else:
            if path.suffix != '.py':
                path = Path(f'{ str(path) }.py')
            imp_analysis_str = 'task_cache'
            dir_parent_name = pathlib.WindowsPath(str(i)).parts[-2]
            save_dir = root_task_path.joinpath(dir_parent_name)
            save_dir.mkdir(parents=True, exist_ok=True)
            imp_analysis_str += f'.{ dir_parent_name }'
            cache_task = save_dir.joinpath(path.name)
            cache_task.write_bytes(path.read_bytes())
            task_list += analysis_py_file_tasks(f'{ imp_analysis_str }.{ path.stem }')


perform_pool = PerFormPool()
for task in task_list:
    perform_pool.put_task(task)
    
perform_pool.running()
shutil.rmtree(root_task_path)
