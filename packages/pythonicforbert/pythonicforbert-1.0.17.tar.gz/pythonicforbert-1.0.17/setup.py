#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
setup(
    name='pythonicforbert',
    version='1.0.17',
    description='a package for your bert using',
    long_description='使用pytorch实现你的bert项目',
    author='xiaoguzai',
    author_email='474551240@qq.com',
    license='Apache License 2.0',
    url='https://github.com/boss2020/pytorch-transformer',
    download_url='https://github.com/boss2020/pytorch-transformer/master.zip',
    packages=find_packages(),
    #分发静态文件需要
    include_package_data=True,
    install_requires=['torch>=1.5.0']
)
