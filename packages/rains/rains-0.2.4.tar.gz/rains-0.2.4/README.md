# 框架简介

rains 旨在于构建一个开箱即用、稳定且高效的工程化全栈自动化测试框架。

框架的核心原生实现了一个高性能的多进程任务执行器，它能够兼容多个不同平台的测试套件，这意味着您可以随心所欲的在项目中编写不同平台的测试任务，例如 "Web项目" 与 "Api项目"，然后调用执行器或者通过rains命令行工具运行这些任务。


***


# 环境安装
    根据不同需求安装对应的依赖。


    **[注意] 携带 "*" 标识为建议安装，其余根据需求选择即可。**


### * 拉取 rains 项目
    安装该项依赖的目的在于获取rains命令行工具。

    通过 GIT 拉取项目:

    git clone https://gitee.com/catcat7/rains.git


    **[注意] 拉取项目后需要将其加入系统环境变量中。**


### * 安装 rains 库
    安装该项依赖的目的在于让Python全局支持rains语法补全，方便编写任务脚本。

    通过 pip 安装 rains 库:

    pip install rains


### Web测试套件依赖
    rains.kit.web 基于 Selenium(3.14.1) 二次开发实现，使用时需要安装以下依赖：

    1. 浏览器

    Chrome :: https://www.google.cn/chrome/
    
    2. 浏览器驱动

    ChromeDriver :: https://registry.npmmirror.com/binary.html?path=chromedriver/


    **[注意] 需要注意的是浏览器驱动与浏览器的版本必须一致。**

    **[注意] 需要将浏览器驱动路径放置于 rains 项目中，后者加入系统环境变量中。**


***

