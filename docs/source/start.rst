Getting Started
===============

Install
-------

To install Basencode, run in your terminal:
``python3 -m pip install basencode``

Usage
-----

.. code-block:: python
  :linenos:

  >>> from basencode import *
  >>> n1 = Number(12345) # Number constructs an Integer (in this case), Integer can be called too
  # Default digits are used
  >>> n1.repr_in_base(64)
  '30V'
  # Construct Integer from base 64
  >>> Number('30V', 64)
  Integer(12345)
  >>> n1.repr_in_base(8)
  '30071'
  >>> n1.repr_in_octal()
  '30071'
  >>> n1.repr_in_bin()
  '11000000111001'
  # Overriding default digits
  >>> n1.repr_in_base(2, list('-+'))
  '++------+++--+'
  >>> n1.repr_in_bin()
  '++------+++--+'
  >>> n1.repr_in_base(33)
  'bb3'
  >>> from string import digits, ascii_letters, punctuation
  >>> n1.repr_in_base(76, list(digits + ascii_letters + punctuation[:14]))
  '2ax'
  >>> n1.repr_in_base(76) # Digits provided above were stored as default digits for base 76
  '2ax'
  >>> n2 = Integer(54321)
  >>> n1 + n2
  Integer(66666)
  >>> n2 - n1
  Integer(41976)
  >>> n1 * n2
  Integer(670592745)
  # True division will return a Float, and floor division an Integer
  >>> n2 / n1
  Float(4.400243013365735)
  >>> n2 // n1
  Integer(4)
  >>> n2 % n1
  Integer(4941)
  >>> divmod(n2, n1)
  (Integer(4), Integer(4941))
  # Operations can also be performed with ints, though Integers will be returned
  >>> n1 == 12345
  True
  >>> n1 + 54321
  Integer(66666)
  # Modes can be used to indicate how the representation should be
  >>> n1.repr_in_base(64, mode='s') # 'mode' is 's' by default
  '30V'
  >>> n1.repr_in_base(2, digits=['--', '++'], mode='l')
  ['++', '++', '--', '--', '--', '--', '--', '--', '++', '++', '++', '--', '--', '++']
  # Floats can be converted back and forth too
  >>> Number(10.1, 2) # Constructs a Float
  Float(2.5)
  >>> Float(10.1, 2).repr_in_base(8)
  '2.4'
  >>> Float(22.22, 3).repr_in_base(7)
  '11.6136136136136136136136136136136125043055...'

Operating Systems
-----------------

All versions of Basencode work on macOS, Linux, and Windows.

Issues
------

Feel free to report any encountered issues at the `issue tracker <https://github.com/Python3-8/basencode/issues>`_.