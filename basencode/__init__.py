from string import ascii_letters, digits
from typing import Dict, List, Tuple, Union
from decimal import Decimal

__name__ = 'basencode'
__all__ = 'ALL_DIGITS', 'BASE_DIGITS', 'Integer'

ALL_DIGITS = f'{digits}{ascii_letters}+/'
BASE_DIGITS: Dict[int, List[str]] = {1: ['0']}
RADIX_POINT = '.'

for i in range(2, 65):
    BASE_DIGITS[i] = BASE_DIGITS[i - 1] + [ALL_DIGITS[i - 1]]


def get_int_method(method_name, convert_to_number=True):
    int_method = getattr(int, method_name)

    def convert_from_int_and_call(self, other=None):
        if other:
            if isinstance(other, int):
                val = int_method(self._dec_value, other)
            elif isinstance(other, Decimal):
                val = int_method(self._dec_value, int(other))
            else:
                val = int_method(self._dec_value, other._dec_value)
        else:
            val = int_method(self._dec_value)
        if isinstance(val, tuple):
            return tuple(Integer(el) for el in val)
        if type(val) == bool or isinstance(val, int) and not convert_to_number:
            return val
        return Integer(val)

    return convert_from_int_and_call


class Number:  # WORK IN PROGRESS
    def __new__(cls, n: Union[int, str], base: int = 10, digits: List[str] = [],
                radix_point: str = RADIX_POINT):
        pass


class Integer:
    base_digits: Dict[int, List[str]] = BASE_DIGITS

    def __init__(self, n: Union[int, str, Tuple[Union[int, str]], List[Union[int, str]]],
                 base: int = 10, digits: List[str] = []) -> None:
        if type(n) in (int, str):
            n = list(str(n))
        else:
            n = [str(el) for el in n]
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

    def repr_in_base(self, base: int, digits: List[str] = [], mode: str = 's') -> Union[str, list]:
        """
        Represent the `Number` in the base provided in the integer `base`. The
        `digits: list[str]` parameter can be used to represent the `Number` in 
        `base` using a specific set of digits. The `mode: str` parameter
        indicates  whether the final representation will be returned as a `str`
        or a `list` (see `README.md` for use cases; `'s'` means string and
        `'l'` list).
        """
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
        return f'{type(self).__name__}({self._dec_value})'

    def repr_in_dec(self, mode: str = 's') -> Union[str, list]:
        return self.repr_in_base(10, mode=mode)

    def repr_in_bin(self, mode: str = 's') -> Union[str, list]:
        return self.repr_in_base(2, mode=mode)

    def repr_in_octal(self, mode: str = 's') -> Union[str, list]:
        return self.repr_in_base(8, mode=mode)

    def repr_in_hex(self, mode: str = 's') -> Union[str, list]:
        return self.repr_in_base(16, mode=mode)

    def repr_in_base64(self, mode: str = 's') -> Union[str, list]:
        return self.repr_in_base(64, mode=mode)

    @property
    def dec_value(self) -> int:
        return self._dec_value

    __eq__ = get_int_method('__eq__')
    __abs__ = get_int_method('__abs__', convert_to_number=False)
    __bool__ = get_int_method('__bool__')
    __add__ = get_int_method('__add__')
    __sub__ = get_int_method('__sub__')
    __mul__ = get_int_method('__mul__')
    __truediv__ = get_int_method('__truediv__')
    __floordiv__ = get_int_method('__floordiv__')
    __pow__ = get_int_method('__pow__')
    __hash__ = get_int_method('__hash__', convert_to_number=False)
    __mod__ = get_int_method('__mod__')
    __divmod__ = get_int_method('__divmod__')
    __rshift__ = get_int_method('__rshift__')
    __lshift__ = get_int_method('__lshift__')
    __and__ = get_int_method('__and__')
    __or__ = get_int_method('__or__')
    __ceil__ = get_int_method('__ceil__')
