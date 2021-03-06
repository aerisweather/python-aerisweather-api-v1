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
from os import path
import sys

sphinx_conf_dir = path.join(path.dirname(__file__))
module_dir = path.abspath(path.join(sphinx_conf_dir, "..", ".."))
sys.path.insert(0, module_dir)


# -- Project information -----------------------------------------------------

project = "AerisWeather API v1 SDK"
copyright = "2022, AerisWeather"
author = "John Koelndorfer"

from aerisweather_api_v1 import __version__ as project_version

release = project_version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

add_module_names = False


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Intersphinx configuration -----------------------------------------------

intersphinx_mapping = {
    # geojson intersphinx mappings don't actually work because the geojson
    # module doesn't generate # a comprehensive set of docs. Maybe some day...
    "geojson": ("https://geojson.readthedocs.io/en/latest/", None),
    "requests": ("https://docs.python-requests.org/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
}

# -- AerisWeather doc support ------------------------------------------------

extlinks = {
    "aerissignup": ("https://www.aerisweather.com/pricing/", None),
    "aerisauth": ("https://www.aerisweather.com/support/docs/api/getting-started/authentication/", None),
    "aerisdocs": ("https://www.aerisweather.com/support/docs/%s", None),
    "aerisapi": ("https://www.aerisweather.com/support/docs/api/%s", None),
    "aerisapi_epact": ("https://www.aerisweather.com/support/docs/api/reference/endpoints/%s/#actions", None),
    "aerisapi_epfilt": ("https://www.aerisweather.com/support/docs/api/reference/endpoints/%s/#filters", None),
    "aerisapi_epquery": ("https://www.aerisweather.com/support/docs/api/reference/endpoints/%s/#queries", None),
    "aerisapi_epprop": ("https://www.aerisweather.com/support/docs/api/reference/endpoints/%s/#properties", None),
}

extlinks_detect_hardcoded_links = True
