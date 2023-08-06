#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='usetime',  
    version='0.0.1',  
    author='void9main', 
    author_email='void9main@163.com',  
    url='https://github.com/void9main/funtime.git',
    description='一个装饰器，获取函数运行时间',
    packages=['usetime'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'timeClk=usetime:timeClk',
        ]
    }
)
