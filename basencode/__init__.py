from typing import Dict, List, Union
from string import digits, ascii_lowercase, ascii_uppercase

__author__ = 'pranav.pooruli@gmail.com'
__name__ = 'basencode'

ALL_CHARACTERS = f'{digits}{ascii_uppercase}{ascii_lowercase}+/'
BASE_DIGITS: Dict[int, List[str]] = {1: ['0']}

for i in range(2, 65):
    BASE_DIGITS[i] = BASE_DIGITS[i - 1] + [ALL_CHARACTERS[i - 1]]


class Integer:
    base_digits: Dict[int, List[str]] = BASE_DIGITS

    def __init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None:
        if base == 10:
            self.dec_value = int(n)
            if int(n) < 0:
                raise ValueError('n must be positive')
            return
        if not isinstance(n, str):
            raise TypeError(
                f'base is not 10, so expected n to be of type {str} but got {type(n)}')
        n = n.upper()
        digits_: List[str] = self.get_digits(base, digits)
        if base == 1:
            self.dec_value = len(n)
            return
        elif n == digits_[0]:
            self.dec_value = 0
            return
        place: int = len(n)
        num: int = 0
        while place:
            num += digits_.index(n[::-1][place - 1]) * base ** (place - 1)
            place -= 1
        self.dec_value = num

    def to_base(self, base: int, digits: List[str] = []) -> str:
        digits_: List[str] = self.get_digits(base, digits)
        if base == 1:
            return digits_[0] * self.dec_value
        elif self.dec_value == 0:
            return digits_[0]
        place: int = 0
        while True:
            if base ** place <= self.dec_value and base ** (place + 1) > self.dec_value:
                break
            place += 1
        new_digits: str = ''
        left: int = self.dec_value
        while left:
            if base ** place > left:
                new_digits += digits_[0]
            else:
                new_digit = left // (base ** place)
                new_digits += digits_[new_digit]
                left %= (base ** place)
            if left:
                place -= 1
        new_digits += digits_[0] * place
        return new_digits

    def to_dec(self) -> int:
        return self.dec_value

    def to_bin(self) -> str:
        return self.to_base(2)

    def to_octal(self) -> str:
        return self.to_base(8)

    def to_hex(self) -> str:
        return self.to_base(16)

    def to_base64(self) -> str:
        return self.to_base(64)

    def get_digits(self, base: int, digits: List[str]) -> List[str]:
        digits_: List[str]
        if not digits:
            if base not in self.base_digits:
                raise ValueError(
                    f'abnormal base base {base} provided, digits must not be empty')
            else:
                digits_ = self.base_digits[base]
        else:
            digits_ = self.remove_dupl_digits(digits)
            self.base_digits[base] = digits_
        if len(digits_) != base:
            raise ValueError(
                f'expected exactly {base} digits for base {base}, got {len(digits_)} after removing duplicates')
        return digits_

    def remove_dupl_digits(self, l: List[str]) -> List[str]:
        dupl = set()
        dupl_add = dupl.add
        return [x for x in l if not (x in dupl or dupl_add(x))]

    def __eq__(self, other):
        return self.dec_value == other.dec_value

    def __repr__(self):
        return f'Integer({self.dec_value})'

    def __add__(self, other):
        return Integer(self.dec_value + other.dec_value)

    def __sub__(self, other):
        return Integer(self.dec_value - other.dec_value)

    def __mul__(self, other):
        return Integer(self.dec_value * other.dec_value)

    def __truediv__(self, other):
        return Integer(self.dec_value // other.dec_value)

    def __floordiv__(self, other):
        return self / other

    def __mod__(self, other):
        return Integer(self.dec_value % other.dec_value)

    def __divmod__(self, other):
        return tuple(Integer(val) for val in divmod(self.dec_value, other.dec_value))
