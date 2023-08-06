# -*- coding: utf-8 -*-
import sys
from pathlib import Path
from biopal.__init__ import __version__

sys.path.insert(0, str(Path(__file__).parent.parent.absolute()))

# Build instructions
#   Build latex pdf:
#       python -m sphinx -b latex -a doc doc/_buildlatex
#       cd doc/_buildlatex
#       make.bat
#   Build API Doc html:
#       nox -r -fb conda -s build_doc

# -- Project information -----------------------------------------------------
project = "BioPAL"  # This will be the title of sphinx latex pdf: if empty the pdf title will be the title of index.rst (see html_title for API doc title)
author = "BioPAL team"
copyright = "2021, BioPAL team"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
	"sphinx.ext.graphviz",
    "numpydoc",
    "nbsphinx",
	
]
autosummary_generate = True
exclude_patterns = ["_build", "**.ipynb_checkpoints", "legacy"]

# -- HTML options ------------------------------------------------------------
html_title = "BioPAL"  # This will be the title for the api doc html
html_logo = "_static/logo.png"
html_static_path = ["_static"]
html_theme = "furo"

# -- LATEX options ------------------------------------------------------------
latex_engine = "xelatex"
latex_logo = "_static/logo.png"

# make title is for the cover page:
latex_maketitle = r"""
\begin{titlepage}

\raggedleft % those are for align all that follows on the right
\sphinxlogo
Generic string on the right \par % "par is used for carriage return"

\centering  % those are for align all that follows on the center
\sphinxlogo
Generic string centred \par

\raggedright   % those are for align all that follows on the left
\sphinxlogo
Generic string on the left \par
\tiny Generic string on the left tiny\par
\small Generic string on the left small\par
\large Generic string on the left large\par
\huge Generic string on the left huge\par
\vspace{5mm} % this generates 5mm of vertical space
\today \par
\vspace{5mm}
BioPAL Team \par

\end{titlepage}
"""
latex_elements = {"maketitle": latex_maketitle}
