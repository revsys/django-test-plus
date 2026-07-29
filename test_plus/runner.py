import logging

from django.test.runner import DiscoverRunner as DefaultRunner


class NoLoggingRunner(DefaultRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # Disable logging below CRITICAL while running the tests
        logging.disable(logging.CRITICAL)

        return super().run_tests(test_labels, extra_tests, **kwargs)
