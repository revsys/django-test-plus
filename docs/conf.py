# django-test-plus documentation build configuration.
#
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# autodoc imports test_plus, which needs a configured Django. The test project
# supplies the settings.
sys.path.insert(0, os.path.abspath("../"))
sys.path.insert(0, os.path.abspath("../test_project/"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
import django

django.setup()

# -- Project information -----------------------------------------------------

project = "django-test-plus"
copyright = "2015, Frank Wiles"
author = "Frank Wiles"

# The short X.Y version. Kept in sync by bumpver, see [tool.bumpver] in
# pyproject.toml.
version = "2.5.0"
# The full version, including alpha/beta/rc tags.
release = version

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_prompt",
]

source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build"]

# Link Python and Django names to their upstream documentation.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = []

# Adds an "Edit this page on GitHub" link to every page.
html_theme_options = {
    "source_repository": "https://github.com/revsys/django-test-plus/",
    "source_branch": "main",
    "source_directory": "docs/",
}
