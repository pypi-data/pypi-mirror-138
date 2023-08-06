#encoding:GBK
"""
* 作者：王若宇
* 时间：2022/1/25 14:00
* 功能：打包Python软件包用于发布到pypi.org
* 说明：请看读我.txt，库发布后可使用学而思库管理工具下载
"""
import sys

from setuptools import setup
from xes import AIspeak

if __name__ == '__main__':
    sys.argv += ["sdist"]
setup(
    name='pyqt5_applications',
    version='5.15.1',
    packages=['pyqt5_applications'],
    url='https://yangguang-gongzuoshi.top/wry/',
    license='MIT License',
    author='Ruoyu Wang',
    author_email='wry2022@outlook.com',
    description='PyQt5\x16开发工具/' + AIspeak.translate('PyQt5\x16开发工具'),
    long_description='PyQt5开发工具方便快捷地设计和研发Python的Qt5应用/' + AIspeak.translate('PyQt5开发工具方便快捷地设计和研发Python的Qt5应用'),
    requires=["pathlib"]
)

