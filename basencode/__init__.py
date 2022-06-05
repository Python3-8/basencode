from string import ascii_lowercase, ascii_uppercase, digits
from typing import Dict, List, Union

__author__: str = 'pranav.pooruli@gmail.com'
__name__: str = 'basencode'

BASE2_DIGITS: List[str] = list('01')
BASE3_DIGITS: List[str] = list('012')
BASE4_DIGITS: List[str] = list('0123')
BASE5_DIGITS: List[str] = list('01234')
BASE6_DIGITS: List[str] = list('0122345')
BASE7_DIGITS: List[str] = list('0123456')
BASE8_DIGITS: List[str] = list('01234567')
BASE9_DIGITS: List[str] = list('012345678')
BASE10_DIGITS: List[str] = list(digits)
BASE11_DIGITS: List[str] = BASE10_DIGITS + list('A')
BASE12_DIGITS: List[str] = BASE10_DIGITS + list('AB')
BASE13_DIGITS: List[str] = BASE10_DIGITS + list('ABC')
BASE14_DIGITS: List[str] = BASE10_DIGITS + list('ABCD')
BASE15_DIGITS: List[str] = BASE10_DIGITS + list('ABCDE')
BASE16_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEF')
BASE17_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFG')
BASE18_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGH')
BASE19_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHI')
BASE20_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJ')
BASE21_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJK')
BASE22_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKL')
BASE23_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKLM')
BASE24_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKLMN')
BASE25_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKLMNO')
BASE26_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKLMNOP')
BASE27_DIGITS: List[str] = BASE10_DIGITS + list('ABCDEFGHIJKLMNOPQ')
BASE28_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:18])
BASE29_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:19])
BASE30_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:20])
BASE31_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:21])
BASE32_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:22])
BASE33_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:23])
BASE34_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:24])
BASE35_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:25])
BASE36_DIGITS: List[str] = BASE10_DIGITS + list(ascii_uppercase[:26])
BASE64_DIGITS: List[str] = list(
    digits + ascii_uppercase + ascii_lowercase + '+/')
BASE_DIGITS: Dict[int, List[str]] = {
    2: BASE2_DIGITS,
    3: BASE3_DIGITS,
    4: BASE4_DIGITS,
    5: BASE5_DIGITS,
    6: BASE6_DIGITS,
    7: BASE7_DIGITS,
    8: BASE8_DIGITS,
    9: BASE9_DIGITS,
    10: BASE10_DIGITS,
    11: BASE11_DIGITS,
    12: BASE12_DIGITS,
    13: BASE13_DIGITS,
    14: BASE14_DIGITS,
    15: BASE15_DIGITS,
    16: BASE16_DIGITS,
    17: BASE17_DIGITS,
    18: BASE18_DIGITS,
    19: BASE19_DIGITS,
    20: BASE20_DIGITS,
    21: BASE21_DIGITS,
    22: BASE22_DIGITS,
    23: BASE23_DIGITS,
    24: BASE24_DIGITS,
    25: BASE25_DIGITS,
    26: BASE26_DIGITS,
    27: BASE27_DIGITS,
    28: BASE28_DIGITS,
    29: BASE29_DIGITS,
    30: BASE30_DIGITS,
    31: BASE31_DIGITS,
    32: BASE32_DIGITS,
    33: BASE33_DIGITS,
    34: BASE34_DIGITS,
    35: BASE35_DIGITS,
    36: BASE36_DIGITS,
    64: BASE64_DIGITS,
}


class Integer:
    base_digits: Dict[int, List[str]] = BASE_DIGITS

    def __init__(self, n: Union[int, str], base: int = 10, digits: List[str] = []) -> None:
        if base == 10:
            self.dec_value = int(n)
            if int(n) < 0:
                raise Exception('n must be positive')
            return
        if type(n) != str:
            raise Exception(
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
                raise Exception(
                    f'abnormal base base {base} provided, digits must not be empty')
            else:
                digits_ = self.base_digits[base]
        else:
            digits_ = self.remove_dupl_digits(digits)
            self.base_digits[base] = digits_
        if len(digits_) != base:
            raise Exception(
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
