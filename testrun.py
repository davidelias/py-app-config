#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

import unittest
tests = unittest.TestLoader().discover('app_config')
unittest.TextTestRunner(verbosity=1).run(tests)
