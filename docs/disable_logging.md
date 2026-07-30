# Disable logging

You can disable logging during testing by changing the [TEST_RUNNER](https://docs.djangoproject.com/en/1.8/topics/testing/advanced/#using-different-testing-frameworks) in your settings file to:

```python
TEST_RUNNER = 'test_plus.runner.NoLoggingRunner'
```
