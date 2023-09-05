import os
import shutil
import tempfile

from pytest import File, Item

from pytest_translations.config import MARKER_NAME
from pytest_translations.utils import (
    TranslationException,
    msgfmt,
    open_mo_file,
    open_po_file,
)


class MoFile(File):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if hasattr(self, "add_marker"):
            self.add_marker(MARKER_NAME)
        else:
            self.keywords[MARKER_NAME] = True

    def collect(self):
        yield MoItem.from_parent(
            name=self.name,
            parent=self,
        )


class MoItem(Item):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.add_marker(MARKER_NAME)

    def runtest(self):
        po_path, _ = os.path.splitext(str(self.path))
        po_path += ".po"

        if not os.path.exists(po_path):
            raise TranslationException("corresponding .po file does not exist", [])

        po_file = open_po_file(po_path)

        temp_dir = tempfile.mkdtemp()

        try:
            test_file = os.path.join(temp_dir, "test.mo")
            po_file.save_as_mofile(test_file)

            original_parsed = open_mo_file(self.path)
            test_parsed = open_mo_file(test_file)

            if len(original_parsed) != len(test_parsed):
                raise TranslationException("mo-file length does not match po.", [])

            diff = []

            for lhs, rhs in zip(original_parsed, test_parsed):
                if not (
                    lhs.msgid == rhs.msgid
                    and lhs.msgid_plural == rhs.msgid_plural
                    and lhs.msgstr == rhs.msgstr
                    and lhs.msgstr_plural == rhs.msgstr_plural
                ):
                    diff.append((lhs, rhs))

            if diff:
                raise TranslationException(
                    "mo-file content does not match po.",
                    diff,
                )

        finally:
            shutil.rmtree(temp_dir)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TranslationException):
            msg, diff = excinfo.value.args

            msg += "\n" + "\n".join(
                "{0} -> {1}".format(
                    msgfmt(lhs),
                    msgfmt(rhs),
                )
                for lhs, rhs in diff
            )

            return msg

        else:
            return super().repr_failure(excinfo)

    def reportinfo(self):
        return (self.path, -1, "mo-test")
