def msgfmt(i):
    return '"{0}": "{1}"'.format(
        i.msgid,
        i.msgstr,
    )


def open_po_file(fn):
    import polib

    try:
        return polib.pofile(str(fn))
    except Exception as e:
        raise TranslationException(
            str(e),
            [],
        )


def open_mo_file(fn):
    import polib

    try:
        return polib.mofile(str(fn))
    except Exception as e:
        raise TranslationException(
            str(e),
            [],
        )


class TranslationException(Exception):
    pass
