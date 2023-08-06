"""
When ``wcwidth`` is installed, if ``cjkjust.raises_on_indeterminate`` is set
to ``False`` (default), the display width of all characters ``c`` such that
``wcwidth.wcwidth(c) == -1`` will be treated as 1; otherwise, ``ValueError``
will be raised. When ``wcwidth`` is not installed, the value of
``cjkjust.raises_on_indeterminate`` has no effect.
"""

__all__ = [
    'is_wide',
    'cjklen',
    'cjkljust',
    'cjkrjust',
    'cjkcenter',
]

raises_on_indeterminate = False

try:
    import wcwidth
except ImportError:
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
else:

    def is_wide(char):
        """
        Returns ``True`` if ``char`` is a character displayed wide.
        """
        return wcwidth.wcwidth(char) == 2

    # reimplement `wcswidth` from
    # https://github.com/jquast/wcwidth/blob/master/wcwidth/wcwidth.py
    def cjklen(string):
        if not raises_on_indeterminate:
            width = 0
            for char in string:
                wcw = wcwidth.wcwidth(char)
                if wcw < 0:
                    wcw = 1
                width += wcw
            return width
        return wcwidth.wcswidth(string)

    def cjkljust(string, width, fillbyte=' '):
        """
        Same as ``str.ljust`` except for support of CJK characters.
        """
        display_width = cjklen(string)
        if display_width < 0:
            raise ValueError(
                'string {!r} contains character(s) having indeterminate '
                'effect on the terminal'.format(string))
        return string.ljust(len(string) + width - display_width, fillbyte)

    def cjkrjust(string, width, fillbyte=' '):
        """
        Same as ``str.rjust`` except for support of CJK characters.
        """
        display_width = cjklen(string)
        if display_width < 0:
            raise ValueError(
                'string {!r} contains character(s) having indeterminate '
                'effect on the terminal'.format(string))
        return string.rjust(len(string) + width - display_width, fillbyte)

    def cjkcenter(string, width, fillbyte=' '):
        """
        Same as ``str.center`` except for support of CJK characters.
        """
        display_width = cjklen(string)
        if display_width < 0:
            raise ValueError(
                'string {!r} contains character(s) having indeterminate '
                'effect on the terminal'.format(string))
        return string.center(len(string) + width - display_width, fillbyte)
