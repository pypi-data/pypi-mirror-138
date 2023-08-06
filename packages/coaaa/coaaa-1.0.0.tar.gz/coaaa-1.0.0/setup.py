#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
import os
from setuptools import setup, find_packages            #这个包没有的可以pip一下

__version__='1.0.0'  #版本号
requirements=open('requirements.txt').readline()  #依赖文件


setup(
    name = "co",      #这里是pip项目发布的名称
    version = __version__ ,  #版本号，数值大的会优先被pip
    keywords = ("pip", "co"),
    description = "API",  #描述
    long_description = "API",  #详细描述
    license = "",  #程序的授权信息

    url = "",     #项目相关文件地址，一般是github
    author = "cxx",
    author_email = "cuixiaoxia@chinasofti.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",  #程序适应的软件平台
    #install_requires = [""]          #这个项目需要的第三方库
	install_requires=requirements,  #安装依赖
	)

"""





from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))
setup(
    name='coaaa',
    version='1.0.0',
    description='common',
    #long_description=str(open(path.join(here, "README.md")).read()),
    # The project's main homepage.
    url='',
    # Author details
    author='cxx',
    author_email='cuixiaoxia@chinasofti.com',
    # Choose your license
    license='',

    #py_modules=["coaaa"],
    #install_requires=['colorama']
	py_modules=["coaaa.lib.readexcel","coaaa.lib.writeexcel"],
)






#  setup.py各参数介绍：
#
# --name 包名称
#
# --version (-V) 包版本
#
# --author 程序的作者
#
# --author_email 程序的作者的邮箱地址
#
# --maintainer 维护者
#
# --maintainer_email 维护者的邮箱地址
#
# --url 程序的官网地址
#
# --license 程序的授权信息
#
# --description 程序的简单描述
#
# --long_description 程序的详细描述
#
# --platforms 程序适用的软件平台列表
#
# --classifiers 程序的所属分类列表
#
# --keywords 程序的关键字列表
#
# --packages 需要处理的包目录（包含__init__.py的文件夹）
#
# --py_modules 需要打包的python文件列表
# --download_url 程序的下载地址
#
# --cmdclass
#
# --data_files 打包时需要打包的数据文件，如图片，配置文件等
#
# --scripts 安装时需要执行的脚步列表
#
# --package_dir 告诉setuptools哪些目录下的文件被映射到哪个源码包。一个例子：package_dir = {'': 'lib'}，表示“root package”中的模块都在lib 目录中。
#
# --requires 定义依赖哪些模块
#
# --provides定义可以为哪些模块提供依赖
#
# --find_packages() 对于简单工程来说，手动增加packages参数很容易，刚刚我们用到了这个函数，它默认在和setup.py同一目录下搜索各个含有 __init__.py的包。