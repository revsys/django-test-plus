import os
import sys
from setuptools import setup, find_packages

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_project.settings'

# Add test_plus to Python path
BASE_DIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE_DIR, 'test_project'))

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-test-plus',
    version="1.0.13",
    description="django-test-plus provides useful additions to Django's default TestCase",
    long_description=readme,
    author='Frank Wiles',
    author_email='frank@revsys.com',
    url='https://github.com/revsys/django-test-plus/',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=['Django>=1.4.20'],
    tests_require=[
        'Django>=1.4.20',
        'factory-boy>=2.5.2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    test_suite='runtests.runtests'
)
