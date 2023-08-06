import os.path
from setuptools import setup
from unittest import TestLoader


def tests():
    return TestLoader().discover('test', pattern='test_*.py')


setup(
    name='realtimeconfig',
    version='0.0.1',
    packages=[
        "realtimeconfig/"
    ],
    url='https://realtimeconfig.com',
    install_requires=[
        "websocket-client",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'realtimeconfig-monitor=realtimeconfig.monitor:main',
            
    ]})
