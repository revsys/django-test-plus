# django-test-plus

> Useful additions to Django's default TestCase.

Have your tests inherit from `test_plus.test.TestCase` rather than the normal
`django.test.TestCase`, and the boilerplate mostly goes away.

```python
from test_plus.test import TestCase

class MyViewTests(TestCase):

    def test_the_view(self):
        self.get('my-url-name')
        self.response_200()
```

- [Usage](usage.md) — including the pytest fixtures and testing DRF views
- [Methods](methods.md) — requests, status assertions, response and context helpers
- [Authentication helpers](auth_helpers.md) — `assertLoginRequired` and the `login()` context
- [Ensuring low query counts](low_query_counts.md) — `assertNumQueriesLessThan` and `assertGoodView`
- [Testing class-based views](cbvtestcase.md)
- [Disable logging](disable_logging.md)
- [API reference](reference.md)
