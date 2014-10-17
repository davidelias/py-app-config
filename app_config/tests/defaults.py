#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
Default dictionaries, lists, and configuration details for use in testing
this package.

'''

# This is a Mock object, we should probably rename it.
# We have this so we can emulate opts.attr type of option parsing
class OptParserLikeObject(object):
    '''
    An OptionParser-like object for testing attribute access

    '''
    option1 = 'foobar'
    option2 = 'QUXBAR'


# We'll test attribute access with this instance
TEST_OPTS_ATTR = OptParserLikeObject()

# The Option Parser as a dictionary
TEST_OPTS_DICT = {
    'option1': 'foobar',
    'option2': 'QUXBAR',
    'arg1': True,
    'arg2': False,
    'some-list': ['foo', 'bar'],
    'opt4': 'FooBar',
    'OPT5': 'BONANZA',
}

# First of 2, for tests merging dictionaries
TEST_MERGE_DICT_A = {
    'foo': 'bar',
    'zap': 'zang'
}

# Second of 2, for tests merging dictionaries
TEST_MERGE_DICT_B = {
    'baz': 'baq',
    'quz': '${zap}'
}

# Expected result from merging these last two dictionaries plus defaults/etc
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

# To test the process of normalizing config keys
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

# Expected result after normalizing
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

#
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

# Expected result from running _dash_to_underscore() on our test dict
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

# Expected result from running _lowercase_keys() on our test dict
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

# Expected result from _remove_empty_keys()
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

# dictionary of env vars to inject into the environment for testing
ENV_KEYS_TO_INJECT = {
    'FOOBAR': 'raboof',
    'QUAAAA': 'aaaauq',
    'QUA_FOO': 'pook',
    'QUA-FOO': 'pookie',
    'BELFAST': 'ignored',
}

# List of keys to retrieve from the environment
ENV_KEYS_TO_EXTRACT = [
    'FOOBAR',
    'QUAAAA',
    'QUA_FOO',
    'QUA-FOO',
]

# Expected result from unittests on environment variable extraction
ENV_KEYS_EXPECTED = {
    'FOOBAR': 'raboof',
    'QUAAAA': 'aaaauq',
    'QUA_FOO': 'pook',
    # this doesn't actually work as I would expect
    'QUA-FOO': 'pookie',
}

# Expected result from unittests on env extraction through ConfigBase subclass
# These have been normalized, whereas the last dict was not.
DEFAULT_WITH_ENV_EXPECTED = {
    'foobar': 'raboof',
    'quaaaa': 'aaaauq',
    # this doesn't actually work as I would expect
    'qua_foo': 'pook',
}

# For testing ConfigBase with a default config
DEFAULT_CONFIG = {
    'Key': 'value',
    'opt': 2937,
    'fod': 'der',
    'cod': False,
    'c_d': True,
}

# We write this to a .json file for testing file load/merge
JSON_TEST_FILE = {
    'TRUE': True,
    'False': False,
    'null': None,
    'list': [1, '2', 'three'],
    'dict': {'foo': 'bar'},
}

# We write this to a .yaml file for testing file load/merge
YAML_TEST_FILE = {
    'YAML': 'file',
    '_list': ['my', 'list', 'todo'],
}

# We write this to a .yml file for testing file load/merge
YML_TEST_FILE = {
    'YML': 'short',
    'dict': {'boo': 'far'},
}

# We group them together for ease later
TEST_FILES = [
    JSON_TEST_FILE,
    YAML_TEST_FILE,
    YML_TEST_FILE,
]

# Extract these keys/attr from the option parser object
LIST_OF_OPTS_TO_EXTRACT = [
    'option1',
    'arg1',
    'arg2',
    # keys are not normalized after extraction
    'some-list',
    'OPT5',
]

# Expected result for ConfigBase test with a default config
DEFAULT_CONFIG_EXPECTED = DEFAULT_CONFIG
# Expected result for ConfigBase test with opts to extract
DEFAULT_WITH_OPTS_EXPECTED = {
    'option1': 'foobar',
    'arg1': True,
    'arg2': False,
    'some_list': ['foo', 'bar'],
    'opt5': 'BONANZA',
}
#DEFAULT_ENV_KEYS = {
#    'FOOBAR': 'True',
#    'BAZ_BAQ': 'qab',
#    'BAZ-BAQ': '9',
#}


