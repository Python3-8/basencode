# basencode

Convert numbers of any base back and forth.

## Getting Started

To install `basencode`, run `python3 -m pip install basencode`. Now you should be able to use `basencode` in any Python program.

## Example
```py
>>> from basencode import *
>>> myint1 = Integer(12345)
>>> myint1.to_base(64) # Default digits are used, but can be overridden
'30v'
>>> myint1.to_base(8)
'30071'
>>> myint1.to_octal()
'30071'
>>> myint1.to_bin()
'11000000111001'
>>> myint1.to_base(2, list('-+')) # Default digits are overridden
'++------+++--+'
>>> myint1.to_base(33)
'BB3'
>>> from string import ascii_lowercase, ascii_uppercase, digits, punctuation
>>> myint1.to_base(76, list(digits + ascii_lowercase + ascii_uppercase + punctuation[:14]))
'2ax'
>>> myint1.to_base(76) # Digits provided above were stored as default digits for base 76
'2ax'
>>> myint2 = Integer(54321)
>>> myint1 + myint2
Integer(66666)
>>> myint2 - myint1
Integer(41976)
>>>
>>> myint1 * myint2
Integer(670592745)
>>> myint2 / myint1
Integer(4)
>>> myint2 // myint1
Integer(4)
>>> myint2 % myint1
Integer(4941)
>>> divmod(myint2, myint1)
(Integer(4), Integer(4941))

```

## TODO
* Support operations between `int` and `Integer`
* Add support for `float`s
* Retain all default digits during arithmetic operations

## Literally Everything

### Global Variables

* `BASEN_DIGITS`: `List[str]` of default digits for base `N`, default digits are defined for bases 2-36 and 64 
* `BASE_DIGITS`: `Dict[int, List[str]]` of all default digits

### Classes

* `Integer`: `Integer` class

#### Class Properties

* `Integer.base_digits`: `Dict[int, List[str]]` of all default digits for the `Integer`, updated by `Integer.get_digits`
* `Integer.dec_value`: `int` of the decimal value of the `Integer`, never changes after initialization

#### Class Methods
* `Integer.__init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None`: Takes `n` (`str` preferred, `int` is okay if `base` is `10`) and converts it from `base` (`int`) to decimal and stores in `Integer.dec_value`, `digits` (`List[str]`) is required if `base` does not have default digits (see `BASEN_DIGITS`)
* `Integer.to_base(self, base: int, digits: List[str] = []) -> str`: Converts `Integer.dec_value` to `base` (`int`), and converts it from `base` (`int`) to decimal and stores in `Integer.dec_value`, `digits` (`List[str]`) is required if `base` does not have default digits (see `BASEN_DIGITS`)
* `Integer.to_dec(self) -> int`: Returns `Integer.dec_value`
* `Integer.to_bin(self) -> str`: Uses `Integer.to_base` to convert `Integer.dec_value` to binary
* `Integer.to_octal(self) -> str`: Uses `Integer.to_base` to convert `Integer.dec_value` to octal
* `Integer.to_hex(self) -> str`: Uses `Integer.to_base` to convert `Integer.dec_value` to hexadecimal
* `Integer.to_base64(self) -> str`: Uses `Integer.to_base` to convert `Integer.dec_value` to base 64
* `Integer.get_digits(self, base: int, digits: List[str]) -> List[str]`: Validates `digits` (which is a `List[str]` by removing duplicates and checking if the number of digits matches the base), and returns either default digits (if `base` has defined default digits and `digits` is empty) or the validated `digits` (either if `base` is an abnormal base or `base` is a known base but the digits are overridden), this method is called by `Integer.__init__`
* `Integer.remove_dupl_digits(self, l: List[str]) -> List[str]`: Removes duplicates from `l` (`List[str]`) and returns the new `List[str]`, this method is called by `Integer.get_digits`

## Things to Know
* When providing the `digits` property, make sure the digits are in order from lowest value to highest value, for example, the `digits` property for hexadecimal would look like this: `list('0123456789ABCDEF')`
