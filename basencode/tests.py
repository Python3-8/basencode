from string import ascii_letters, digits, punctuation

from basencode import *


def test_number_creation_and_conversion():
    n1 = Number(12345)
    assert n1.to_base(64) == "30V"
    assert n1.to_base(8) == "30071"
    assert n1.to_octal() == "30071"
    assert n1.to_base(2) == "11000000111001"
    assert n1.to_base(33) == "bb3"


def test_digit_overriding():
    n1 = Number(12345)
    # Overriding digits
    assert n1.to_base(2, list("-+")) == "++------+++--+"
    assert n1.to_base(76, list(digits + ascii_letters + punctuation[:14])) == "2ax"
    # The digits must now be stored
    assert n1.to_base(76) == "2ax"


def test_number_methods():
    n1 = Number(12345)
    n2 = Number(54321)
    assert n1 == Number(12345) == 12345
    assert n1 + n2 == Number(66666)
    assert n2 - n1 == Number(41976)
    assert n1 * n2 == Number(670592745)
    assert n2 / n1 == Number(4)
    assert n2 // n1 == Number(4)
    assert divmod(n2, n1) == (Number(4), Number(4941))


def test_compatability_with_ints():
    n1 = Number(12345)
    assert n1 == 12345
    assert n1 + 54321 == Number(66666)
