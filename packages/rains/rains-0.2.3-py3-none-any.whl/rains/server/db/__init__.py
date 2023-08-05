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
[ 数据库模块 ]

"""

from rains.server.db.rains_db import RainsDb
from rains.server.db.rains_sql import RainsSql
from rains.server.db.common import RainsDbParameterHandler


DB: RainsDb = RainsDb()
""" [ 数据库实例 ] """

SQL: RainsSql = RainsSql()
""" [ SQL语句实例 ] """


__all__ = [
    'DB', 
    'SQL', 
    'RainsDbParameterHandler'
]
