"""A py.test plugin to check ``gettext`` ``po`` & ``mo`` files."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


__version__ = '1.0.5'


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        '--translations',
        action='store_true',
        help="perform some checks on .mo and .po files"
    )


def pytest_collect_file(path, parent):
    from .mo_files import MoFileItem
    from .po_files import PoFile
    config = parent.config
    if config.option.translations:
        if path.ext == '.mo':
            return MoFileItem(
                path,
                parent=parent
            )
        elif path.ext == '.po':
            return PoFile(
                path,
                parent=parent
            )
