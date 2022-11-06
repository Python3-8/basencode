Getting Started
===============

Install
-------

To install the latest published version of Basencode from PyPI, run in your terminal:

.. code-block:: shell

  $ python3 -m pip install basencode

With Basencode installed, scroll down to learn how to use it.

Basic Usage
-----------

First, import Basencode.

.. code-block:: python

  >>> from basencode import *

This should load Basencode's three globals and the ``Number``, ``Integer``, and ``Float`` classes.

To construct an ``Integer``, run:

.. code-block:: python

  >>> Integer(12345)
  Integer(12345)

To construct a ``Float``, run:

.. code-block:: python

  >>> Float(12.345)
  Float(12.345)

The ``Number`` class can be used to construct an ``Integer`` or a ``Float`` depending on the number.

.. code-block:: python

  >>> Number(12345)
  Integer(12345)
  >>> Number(12.345)
  Float(12.345)

To represent a number in another number system, run:

.. code-block:: python

  >>> n1 = Number(12.345)
  >>> n1.repr_in_base(2, max_frac_places=5) # max_frac_places defaults to 100
  '1100.01011'
  >>> n1.repr_in_base(2, max_frac_places=10)
  '1100.0101100001'
  >>> Number(37).repr_in_base(37)
  '10'
  >>> Number(44.5).repr_in_base(64)
  'I.w'

Tips
----

- When providing the ``digits`` property, make sure the digits are in order from the lowest to the highest value, for example, the ``digits`` property for hexadecimal would look like this: ``list('0123456789abcdef')``
- By default, the default digits for all bases up to base 64 go as so:

  - Digits 0-9
  - Lowercase alphabet
  - Uppercase alphabet
  - ``+`` and ``/``

  therefore, ``Number('DF', 16)`` without overriding the digits for base 16 will throw an error because hexadecimal only has the digits 0-f (**lowercase** "f"). ``Number('df', 16)`` will construct ``Integer(223)``.

Operating Systems
-----------------

All versions of Basencode work on macOS, Linux, and Windows.

Issues
------

Feel free to report any encountered issues at the `issue tracker <https://github.com/Python3-8/basencode/issues>`_.