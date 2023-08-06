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
[ 工具相关 ]

"""

import re
import yaml

from rains.baseic.error import YamlHandlerError


# ----------------------------------
class Regular(object):
    """
    [ 正则封装 ]

    """

    # ------------------------------
    @staticmethod
    def get_function_doc_name(doc: str) -> str:
        """
        [ 获取函数注释中的名称 ]

        """
        
        return re.findall(r'\[ (.*) \]', doc)[0]

    # ------------------------------
    @staticmethod
    def get_function_doc_explain(doc: str) -> list:
        """
        [ 获取函数注释中的说明 ]

        """

        return re.findall(r'\* (.*)', doc)


# ----------------------------------
class YamlHandler(object):
    """
    [ YAML处理器 ]

    """

    # ------------------------------
    @staticmethod
    def read(yaml_path: str) -> dict:
        ...

    # ------------------------------
    @staticmethod
    def write(
        yaml_path: str, 
        data_dict: dict,
        mode: str = 'w',
        encoding: str = 'UTF-8'
    ) -> bool:
        """
        [ 写入 ]

        ---
        参数:
            yaml_path { str } : YAML文件路径.
            data_dict { dict } : 数据字典.
            mode { str } : 模式.
            encoding { str } : 编码.

        ---
        返回:
            bool : 成功写入返回 True, 否则抛出 YamlHandlerError 异常.

        """
        try:
            with open(yaml_path, mode, encoding=encoding) as f:
                yaml.dump(data_dict, f, allow_unicode=True)
            return True

        except BaseException as error:
            raise YamlHandlerError(error)
