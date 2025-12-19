# Changes

## Version 2.4.1 - December 19th, 2025

  - Migrate from setup.py/setup.cfg to pyproject.toml with hatchling
  - Use uv for building and publishing

## Version 2.4.0 - December 19th, 2025

  - Add Django 6.0 support
  - Add Python 3.14 support
  - Drop Python 3.9 support

## Version 2.3.0 - July 2nd, 2025

  - Add Django 5.2 support 
  - Drop Django 3.2 tests
  - Add Python 3.13 tests 
  - Cleanup Github Actions and README a bit

## Version 2.2.4 - June 24th, 2024

  - Fix bug with APITest case 

## Version 2.2.3 - July 11th, 2023

  - Fix bug where email addresses were not created by make_user()

## Version 2.2.2 - June 27, 2023

  - Fix issue with User creation helper when User model doesn't have a username field
  - Improve assertNumQueriesLessThan
  - Add assertInContext

## version 2.2.1 - October 12, 2022

  - Add Django 4.2 support

## version 2.2.0 - May 19th, 2021

  - Add support for Django 3.2.

## version 2.1.1 - May 19th, 2021

  - Add official support for Python 3.9.

## version 2.0.1 - May 19th, 2021

  - Make assertLoginRequired work for pytest tp fixture.

## version 2.0.0 - May 18th, 2021

  - Drops Python 2.7, 3.4, and pypy and Django 1.11 support.
  - Add Django 3.1 support.

## version 1.4.0 - December 3rd, 2019

  - Added Django 3.0 support
  - Misc dependency updates

## version 1.3.1 - July 31st, 2019

  - Made `make_user` and `get_instance` class based methods, so they can be used
    in `setupUpTestData`. Thanks @avelis for the report.
  
## version 1.3.0 - July 31st, 2019

  - Add `tp_api` pytest fixture.

## version 1.2.0 - May 5h, 2019

  - Add optional `msg` argument to assertEqual method. Thanks @davitovmasyan.

## version 1.1.1 - July 2nd, 2018

  - Fix premature loading of Django settings under pytest
   
## version 1.1.0 - May 20th, 2018

  - Added real pytest fixture support! 
  - Stopped testing support below Django 1.11.x. django-test-plus should probably continue to work for a long time, but Django 1.11 is the only pre-2.x version that is still supported so all we are going to worry about.
  - Moved README and docs to Markdown
   
  ## version 1.0.22 - January 9th, 2018

  - Fix bug where we did not pass data dictionary to RequestFactory.get() properly
  
## version 1.0.21 - December 15th, 2017

  - Add response_204 method

## version 1.0.20 - October 31st, 2017

  - The Halloween Release!
  - Fixes to CI to ensure we really test Django 2.0

## version 1.0.19 - October 24th, 2017

  - Django 2.0 support
  - Dropped support for Python 3.3
  - Dropped support for Django < 1.8
  - Added APITestCase for better DRF testing

## version 1.0.18 - June 26th, 2017

  - Allow custom Request objects in get() and post()
  - Begin testing against Python 3.6 and Django 1.11

## version 1.0.17 - January 31st, 2017

  - Added assertResponseHeaders

## version 1.0.16 - October 19th, 2016

  - Added print_form_errors utility

## version 1.0.15 - August 18th, 2016

  - Added helper methods for more HTTP methods like put, patch, and trace
  - Added assertResponseContains and assertResponseNotContains

## version 1.0.14 - June 25th, 2016

  - Fixed documentation typo
  - Added response_400() test
  - Added Guinslym and David Arcos to AUTHORS.txt

## version 1.0.13 - May 23rd, 2016

  - Added response_401() test
  - Fixed situation where User models without a 'username' field could not be
    used as easily.  Now credential field is automatically determined.
  - Fixed assertLoginRequired when settings.LOGIN_URL is a named URL pattern
  - Removed support for Django 1.4.x as it is well beyond it's end of life and causes a headache for supporting newer releases

## version 1.0.12 - March 4th, 2016

  - Fixed incorrect documentation
  - Added response_405 and response_410 test methods

## version 1.0.11 - November 11, 2015

  - Fixed bad README typos and merge artifacts

## version 1.0.10 - November 11, 2015

  - Added response_405() test
  - requirements.txt typo

## version 1.0.9 - August 28, 2015

  - README typo
  - Fix more bad argument handling in CBVTest methods
  - Fix alias issue with PyCharm

## version 1.0.8 - August 12, 2015

  - Bug fix with argument order

## version 1.0.7 - July 31st, 2015

  - get/post test methods now accept the `follow` boolean.

## version 1.0.6 - July 12th, 2015

  - Allow overriding password to be not just 'password'
  - Added CBVTestCase to be able to test generic CBVs without hitting routing or middleware

## version 1.0.5 - June 16th, 2015

  - Allow 'from test_plus import TestCase'
  - Make response_XXX() be able to use last_response
  - Add extra lazy option of passing full URL to get() and post()
  - Pass along QUERY_STRING information via data kwargs on gets()

## version 1.0.4 - May 29th, 2015

  - README formatting fixes
  - Added get_context() method
  - Added assertContext() method

## version 1.0.3 - May 28th, 2015

  - Added extras kwargs to be able to pass to url resolution
  - Added response_403
  - README typo

## version 1.0.2 - May 23rd, 2015

  - Actually fixing README by moving README.md to README.rst
  - Added docs for assertNuMQueriesLessThan()

## version 1.0.1 - May 23rd, 2015

  - Fixing README markdown on PyPI issue

## version 1.0.0 - May 23rd, 2015

  - Initial release
