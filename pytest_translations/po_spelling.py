import os
import re

from pytest import Item, skip

from pytest_translations.config import MARKER_NAME
from pytest_translations.utils import TranslationException

try:
    import enchant
    from enchant.tokenize import (
        get_tokenizer, URLFilter,
        EmailFilter, HTMLChunker
    )
except ImportError:
    enchant = None


def is_enchant_installed():
    return not (enchant is None)


if enchant:
    supported_languages = [
        name.split('_')[0]
        for name, _ in enchant.list_dicts()
    ]
else:
    supported_languages = []


def word_lists():
    PWL = os.getenv('PYTEST_TRANSLATIONS_PRIVATE_WORD_LIST')

    if enchant and PWL and os.path.exists(PWL):
        return {
            fn: os.path.join(PWL, fn)
            for fn in os.listdir(PWL)
            if not os.path.isdir(fn)
        }

    else:
        return {}


class PoSpellCheckingItem(Item):
    def __init__(self, line, language, name, parent):
        self.line = line
        self.language = language

        wl = word_lists()

        private_word_list = wl.get(language, None)

        if enchant and language in supported_languages:
            self.lang_dict = enchant.DictWithPWL(language, pwl=private_word_list)
        else:
            self.lang_dict = None

        super(PoSpellCheckingItem, self).__init__(name, parent)
        self.add_marker(MARKER_NAME)

    def runtest(self):
        if not enchant:
            skip("enchant is not installed")

        if not self.language:
            skip("no language defined in PO file")

        if self.language not in supported_languages:
            skip(
                "aspell dictionary for language {} not found.".format(self.language)
            )

        text = self.line.msgstr

        # remove python format placeholders, old and new,
        # where it's a problem.
        # 1. replace everything between curly braces
        text = re.sub('{.*?}', '', text)
        # 2. remove everything between %( and )
        text = re.sub('\%\(.*?\)', '', text)

        tokenizer = get_tokenizer(
            chunkers=[
                HTMLChunker,
            ],
            filters=(
                EmailFilter,
                URLFilter,
            ),
        )
        tokens = tokenizer(text)

        errors = [
            t
            for t, _ in tokens
            if not self.lang_dict.check(t)
            ]

        if errors:
            raise TranslationException(
                "Spell checking failed: {}".format(', '.join(errors)),
                self.line.msgstr,
                [
                    (t, self.lang_dict.suggest(t))
                    for t in errors
                    ]
            )

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, TranslationException):
            msg, line, wrong = excinfo.value.args
            lines = [msg, "%s" % self.fspath, "msgstr \"%s\"" % line]
            for i in wrong:
                lines.append("%s: %s" % i)

            return "\n".join(lines)

        else:
            return super(PoSpellCheckingItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.fspath, -1, 'po-spelling')
