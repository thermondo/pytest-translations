|version| |ci| |coverage| |license|

PyTest Translations
===================

A py.test plugin to check ``gettext`` ``po`` & ``mo`` files.

Test check for:

-  Spelling (using enchant & aspell)
-  Consistency of ``mo`` files
-  Obsolete translations
-  Fuzzy translations

Installation
------------

Install the PyPi package.

.. code:: bash

    pip install pytest-translations

The spell checking requires enchant and aspell including the correct
dictionary.

On Linux simply install:

.. code:: bash

    sudo apt-get install python3-enchant python-enchant aspell-{en|de|CHOSE YOUR LANGUAGE CODES}

To set up travis-ci simply add the apt packages to your travis-ci config
YAML:

.. code:: yaml

    addons:
      apt:
        packages:
        - python-enchant
        - python3-enchant
        - aspell-en
        - aspell-de

On Mac you can use brew to install:

.. code:: bash

    brew install aspell --with-lang-{en|de|CHOSE YOUR LANGUAGE CODES}
    brew install enchant

Usage
-----

To execute the translation tests simply run

.. code:: bash

    py.test --translations

Every file ending in ``.mo`` and ``.po`` will be discovered and tested,
starting from the command line arguments.

You also can execute only the translation-tests by using:

.. code:: bash

    py.test -m translations --translations

Private Word Lists
~~~~~~~~~~~~~~~~~~

You will almost certainly use words that are not included in the default
dictionaries. That is why you can add your own word list that you want
to add to the dictionary.

You may do so by adding a plain text file where each line is a word.
Words beginning with a capital letter are case sensitive where lower case words
are insensitive.

There can be one file for each language contained in a single folder.
The files should be named like the proper language code.

For example:

.. code:: bash

    .
    └── .spelling
        ├── de
        ├── en_GB
        └── en_US

What’s left to do is to set an environment variable to point to right
directory.

For example:

.. code:: bash

    export PYTEST_TRANSLATIONS_PRIVATE_WORD_LIST=path/to/my/.spelling

.. |version| image:: https://img.shields.io/pypi/v/pytest-translations.svg
   :target: https://pypi.python.org/pypi/pytest-translations/
.. |ci| image:: https://api.travis-ci.org/Thermondo/pytest-translations.svg?branch=master
   :target: https://travis-ci.org/Thermondo/pytest-translations
.. |coverage| image:: https://codecov.io/gh/Thermondo/pytest-translations/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Thermondo/pytest-translations
.. |license| image:: https://img.shields.io/badge/license-APL_2-blue.svg
   :target: LICENSE
