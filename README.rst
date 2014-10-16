App Config
==========

When writing a Python application for the web, console, embedded system, or what
have you, *we should not be distracted by having to write, debug, and maintain
code to manage getting config from the user or environment*. Use this library if
you would rather ignore that problem.


What
----

.. code::

   >>> from app_config import ConfigBase
   >>> c = ConfigBase()
   >>> print c
   {}

* Simple, yet still powerful, generic configuration class for Python
  applications.
* Based on YAML, supports JSON, and much more.
* Config is a glorified dictionary, so is this (subclasses ``UserDict.UserDict``).
* There are reasonable expectations, deep merging, syncing config to/from
  config files, etc.


Features
--------

* Tries not to get in your way, but gives you a helping hand through the mundane.
* Simpler and more enjoyable to use than ConfigParser.
* Integrates well with option/argument parsing and environment variables.
* Read from one or more config files, merging the results together in order.
* Supports reading files formatted in YAML and JSON. Support for INI will come.
* Write/save to file, YAML formatted.
* Sensible deep-dictionary merging.
* Logging in places you want it, so you can debug what comes from where, when you
  need it.


Why
---

Using broken, complicated, and annoying libraries for basic configuration
management in Python applications became too painful to resist the temptation to
address the problem ourselves. Right?


How it works
------------

And how to use it.


Empty Config
~~~~~~~~~~~~

It's just a dictionary, no really:

.. code::

   >>> from app_config import ConfigBase
   >>> c = ConfigBase()
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base retrieving keys from the shell environment: []
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base config object init complete, the result: {}
   >>> print c
   {}


Logging
~~~~~~~

``app_config`` will likely be embedded within other applications where logging
is already taken care of.

We want to see what is happening internally, but only when it is meaningful. To
address this, ``app_config`` will..

* create its own logger if one is not provided;
* enable debug by default, when providing its own logger object;
* generate DEBUG log messages when doing important things.


Loading and saving files, retrieving options and environment variables, and
merging in updates to the config dictionary are all logged.

You can provide your own logger to the class, controlling debug and logging as
you determine:

.. code::

   >>> import logging
   >>> from app_config import ConfigBase
   >>> logging.basicConfig(format='%(levelname)s: %(name)s %(message)s',
   >>>                     level=logging.ERROR)
   >>> logger = logging.getLogger('app_config.test')
   >>> c = ConfigBase(lgr=logger)
   >>> print c
   {}


Runtime Config

~~~~~~~~~~~~~~

.. code::

   >>> from app_config import ConfigBase
   >>> c = ConfigBase({'foo': 'bar', 'baz': ['quz', 'qux', 'quu']})
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base retrieving keys from the shell environment: []
   DEBUG: app_config.base merging {} into {}
   DEBUG: app_config.base merging {'foo': 'bar', 'baz': ['quz', 'qux', 'quu']} into {}
   DEBUG: app_config.base config object init complete, the result: {'foo': 'bar', 'baz': ['quz', 'qux', 'quu']}

Note that runtime config is merged in after loading files, extracting environment
variables, and parsing options. The intention is to give the app a way to set
config that is determined by the app at run time, overriding everything else.


Load from File
~~~~~~~~~~~~~~

Create some config files with either YAML or JSON:

.. code::

   % echo '{foo: bar}' > /tmp/config.yaml
   % echo '{"baz": ["quz", "qux", "quu"]}' > /tmp/config.json
   % echo '{fuz: baq, foo: foobar}' > /tmp/config.yml


Read two of these files on init:

