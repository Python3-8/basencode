"""
Basencode
=========
"""

from string import ascii_letters, digits as string_digits
from typing import Dict, List, Tuple, Union
from math import ceil, isclose
from decimal import Decimal
from copy import deepcopy

__all__ = 'ALL_DIGITS', 'BASE_DIGITS', 'RADIX_POINT', 'Integer', 'Float', 'Number'

#: All digits used in default digits for ``_Number``\s
ALL_DIGITS = f'{string_digits}{ascii_letters}+/'

#: The default radix point for ``Float``\s
RADIX_POINT = '.'

#: All default digits for ``_Number``\s
BASE_DIGITS: Dict[int, List[str]] = {2: ['0', '1']}
for i in range(3, 65):
    BASE_DIGITS[i] = BASE_DIGITS[i - 1] + [ALL_DIGITS[i - 1]]

_NUM_METHODS = {
    '__eq__': lambda self, other: self == other,
    '__bool__': bool,
    '__abs__': abs,
    '__add__': lambda self, other: self + other,
    '__sub__': lambda self, other: self - other,
    '__mul__': lambda self, other: self * other,
    '__truediv__': lambda self, other: self / other,
    '__floordiv__': lambda self, other: self // other,
    '__pow__': lambda self, other: self ** other,
    '__hash__': hash,
    '__mod__': lambda self, other: self % other,
    '__divmod__': divmod,
    '__rshift__': lambda self, other: self >> other,
    '__lshift__': lambda self, other: self << other,
    '__and__': lambda self, other: self & other,
    '__or__': lambda self, other: self | other,
    '__ceil__': ceil,
    '__round__': round,
    '__int__': int,
    '__float__': float,
}


def get_num_method(method_name, convert_to_number=True, strict=False):
    """Gets a built-in Python method and modifies it for overloading operators in ``_Number`` and its children.

    :param method_name: The name of the method
    :param convert_to_number: Whether or not to convert the result to an instance of ``_Number``; defaults to ``True``.
    :returns: The modified method to be used to overload an operator
    """
    num_method = _NUM_METHODS.get(method_name)
    if not num_method:
        raise AttributeError(f'{method_name} is not a valid method')

    def convert_from_int_and_call(self, other=None):
        TYPE_DICT = {
            int: Integer if convert_to_number else int,
            float: Float if convert_to_number else float,
            Decimal: float if strict else Decimal,
            bool: bool,
        }
        if other:
            if isinstance(other, _Number):
                val = num_method(self.dec_value, other.dec_value)
            elif isinstance(other, Decimal):
                val = num_method(Decimal(str(self.dec_value)), other)
            else:
                val = num_method(self.dec_value, other)
        else:
            val = num_method(self.dec_value)
        t = TYPE_DICT[type(val[0]) if isinstance(val, tuple) else type(val)]
        if isinstance(val, tuple):
            return tuple(Float(el) for el in val) if t == Decimal else tuple(t(el) for el in val)
        elif isinstance(val, Decimal):
            if strict:
                return t(val)
            else:
                return (new_type := Float if val % Decimal('1')
                        else Integer)(str(val) if new_type == Float else str(int(val)))
        return t(val)

    return convert_from_int_and_call


class Number:
    """Constructs a ``Float`` if a number with a radix point is provided, otherwise an ``Integer``.

    :param n: The number to be converted to decimal and stored
    :param base: The base in which the number provided is represented (this information is used to convert the number to decimal)
    :param digits: The digits used in the provided representation of the number
    :param radix_point: The radix point used in the provided representation of the number, if at all
    :returns: A ``Float`` if a number with a radix point is provided, otherwise an ``Integer``
    :rtype: Float | Integer
    """

    def __new__(cls, n: Union[int, float, str, Tuple[Union[int, str]], List[Union[int, str]]],
                base: int = 10, digits: List[str] = None, radix_point: str = RADIX_POINT):
        digits = digits if digits else []
        if isinstance(n, int) or isinstance(n, float) or isinstance(n, Decimal):
            n_ = str(n)
        else:
            n_ = n
        if radix_point in n_:
            return Float(n, base, digits, radix_point)
        else:
            return Integer(n, base, digits)


