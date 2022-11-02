from string import ascii_letters, digits, punctuation
from basencode import *
import pytest


def test_number_creation_and_conversion():
    n1 = Integer(12345)
    assert n1.repr_in_base(64) == '30V'
    assert n1.repr_in_base(8) == '30071'
    assert n1.repr_in_octal() == '30071'
    assert n1.repr_in_base(2) == '11000000111001'
    assert n1.repr_in_base(33) == 'bb3'
    # Construct number from another base
    n2 = Integer('30V', 64)
    assert n1._dec_value == n2._dec_value


def test_different_modes():
    n1 = Integer(12345)
    assert n1.repr_in_base(64, mode='s') == '30V'
    assert n1.repr_in_base(64, mode='l') == ['3', '0', 'V']
    assert n1.repr_in_base(2, mode='l') == [
        '1', '1', '0', '0', '0', '0', '0', '0', '1', '1', '1', '0', '0', '1']
    assert n1.repr_in_base(2, digits=['++', '--'], mode='l') == [
        '--',
        '--',
        '++',
        '++',
        '++',
        '++',
        '++',
        '++',
        '--',
        '--',
        '--',
        '++',
        '++',
        '--',
    ]


def test_digit_overriding():
    n1 = Integer(12345)
    # Overriding digits
    assert n1.repr_in_base(2, list('-+')) == '++------+++--+'
    assert n1.repr_in_base(
        76, list(digits + ascii_letters + punctuation[:14])) == '2ax'
    # The digits must now be stored
    assert n1.repr_in_base(76) == '2ax'


def test_number_methods():
    n1 = Integer(12345)
    n2 = Integer(54321)
    assert n1 == Integer(12345) == 12345
    assert n1 + n2 == Integer(66666)
    assert n2 - n1 == Integer(41976)
    assert n1 * n2 == Integer(670592745)
    assert n2 / n1 == Float(54321 / 12345)
    assert n2 // n1 == Integer(4)
    assert divmod(n2, n1) == (Integer(4), Integer(4941))
    assert abs(n1) == 12345
    assert bool(n1) == True

def test_float_methods():
    f1 = Float(24.6)
    f2 = Float(98.7)
    assert f1 == Float(24.6) == 24.6
    assert f1 + f2 == Float(123.3)
    assert f2 - f1 == Float(74.1)
    assert f1 * f2 == Float(2428.02)
    assert f2 / f1 == Float(4.01219512)
    assert f2 // f1 == Integer(4)
    assert divmod(f2, f1) == (Float(4.0), Float(0.3))
    assert abs(f1) == 24.6
    assert bool(f1) == True

@pytest.mark.skip
def test_harmony_between_classes():
    n1 = Integer(12345)
    f1 = Float(0.5)
    f2 = Float(12345.0)
    assert n1 == 12345
    assert f1 == 0.5
    assert n1 + 54321 == Integer(66666)

