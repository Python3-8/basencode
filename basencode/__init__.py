from multiprocessing.sharedctypes import Value
from string import ascii_letters, digits
from typing import Dict, List, Tuple, Union
from math import isclose


__name__ = 'basencode'
__all__ = 'ALL_DIGITS', 'BASE_DIGITS', 'RADIX_POINT', 'Integer', 'Float'


RADIX_POINT = '.'


ALL_DIGITS = f'{digits}{ascii_letters}+/'
BASE_DIGITS: Dict[int, List[str]] = {2: ['0', '1']}

for i in range(3, 65):
    BASE_DIGITS[i] = BASE_DIGITS[i - 1] + [ALL_DIGITS[i - 1]]

INT_FUNCS = dir(int)
FLOAT_FUNCS = dir(float)


def get_num_method(method_name, cls, convert_to_number=True):
    if method_name not in INT_FUNCS and method_name not in FLOAT_FUNCS:
        raise AttributeError(f'{method_name} is not a valid function')
    num_method = getattr(cls, method_name)

    def convert_from_int_and_call(self, other=None):
        TYPE_DICTIONARY = {
            int: Integer,
            float: Float,
            bool: bool,
        }
        if other:
            if isinstance(other, Number):
                val = num_method(self._dec_value, other._dec_value)
                print(val, cls, method_name, other, self._dec_value, other._dec_value)
            else:
                val = num_method(self._dec_value, other)
        else:
            val = num_method(self._dec_value)
        t = TYPE_DICTIONARY[type(val) if type(val) != tuple else type(val[0])]

        if isinstance(val, tuple):
            return tuple(t(el) for el in val)
        elif t == int and not convert_to_number:
            return val
        return t(val)

    return convert_from_int_and_call


