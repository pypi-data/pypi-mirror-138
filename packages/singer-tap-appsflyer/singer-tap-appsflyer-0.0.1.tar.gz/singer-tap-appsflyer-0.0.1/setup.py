#!/usr/bin/env python

from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name='singer-tap-appsflyer',
    version='0.0.1',
    description='Singer.io tap for extracting data from the AppsFlyer API',
    author='Stitch, Inc. & Izzudin Hafiz',
    url='https://github.com/izzudinhafiz/tap-appsflyer',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_appsflyer'],
    install_requires=[
        'attrs==16.3.0',
        'singer-python==1.6.0a2',
        'requests==2.20.0',
        'backoff==1.3.2',
    ],
    extras_require={
        'dev': [
            'bottle',
            'faker'
        ]
    },
    entry_points={
        'console_scripts': [
            'tap-appsflyer=tap_appsflyer:main'
        ]
    },
    packages=['tap_appsflyer'],
    package_data={
        'tap_appsflyer/schemas/raw_data': [
            'installations.json',
            'in_app_events.json'
        ],
    },
    include_package_data=True,
)
