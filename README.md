[![version](https://img.shields.io/pypi/v/pytest-translations.svg)](https://pypi.python.org/pypi/pytest-translations/)
[![ci](https://api.travis-ci.org/Thermondo/pytest-translations.svg?branch=master)](https://travis-ci.org/Thermondo/pytest-translations)
[![coverage](https://coveralls.io/repos/Thermondo/pytest-translations/badge.svg?branch=master)](https://coveralls.io/r/Thermondo/pytest-translations)
[![code-health](https://landscape.io/github/Thermondo/pytest-translations/master/landscape.svg?style=flat)](https://landscape.io/github/Thermondo/pytest-translations/master)
[![license](https://img.shields.io/badge/license-APL_2-blue.svg)](LICENSE)
[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Thermondo/pytest-translations?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

# PyTest Translations

A py.test plugin to check `gettext` `po` & `mo` files.

Test check for:

* Spelling (using enchant & aspell)
* Consistency of `mo` files
* Obsolete translations
* Fuzzy translations

## Installation

Install the PyPi package.
```bash
pip install pytest-translations
```

The spell checking requires enchant and aspell including the correct dictionary.

On Linux simply install:

```bash
sudo apt-get install python3-enchant python-enchant aspell-{en|de|CHOSE YOUR LANGUAGE CODES} 
```

To set up travis-ci simply add the apt packages to your travis-ci config YAML:

```YAML
addons:
  apt:
    packages:
    - python-enchant
    - python3-enchant
    - aspell-en
    - aspell-de
```

On Mac you can use brew to install:

```bash
brew install aspell --with-lang-{en|de|CHOSE YOUR LANGUAGE CODES}
brew install enchant
```

## Usage

To execute the translation tests simply run
```bash
py.test --translations
```
Every file ending in ``.mo`` and ``.po`` will be discovered and tested, 
starting from the command line arguments. 

You also can execute only the translation-tests by using:
```bash
py.test -m translations --translations
```

### Private World Lists
You will almost certainly use words that are not included
in the default dictionaries. That is why you can add your
own word list that you want to add to the dictionary.

You may do so by adding a plain text file where each line
is a word.
Capital words are case sensitive where lower case words are insensitive.

There can be one file for each language contained in a single folder.
The files should be named like the proper language code.

For example:
```bash
.
└── .spelling
    ├── de
    ├── en_GB
    └── en_US
```

What's left to do is to set an environment variable to point to right
directory.

For example:
```bash
export PYTEST_TRANSLATIONS_PRIVATE_WORD_LIST=path/to/my/.spelling
```

## [License](LICENSE)