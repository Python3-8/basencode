Changelog
=========

Version 2.1.0
-------------

Nov 7, 2022

* Uses ``Decimal`` (from Python's built-in module ``decimal``) in ``Float``\s for more accurate representations
* Added ``max_frac_places`` parameter to ``Float.repr_in_base``
* Added support for operations with ``Decimal``
* Overloaded more operators
* Code improvements
* Bugfixes

Version 2.0.0
-------------

Nov 2, 2022

* Added support for floating point numbers
* Added ``Number`` class
* Created a parent class for ``Integer``\s and ``Float``\s, ``_Number``
* Overloaded more operators
* Bugfixes

Version 1.1.0
-------------

Oct 29, 2022

* Added default digits for bases up to base 64
* Uses correct exceptions instead of raising plain ``Exception``\s

Version 1.0.0
-------------

Jun 5, 2022

* Support for whole numbers