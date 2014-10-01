#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
The opinionated config class for Python applications
'''

import UserDict


class ConfigBase(UserDict.UserDict):
    '''
    Base class that provides a meaningful (opinionated) foundation to build an
    object suitable for all of an Application's configuration. It is meant to be
    dict-like in nature, subclassing ``UserDict.UserDict``.
    '''
    # a place to store the config keys (data)
    data = {}
