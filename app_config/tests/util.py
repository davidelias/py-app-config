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


TEST_DICT = {
    'UPPERCASE': 'Foo',
    '--DOUBLE_dash': True,
    'BAR': None,
    '--qux': 'qoof',
    'FOO': 'Foo',
    '--qux-quz': 'quam',
    'BAQ': None,
    '--qux-quiz-clash': 'quack',
    'FOOBAR': False,
    '--quxa': 'qoof',
    'baz': 'fox',
    'bax': '${baz}',
    '--quz-fux': '',
    'FOOBAR': 12,
    'FoQzAr': [],
    'ZozQAr': [1, 3, 9],
    '-Foz-Rox': 'YAML',
    'HarZaq': True,
    '--mix_nix': 'true',
    '-kox_rox': (True, 0, 'Zilch'),
    'Naahtal': 'z00m',
}

DASH_TO_UNDERSCORE_EXPECTED = {
    'UPPERCASE': 'Foo',
    '__DOUBLE_dash': True,
    'BAR': None,
    '__qux': 'qoof',
    'FOO': 'Foo',
    '__qux_quz': 'quam',
    'BAQ': None,
    '__qux_quiz_clash': 'quack',
    'FOOBAR': False,
    '__quxa': 'qoof',
    'baz': 'fox',
    'bax': '${baz}',
    '__quz_fux': '',
    'FOOBAR': 12,
    'FoQzAr': [],
    'ZozQAr': [1, 3, 9],
    '_Foz_Rox': 'YAML',
    'HarZaq': True,
    '__mix_nix': 'true',
    '_kox_rox': (True, 0, 'Zilch'),
    'Naahtal': 'z00m',
}

LOWERCASE_EXPECTED = {
    'uppercase': 'Foo',
    '--double_dash': True,
    'bar': None,
    '--qux': 'qoof',
    'foo': 'Foo',
    '--qux-quz': 'quam',
    'baq': None,
    '--qux-quiz-clash': 'quack',
    'foobar': False,
    '--quxa': 'qoof',
    'baz': 'fox',
    'bax': '${baz}',
    '--quz-fux': '',
    'foobar': 12,
    'foqzar': [],
    'zozqar': [1, 3, 9],
    '-foz-rox': 'YAML',
    'harzaq': True,
    '--mix_nix': 'true',
    '-kox_rox': (True, 0, 'Zilch'),
    'naahtal': 'z00m',
}

REMOVED_EMPTY_KEYS_EXPECTED = {
    'UPPERCASE': 'Foo',
    '--DOUBLE_dash': True,
    '--qux': 'qoof',
    'FOO': 'Foo',
    '--qux-quz': 'quam',
    '--qux-quiz-clash': 'quack',
    'FOOBAR': False,
    '--quxa': 'qoof',
    'baz': 'fox',
    'bax': '${baz}',
    '--quz-fux': '',
    'FOOBAR': 12,
    'FoQzAr': [],
    'ZozQAr': [1, 3, 9],
    '-Foz-Rox': 'YAML',
    'HarZaq': True,
    '--mix_nix': 'true',
    '-kox_rox': (True, 0, 'Zilch'),
    'Naahtal': 'z00m',
}

ENV_KEYS_EXPECTED = {
    'FOOBAR': 'raboof',
    'QUAAAA': 'aaaauq',
}


class OptParserLikeObject(object):
    '''
    An OptionParser-like object for testing attribut
    '''
    option1 = 'foobar'
    option2 = 'QUXBAR'


TEST_OPTS_ATTR = OptParserLikeObject()

TEST_OPTS_DICT = {
    'option1': 'foobar',
    'option2': 'QUXBAR',
}

TEST_MERGE_DICT_A = {
    'foo': 'bar',
    'zap': 'zang'
}

TEST_MERGE_DICT_B = {
    'baz': 'baq',
    'quz': '${zap}'
}

TEST_MERGE_DICT_EXPECTED = {
    'UPPERCASE': 'Foo',
    '--DOUBLE_dash': True,
    'BAR': None,
    '--qux': 'qoof',
    'FOO': 'Foo',
    '--qux-quz': 'quam',
    'BAQ': None,
    '--qux-quiz-clash': 'quack',
    'FOOBAR': False,
    '--quxa': 'qoof',
#   'baz': 'fox',      This key is expected to have been updated to 'baq'
    'bax': 'baq',
    '--quz-fux': '',
    'FOOBAR': 12,
    'FoQzAr': [],
    'ZozQAr': [1, 3, 9],
    '-Foz-Rox': 'YAML',
    'HarZaq': True,
    '--mix_nix': 'true',
    '-kox_rox': (True, 0, 'Zilch'),
    'Naahtal': 'z00m',
    'foo': 'bar',
    'zap': 'zang',
    'baz': 'baq',
    'quz': 'zang'
}

TEST_KEYS_TO_NORMALIZE = {
    '--quz-fux': '',
    'FOOBAR': 12,
    'FoQzAr': [],
    'ZozQAr': [1, 3, 9],
    '_Fuz_Mux': None,
    '-Foz-Rox': 'YAML',
    'HarZaq': True,
    'hazzal': 'aur1',
    '--mix_nix': 'true',
    '-kox_rox': (True, 0, 'Zilch'),
    'Nor-Qaz': None,
    'iXcal': False,
    'Naahtal': 'z00m',
}

NORMALIZED_KEYS_EXPECTED = {
    'uppercase': 'Foo',
    '__double_dash': True,
    '__qux': 'qoof',
    'foo': 'Foo',
    '__qux_quz': 'quam',
    '__qux_quiz_clash': 'quack',
    'foobar': False,
    '__quxa': 'qoof',
    'baz': 'fox',
    'bax': '${baz}',
    '__quz_fux': '',
    'foobar': 12,
    'foqzar': [],
    'zozqar': [1, 3, 9],
    '_foz_rox': 'YAML',
    'harzaq': True,
    '__mix_nix': 'true',
    '_kox_rox': (True, 0, 'Zilch'),
    'naahtal': 'z00m'
}


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
        os.environ['FOOBAR'] = 'raboof'
        os.environ['QUAAAA'] = 'aaaauq'
        env = _get_keys_from_env(['FOOBAR', 'QUAAAA'])
        self.assertEqual(env, ENV_KEYS_EXPECTED)


    def test_merge(self):
        a = TEST_MERGE_DICT_A
        b = TEST_MERGE_DICT_B
        c = _merge(a, b)
        merged = _merge(TEST_DICT, c)
        self.assertSequenceEqual(merged, TEST_MERGE_DICT_EXPECTED)


if __name__ == '__main__':
    unittest.main()
