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
[ Web工厂类 ]

"""

from typing import Any

from selenium.webdriver.common.by import By

from rains.kit.web.packaging.web_plant_view import WebPlantView
from rains.kit.web.packaging.web_plant_element import WebPlantElement
from rains.kit.web.packaging.web_element_structure import WebElementStructure


BY: By = By
""" [ 元素定位策略 ] """


# ----------------------------------
class WebPlant(object):
    """
    [ Web工厂类 ]

    * 提供了对浏览器视图访问与控件元素的构建封装.

    """

    _web_driver: Any
    """ [ Web驱动程序 ] """

    # ------------------------------
    def __init__(self, web_driver: Any):
        """
        [ Web工厂类 ]

        ---
        参数:
            web_driver { WebDriver } : Web 驱动程序.

        """

        self._web_driver = web_driver

    # ------------------------------
    @property
    def driver(self):
        return self._web_driver

    # ------------------------------
    @property
    def view(self) -> WebPlantView:
        """
        [ Web视图 ]

        * 封装了浏览器本身的功能, 如获取浏览器信息、弹窗控制、标签页控制等.

        ---
        返回:
            WebPlantView : Web 视图对象.

        """

        return WebPlantView(self._web_driver)

    # ------------------------------
    def _map_view(self):
        return self.view

    # ------------------------------
    def element(self, 
                page: str, 
                name: str, 
                by_key: str, 
                by_value: str, 
                anchor_by_key: str = None, 
                anchor_by_value: str = None, 
                anchor_location_id: int = None) -> WebPlantElement:
        """
        [ Web元素控件 ]

        * 基于元素特征构建指向该元素的元素控件对象.
        * 封装了对页面元素的操作功能, 如获取元素信息、模拟鼠标、输入框、下拉框等操作.
        
        ---
        参数:
            page { str } : 页面名称.
            name { str } : 元素名称.
            by_key { str } : 元素定位策略.
            by_value { str } : 元素定位策略对应的值.
            anchor_by_key { str, optional } : 锚点元素定位策略.
            anchor_by_value { str, optional } : 锚点元素定位策略对应的值.
            anchor_location_id { str, optional } : 锚点元素定位ID.

        ---
        返回:
            WebPlantElement : Web 元素控件对象.

        """

        element_structure = WebElementStructure(
            page, 
            name, 
            by_key, 
            by_value, 
            anchor_by_key, 
            anchor_by_value, 
            anchor_location_id
        )

        return WebPlantElement(self._web_driver, element_structure)
