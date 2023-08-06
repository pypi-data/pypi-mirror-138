#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='extract-6a6f6a6f',
    version='1.0.0',
    license='MIT',
    author='Jonas (Jojo) Uliana',
    author_email='jonas.uliana@passwd.com.br',
    description='Just pull an application from an Android device',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/zone016/lazy-android-app-extraction',
    project_urls={
        'Bug Tracker': 'https://github.com/zone016/lazy-android-app-extraction/issues',
    },
    keywords=['android', 'extract'],
    install_requires=[
        'colorama~=0.4.4',
        'termcolor~=1.1.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['extract = lazy.extract:main']
    }
)
