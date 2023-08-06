__all__ = [
    'is_wide',
    'cjklen',
    'cjkljust',
    'cjkrjust',
    'cjkcenter',
]

import unicodedata


def is_wide(char):
    """
    Returns ``True`` if ``char`` is a character displayed wide.
    """
    return unicodedata.east_asian_width(char) in 'FW'


def cjklen(string):
    """
    Returns the length of ``string`` where wide characters count for length
    of two.
    """
    return sum(2 if is_wide(char) else 1 for char in string)


def count_cjk_chars(string):
    """
    Count number of wide characters.
    """
    return sum(map(is_wide, string))


def cjkljust(string, width, fillbyte=' '):
    """
    Same as ``str.ljust`` except for support of CJK characters.

    >>> cjkljust('hello', 10, '*')
    'hello*****'
    >>> cjkljust('你好world', 10, '*')
    '你好world*'
    >>> cjkljust('你好world', 1, '*')
    '你好world'
    """
    #return string.ljust(len(string) + width - cjklen(string), fillbyte)
    return string.ljust(width - count_cjk_chars(string), fillbyte)


def cjkrjust(string, width, fillbyte=' '):
    """
    Same as ``str.rjust`` except for support of CJK characters.
    """
    #return string.rjust(len(string) + width - cjklen(string), fillbyte)
    return string.rjust(width - count_cjk_chars(string), fillbyte)


def cjkcenter(string, width, fillbyte=' '):
    """
    Same as ``str.center`` except for support of CJK characters.
    """
    return string.center(width - count_cjk_chars(string), fillbyte)
