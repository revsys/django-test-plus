Ensuring low query counts
-------------------------

assertNumQueriesLessThan(number) - context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django provides
`assertNumQueries <https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries>`__
which is great when your code generates a specific number of
queries. However, if this number varies due to the nature of your data,
with this method you can still test to ensure the code doesn't start producing a ton
more queries than you expect::

    def test_something_out(self):

        with self.assertNumQueriesLessThan(7):
            self.get('some-view-with-6-queries')


assertGoodView(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method does a few things for you. It:

    - Retrieves the name URL
    - Ensures the view does not generate more than 50 queries
    - Ensures the response has status code 200
    - Returns the response

Often a wide, sweeping test like this is better than no test at all. You
can use it like this::

    def test_better_than_nothing(self):
        response = self.assertGoodView('my-url-name')
