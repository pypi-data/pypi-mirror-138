#encoding:GBK
"""
* ���ߣ�������
* ʱ�䣺2022/1/25 14:00
* ���ܣ����Python��������ڷ�����pypi.org
* ˵�����뿴����.txt���ⷢ�����ʹ��ѧ��˼�����������
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
    description='PyQt5\x16��������/' + AIspeak.translate('PyQt5\x16��������'),
    long_description='PyQt5�������߷����ݵ���ƺ��з�Python��Qt5Ӧ��/' + AIspeak.translate('PyQt5�������߷����ݵ���ƺ��з�Python��Qt5Ӧ��'),
    requires=["pathlib"]
)

