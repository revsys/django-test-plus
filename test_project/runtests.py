#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

from django.conf import settings

# Add test_plus to Python path
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join('..', BASE_DIR))


def runtests(*test_args):
    import django.test.utils
    if django.VERSION[0:2] >= (1, 7):
        django.setup()
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['test_app'])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
