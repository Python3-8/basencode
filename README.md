# basencode

Convert numbers of any base back and forth.

## Getting Started

To install `basencode`, run `python3 -m pip install basencode`. Now you should be able to use `basencode` in any Python program.

## Example

```py
>>> from basencode import *
>>> n1 = Number(12345)
# Default digits are used
>>> n1.repr_in_base(64)
'30V'
# Construct Number from base 64
>>> Number('30V', 64)
Number(12345)
>>> n1.repr_in_base(8)
'30071'
>>> n1.to_octal()
'30071'
>>> n1.to_bin()
'11000000111001'
# Overriding default digits
>>> n1.repr_in_base(2, list('-+'))
'++------+++--+'
>>> n1.to_bin()
'++------+++--+'
>>> n1.repr_in_base(33)
'bb3'
>>> from string import digits, ascii_letters, punctuation
>>> n1.repr_in_base(76, list(digits + ascii_letters + punctuation[:14]))
'2ax'
>>> n1.repr_in_base(76) # Digits provided above were stored as default digits for base 76
'2ax'
>>> n2 = Number(54321)
>>> n1 + n2
Number(66666)
>>> n2 - n1
Number(41976)
>>> n1 * n2
Number(670592745)
# Both true and floor division return a Number and perform the same functionality (as of now)
>>> n2 / n1
Number(4)
>>> n2 // n1
Number(4)
>>> n2 % n1
Number(4941)
>>> divmod(n2, n1)
(Number(4), Number(4941))
# Operations can also be performed with integers, though Numbers will be returned
>>> n1 == 12345
True
>>> n1 + 54321
Number(66666)
# Modes can be used to indicate how the representation should be
>>> n1.repr_in_base(64, mode='s') # 'mode' is 's' by default
'30V'
>>> n1.repr_in_base(2, digits=['--', '++'], mode='l')
['++', '++', '--', '--', '--', '--', '--', '--', '++', '++', '++', '--', '--', '++']
```

## TODO

- Add support for `float`s
- Retain all default digits during arithmetic operations

## Documentation

### Global Variables

- `ALL_DIGITS`: `str` of all digits used in default digits
- `BASE_DIGITS`: `Dict[int, List[str]]` of all default digits for bases 1-64

### Classes

- `Number`: `Number` class

#### Class Properties

- `Number.base_digits`: `Dict[int, List[str]]` of all default digits for the `Number`, updated by `Number._get_digits`
- `Number.dec_value -> int`: This getter returns the decimal value of the `Number` as an `int` which is stored in `Number._dec_value`

#### Class Methods

- `Number.__init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None`: Takes `n` (`str` preferred, `int` is okay if `base` is `10`) and converts it from `base` (`int`) to decimal and stores in `Number._dec_value`; `digits` (`List[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `Number.repr_in_base(self, base: int, digits: List[str] = []) -> str`: Converts `Number._dec_value` to `base` (`int`), and returns a `str`; `digits` (`List[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `Number.to_dec(self) -> int`: Returns `Number._dec_value`
- `Number.to_bin(self) -> str`: Uses `Number.repr_in_base` to convert `Number._dec_value` to binary
- `Number.to_octal(self) -> str`: Uses `Number.repr_in_base` to convert `Number._dec_value` to octal
- `Number.to_hex(self) -> str`: Uses `Number.repr_in_base` to convert `Number._dec_value` to hexadecimal
- `Number.repr_in_base64(self) -> str`: Uses `Number.repr_in_base` to convert `Number._dec_value` to base 64

## Things to Note

- When providing the `digits` property, make sure the digits are in order from lowest value to highest value, for example, the `digits` property for hexadecimal would look like this: `list('0123456789abcdef')`
- By default, the default digits for all bases up to base 64 go as so:

  - Digits 0-9
  - Lowercase alphabet
  - Uppercase alphabet
  - `+` and `/`

  therefore, `Number('DF', 16)` without overriding the digits for base 16 will throw an error because hexadecimal only has the digits 0-f (**lowercase** "f"). `Number('df', 16)` will construct `Number(223)`.
