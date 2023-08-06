#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: Hewen
@file:setup.py
@time:2022/01/18
@Email: hewenwork@gmail.com
"""
from setuptools import setup, find_packages

setup(
    name="Rdtest",
    version="0.0.13",
    author="Hewen",
    license='MIT',
    author_email="hewenwork@gmail.com",
    url="https://www.rdtest.fit",
    description=u"自用测试包, Windows操作相关",
    # package_dir={"": "Rdtest"},
    keywords='Rdtest',  # 项目的关键字
    packages=find_packages(include=['Rdtest', 'Rdtest.*']),
    install_requires=["requests_html", "chardet", "configparser"],
    include_package_data=True,
    # entry_points={
    #     'console_scripts': [
    #         'tobe=tobe:main'
    #     ],
    # },
    python_requires=">=3.5"
    # classifiers=

)
