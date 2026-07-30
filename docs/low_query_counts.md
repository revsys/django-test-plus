# Ensuring low query counts

## assertNumQueriesLessThan(number) - context

Django provides [assertNumQueries](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries) which is great when your code generates a specific number of queries. However, if this number varies due to the nature of your data, with this method you can still test to ensure the code doesn't start producing a ton more queries than you expect:

```python
def test_something_out(self):

    with self.assertNumQueriesLessThan(7):
        self.get('some-view-with-6-queries')
```

## assertGoodView(url_name, \*args, verbose=False, \*\*kwargs)

This method does a few things for you. It:

> - Retrieves the name URL
> - Ensures the view does not generate more than 50 queries
> - Ensures the response has status code 200
> - Returns the response

Often a wide, sweeping test like this is better than no test at all. You can use it like this:

```python
def test_better_than_nothing(self):
    response = self.assertGoodView('my-url-name')
```

Both helpers are available on the pytest `tp` fixture too (see [pytest usage](usage.md#pytest-usage)). Both count queries, so they need database access. Ask for pytest-django's `db` fixture alongside `tp`:

```python
def test_better_than_nothing(tp, db):
    response = tp.assertGoodView('my-url-name')

def test_something_out(tp, db):
    with tp.assertNumQueriesLessThan(7):
        tp.get('some-view-with-6-queries')
```
