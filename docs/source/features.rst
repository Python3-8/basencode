Features
========

Constructing from different bases
---------------------------------

Numbers can be constructed not only from decimal, but rather from any base.

.. code-block:: python

  >>> n = Number(2.5)
  >>> n.repr_in_base(2)
  '10.1'
  >>> Number(10.1, 2)
  Float(2.5)
  >>> Number('10.1', 2)
  Float(2.5)
  >>> Number(('1', '0', '.', '1'), 2)
  Float(2.5)
  >>> Number('+-/+', 2, digits=['-', '+'], radix_point='/') # Custom digits and a custom radix point can be used as well
  Float(2.5)

Custom digits and radix point
-----------------------------

By default, digits are only present for bases 2-64. Therefore, Basencode lets you provide your own custom digits for not only bases above 64, but any base. You can also supply a custom radix point, for instance, if the default "." is one of your digits.

.. code-block:: python

  >>> n = Number('36⠿25', radix_point='⠿')  # 36.25
  >>> n.repr_in_base(2, digits=['-', '+'])
  '+--+--⠿-+'
  >>> n.repr_in_base(94)
  ...
  ValueError: abnormal base base 94 provided, digits must not be empty
  >>> from string import digits, ascii_letters, punctuation
  >>> n.repr_in_base(94,
  ...    digits=list(digits + ascii_letters + punctuation),
  ...    max_frac_places=10,
  ... )
  'A⠿nK~~~~~~~~'

Memory of default digits and radix point
----------------------------------------

Provision of digits to ``repr_in_base`` causes the provided digits to be stored on the object.

.. code-block:: python

  >>> n = Number('36⠿25', radix_point='⠿')  # This radix point is stored as the default for this object
  >>> n.repr_in_base(2, digits=['-', '+'])  # These digits have now been stored as default digits
  '+--+--⠿-+'
  >>> n.repr_in_base(2)
  '+--+--⠿-+'
  >>> from string import digits, ascii_letters, punctuation
  >>> n.repr_in_base(94,
  ...    digits=list(digits + ascii_letters + punctuation),
  ...    max_frac_places=2,
  ... )  # These digits have now been stored as default digits
  'A⠿nK'
  >>> n.repr_in_base(94)
  'A⠿nK~~~~~~~~~~~~Q0"2*hcnQp~,]BCN%Kq)sQE"s=GZp&s)vyC@?n.cfG>Z1V|V*h]7v?%ED.rRM["6>jHA:SAqMZZto/(#|:IS6k'
  >>> Number(n.dec_value).repr_in_base(94)  # This is a new object without default digits for base 94
  ...
  ValueError: abnormal base base 94 provided, digits must not be empty

Representation mode
-------------------

Representations using ``repr_in_base`` can be returned as strings or as lists. This is useful when digits contain two or more characters.

.. code-block:: python

  >>> Number(134.75).repr_in_base(2, digits=['-+', '+-'])  # Digits are indistinguishable
  '+--+-+-+-++-+--+.+-+-'
  >>> Number(134.75).repr_in_base(2, digits=['-+', '+-'], mode='l')  # Digits are now separated
  ['+-', '-+', '-+', '-+', '-+', '+-', '+-', '-+', '.', '+-', '+-']

It must be noted that this works with ``Integer``\s as well.

Arithmetic operators
--------------------

Operator overloading has been done, and a variety of Python operators are supported.

.. code-block:: python

  >>> import math
  >>> i = Number(123)
  >>> f = Number(1.24)
  >>> math.ceil(f)
  Integer(2)
  >>> round(f)
  Integer(1)
  >>> bool(i), bool(f), bool(Number(0)), bool(Number(0.))
  (True, True, False, False)
  >>> i / f, i / 1.24
  (Float(99.19354838709677419354838710), Float(99.19354838709677))
  >>> i // f
  Integer(99)
  >>> i % f
  Float(0.24)
  >>> divmod(i, f)
  (Float(99), Float(0.24))
  >>> i + f, i - f, i * f
  (Float(124.24), Float(121.76), Float(152.52))
  >>> abs(i), abs(f)
  (123, 1.24)
  >>> i == 123, f == Number(1.24)
  (True, True)
  >>> i != 123, f != Number(1.24)
  (False, False)
  >>> i << 3, i >> Number(3)  # Bitwise operators only work with Integers
  (Integer(984), Integer(15))
  >>> i & 999, i | Number(999)
  (Integer(99), Integer(1023))
  >>> hash(i), hash(f)
  (123, 1752440687002407404)

It must be noted that instances of ``Decimal`` (from Python's built-in module ``decimal``) can also be used as operands.
