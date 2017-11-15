from pytest import File, Item

from pytest_translations.config import MARKER_NAME
from pytest_translations.po_spelling import PoSpellCheckingItem
from pytest_translations.utils import TranslationException, open_po_file, msgfmt


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
        try:
            parsed = open_po_file(self.fspath)
        except TranslationException:
            # if the PO file is invalid, we can't do spellchecking.
            # the other tests will fail then, but this here is the collection phase.
            pass
        else:
            language = parsed.metadata.get('Language', '')
            for line in parsed.translated_entries():
                yield PoSpellCheckingItem(
                    line,
                    language,
                    self.name,
                    self,
                )


class PoBaseItem(Item):
    def __init__(self, name, parent):
        super(PoBaseItem, self).__init__(name, parent)
        self.add_marker(MARKER_NAME)

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TranslationException):
            msg, wrong = excinfo.value.args

            msg += "\n{0}".format(self.fspath)

            msg += '\n' + '\n'.join(
                msgfmt(i)
                for i in wrong
            )

            return msg

        else:
            return super(PoBaseItem, self).repr_failure(excinfo)


class PoUntranslatedItem(PoBaseItem):
    def runtest(self):
        parsed = open_po_file(self.fspath)

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
        parsed = open_po_file(self.fspath)

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
        parsed = open_po_file(self.fspath)

        fuzzy = parsed.fuzzy_entries()

        if not fuzzy:
            return

        raise TranslationException(
            'found fuzzy entries in file.',
            fuzzy,
        )

    def reportinfo(self):
        return (self.fspath, -1, "po-fuzzy")
