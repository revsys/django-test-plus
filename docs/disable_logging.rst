Disable logging
---------------

You can disable logging during testing by changing the `TEST\_RUNNER
<https://docs.djangoproject.com/en/1.8/topics/testing/advanced/#using-different-testing-frameworks>`_
in your settings file to::

    TEST_RUNNER = 'test_plus.runner.NoLoggingRunner'
