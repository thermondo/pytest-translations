# coding=utf8
import os

import polib
import pytest

pytest_plugins = "pytester",


def test_version():
    import pytest_translations
    assert pytest_translations.__version__


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
            "*collected 4*",
            "*Invalid mo file*",
            "*1 failed*3 passed*",
        ])

    def test_ok(self, testdir, pomo):
        result = testdir.runpytest("--translations")
        assert result.ret == 0
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*4 passed*",
        ])

    def test_missing_po(self, testdir, pomo):
        po, mo = pomo
        os.unlink(po)

        result = testdir.runpytest("--translations")
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
            #: asdf.py:111
            msgid "bike"
            msgstr "Fahrrad"
            """
        )

        result = testdir.runpytest("--translations")
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 4*",
            "*mo*file content does not match po*",
            "*bike*Fahrrad*",
            "*1 failed*3 passed*",
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
        assert result.ret == 0
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
        result = testdir.runpytest('--translations')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*Syntax error*",
            "*3 failed*",
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
        result = testdir.runpytest('--translations')
        assert result.ret == 0
        result.stdout.fnmatch_lines([
            "*collected 3*",
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
        result = testdir.runpytest('--translations')
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
        result = testdir.runpytest('--translations')
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
        result = testdir.runpytest('--translations')
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
        result = testdir.runpytest('--translations')
        assert result.ret == 1
        result.stdout.fnmatch_lines([
            "*collected 3*",
            "*untranslated*",
            "*fuzzy*",
            "*obsolete*",
            "*3 failed*",
        ])