class Number:
    base_digits: Dict[int, List[str]] = BASE_DIGITS
    def __init__(self, n: Union[int, float, str, Tuple[Union[int, str]], List[Union[int, str]]],
                 base: int = 10, digits: List[str] = []):
        if type(n) in (int, str, float):
            n = list(str(n))
        else:
            n = [str(el) for el in n]
        digits_: List[str] = self._get_digits(base, digits)
        if base < 2:
            raise ValueError(f'base must be greater than 1, got {base}')

        radindex = None
        frac_part = []
        if hasattr(self, 'radix_point'):
            radindex = n.index(self.radix_point)
            frac_part = n[radindex + 1:]

        int_part = n[:radindex]
        place: int = len(int_part)
        num: int = 0
        while place:
            num += digits_.index(int_part[::-1]
                                [place - 1]) * base ** (place - 1)
            place -= 1
                

        place -= 1
        for digit in frac_part:
            num += digits_.index(digit) * base ** place
            place -= 1
        self._dec_value = num

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

    def repr_in_dec(self, mode: str = 's') -> Union[str, List[str]]:
        return self.repr_in_base(10, mode=mode)

    def repr_in_bin(self, mode: str = 's') -> Union[str, List[str]]:
        return self.repr_in_base(2, mode=mode)

    def repr_in_octal(self, mode: str = 's') -> Union[str, List[str]]:
        return self.repr_in_base(8, mode=mode)

    def repr_in_hex(self, mode: str = 's') -> Union[str, List[str]]:
        return self.repr_in_base(16, mode=mode)

    def repr_in_base64(self, mode: str = 's') -> Union[str, List[str]]:
        return self.repr_in_base(64, mode=mode)

    @property
    def dec_value(self) -> Union[int, float]:
        return self._dec_value
    def repr_in_base(self, base: int, digits: List[str] = [], mode: str = 's') -> Union[str, List[str]]:
        """
        Represent the `Integer` in the base provided in the integer `base`. The
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
        if base < 2:
            raise ValueError(f'base must be greater than 1, got {base}')
        elif self._dec_value == 0:
            return digits_[0]
        place: int = 0
        while True:
            if base ** place <= self._dec_value and base ** (place + 1) > self._dec_value:
                break
            place += 1
        new_digits: list = []
        remaining: int = self._dec_value
        while remaining:
            if base ** place > remaining:
                new_digits.append(digits_[0])
            else:
                print(base, place)
                new_digit = int(remaining // (base ** place))
                new_digits.append(digits_[new_digit])
                remaining %= base ** place
            if remaining:
                place -= 1
        new_digits += digits_[0] * place
        return new_digits if mode == 'l' else ''.join(new_digits)


class Integer(Number):
    __eq__ = get_num_method('__eq__', int)
    __bool__ = get_num_method('__bool__', int)
    __abs__ = get_num_method('__abs__', int, False)
    __add__ = get_num_method('__add__', int)
    __sub__ = get_num_method('__sub__', int)
    __mul__ = get_num_method('__mul__', int)
    __truediv__ = get_num_method('__truediv__', int)
    __floordiv__ = get_num_method('__floordiv__', int)
    __pow__ = get_num_method('__pow__', int)
    __hash__ = get_num_method('__hash__', int, False)
    __mod__ = get_num_method('__mod__', int)
    __divmod__ = get_num_method('__divmod__', int)
    __rshift__ = get_num_method('__rshift__', int)
    __lshift__ = get_num_method('__lshift__', int)
    __and__ = get_num_method('__and__', int)
    __or__ = get_num_method('__or__', int)
    __ceil__ = get_num_method('__ceil__', int)


class Float(Number):
    def __init__(self, n: Union[float, str, Tuple[Union[int, str]], List[Union[int, str]]], base: int = 10, digits: List[str] = [], radix_point: str = RADIX_POINT):
        if radix_point not in str(n):
            raise ValueError(f'{n}, a float, does not have a radix point')
        self.radix_point = radix_point
        super().__init__(n, base, digits)

    def repr_in_base(self, base: int, digits: List[str] = [], mode: str = 's') -> Union[str, List[str]]:
        """
        Represent the `Float` in the base provided in the integer `base`. The
        `digits: list[str]` parameter can be used to represent the `Number` in 
        `base` using a specific set of digits. The `mode: str` parameter
        indicates  whether the final representation will be returned as a `str`
        or a `list` (see `README.md` for use cases; `'s'` means string and
        `'l'` list).
        """
        int_part = int(self._dec_value)
        new_digits = Number(int_part).repr_in_base(base, mode='l')
        digits_: List[str] = self._get_digits(base, digits)
        # fractional part
        new_digits += self.radix_point
        place = -1
        remaining: float = self._dec_value - int_part
        while remaining:
            if base ** place > remaining:
                new_digits.append(digits_[0])
            else:
                new_digit = int(remaining / (base ** place))
                new_digits.append(digits_[new_digit])
                remaining -= new_digit * base ** place
            if remaining:
                place -= 1
        new_digits += digits_[0] * place
        return new_digits if mode == 'l' else ''.join(new_digits)

    def __eq__(self, other) -> bool:
        if isinstance(other, Number):
            other = other.dec_value
        return isclose(self._dec_value, other, rel_tol=1e-6)

    __bool__ = get_num_method('__bool__', float)
    __abs__ = get_num_method('__abs__', float, False)
    __add__ = get_num_method('__add__', float)
    __sub__ = get_num_method('__sub__', float)
    __mul__ = get_num_method('__mul__', float)
    __truediv__ = get_num_method('__truediv__', float)
    __floordiv__ = get_num_method('__floordiv__', float)
    __pow__ = get_num_method('__pow__', float)
    __hash__ = get_num_method('__hash__', float, False)
    __mod__ = get_num_method('__mod__', float)
    __divmod__ = get_num_method('__divmod__', float)
    __or__ = get_num_method('__or__', float)
    __ceil__ = get_num_method('__ceil__', float)
