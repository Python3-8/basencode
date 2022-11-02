# basencode [![Downloads](https://static.pepy.tech/personalized-badge/basencode?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20downloads)](https://pepy.tech/project/basencode)

Convert numbers of any base back and forth.

## Getting Started

To install `basencode`, run `python3 -m pip install basencode`. Now you should be able to use `basencode` in any Python program.

## Example

```py
>>> from basencode import *
>>> n1 = Number(12345) # Number constructs an Integer (in this case), Integer can be called too
# Default digits are used
>>> n1.repr_in_base(64)
'30V'
# Construct Integer from base 64
>>> Number('30V', 64)
Integer(12345)
>>> n1.repr_in_base(8)
'30071'
>>> n1.repr_in_octal()
'30071'
>>> n1.repr_in_bin()
'11000000111001'
# Overriding default digits
>>> n1.repr_in_base(2, list('-+'))
'++------+++--+'
>>> n1.repr_in_bin()
'++------+++--+'
>>> n1.repr_in_base(33)
'bb3'
>>> from string import digits, ascii_letters, punctuation
>>> n1.repr_in_base(76, list(digits + ascii_letters + punctuation[:14]))
'2ax'
>>> n1.repr_in_base(76) # Digits provided above were stored as default digits for base 76
'2ax'
>>> n2 = Integer(54321)
>>> n1 + n2
Integer(66666)
>>> n2 - n1
Integer(41976)
>>> n1 * n2
Integer(670592745)
# Both true and floor division return an Integer and perform the same functionality (as of now)
>>> n2 / n1
Float(4.400243013365737)
>>> n2 // n1
Integer(4)
>>> n2 % n1
Integer(4941)
>>> divmod(n2, n1)
(Integer(4), Integer(4941))
# Operations can also be performed with ints, though Integers will be returned
>>> n1 == 12345
True
>>> n1 + 54321
Integer(66666)
# Modes can be used to indicate how the representation should be
>>> n1.repr_in_base(64, mode='s') # 'mode' is 's' by default
'30V'
>>> n1.repr_in_base(2, digits=['--', '++'], mode='l')
['++', '++', '--', '--', '--', '--', '--', '--', '++', '++', '++', '--', '--', '++']
# Floats can be converted back and forth too
>>> Float(10.1, 2)
Float(2.5)
>>> Float(10.1, 2).repr_in_base(8)
'2.4'
>>> Float(22.22, 3).repr_in_base(7)
'11.613613613613613611501...'
```

## TODO

1. Use `decimal.Decimal`s in `Float`s to reduce miscalculation

## Documentation

### Global Variables

- `ALL_DIGITS`: `str` of all digits used in default digits
- `BASE_DIGITS`: `dict[int, list[str]]` of all default digits for bases 1-64
- `RADIX_POINT`: `str` - the default radix point for `Float`s

### Number class

The `Number` class is a sort of wrapper that creates an `Integer` or a `Float`
depending on the number provided.

### Integer class

#### Class Properties

- `base_digits`: `dict[int, list[str]]` of all default digits for the `Integer`, updated by `Integer._get_digits`
- `dec_value -> int`: This getter returns the decimal value of the `Integer` as an `int` which is stored in `Integer._dec_value`

#### Class Methods

- `__init__(self, n: int | str | tuple[int | str], base: int = 10, digits: list[str] = []) -> None`: Takes `n`, converts it from `base` (`int`) to decimal, stores in `Integer._dec_value`; `digits` (`list[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `repr_in_base(self, base: int, digits: list[str] = [], mode: str = 's') -> str | list[str]`: Converts `Integer._dec_value` to `base` (`int`), and returns the result as a a `str` if `mode` (`int`) is `'s'`, or a `list` if `mode` is `'l'`; `digits` (`list[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `repr_in_dec(self, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(10, mode=mode)` (see `Integer.repr_in_base`)
- `repr_in_bin(self, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(2, mode=mode)` (see `Integer.repr_in_base`)
- `repr_in_octal(self, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(8, mode=mode)` (see `Integer.repr_in_base`)
- `repr_in_hex(self, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(16, mode=mode)` (see `Integer.repr_in_base`)
- `repr_in_base64(self, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(64, mode=mode)` (see `Integer.repr_in_base`)

### Float class

#### Class Properties

- `base_digits`: `dict[int, list[str]]` of all default digits for the `Float`, updated by `Float._get_digits`
- `dec_value -> float`: This getter returns the decimal value of the `Float` as a `float` which is stored in `Float._dec_value`

#### Class Methods

- `__init__(self, n: int | str | tuple[int | str], base: int = 10, digits: list[str] = [], radix_point: str = RADIX_POINT) -> None`: Takes `n`, converts it from `base` (`int`) to decimal, stores in `Float._dec_value`; `digits` (`list[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `repr_in_base(self, base: int, digits: list[str] = [], radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Converts `Float._dec_value` to `base` (`int`), and returns the result as a a `str` if `mode` (`int`) is `'s'`, or a `list` if `mode` is `'l'`; `digits` (`list[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `repr_in_dec(self, radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(10, radix_point=radix_point, mode=mode)` (see `Float.repr_in_base`)
- `repr_in_bin(self, radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(2, radix_point=radix_point, mode=mode)` (see `Float.repr_in_base`)
- `repr_in_octal(self, radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(8, radix_point=radix_point, mode=mode)` (see `Float.repr_in_base`)
- `repr_in_hex(self, radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(16, radix_point=radix_point, mode=mode)` (see `Float.repr_in_base`)
- `repr_in_base64(self, radix_point: str = RADIX_POINT, mode: str = 's') -> str | list[str]`: Returns `repr_in_base(64, radix_point=radix_point, mode=mode)` (see `Float.repr_in_base`)

## Things to Note

- When providing the `digits` property, make sure the digits are in order from lowest value to highest value, for example, the `digits` property for hexadecimal would look like this: `list('0123456789abcdef')`
- By default, the default digits for all bases up to base 64 go as so:

  - Digits 0-9
  - Lowercase alphabet
  - Uppercase alphabet
  - `+` and `/`

  therefore, `Number('DF', 16)` without overriding the digits for base 16 will throw an error because hexadecimal only has the digits 0-f (**lowercase** "f"). `Number('df', 16)` will construct `Integer(223)`.
