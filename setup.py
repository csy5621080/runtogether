#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
'''
python3 setup.py sdist build
python3 setup.py bdist_wheel
twine upload dist/*
'''

setup(
    name='runtogether',
    version='0.0.4.0',  # 项目版本
    author='小成',  # 项目作者
    author_email='499938136@qq.com',  # 作者email
    url='https://github.com/csy5621080/runtogether',  # 项目代码仓库
    description='多端口代理/类gunicorn',  # 项目描述
    packages=['runtogether'],  # 包名
    install_requires=['psutil', 'argparse'],
    entry_points={'console_scripts': [
        'rtg = runtogether.command:main'
    ]},
)