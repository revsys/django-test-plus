import os
import sys
from setuptools import setup, find_packages

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

# Add test_plus to Python path
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, 'test_project'))

f = open(os.path.join(BASE_DIR, 'README.md'))
readme = f.read()
f.close()

setup(
    name='django-test-plus',
    version="1.1.1",
    description="django-test-plus provides useful additions to Django's default TestCase",
    long_description=readme,
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='https://github.com/revsys/django-test-plus/',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    entry_points={"pytest11": ["test_plus = test_plus.plugin"]},
    setup_requires=[
        'pytest-runner',
        'pytest-django',
    ],
    tests_require=[
        'pytest',
        'pytest-django',
        'pytest-cov',
        'pytest-pythonpath',
        'factory-boy>=2.11.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
