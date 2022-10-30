# basencode

Convert numbers of any base back and forth.

## Getting Started

To install `basencode`, run `python3 -m pip install basencode`. Now you should be able to use `basencode` in any Python program.

## Example

```py
>>> from basencode import *
>>> n1 = Number(12345)
>>> n1.to_base(64) # Default digits are used, but can be overridden
'30V'
>>> Number('30V', 64) # Construct Number from base 64
Number(12345)
>>> n1.to_base(8)
'30071'
>>> n1.to_octal()
'30071'
>>> n1.to_bin()
'11000000111001'
>>> n1.to_base(2, list('-+'))
'++------+++--+'
>>> n1.to_bin() # Default digits were overridden
'++------+++--+'
>>> n1.to_base(33)
'bb3'
>>> from string import digits, ascii_letters, punctuation
>>> n1.to_base(76, list(digits + ascii_letters + punctuation[:14]))
'2ax'
>>> n1.to_base(76) # Digits provided above were stored as default digits for base 76
'2ax'
>>> n2 = Number(54321)
>>> n1 + n2
Number(66666)
>>> n2 - n1
Number(41976)
>>> n1 * n2
Number(670592745)
>>> n2 / n1
Number(4)
>>> n2 // n1
Number(4)
>>> n2 % n1
Number(4941)
>>> divmod(n2, n1)
(Number(4), Number(4941))
```

## TODO

- Add support for `float`s
- Retain all default digits during arithmetic operations

## Documentation

### Global Variables

- `BASE_DIGITS`: `Dict[int, List[str]]` of all default digits for bases 1-64

### Classes

- `Number`: `Number` class

#### Class Properties

- `Number.base_digits`: `Dict[int, List[str]]` of all default digits for the `Number`, updated by `Number._get_digits`
- `Number.dec_value -> int`: This getter returns the decimal value of the `Number` as an `int` which is stored in `Number._dec_value`

#### Class Methods

- `Number.__init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None`: Takes `n` (`str` preferred, `int` is okay if `base` is `10`) and converts it from `base` (`int`) to decimal and stores in `Number._dec_value`; `digits` (`List[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `Number.to_base(self, base: int, digits: List[str] = []) -> str`: Converts `Number._dec_value` to `base` (`int`), and returns a `str`; `digits` (`List[str]`) is required if `base` does not have default digits (see `BASE_DIGITS`)
- `Number.to_dec(self) -> int`: Returns `Number._dec_value`
- `Number.to_bin(self) -> str`: Uses `Number.to_base` to convert `Number._dec_value` to binary
- `Number.to_octal(self) -> str`: Uses `Number.to_base` to convert `Number._dec_value` to octal
- `Number.to_hex(self) -> str`: Uses `Number.to_base` to convert `Number._dec_value` to hexadecimal
- `Number.to_base64(self) -> str`: Uses `Number.to_base` to convert `Number._dec_value` to base 64

## Things to Know

- When providing the `digits` property, make sure the digits are in order from lowest value to highest value, for example, the `digits` property for hexadecimal would look like this: `list('0123456789abcdef')`
- By default, the default digits for all bases up to base 64 go as so:

  - Digits 0-9
  - Lowercase alphabet
  - Uppercase alphabet
  - `+` and `/`

  therefore, `Number('DF', 16)` without overriding the digits for base 16 will throw an error because hexadecimal only has the digits 0-f (**lowercase** "f"). `Number('df', 16)` will construct `Number(223)`.
