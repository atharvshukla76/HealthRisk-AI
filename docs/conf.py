# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'MatRisk AI'
copyright = '2026, Zetheta Algorithms Private Limited'
author = 'Intern'

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
