from decimal import Decimal
from string import ascii_letters, digits
from typing import Dict, List, Union

__name__ = 'basencode'
__all__ = 'ALL_DIGITS', 'BASE_DIGITS', 'Number'

ALL_DIGITS = f'{digits}{ascii_letters}+/'
BASE_DIGITS: Dict[int, List[str]] = {1: ['0']}

for i in range(2, 65):
    BASE_DIGITS[i] = BASE_DIGITS[i - 1] + [ALL_DIGITS[i - 1]]


def get_int_method(method_name):
    int_method = getattr(int, method_name)

    def convert_from_int_and_call(self, other):
        if isinstance(other, int):
            val = int_method(self._dec_value, other)
        elif isinstance(other, Decimal):
            val = int_method(self._dec_value, int(other))
        else:
            val = int_method(self._dec_value, other._dec_value)
        if isinstance(val, tuple):
            return tuple(Number(el) for el in val)
        return Number(val)

    return convert_from_int_and_call


class Number:
    base_digits: Dict[int, List[str]] = BASE_DIGITS

    def __init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None:
        if base == 10:
            self._dec_value = int(n)
            if int(n) < 0:
                raise ValueError('n must be positive')
            return
        if not isinstance(n, str):
            raise TypeError(
                f'base is not 10, so expected n to be of type {str} but got {type(n)}')
        digits_: List[str] = self._get_digits(base, digits)
        if base == 1:
            self._dec_value = len(n)
            return
        elif n == digits_[0]:
            self._dec_value = 0
            return
        place: int = len(n)
        num: int = 0
        while place:
            num += digits_.index(n[::-1][place - 1]) * base ** (place - 1)
            place -= 1
        self._dec_value = num

    def repr_in_base(self, base: int, digits: List[str] = [], mode='s') -> Union[str, list]:
        '''
        Represent a Number in any positive integer base.

        Args:
        `base: int`         --> The base in which the representation should be
        `digits: List[Str]` --> The digits to be used in the representation (uses digits from BASE_DIGITS)
        `mode: str`         --> Either 's' (str) or 'l' (list); how the representation should be returned. Defaults to 's'

        Returns:
        A `str` or `list` (based on the mode) which is a representation of the Number in the given base

        '''
        if mode not in ('s', 'l'):
            raise ValueError(
                f"expected mode to be either 's' or 'l', but got {mode}")
        digits_: List[str] = self._get_digits(base, digits)
        if base == 1:
            return digits_[0] * self._dec_value
        elif self._dec_value == 0:
            return digits_[0]
        place: int = 0
        while True:
            if base ** place <= self._dec_value and base ** (place + 1) > self._dec_value:
                break
            place += 1
        new_digits: list = []
        left: int = self._dec_value
        while left:
            if base ** place > left:
                new_digits.append(digits_[0])
            else:
                new_digit = left // (base ** place)
                new_digits.append(digits_[new_digit])
                left %= base ** place
            if left:
                place -= 1
        new_digits += digits_[0] * place
        return new_digits if mode == 'l' else ''.join(new_digits)

    def _get_digits(self, base: int, digits: List[str]) -> List[str]:
        digits_: List[str]
        if not digits:
            if base not in self.base_digits:
                raise ValueError(
                    f'abnormal base base {base} provided, digits must not be empty')
            else:
                digits_ = self.base_digits[base]
        else:
            digits_ = self._remove_dupl_digits(digits)
            self.base_digits[base] = digits_
        if len(digits_) != base:
            raise ValueError(
                f'expected exactly {base} digits for base {base}, got {len(digits_)} after removing duplicates'
            )
        return digits_

    def _remove_dupl_digits(self, l: List[str]) -> List[str]:
        dupl = set()
        dupl_add = dupl.add
        return [x for x in l if not (x in dupl or dupl_add(x))]

    def __repr__(self):
        return f'Number({self._dec_value})'

    def to_dec(self) -> int:
        return self._dec_value

    def to_bin(self) -> str:
        return self.repr_in_base(2)

    def to_octal(self) -> str:
        return self.repr_in_base(8)

    def to_hex(self) -> str:
        return self.repr_in_base(16)

    def repr_in_base64(self) -> str:
        return self.repr_in_base(64)

    @property
    def dec_value(self) -> int:
        return self._dec_value

    def __eq__(self, other):
        return self._dec_value == other

    def __bool__(self):
        return bool(self._dec_value)

    def __abs__(self):
        return self._dec_value

    __add__ = get_int_method('__add__')
    __sub__ = get_int_method('__sub__')
    __mul__ = get_int_method('__mul__')
    __truediv__ = get_int_method('__truediv__')
    __floordiv__ = get_int_method('__floordiv__')
    __mod__ = get_int_method('__mod__')
    __divmod__ = get_int_method('__divmod__')
