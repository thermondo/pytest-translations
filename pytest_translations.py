from __future__ import (absolute_import, unicode_literals, division,
                        print_function)

import os
import tempfile
import shutil

from py.test.collect import File, Item


MARKER_NAME = 'translations'


def pytest_collect_file(path, parent):
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


def _msgfmt(i):
    return '"{}": "{}"'.format(
        i.msgid,
        i.msgstr,
    )


class TranslationException(Exception):
    pass


class PoBaseItem(Item):
    def __init__(self, name, parent):
        super(PoBaseItem, self).__init__(name, parent)
        self.add_marker(MARKER_NAME)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TranslationException):
            msg, wrong = excinfo.value.args

            msg += "\n{}".format(self.fspath)

            msg += '\n' + '\n'.join(
                _msgfmt(i)
                for i in wrong
            )

            return msg

        else:
            return super(PoBaseItem, self).repr_failure(excinfo)


class PoUntranslatedItem(PoBaseItem):
    def runtest(self):
        import polib
        parsed = polib.pofile(str(self.fspath))

        untranslated = parsed.untranslated_entries()

        if not untranslated:
            return

        raise TranslationException(
            'found untranslated entries in file.',
            untranslated,
        )

    def reportinfo(self):
        return (self.fspath, -1, "po-untranslated")


class PoObsoleteItem(PoBaseItem):
    def runtest(self):
        import polib
        parsed = polib.pofile(str(self.fspath))

        obsolete = parsed.obsolete_entries()

        if not obsolete:
            return

        raise TranslationException(
            'found obsolete entries in file.',
            obsolete,
        )

    def reportinfo(self):
        return (self.fspath, -1, "po-obsolete")


class PoFuzzyItem(PoBaseItem):
    def runtest(self):
        import polib
        parsed = polib.pofile(str(self.fspath))

        fuzzy = parsed.fuzzy_entries()

        if not fuzzy:
            return

        raise TranslationException(
            'found fuzzy entries in file.',
            fuzzy,
        )

    def reportinfo(self):
        return (self.fspath, -1, "po-fuzzy")


class PoFile(File):
    def __init__(self, path, parent):
        super(PoFile, self).__init__(path, parent)

        if hasattr(self, 'add_marker'):
            self.add_marker(MARKER_NAME)
        else:
            self.keywords[MARKER_NAME] = True

    def collect(self):
        yield PoUntranslatedItem(
            self.name,
            self,
        )
        yield PoFuzzyItem(
            self.name,
            self,
        )
        yield PoObsoleteItem(
            self.name,
            self,
        )


class MoFileItem(Item, File):
    def __init__(self, path, parent):
        super(MoFileItem, self).__init__(path, parent)

        if hasattr(self, 'add_marker'):
            self.add_marker(MARKER_NAME)
        else:
            self.keywords[MARKER_NAME] = True

    def runtest(self):
        import polib
        po_path, _ = os.path.splitext(str(self.fspath))
        po_path = po_path + ".po"

        po_file = polib.pofile(po_path)

        temp_dir = tempfile.mkdtemp()

        try:
            test_file = os.path.join(temp_dir, 'test.mo')
            po_file.save_as_mofile(test_file)

            original_parsed = polib.mofile(str(self.fspath))
            test_parsed = polib.mofile(test_file)

            if len(original_parsed) != len(test_parsed):
                raise TranslationException(
                    'mo-file length does not match po.',
                    []
                )

            diff = []

            for l, r in zip(original_parsed, test_parsed):
                if not (l.msgid == r.msgid and
                        l.msgid_plural == r.msgid_plural and
                        l.msgstr == r.msgstr and
                        l.msgstr_plural == r.msgstr_plural
                        ):

                    diff.append(
                        (l, r)
                    )

            if diff:
                raise TranslationException(
                    'mo-file content does not match po.',
                    diff,
                )

        finally:
            shutil.rmtree(temp_dir)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TranslationException):
            msg, diff = excinfo.value.args

            msg += '\n' + '\n'.join(
                '{} -> {}'.format(
                    _msgfmt(l),
                    _msgfmt(r),
                )
                for l, r in diff
            )

            return msg

        else:
            return super(MoFileItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "mo-test")
