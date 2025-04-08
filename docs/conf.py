# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath('../backend'))
# sys.path.insert(0, os.path.abspath('../backend/frege/analyzers/core/'))
# sys.path.insert(0, os.path.abspath('../backend/frege/indexers/'))
# sys.path.insert(0, os.path.abspath('../backend/frege/management/'))
# sys.path.insert(0, os.path.abspath('../backend/frege/repositories/'))


project = 'FREGE'
author = 'IG, DD'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'Eng'

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_mock_imports = ['celery', 'django', 'lizard', 'lizard_ext', 'github', 'radon']
