#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
Tests for the utility functions used internally by the ``app_config`` module.

'''

import os
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

from app_config.base import (_normalize_keys, _dash_to_underscore,
                             _lowercase_keys, _remove_empty_keys,
                             _get_opt, _get_keys_from_env, _merge)
from app_config.tests.defaults import *


class TestUtilityFunctions(unittest.TestCase):
    '''
    Tests for the following functions:

     * ``_normalize_keys()``
     * ``_dash_to_underscore()``
     * ``_lowercase_keys()``
     * ``_remove_empty_keys()``
     * ``_get_opt()``
     * ``_get_keys_from_env()``
     * ``_merge()``

    '''
    def test_normalize_keys(self):
        normalized = _normalize_keys(TEST_DICT)
        self.assertSequenceEqual(normalized, NORMALIZED_KEYS_EXPECTED)


    def test_dash_to_underscore(self):
        underscored = _dash_to_underscore(TEST_DICT)
        self.assertSequenceEqual(underscored, DASH_TO_UNDERSCORE_EXPECTED)


    def test_lowercase_keys(self):
        lowercased = _lowercase_keys(TEST_DICT)
        self.assertSequenceEqual(lowercased, LOWERCASE_EXPECTED)


    def test_remove_empty_keys(self):
        vacuumed = _remove_empty_keys(TEST_DICT)
        self.assertSequenceEqual(vacuumed, REMOVED_EMPTY_KEYS_EXPECTED)


    def test_get_opt_attribute(self):
        opts = TEST_OPTS_ATTR
        o1 = _get_opt(opts, 'option1')
        o2 = _get_opt(opts, 'option2')
        self.assertEqual(o1, 'foobar')
        self.assertEqual(o2, 'QUXBAR')


    def test_get_opt_dictionary(self):
        opts = TEST_OPTS_DICT
        o1 = _get_opt(opts, 'option1')
        o2 = _get_opt(opts, 'option2')
        self.assertEqual(o1, 'foobar')
        self.assertEqual(o2, 'QUXBAR')


    def test_get_keys_from_env(self):
        os.environ.update(ENV_KEYS_TO_INJECT)
        env = _get_keys_from_env(ENV_KEYS_TO_EXTRACT)
        self.assertEqual(env, ENV_KEYS_EXPECTED)


    def test_merge(self):
        a = TEST_MERGE_DICT_A
        b = TEST_MERGE_DICT_B
        c = _merge(a, b)
        merged = _merge(TEST_DICT, c)
        self.assertSequenceEqual(merged, TEST_MERGE_DICT_EXPECTED)


if __name__ == '__main__':
    unittest.main()
