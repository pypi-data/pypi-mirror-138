from setuptools import setup

setup(
    name='yixsoft-ezmysql',
    version='0.0.1',
    author='yixsoft',
    author_email='davepotter@163.com',
    url='https://gitee.com/yixsoft/python-ezymysql',
    packages=['ezmysql'],
    description=u'Auto scan table structure and generate sql & execute by dict',
    install_requires=['mysql-connector']
)
