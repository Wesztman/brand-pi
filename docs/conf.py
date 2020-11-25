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
sys.path.append(os.path.abspath('./_sphinx_ext/'))

import subprocess
import sphinx_rtd_theme
import recommonmark
from recommonmark.transform import AutoStructify


# -- Project information -----------------------------------------------------

project = 'Fire Extinguisher 2020'
author = 'Team Bränd'

# -- Global variables -----------------------------------------------------

# Only works for .rst for now
# rst_epilog = """
# .. |art_nr| replace:: {0}
# .. |release_date| replace:: {1}
# """.format(
#     art_nr,
#     release_date
# )

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_rtd_theme',
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinxcontrib.plantuml',
    'toctree_filter',
    'sphinx-prompt',
    'sphinx_substitution_extensions'
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
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    'style_external_links': True,
    'collapse_navigation': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    'css/custom.css',
]

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
#html_js_files = [
#    'js/feedback.js',
#]

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = 'assets/media/oae.png'

# View source ulr lik int eh top right corner. Pints to mater branch in duc repo.
output = subprocess.check_output(["git", "rev-parse", "HEAD"])
git_sha = str(output, 'utf-8')

# html_context = {
#     "display_azure_devops": True,
#     'source_url_prefix': azure_repos_url + '?' + git_version + '&path=doc/'
# }

source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
source_suffix = ['.rst', '.md']

# PlantUML
plantuml = 'java -jar %s ' % (os.path.join(os.path.dirname(__file__), "_plantuml/plantuml.1.2020.2.jar"))

# If file is tagged with prefix underscore and toc content prefixed with internal i.e :internal:protocol/_index then this is ignored in build output
if tags.has('external'):
    exclude_patterns.append('**/_*')
    toc_filter_exclude = ['internal']

# app setup hook
def setup(app):
    app.add_config_value('recommonmark_config', {
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)
