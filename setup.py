#!/usr/bin/env python
#coding=utf8

try:
    from  setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name = 'tornado_api_demo',
        version = '1.0',
        install_requires = [
                'tornado',
                'sqlalchemy', 
                'redis'],
        description = '使用tornado开发api后台的例子',
        url = 'https://github.com/zhouxianggen/tornado_api_demo.git', 
        author = 'zhouxianggen',
        author_email = 'zhouxianggen@gmail.com',
        classifiers = [ 'Programming Language :: Python :: 3.7',],
        packages = ['tornado_api_demo'],
        data_files = [
                ('/conf/supervisor/program/', ['demo.ini']),
                ],
        entry_points = {
                'console_scripts': [
                        'run_demo = tornado_api_demo.run:main',
                        ]
                }
        )

