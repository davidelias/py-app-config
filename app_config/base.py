#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
The opinionated config object for Python applications

'''

import os
import UserDict

from reclass.datatypes import Parameters


def _normalize_keys(items):
     '''
     Generate a new dictionary with renamed keys. All occurances of '-' are
     replaced with '_', and all keys are lowercased.

     '''
     return _dash_to_underscore(_lowercase_keys(_remove_empty_keys(items)))


def _dash_to_underscore(items):
     '''
     Generate a new dictionary with renamed keys. All occurances of '-' are
     replaced with '_'.

     '''
     return {k.replace('-', '_'):v for k,v in items.iteritems()}


def _lowercase_keys(items):
     '''
     Generate a new dictionary with renamed keys. All keys are ensured to be
     lower-cased.

     '''
     return {k.lower():v for k,v in items.iteritems()}


def _remove_empty_keys(d={}):
    '''
    Returns a dictionary, having deleted (removed) the empty keys.

    '''
    return {k:v for k,v in d.iteritems() if v is not None}


def _get_opt(opts=None, key=None):
    '''
    Attempt to retrieve the named option, Returns None if not found or an
    exception is thrown. Lookup ``opts.key`` and ``opts[key]``.

    '''
    try:
        opt = getattr(opts, key)
        return opt
    except:
        try:
            opt = opts[key]
            return opt
        except:
            return None


def _get_keys_from_env(keys=[]):
    '''
    Construct a dictionary of key/value pairs using the list of ``keys``
    provided and ``os.environ.get()`` to retrieve the key from the shell
    environment.

    Use ``_remove_empty_keys()`` to ensure there are no empty keys

    '''
    return _remove_empty_keys({k: os.environ.get(k) for k in keys})


def _merge(a, b):
    '''
    merge the contents of dictionary ``b`` into dictionary ``a``, using reclass'
    sensible form of deep-dictionary merging and interpolation.
    '''
    m = Parameters(a)
    m.merge(b)
    m.interpolate()
    return m.as_dict()


class ConfigBase(UserDict.UserDict):
    '''
    Base class that provides a meaningful (opinionated) foundation to build an
    object suitable for all of an Application's configuration. It is meant to be
    dict-like in nature, subclassing ``UserDict.UserDict``.

    '''
    # a place to store the config keys (data)
    data = {}
