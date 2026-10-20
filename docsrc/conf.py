# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('_extensions'))


# -- Project information -----------------------------------------------------

project = 'ELF Object File Format'
copyright = '2026, Xinuos'
author = 'Xinuos'
version = '4.3 DRAFT'
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'
html_theme_options = {
    'show_relbars': True,
    'font_family': '"Open Sans", sans-serif',
}
html_copy_source = False;
html_scaled_image_link = False;

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

numfig = True
numfig_format = {
    'figure' : 'Figure %s'
}

highlight_language = 'c';

# -- Options for latex output -------------------------------------------------

latex_documents = [
    ('index', 'elf.tex', 'ELF Object File Format', 'Xinuos, Inc.', 'manual', True)
]

latex_docclass = {
    'manual': 'book'
}

latex_top_level_sectioning = 'chapter'

latex_show_pagerefs = True

latex_table_style = ['booktabs', 'nocolorrows']

latex_elements = {
    'releasename': 'Version',
    'fontpkg': r"""
\usepackage[default,defaultsans]{opensans}
\usepackage{inconsolata}
\usepackage[T1]{fontenc}
""",
    'fncychap': '',
    'tableofcontents': r'\elftableofcontents',
    'preamble': r'\input{elfstyles.tex.txt}'
}

latex_additional_files = [
    '_latex/elfstyles.tex.txt'
]

latex_theme = 'manual'

latex_theme_options = {
}

