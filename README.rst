django-test-plus
================

Useful additions to Django's default TestCase from `Revolution
Systems <http://www.revsys.com/>`__

|travis ci status image| |Coverage Status|

Rationale
---------

Let's face it, writing tests isn't always fun. Part of the reason for
that is all of the boilerplate you end up writing. django-test-plus is
an attempt to cut down on some of that when writing Django tests. We
guarantee it will increase the time before you get carpal tunnel by at
least 3 weeks!

Support
-------

Supports: Python 2 and Python 3

Supports Django Versions: 1.4, 1.5, 1.6, 1.7, and 1.8

Documentation
--------------

Full documentation is available at http://django-test-plus.readthedocs.org

Usage
-----

Using django-test-plus is pretty easy, simply have your tests inherit
from test\_plus.test.TestCase rather than the normal
django.test.TestCase like so::

    from test_plus.test import TestCase

    class MyViewTests(TestCase):
        ...

This is sufficient to get things rolling, but you are encouraged to
create *your own* sub-class on a per project basis. For more details, see
the Usage section of the docs.



.. |travis ci status image| image:: https://secure.travis-ci.org/revsys/django-test-plus.png
   :target: http://travis-ci.org/revsys/django-test-plus
.. |Coverage Status| image:: https://coveralls.io/repos/revsys/django-test-plus/badge.svg?branch=master
   :target: https://coveralls.io/r/revsys/django-test-plus?branch=master
