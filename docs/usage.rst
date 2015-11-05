Usage
-----

Using django-test-plus is pretty easy, simply have your tests inherit
from test\_plus.test.TestCase rather than the normal
django.test.TestCase like so::

    from test_plus.test import TestCase

    class MyViewTests(TestCase):
        ...

This is sufficient to get things rolling, but you are encouraged to
create *your own* sub-class on a per project basis. This will allow you
to add your own project specific helper methods.

For example, if you have a django project named 'myproject', you might
create the following in ``myproject/test.py``::

    from test_plus.test import TestCase as PlusTestCase

    class TestCase(PlusTestCase):
        pass

And then in your tests use::

    from myproject.test import TestCase

    class MyViewTests(TestCase):
        ...

Note that you can also option to import it like this if you want, which is
more similar to the regular importing of Django's TestCase::

    from test_plus import TestCase
