===============================
pytest-translations
===============================

.. image:: https://badge.fury.io/py/pytest-translations.png
    :target: http://badge.fury.io/py/pytest-translations

.. image:: https://travis-ci.org/thermondo/pytest-translations.png?branch=master
        :target: https://travis-ci.org/thermondo/pytest-translations

.. image:: https://pypip.in/d/pytest-translations/badge.png
        :target: https://pypi.python.org/pypi/pytest-translations


py.test plugin to test your translation files. 

Usage
---------

install via::

    pip install pytest-translations

if you then type::

    py.test --translations
    
every file ending in ``.mo`` and ``.po`` will be discovered and tested, 
starting from the command line arguments. 

You also can execute only the translation-tests by using::

    py.test -m translations --translations

This plugin uses `polib <https://polib.readthedocs.org/en/latest/>`_ to parse and test the catalogs. 


Assertions on compiled ``.mo`` catalogs
---------------------------------------
- there has to be a ``.po``-file with the exact same name (only the different extension)
- is has to be parseable 
- the ``.po`` file compiled again has to lead to the exact same entries

Assertions on plain ``.po`` catalogs
---------------------------------------
- it has to be parseable 
- there mustn't be any untranslated entries
- there mustn't be any fuzzy entries
- there mustn't be any obsolete entries


Developing
---------- 
happens on 
https://github.com/thermondo/pytest-translations/

