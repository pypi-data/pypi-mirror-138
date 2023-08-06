#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import setuptools


with open('README.md', 'r') as fin:
    long_description = fin.read()
with open('LICENSE', 'r') as fin:
    license = fin.read()

setuptools.setup(
    name='cs-sync',
    version='0.0.19',
    license=license,
    author='Kyle L. Davis',
    author_email='AceofSpades5757.github@gmail.com',
    install_requires=[
        'typer',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://kyleldavis.com/',
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points="""
        [console_scripts]
        cssync=cs_sync.main:cli
    """,
)