class _Number:
    """The parent class for all ``Float``\\s and ``Integer``\\s

    :param n: The number to be converted to decimal and stored
    :param base: The base in which the number provided is represented (this information is used to convert the number to decimal)
    :param digits: The digits used in the provided representation of the number
    :meta public:
    """

    def __init__(self, n: Union[int, float, str, Tuple[Union[int, str]], List[Union[int, str]]],
                 base: int = 10, digits: List[str] = None):
        digits = digits if digits else []
        if type(n) in (int, str, float, Decimal):
            n = list(str(n))
        else:
            n = [str(el) for el in n]
        self.base_digits: Dict[int, List[str]] = deepcopy(BASE_DIGITS)
        digits_: List[str] = self._get_digits(base, digits)
        if base < 2:
            raise ValueError(f'base must be greater than 1, got {base}')
        radindex = None
        frac_part = []
        if hasattr(self, 'radix_point'):
            radindex = n.index(self.radix_point)
            frac_part = n[radindex + 1:]
        whole_part = n[:radindex]
        place: int = len(whole_part)
        num: int = 0
        while place:
            num += digits_.index(whole_part[::-1]
                                 [place - 1]) * base ** (place - 1)
            place -= 1
        place -= 1
        for digit in frac_part:
            num += Decimal(digits_.index(digit)) * \
                Decimal(base) ** Decimal(place)
            place -= 1
        self._dec_value: Union[int, float, Decimal] = num

    def __repr__(self):
        return f'{type(self).__name__}({self._dec_value})'

    def _get_digits(self, base: int, digits: List[str]) -> List[str]:
        digits_: List[str]
        if base < 2:
            raise ValueError(f'base must be less greater than 1, got {base}')
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
                f'expected exactly {base} digits for base {base}, got '
                f'{len(digits_)} after removing duplicates'
            )
        return digits_

    def _remove_dupl_digits(self, l: List[str]) -> List[str]:
        dupl = set()
        dupl_add = dupl.add
        return [x for x in l if not (x in dupl or dupl_add(x))]

    def repr_in_dec(self, digits: List[str] = None, mode: str = 's') -> Union[str, List[str]]:
        """Uses ``repr_in_base`` to convert the ``_Number`` to decimal.

        :param digits: The digits to use in the representation
        :param mode: Whether to return the representation as a string or a list
        :returns: The decimal representation of the ``_Number``'s decimal value
        :rtype: str | list[str]
        """
        return self.repr_in_base(10, digits=digits, mode=mode)

    def repr_in_bin(self, digits: List[str] = None, mode: str = 's') -> Union[str, List[str]]:
        """Uses ``repr_in_base`` to convert the ``_Number`` to binary.

        :param digits: The digits to use in the representation
        :param mode: Whether to return the representation as a string or a list
        :returns: The binary representation of the ``_Number``'s decimal value
        :rtype: str | list[str]
        """
        return self.repr_in_base(2, digits=digits, mode=mode)

    def repr_in_octal(self, digits: List[str] = None, mode: str = 's') -> Union[str, List[str]]:
        """Uses ``repr_in_base`` to convert the ``_Number`` to octal.

        :param digits: The digits to use in the representation
        :param mode: Whether to return the representation as a string or a list
        :returns: The octal representation of the ``_Number``'s decimal value
        :rtype: str | list[str]
        """
        return self.repr_in_base(8, digits=digits, mode=mode)

    def repr_in_hex(self, digits: List[str] = None, mode: str = 's') -> Union[str, List[str]]:
        """Uses ``repr_in_base`` to convert the ``_Number`` to hexadecimal.

        :param digits: The digits to use in the representation
        :param mode: Whether to return the representation as a string or a list
        :returns: The hexadecimal representation of the ``_Number``'s decimal value
        :rtype: str | list[str]
        """
        return self.repr_in_base(16, digits=digits, mode=mode)

    def repr_in_base64(self, digits: List[str] = None, mode: str = 's') -> Union[str, List[str]]:
        """Uses ``repr_in_base`` to convert the ``_Number`` to base 64.

        :param digits: The digits to use in the representation
        :param mode: Whether to return the representation as a string or a list
        :returns: The base 64 representation of the ``_Number``'s decimal value
        :rtype: str | list[str]
        """
        return self.repr_in_base(64, digits=digits, mode=mode)

    @property
    def dec_value(self) -> Union[int, float, Decimal]:
        """Getter returns the decimal value of the ``_Number``."""
        return self._dec_value

    def repr_in_base(self, base: int, digits: List[str] = None, mode: str = 's') \
            -> Union[str, List[str]]:
        """Represents the decimal value of the instance of ``_Number`` in the base provided.

        :param base: The base to represent the ``_Number``'s decimal value in
        :param digits: The digits to use in the representation; these are also set as the default digits (for this object) for the base provided.
        :param mode: Whether to return the representation as a string or a list
        :returns: The representation of the ``_Number``'s decimal value in the base provided
        :rtype: str | list[str]
        """
        digits = digits if digits else []
        if mode not in ('s', 'l'):
            raise ValueError(
                f"expected mode to be either 's' or 'l', but got {mode}")
        digits_: List[str] = self._get_digits(base, digits)
        if base < 2:
            raise ValueError(f'base must be greater than 1, got {base}')
        elif self._dec_value == 0:
            return digits_[0] if mode == 's' else [digits_[0]]
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
                new_digit = int(remaining // (base ** place))
                new_digits.append(digits_[new_digit])
                remaining %= base ** place
            if remaining:
                place -= 1
        new_digits.extend([digits_[0]] * place)
        return new_digits if mode == 'l' else ''.join(new_digits)

    __eq__ = get_num_method('__eq__')
    __bool__ = get_num_method('__bool__')
    __abs__ = get_num_method('__abs__', False, True)
    __add__ = get_num_method('__add__')
    __sub__ = get_num_method('__sub__')
    __mul__ = get_num_method('__mul__')
    __truediv__ = get_num_method('__truediv__')
    __floordiv__ = get_num_method('__floordiv__')
    __pow__ = get_num_method('__pow__')
    __hash__ = get_num_method('__hash__', False)
    __mod__ = get_num_method('__mod__')
    __divmod__ = get_num_method('__divmod__')
    __ceil__ = get_num_method('__ceil__')
    __round__ = get_num_method('__round__')
    __int__ = get_num_method('__int__', False)
    __float__ = get_num_method('__float__', False)


class Integer(_Number):
    """The ``Integer`` class, a child of ``_Number``, for whole numbers

    :param n: The number to be converted to decimal and stored
    :param base: The base in which the number provided is represented (this information is used to convert the number to decimal)
    :param digits: The digits used in the provided representation of the number
    """

    __or__ = get_num_method('__or__')
    __and__ = get_num_method('__and__')
    __rshift__ = get_num_method('__rshift__')
    __lshift__ = get_num_method('__lshift__')


class Float(_Number):
    """The ``Float`` class, a child of ``_Number``, for non-negative floating point numbers

    :param n: The number to be converted to decimal and stored
    :param base: The base in which the number provided is represented (this information is used to convert the number to decimal)
    :param digits: The digits used in the provided representation of the number
    :param radix_point: The radix point used in the provided representation of the number, if at all
    """

    def __init__(self, n: Union[float, str, Tuple[Union[int, str]], List[Union[int, str]]],
                 base: int = 10, digits: List[str] = None, radix_point: str = RADIX_POINT):
        digits = digits if digits else []
        if type(n) in (tuple, list):
            n = [str(el) for el in n]
        else:
            n = str(n)
        if radix_point not in n:
            n = n + (radix_point if isinstance(n, str) else [radix_point])
        self.radix_point = radix_point
        super().__init__(n, base, digits)

    def repr_in_base(self, base: int, digits: List[str] = None, mode: str = 's',
                     max_frac_places: int = 100) -> Union[str, List[str]]:
        """Represents the decimal value of the instance of ``_Number`` in the base provided.

        :param base: The base to represent the ``_Number``'s decimal value in
        :param digits: The digits to use in the representation; these are also set as the default digits (for this object) for the base provided.
        :param mode: Whether to return the representation as a string or a list
        :param max_frac_places: The maximum number of digits succeeding the radix point
        :returns: The representation of the ``_Number``'s decimal value in the base provided
        :rtype: str | list[str]
        """
        digits = digits if digits else []
        whole_part = int(self._dec_value)
        digits_: List[str] = self._get_digits(base, digits)
        new_digits = Integer(whole_part).repr_in_base(
            base, digits=digits_, mode='l')
        # fractional part
        new_digits += self.radix_point
        place = -1
        remaining: Decimal = self._dec_value - Decimal(whole_part)
        while remaining and len(new_digits[new_digits.index(self.radix_point) + 1:]
                                ) < max_frac_places:
            if Decimal(base) ** Decimal(place) > remaining:
                new_digits.append(digits_[0])
            else:
                new_digit = int(remaining / Decimal(base) ** Decimal(place))
                new_digits.append(digits_[new_digit])
                remaining -= Decimal(new_digit) * \
                    Decimal(base) ** Decimal(place)
            if remaining:
                place -= 1
        new_digits += digits_[0] * place
        if new_digits[-1] == self.radix_point:
            new_digits += digits_[0]
        return new_digits if mode == 'l' else ''.join(new_digits)

    def __eq__(self, other) -> bool:
        if isinstance(other, _Number):
            other = other._dec_value
        return isclose(float(self._dec_value), other, rel_tol=1e-6)

    __hash__ = _Number.__hash__
