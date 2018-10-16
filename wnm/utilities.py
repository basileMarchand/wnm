

import os
from shutil import copyfile

def get_share_data_dir():
    sep = os.path.sep
    base_dir = sep.join( os.path.abspath( __file__ ).split( os.path.sep )[:-2] + ["share","data"] )
    return base_dir


def write_wnm_documentation( f ):
    base_dir = get_share_data_dir()
    copyfile(os.path.join(base_dir, "Notice.rst"), f.name)


def write_rst_documentation( f ):
    base_dir = get_share_data_dir()
    copyfile(os.path.join(base_dir, "reStructuredText.rst"), f.name)

def write_sphinx_config( f, conf ):
    content = """
# -*- coding: utf-8 -*- 
#
# Working Notes Manager build config for Sphinx
#
import sys, os
extensions = ['sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.mathjax']
source_suffix = '.rst'
master_doc = 'index'
project = u'Working Notes Manager'
copyright = u'2018, Basile Marchand'
version = '0.1.0'
# The full version, including alpha/beta/rc tags.
release = '0.1.0'
pygments_style = 'sphinx'
html_theme = '{}'
html_logo = "_static/wnm_logo_2.png"
html_static_path = ['_static']
html_use_index = True
html_show_sourcelink = True
html_show_sphinx = True
htmlhelp_basename = 'WorkingNotes'
""".format(conf.sphinx.theme)

    f.write( content )


def write_root_index( f, conf ):
    f.write(""".. master file

{}
{}

Category:

.. toctree::
   :maxdepth: 1

   Documentation about WorkingNotes usage <category_help/Notice>
   A short introduction to reStructuredText <category_help/reStructuredText>


Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

""".format( conf.manager.notes.notebook.name, "".join(["="]*(len(conf.manager.notes.notebook.name)))) )


def install_logo( _static ):
    base_dir = get_share_data_dir()
    copyfile(os.path.join(base_dir, "wnm_logo_2.png"), os.path.join(_static,"wnm_logo_2.png") )
