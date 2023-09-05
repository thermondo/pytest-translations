"""A py.test plugin to check ``gettext`` ``po`` & ``mo`` files."""


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--translations",
        action="store_true",
        help="perform some checks on .mo and .po files",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "translations: translation tests")


def pytest_collect_file(file_path, parent):
    from .mo_files import MoFile
    from .po_files import PoFile

    config = parent.config
    if config.option.translations:
        if file_path.suffix == ".mo":
            return MoFile.from_parent(
                path=file_path,
                parent=parent,
            )
        elif file_path.suffix == ".po":
            return PoFile.from_parent(path=file_path, parent=parent)
