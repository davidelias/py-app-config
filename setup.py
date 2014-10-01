#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

from setuptools import setup, find_packages

from app_config import NAME, DESC, VERSION, AUTHOR, EMAIL, LICENSE, URL


setup(
    name = 'app_config',
    description = DESC,
    version = VERSION,
    author = AUTHOR,
    author_email = EMAIL,
    license = LICENSE,
    url = URL,
    packages = find_packages(),
    # add reclass to the list of requirements
    install_requires = ['pyyaml']
)
