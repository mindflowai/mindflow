# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

sys.path.insert(0, os.path.abspath("../"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Mindflow"
copyright = "2023, Mindflow AI"
author = "Chris Steege, Dyllan McCreary, Tarik Kaan Koc"
release = "0.3.14"
version = "latest"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
]

suppress_warnings = ["autosectionlabel.*"]

# Napoleon settings
napoleon_numpy_docstring = True

# html_context configuration for GitHub edit link
html_context = {
    "display_github": True,
    "github_user": "mindflowai",
    "github_repo": "mindflow",
    "github_version": "main/docs/",
}

templates_path = ["source/_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "English"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["source/_static"]

source_suffix = [".rst", ".md"]

# Below html_theme_options config depends on the theme.
html_logo = "source/_static/main-logo.png"

html_theme_options = {"logo_only": True, "display_version": True}

# -- Options for EPUB output
epub_show_urls = "footnote"
