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

## llms.txt

This documentation is available in the [llms.txt](https://llmstxt.org/) format, a
Markdown convention suited to LLMs and AI coding assistants.

Two files are published:

- [`llms.txt`](https://django-test-plus.readthedocs.io/en/latest/llms.txt) — a
  short description of the project plus links to each section of the
  documentation. The structure is described [here](https://llmstxt.org/#format).
- [`llms-full.txt`](https://django-test-plus.readthedocs.io/en/latest/llms-full.txt) —
  the same index with the content of every page included inline, including the
  generated API reference.

Every page is also published as Markdown alongside its HTML, so you can link an
assistant at a single section rather than the whole corpus. Append `.md` to the
page name:

```
https://django-test-plus.readthedocs.io/en/latest/usage.md
https://django-test-plus.readthedocs.io/en/latest/methods.md
https://django-test-plus.readthedocs.io/en/latest/reference.md
```

These files are not picked up automatically by IDEs or coding agents today, but
most will use them if you supply a link or paste the text.
