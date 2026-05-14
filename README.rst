rivtlib
========

**rivtlib is alpha software. Some features are not complete and the program has
bugs.**

*rivt* is an extensible, open source tool for writing and sharing engineering
documents. This has always been a challenge because engineering documents are
complex. They may include text, images, tables, calculations, models and
computer code. 

A *rivt file* is a Python file (.py) that imports the *rivtlib* Python package
and includes *rivt markup*. *Markup* publishes the file as a 
**text, PDF or HTML doc** that can be assembled and 
linked, with other *docs*, into a *rivt report*.

The primary use case for *rivt* is producing clear, acurate engineering
documents that are: 

#. Easier to write and format than LaTeX, Excel, Word or other general purpose word processors.

#. Do not need to be formatted to the precise standards of a formal journal publication.

A second use case is when documents may need to be produced in a variety of
formats from the same input file. For futher details please refer to the 
`rivt user manual <https://rivt.info>`__.

Use Cases
-----------

In addition to publishing engineering documents for:

#. internal communication.
#. research documentation.
#. government permits.
#. technical reports.
#. funding applications.
#. teaching.
#. presentations.

*rivt* can: 

#. function as a front and back end for external software. 
#. be used for real time collaboration.

The table below compares limitations between different software
programs. *rivt* is designed to address these limitations and serve as a
complement or replacement to existing software.


Software Comparison
--------------------

============ ========= ======== ======== ========= ========= ============= 
Program      Rep [1]_  Ver [2]_ Txt [3]_ Comp [4]_  CP [5]_   Collab [6]_  
============ ========= ======== ======== ========= ========= ============= 
Matlab         no       no         no      no          no       no   
Mathcad        no       no         no      no          no       no   
Mathematica    no       no         no      no          no       no   
Cloud SaaS    limited   no         no      no          yes      limited  
Excel         limited   no         no      yes         no       yes 
Jupyter        no       no         no      yes         yes      yes  
**rivt**      **yes**  **yes**   **yes**  **yes**   **yes**    **yes**
============ ========= ======== ======== ========= ========= ============= 


.. [1] Report generation
.. [2] Native version control
.. [3] Plain text, readable input files
.. [4] Forward and backward compatibility
.. [5] Cross-platform
.. [6] Collaboration support


Modules Summary
----------------


=====================================================
Module Name:  rvapi.py
=====================================================

IMPORTS:
  - import fnmatch
  - import logging
  - import os
  - import sys
  - import warnings
  - from importlib.metadata import version
  - from pathlib import Path
  - import __main__
  - import rivtlib.rvunits as rvunit
  - from rivtlib import rvdoc, rvparse

CLASSES & METHODS:

 TOP-LEVEL FUNCTIONS:
 (204 lines total)
  - cmdhelp() -> 12 lines
  - doc_parse() -> 23 lines
  - R() -> 36 lines
  - I() -> 34 lines
  - V() -> 30 lines
  - T() -> 33 lines
  - D() -> 10 lines
  - S() -> 8 lines
  - X() -> 9 lines
=====================================================


=====================================================   
Module Name:  rvparse.py
=====================================================   

IMPORTS:
  - import logging
  - import os
  - import sys
  - import warnings
  - from io import StringIO
  - from pathlib import Path
  - import tabulate
  - from fastcore.utils import store_attr
  - import __main__
  - from . import rvcmd, rvtag

CLASSES & METHODS:
    Class: Rs (333 lines total)
    └─ Method: __init__() -> 126 lines
    └─ Method: content() -> 177 lines
    └─ Method: prt_tabl() -> 22 lines

 TOP-LEVEL FUNCTIONS:
=====================================================  


=====================================================   
Module Name:  rvtag.py
=====================================================   

IMPORTS:
  - import csv
  - import textwrap
  - from pathlib import Path
  - import docutils.parsers.rst.tableparser
  - import docutils.statemachine
  - import sympy as sp
  - import tabulate
  - from fastcore.utils import store_attr
  - from numpy import *
  - from sympy.abc import _clash2

CLASSES & METHODS:
    Class: Tag (337 lines total)
    └─ Method: __init__() -> 22 lines
    └─ Method: taglx() -> 173 lines
    └─ Method: tagbx() -> 108 lines
    └─ Method: parse_simple_rst_table() -> 23 lines     

 TOP-LEVEL FUNCTIONS:
===================================================== 


=====================================================   
Module Name:  rvcmd.py
=====================================================   

IMPORTS:
  - import csv
  - import sys
  - import textwrap
  - from io import StringIO
  - from pathlib import Path
  - import numpy as np
  - import pandas as pd
  - import sympy as sp
  - import tabulate
  - from fastcore.utils import store_attr
  - from IPython.display import display as _display     
  - from PIL import Image
  - from sympy.abc import _clash2
  - from rivtlib.rvunits import *
  - from rivtlib.unum.core import Unum

CLASSES & METHODS:
    Class: Cmd (954 lines total)
    └─ Method: __init__() -> 34 lines
    └─ Method: cmdx() -> 13 lines
    └─ Method: vdefine() -> 51 lines
    └─ Method: vassign() -> 109 lines
    └─ Method: vfunc() -> 114 lines
    └─ Method: vcompare() -> 114 lines
    └─ Method: IMAGE() -> 44 lines
    └─ Method: IMAGE2() -> 79 lines
    └─ Method: TABLE() -> 76 lines
    └─ Method: TEXT() -> 12 lines
    └─ Method: VALTABLE() -> 105 lines
    └─ Method: PYTHON() -> 70 lines
    └─ Method: LATEX() -> 5 lines
    └─ Method: WIN() -> 19 lines
    └─ Method: OSX() -> 19 lines
    └─ Method: LINUX() -> 19 lines
    └─ Method: wrap_pad() -> 15 lines

 TOP-LEVEL FUNCTIONS:
=====================================================


=====================================================   
Module Name:  rvdoc.py
=====================================================   

IMPORTS:
  - import configparser
  - import logging
  - import os
  - import shutil
  - import subprocess
  - import warnings
  - from datetime import datetime
  - from pathlib import Path
  - from fastcore.utils import store_attr
  - import __main__

CLASSES & METHODS:
    Class: Cmdp (959 lines total)
    └─ Method: __init__() -> 34 lines
    └─ Method: cmdx() -> 73 lines
    └─ Method: htmlx() -> 76 lines
    └─ Method: pdfx() -> 74 lines
    └─ Method: textx() -> 28 lines
    └─ Method: metadatax() -> 26 lines
    └─ Method: attachpdfx() -> 5 lines
    └─ Method: confpy() -> 136 lines
    └─ Method: rivtstyS() -> 376 lines
    └─ Method: coverS() -> 63 lines
    └─ Method: genreport() -> 2 lines
    └─ Method: latexx() -> 32 lines

 TOP-LEVEL FUNCTIONS:
===================================================== 


=====================================================   
Module Name:  rvunits.py
=====================================================   

IMPORTS:
  - import importlib.util
  - import sys
  - from pathlib import Path
  - from rivtlib.unum.core import Unum, new_unit        

CLASSES & METHODS:

 TOP-LEVEL FUNCTIONS:
===================================================== 



