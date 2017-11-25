# coding=utf8
import os

import polib
import pytest


pytest_plugins = "pytester",


class TestMo(object):
    @pytest.fixture
    def pomo(self, testdir):
        pofile = testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car"
            msgstr "Auto"
            """
        )

        p, ext = os.path.splitext(str(pofile))
        mofile = p + ".mo"

        polib.pofile(str(pofile)).save_as_mofile(mofile)

        return str(pofile), str(mofile)

    def test_broken_file(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car"
            msgstr "Auto"
            """
        )
        testdir.makefile(
            'mo',
            """
            asdflkaj sdlkfaj
            """,
        )

        result = testdir.runpytest("--translations")
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 5*",
            "*Invalid mo file*",
            "*1 failed*",
        ])

    def test_ok(self, testdir, pomo):
        result = testdir.runpytest("--translations", '-vvv')
        assert result.ret == 0
        result.stdout.fnmatch_lines([
            "*collected 5*",
            "*4 passed*",
        ])

    def test_missing_po(self, testdir, pomo):
        po, mo = pomo
        os.unlink(po)

        result = testdir.runpytest("--translations", '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 1*",
            "*corresponding .po file does not exist*",
            "*1 failed*",
        ])

    def test_entry_mismatch(self, testdir, pomo):
        po, mo = pomo
        os.unlink(po)

        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: de\n"

            #: asdf.py:111
            msgid "bike"
            msgstr "Fahrrad"
            """
        )

        result = testdir.runpytest("--translations", '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 5*",
            "*mo*file content does not match po*",
            "*bike*Fahrrad*",
        ])


class TestPo(object):
    def test_uses_argument(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car"
            msgstr "Auto"
            """
        )
        result = testdir.runpytest()
        result.stdout.fnmatch_lines([
            "*collected 0*",
        ])

    def test_broken_file(self, testdir):
        testdir.makefile(
            'po',
            """
            asdflkaj sdlkfaj
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*Syntax error*",
        ])

    def test_valid(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car"
            msgstr "Auto"
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 0
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*3 passed*",
        ])

    def test_missing_translation(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car"
            msgstr ""
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*1 failed*2 passed*",
        ])

    def test_fuzzy(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            #, fuzzy
            msgid "car"
            msgstr "Auto"
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*fuzzy*",
            "*1 failed*2 passed*",
        ])

    def test_obsolete(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            #~ msgid "car"
            #~ msgstr "Auto"
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*obsolete*",
            "*1 failed*2 passed*",
        ])

    def test_all(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "car2"
            msgstr ""

            #: asdf.py:111
            #, fuzzy
            msgid "car1"
            msgstr "Auto1"

            #: asdf.py:111
            #~ msgid "car"
            #~ msgstr "Auto"
            """
        )
        result = testdir.runpytest('--translations', '-vvv')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*untranslated*",
            "*fuzzy*",
            "*obsolete*",
            "*3 failed*",
        ])


class TestPoSpellcheck(object):
    def test_broken_file(self, testdir):
        testdir.makefile(
            'po',
            """
            asdflkjasdf laskdjfasdf
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 3*",
        ])

    def test_language_missing_in_po(self, testdir):
        testdir.makefile(
            'po',
            """
            #: asdf.py:111
            msgid "meeting"
            msgstr "meeeting"
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "SKIP * no language defined in PO file",
        ])

    def test_language_catalog_missing(self, testdir):
        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: hr\\n"

            #: asdf.py:111
            msgid "meeting"
            msgstr "meeeting"
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "SKIP * aspell dictionary for language hr not found*",
        ])

    def test_python_format_placeholders(self, testdir):
        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: de\\n"

            #: asdf.py:111
            msgid "meeting"
            msgstr "Langer Text %(salkdjfalsdjf)s {kaksjsalkas} Verabredung"
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*4 passed*",
        ])

    def test_pass(self, testdir):
        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: de\\n"

            #: asdf.py:111
            msgid "meeting"
            msgstr "Verabredung"
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*4 passed*",
        ])

    def test_fail(self, testdir):
        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: de\\n"

            #: asdf.py:111
            msgid "meeting"
            msgstr "meeeting"
            """
        )
        result = testdir.runpytest('--translations', '-vvv', '-r', 's')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            '*Spell checking failed:*',
            '*msgstr "meeeting"*',
            "*1 failed*",
        ])

    def test_wordlist(self, testdir, monkeypatch):
        testdir.makefile(
            'po',
            """
            msgid ""
            msgstr ""
            "Language: de\\n"

            #: asdf.py:111
            msgid "meeting"
            msgstr "meeeting"
            """
        )

        test_dir = str(testdir.tmpdir.dirpath())
        wordlist_de = os.path.join(test_dir, 'de')
        assert not os.path.exists(wordlist_de)

        with open(wordlist_de, 'w+') as wl:
            wl.write("meeeting\n")

        monkeypatch.setenv('PYTEST_TRANSLATIONS_PRIVATE_WORD_LIST', test_dir)

        assert os.path.exists(wordlist_de)

        result = testdir.runpytest('--translations', '-vvv')
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*4 passed*",
        ])
