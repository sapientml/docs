# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sphinx_rtd_theme
import sphinx_fontawesome

project = 'sapientml'
copyright = '2023, The SapientML Authors'
author = 'The SapientML Authors'

version = '0.4.4'
release = '0.4.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', 
    'sphinx.ext.napoleon', 
    'sphinx_rtd_theme', 
    'sphinx_fontawesome', 
    'myst_parser', 
    'sphinxcontrib.autodoc_pydantic',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_show_sourcelink = False
html_static_path = ['_static']
html_logo = 'images/SapientML_negative_logo.svg'
html_theme_options = {
    'logo_only': True,
    'display_version': True
}

# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True

autoclass_content = "both"

autodoc_pydantic_model_show_json = True
autodoc_pydantic_settings_show_json = False