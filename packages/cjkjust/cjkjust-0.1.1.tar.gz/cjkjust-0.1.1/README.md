# cjkjust

Having strings containing CJK characters left-, right-justified or centered gracefully.

## Installation

```
pip install cjkjust
```

## Functions

- `is_wide(char) -> bool`: returns whether a character `char` is wide
- `cjklen(string) -> int`: returns the display width of a `string` containing CJK characters
- `cjkljust(string, width: int, fillbyte=' ')`: has `string` left-justified
- `cjkrjust(string, width: int, fillbyte=' ')`: has `string` right-justified
- `cjkcenter(string, width: int, fillbyte=' ')`: has `string` centered

Caveat: `<TAB>` in `string` ruins the print-out.

## Examples

```python
import cjkjust

# right-justify a column of strings
print(cjkjust.cjkrjust('hello 世界', 20))
print(cjkjust.cjkrjust('你好world', 20))
print(cjkjust.cjkrjust('again and again', 20))
```

## Optional dependency

- `wcwidth`: if installed, 0-width characters will also be well handled in `cjkljust`, `cjkrjust`, and `cjkcenter`
