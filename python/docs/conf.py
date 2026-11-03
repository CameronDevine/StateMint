# Sphinx configuration for the StateMint Python package.
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import StateMint  # noqa: E402

project = 'StateMint'
author = 'Cameron Devine, Joseph L. Garbini and Rico A. R. Picone'
copyright = '2018–2026, ' + author
release = StateMint.__version__
version = '.'.join(release.split('.')[:2])

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.mathjax',
	'sphinx.ext.viewcode',
	'sphinx.ext.napoleon',
]
autodoc_member_order = 'bysource'
source_suffix = {'.rst': 'restructuredtext'}
master_doc = 'index'
language = 'en'
pygments_style = 'sphinx'
html_theme = 'alabaster'
autodoc_mock_imports = ['numpy']
