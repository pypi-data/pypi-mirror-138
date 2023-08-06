#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name='django-dart-reverse',
    version='0.0.11',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: Django',
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
    description='Url collect command for dart',
    long_description=read('../README.md'),
    long_description_content_type='text/markdown',
    author='Marek Procházka',
    author_email='m.prochazka2002@gmail.com',
    url='https://github.com/marekprochazka/django-dart-reverse',
    download_url='https://pypi.org/project/django-dart-reverse/',
    packages=find_packages(),
    package_data={
        'django_dart_reverse': [
            'templates/dart/*',
        ]
    },
    install_requires=[
        'Django>=3',
    ]
)