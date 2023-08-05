# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os

from pkg_resources import parse_version


try:
    from coordio import __version__
except ModuleNotFoundError:
    from sdsstools import get_package_version
    __version__ = get_package_version(__file__, 'sdss-coordio') or 'dev'


# Are we building in RTD?
on_rtd = os.environ.get('READTHEDOCS') == 'True'

# Sphinx template selected in cookiecutter and whether to use releases
sphinx_template = 'alabaster'
use_releases = 'yes'

# Importing matplotlib here with agg to prevent tkinter error in readthedocs
# import matplotlib
# matplotlib.use('agg')


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary',
              'sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.mathjax',
              'sphinx.ext.intersphinx']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']
# source_suffix = '.rst'

# source_parsers = {
#     '.md': 'recommonmark.parser.CommonMarkParser',
# }

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'coordio'
copyright = '{0}, {1}'.format('2020', 'José Sánchez-Gallego and Conor Sayres')
author = 'José Sánchez-Gallego and Conor Sayres'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The short X.Y version.
version = parse_version(__version__).base_version
# The full version, including alpha/beta/rc tags.
release = __version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'py:obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Intersphinx mappings
intersphinx_mapping = {'python': ('https://docs.python.org/3.6', None),
                       'astropy': ('http://docs.astropy.org/en/latest', None),
                       'numpy': ('http://docs.scipy.org/doc/numpy/', None)}

autodoc_mock_imports = ['_tkinter']
autodoc_member_order = 'groupwise'

napoleon_use_rtype = False
napoleon_use_ivar = True

rst_epilog = f"""
.. |numpy_array| replace:: Numpy array
.. |HDUList| replace:: :class:`~astropy.io.fits.HDUList`
.. |coordio_version| replace:: {__version__}
"""


# -- Options for HTML output ----------------------------------------------

html_css_files = [
    'pygments.css'
]

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'alabaster'

html_theme_options = {
    'logo': 'sdssv_logo.png',
    'github_user': 'sdss',
    'github_repo': project,
    'github_button': True,
    'github_type': 'star',
    'sidebar_collapse': True,
    'page_width': '80%'
}

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

html_css_files += ["custom.css"]

html_favicon = './_static/favicon_sdssv.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

# See https://github.com/rtfd/readthedocs.org/issues/1776 for why we do this
if on_rtd:
    html_static_path = []
else:
    html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = '{0}pdoc'.format('coordio')


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, '{0}.tex'.format(project), u'{0} Documentation'.format(project),
     author, 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'coordio', u'{0} Documentation'.format(project),
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, project, u'{0} Documentation'.format(project),
     author, project, 'One line description of project.',
     'Miscellaneous'),
]

if use_releases == 'yes':

    extensions += ['sdsstools.releases']

    releases_github_path = 'sdss/coordio'
    releases_document_name = ['CHANGELOG']
    releases_unstable_prehistory = True
