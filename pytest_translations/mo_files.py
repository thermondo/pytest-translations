import os
import tempfile

import shutil
from pytest import File, Item

from pytest_translations.config import MARKER_NAME
from pytest_translations.utils import TranslationException, open_po_file, open_mo_file, msgfmt


class MoFileItem(Item, File):
    def __init__(self, path, parent):
        super(MoFileItem, self).__init__(path, parent)

        if hasattr(self, 'add_marker'):
            self.add_marker(MARKER_NAME)
        else:
            self.keywords[MARKER_NAME] = True

    def runtest(self):
        po_path, _ = os.path.splitext(str(self.fspath))
        po_path += ".po"

        if not os.path.exists(po_path):
            raise TranslationException(
                "corresponding .po file does not exist",
                []
            )

        po_file = open_po_file(po_path)

        temp_dir = tempfile.mkdtemp()

        try:
            test_file = os.path.join(temp_dir, 'test.mo')
            po_file.save_as_mofile(test_file)

            original_parsed = open_mo_file(self.fspath)
            test_parsed = open_mo_file(test_file)

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
                '{0} -> {1}'.format(
                    msgfmt(l),
                    msgfmt(r),
                )
                for l, r in diff
            )

            return msg

        else:
            return super(MoFileItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, "mo-test")