.. code::

   >>> import os
   >>> from app_config import ConfigBase
   >>> f = os.path.join('/', 'tmp', 'config.yaml')
   >>> g = os.path.join('/', 'tmp', 'config.json')
   >>> h = os.path.join('/', 'tmp', 'config.yml')
   >>> c = ConfigBase(fl=[f, g])
   DEBUG: app_config.base filelist is [], updating to ['/tmp/config.yaml', '/tmp/config.json']
   DEBUG: app_config.base attempting to load data from /tmp/config.yaml
   DEBUG: app_config.base loaded and parsed data from /tmp/config.yaml as yaml: {'foo': 'bar']}
   DEBUG: app_config.base merging {'foo': 'bar'} into {}
   DEBUG: app_config.base attempting to load data from /tmp/config.json
   DEBUG: app_config.base loaded and parsed data from /tmp/config.json as json: {'baz': ['quz', 'qux', 'quu']}
   DEBUG: app_config.base merging {'baz': ['quz', 'qux', 'quu']} into {'foo': 'bar'}


Let's read some more files:

.. code::

   >>> c.load_from([h])
   DEBUG: app_config.base filelist is [], updating to ['/tmp/config.yml']
   DEBUG: app_config.base attempting to load data from /tmp/config.yml
   DEBUG: app_config.base loaded and parsed data from /tmp/config.yml as yaml: {'foo': 'foobar', 'fuz': 'baq'}
   DEBUG: app_config.base merging {'foo': 'foobar', 'fuz': 'baq'} into {'foo': 'bar', 'baz': ['quz', 'qux', 'quu']}
   >>> c
   {'baz': ['quz', 'qux', 'quu'], 'foo': 'foobar', 'fuz': 'baq'}

Save to File
~~~~~~~~~~~~

By default, ``ConfigBase.save()`` will save create a new file in the current
working directory:

.. code::

   >>> c.save()
   DEBUG: app_config.base writing yaml file to /home/user/config.yaml
   True


We can tell ``save()`` to write the file to a specific location:

.. code::

   >>> c.save('/tmp/save.yaml')
   DEBUG: app_config.base updated file path to /tmp/save.yaml
   DEBUG: app_config.base writing yaml file to /tmp/save.yaml
   True


We can also update the file path used internally:

.. code::

   >>> c.file_path = os.path.join('/', 'tmp', 'foobar.yml')
   >>> c.save()
   DEBUG: app_config.base writing yaml file to /tmp/foobar.yml
   True


By default, the file is formatted in YAML:

.. code::

   % cat config.yaml 
   baz: [quz, qux, quu]
   foo: foobar
   fuz: baq



Update/Merge
~~~~~~~~~~~~

``ConfigBase`` uses reclass internally to handle deep-dictionary merging. We
also get reclass' interpolation free as part of the package. If that doesn't
mean much, see the example in the next section.

Here is how we merge in new data:

.. code::

   >>> c
   {'foo': 'bar'}
   >>> c.merge({'foo': 'baz', 'baq': {'bar': 'gaq', 'gar': 'quz'}})
   DEBUG: app_config.base merging {'foo': 'baz', 'baq': {'bar': 'gaq', 'gar': 'quz'}} into {'foo': 'bar'}
   >>> c
   {'foo': 'baz', 'baq': {'bar': 'gaq', 'gar': 'quz'}}


And again:

.. code::

   >>> c.merge({'baq': {'gar': ['gaz', 'gaq']}})
   DEBUG: app_config.base merging {'baq': {'gar': ['gaz', 'gaq']}} into {'foo': 'baz', 'baq': {'bar': 'gaq', 'gar': 'gaz'}}
   >>> c
   {'foo': 'baz', 'baq': {'bar': 'gaq', 'gar': ['gaz', 'gaz', 'gaq']}}


Interpolation
~~~~~~~~~~~~~

This is fun stuff:

.. code::

   >>> c
   {'foo': 'bar'}
   >>> c.merge({'baz': '${foo}'})
   DEBUG: app_config.base merging {'baz': '${foo}'} into {'foo': 'bar'}
   >>> c
   {'foo': 'bar', 'baz': 'bar'}


In this example, we are merging in a new dictionary with a key ``baz`` whose
value is a reference to ``foo``, eg, use the value of ``foo``. The result is
that both ``foo`` and ``baz`` are ``bar``.


Option Parsing
~~~~~~~~~~~~~~

Examples to come.


Using Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Examples to come.
