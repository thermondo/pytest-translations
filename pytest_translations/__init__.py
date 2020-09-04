"""A py.test plugin to check ``gettext`` ``po`` & ``mo`` files."""


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        '--translations',
        action='store_true',
        help="perform some checks on .mo and .po files"
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "translations: translation tests"
    )


def pytest_collect_file(path, parent):
    from .mo_files import MoFileItem
    from .po_files import PoFile

    config = parent.config
    if config.option.translations:
        if path.ext == '.mo':
            return MoFileItem.from_parent(
                fspath=path,
                parent=parent,
            )
        elif path.ext == '.po':
            return PoFile.from_parent(
                fspath=path,
                parent=parent
            )
