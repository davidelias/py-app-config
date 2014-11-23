#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
Unit tests for the ``ConfigBase`` class.

'''

import os
import json
import yaml
import logging
import tempfile
import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from app_config.base import ConfigBase as _ConfigBase
from app_config.tests.defaults import *

logging.basicConfig(format='%(levelname)s: %(name)s %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def _write_file(data, fpath=None, format='yaml'):
    '''
    Write the dictionary ``data`` to the file specified by ``fpath``, formatted
    as either ``json`` or ``yaml`` and specified by ``format``. If ``format`` is
    ``none`` (no formatting), just dump ``data`` as a string to file.write().
    Returns ``True`` on success and ``False`` if there is an Exception in opening
    or dumping data to the file.

    '''
    try:
        with open(fpath, 'w') as tmpfile:
            msg = ('writing %s file to %s with data %s' % (format, fpath, data))
            logger.debug(msg)
            if format == 'json':
                json.dump(data, tmpfile, indent=2)
            elif format == 'yaml':
                yaml.safe_dump(data, tmpfile)
            else:
                tmpfile.write(data)
            return True
    except:
        return False


def _setup_temporary_files():
    '''
    Retrieve the temporary files needed to run our tests for the ``ConfigBase``
    class. Write to the files to ensure they all exist and have the contents we
    wish to test for.

    Returns the list of ``tempfile.NamedTemporaryFile`` objects we create in the
    setup process.

    '''
    tlist = []
    t1 = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    _write_file(JSON_TEST_FILE, t1.name, 'json')
    tlist.append(t1)
    t2 = tempfile.NamedTemporaryFile(delete=False, suffix='.yaml')
    _write_file(YAML_TEST_FILE, t2.name)
    tlist.append(t2)
    t3 = tempfile.NamedTemporaryFile(delete=False, suffix='.yml')
    _write_file(YML_TEST_FILE, t3.name)
    tlist.append(t3)
    # empty, unformatted file
    t4 = tempfile.NamedTemporaryFile(delete=False)
    _write_file(None, t4.name, format='none')
    tlist.append(t4)
    return tlist


class TestConfig(_ConfigBase):
    '''
    Subclass ``ConfigBase`` to add a logger for testing

    '''
    logger = logger

class ConfigWithDefaults(TestConfig):
    '''
    Subclass ``ConfigBase`` to test use of defaults functionality
    '''
    _defaults = DEFAULT_CONFIG


class ConfigWithDefaultOpts(TestConfig):
    '''
    Subclass ``ConfigBase`` to test use of default opts to extract
    '''
    _opts_list = LIST_OF_OPTS_TO_EXTRACT


class ConfigWithDefaultEnv(TestConfig):
    '''
    Subclass ``ConfigBase`` to test use of retrieving specific environment
    variables/keys as part of init.
    '''
    _env_keys = ENV_KEYS_TO_EXTRACT
 

class ExampleConfig(TestConfig):
    '''
    '''
    _defaults = DEFAULT_CONFIG
    _opts_list = LIST_OF_OPTS_TO_EXTRACT
    _env_keys = ENV_KEYS_TO_EXTRACT


class TestConfigBase(unittest.TestCase):
    '''
    Test cases for the ``ConfigBase`` class, including the following
    functionality:

     * init the class with no defaults, env, opts, etc, nothing
     * init the class with defaults

    '''
    def setUp(self):
        self._tmp = _setup_temporary_files()
        os.environ.update(ENV_KEYS_TO_INJECT)

    def tearDown(self):
        for tfile in self._tmp:
            os.unlink(tfile.name)

    def test_init_config_empty(self):
        print 'ConfigBase test #1'
        c = TestConfig()
        self.assertEqual(c, {})

    def test_init_config_with_defaults(self):
        print 'ConfigBase test #2'
        c = ConfigWithDefaults()
        self.assertSequenceEqual(c, DEFAULT_CONFIG_EXPECTED) 

    def test_init_config_with_opts_extract(self):
        print 'ConfigBase test #3'
        c = ConfigWithDefaultOpts(opts=TEST_OPTS_DICT)
        self.assertSequenceEqual(c, DEFAULT_WITH_OPTS_EXPECTED) 

    def test_init_config_with_env_extract(self):
        print 'ConfigBase test #4'
        c = ConfigWithDefaultEnv()
        self.assertSequenceEqual(c, DEFAULT_WITH_ENV_EXPECTED) 

    def test_init_config_with_file_load(self):
        print 'ConfigBase test #5'
        # we define this class here because we did not know the location of the
        # temporary files before setUp(), and because we don't need it in the
        # other tests.
        class ConfigWithDefaultFiles(TestConfig):
            '''
            Subclass ``ConfigBase`` to test use of default files to load
            '''
            # generate the list of files to load, based on setUp() gave us
            _filelist = [t.name for t in self._tmp]
        # the actual test
        c = ConfigWithDefaultFiles()
        self.assertSequenceEqual(c, DEFAULT_WITH_FILE_LOAD_EXPECTED)

    def test_save_config_default_filetype(self):
        print 'ConfigBase test #6'
        c = ExampleConfig()
        # get a temp file we can write our config object to
        tmpfile = tempfile.NamedTemporaryFile()
        # write out the config to our tmpfile
        c.save(tmpfile.name)
        # re-open the file, loading the data as yaml, for testing
        saved = yaml.safe_load(open(tmpfile.name, 'r'))
        # confirm that the file we've written is valid and matches the config
        self.assertSequenceEqual(saved, c)

    def test_save_config_as_yaml_explicit(self):
        print 'ConfigBase test #7'
        c = ExampleConfig()
        # get a temp file we can write our config object to
        tmpfile = tempfile.NamedTemporaryFile()
        # write out the config to our tmpfile
        c.file_path = tmpfile.name
        c.file_format = 'yaml'
        c.save()
        # re-open the file, loading the data as yaml, for testing
        saved = yaml.safe_load(open(tmpfile.name, 'r'))
        # confirm that the file we've written is valid and matches the config
        self.assertSequenceEqual(saved, c)

    def test_save_config_as_json_explicit(self):
        print 'ConfigBase test #8'
        c = ExampleConfig()
        # get a temp file we can write our config object to
        tmpfile = tempfile.NamedTemporaryFile()
        # write out the config to our tmpfile
        c.file_path = tmpfile.name
        c.file_format = 'json'
        c.save()
        # re-open the file, loading the data as json, for testing
        saved = json.load(open(tmpfile.name, 'r'))
        # confirm that the file we've written is valid and matches the config
        self.assertSequenceEqual(saved, c)

    def test_init_with_runtime(self):
        print 'ConfigBase test #9'
        c = ExampleConfig(RUNTIME_CONFIG)
        self.assertSequenceEqual(c, RUNTIME_CONFIG_EXPECTED)


if __name__ == '__main__':
    unittest.main()
