rivtlib
========

**rivtlib is alpha software. Some features are not complete and the program has
bugs.**

*rivt* is an extensible, open source tool for writing engineering documents with
and emphasis on reuse. *rivt* includes the built-in capability to export
selected sections of a *private rivt file* to a *public rivt file* for sharing
and reuse. For futher details please refer to the 
`rivt user manual <https://rivt.info>`__.

A *rivt file* is a Python file (.py) that imports the *rivtlib* Python package
and includes *rivt markup*. *Markup* publishes the file as a 
**text, PDF or HTML doc** that can be assembled and 
linked, with other *docs*, into a *rivt report*.

The primary use case for *rivt* is producing clear, accurate engineering
documents that are: 

#. Easier to write and format than LaTeX, Excel, Word or other general purpose
   word processors.

#. Do not need to be formatted to the precise standards of a formal journal
   publication.

Specific examples include:

#. internal communication
#. research documentation
#. government permits
#. technical reports
#. funding applications
#. teaching
#. presentations

*rivt* can: 

#. function as a front and back end for external software. 
#. be used for real time collaboration.

The table below compares limitations between different software
programs. *rivt* is designed to address these limitations and serve as a
complement or replacement to existing software.


Software Comparison
--------------------

============= ============ ========= ======== ========== =========== ========== ========= ============= ===========
Program       Reprt [1]_   Ver [2]_  Txt [3]_  Priv [4]_  Unts [5]_  Comp [6]_  C-P [7]_   Coll [8]_     Pub [9]_
============= ============ ========= ======== ========== =========== ========== ========= ============= ===========
*Matlab*         no           no         no     no        no           no         no        no            yes
*Mathcad*        no           no         no     no        no           no         no        no            no
*Mathematica*    no           no         no     no        no           no         no        no            yes
*Cloud SaaS*    limited       no         no     no        no           no         yes      limited       limited
*Excel*         limited       no         no     no        no           yes        no        yes           yes
Jupyter          no           no         no     no        no           yes        yes       yes           yes
Quarto           yes          yes        no     no        no           no         yes       yes           yes
**rivt**        **yes**     **yes**   **yes**  **yes**    **yes**     **yes**    **yes**   **yes**       **yes**  
============= ============ ========= ======== ========== =========== ========== ========= ============= ===========


.. [1] Report generation
.. [2] Native version control
.. [3] Plain text input and output files
.. [4] Syntax control of private/public sections
.. [5] Dual units
.. [6] Forward and backward compatibility
.. [7] Cross-platform
.. [8] Collaboration support
.. [9] PDF and HTML documents from the same input file  


Modules - Summary
-------------------

::
    
    ================================================================================
    Total Project Line Count:  5761
    ================================================================================ 

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvapi.py   | Total Lines: 522
    ================================================================================

    IMPORTS:
    - import argparse
    - import fnmatch
    - import glob
    - import logging
    - import os
    - import shutil
    - import subprocess
    - import sys
    - import warnings
    - from importlib.metadata import version
    - from pathlib import Path
    - import __main__
    - import rivtlib.rvunits as rvunit
    - from rivtlib import rvdoc, rvparse, rvtext

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - cmdhelp() -> 12 lines
    - doc_parse() -> 32 lines
    - R() -> 78 lines
    - I() -> 36 lines
    - V() -> 46 lines
    - T() -> 31 lines
    - D() -> 12 lines
    - S() -> 9 lines
    - X() -> 11 lines
    ================================================================================

    
    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvbook.py   | Total Lines: 327================================================================================

    IMPORTS:
    - import configparser
    - import glob
    - import logging
    - import os
    - import subprocess
    - import sys
    - import textwrap
    - import warnings
    - from datetime import datetime
    - from pathlib import Path
    - import __main__
    - import rvrepcfg as rvb

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - pdfx() -> 88 lines
    - txtx() -> 29 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvcmd.py   | Total Lines: 1157================================================================================

    IMPORTS:
    - import csv
    - import sys
    - import textwrap
    - from datetime import datetime
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
        Class: Cmd (1134 lines total)
        └─ Method: __init__() -> 35 lines
        └─ Method: cmdx() -> 13 lines
        └─ Method: vdefine() -> 56 lines
        └─ Method: vassign() -> 113 lines
        └─ Method: vfunc() -> 114 lines
        └─ Method: vcompare() -> 122 lines
        └─ Method: TEXT() -> 48 lines
        └─ Method: RUNFILE() -> 47 lines
        └─ Method: IMAGE() -> 54 lines
        └─ Method: IMAGE2() -> 77 lines
        └─ Method: TABLE() -> 80 lines
        └─ Method: VALTABLE() -> 94 lines
        └─ Method: PYTHON() -> 75 lines
        └─ Method: FUNCTION() -> 82 lines
        └─ Method: wrap_pad() -> 15 lines
        └─ Method: get_image_time() -> 57 lines

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvdoc.py   | Total Lines: 548
    ================================================================================

    IMPORTS:
    - import configparser
    - import glob
    - import logging
    - import os
    - import shutil
    - import subprocess
    - import warnings
    - from datetime import datetime
    - from pathlib import Path
    - import rvdoccfg as rvd
    - from fastcore.utils import store_attr
    - import __main__

    CLASSES & METHODS:
        Class: Cmdp (528 lines total)
        └─ Method: __init__() -> 88 lines
        └─ Method: cmdx() -> 84 lines
        └─ Method: metadatax() -> 33 lines
        └─ Method: attachpdfx() -> 5 lines
        └─ Method: pdfx() -> 27 lines
        └─ Method: pdf_insert() -> 141 lines
        └─ Method: htmlx() -> 38 lines
        └─ Method: txtx() -> 24 lines
        └─ Method: nonex() -> 17 lines
        └─ Method: docreadme() -> 36 lines

    TOP-LEVEL FUNCTIONS:
    ================================================================================
    
    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvdoccfg.py   | Total Lines: 721
    ================================================================================

    IMPORTS:
    - import glob
    - import os
    - import shutil
    - from datetime import datetime
    - from pathlib import Path

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - copy_docs() -> 11 lines
    - pdf_confpy() -> 144 lines
    - pdf_yamlS() -> 420 lines
    - html_templ() -> 41 lines
    - html_confpy() -> 81 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvparse.py   | Total Lines: 409
    ================================================================================

    IMPORTS:
    - import logging
    - import os
    - import re
    - import sys
    - import textwrap
    - import warnings
    - from io import StringIO
    - from pathlib import Path
    - import tabulate
    - from fastcore.utils import store_attr
    - import __main__
    - from . import rvcmd, rvtag

    CLASSES & METHODS:
        Class: Rs (387 lines total)
        └─ Method: __init__() -> 150 lines
        └─ Method: prt_tabl() -> 22 lines
        └─ Method: remove_aster() -> 10 lines
        └─ Method: content() -> 198 lines

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvrepcfg.py   | Total Lines: 790
    ================================================================================

    IMPORTS:
    - import glob
    - import os
    - import shutil
    - from pathlib import Path

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - copy_docs() -> 10 lines
    - pdf_confpy() -> 146 lines
    - pdf_yamlS() -> 402 lines
    - pdf_coverS() -> 68 lines
    - html_confpy() -> 81 lines
    - html_index() -> 57 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvreport.py   | Total Lines: 517
    ================================================================================

    IMPORTS:
    - import configparser
    - import glob
    - import logging
    - import os
    - import subprocess
    - import sys
    - import textwrap
    - import warnings
    - from datetime import datetime
    - from itertools import groupby
    - from pathlib import Path
    - import __main__
    - import rvrepcfg as rvr

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - pdfx() -> 92 lines
    - htmlx() -> 155 lines
    - txtx() -> 40 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvtag.py   | Total Lines: 478
    ================================================================================

    IMPORTS:
    - import ast
    - import csv
    - import io
    - import sys
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
        Class: Tag (460 lines total)
        └─ Method: __init__() -> 23 lines
        └─ Method: taglx() -> 157 lines
        └─ Method: tagbx() -> 178 lines
        └─ Method: build_transcript() -> 66 lines
        └─ Method: parse_simple_rst_table() -> 24 lines

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvtext.py   | Total Lines: 87
    ================================================================================

    IMPORTS:
    - import textwrap

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - typex() -> 14 lines
    - pythonx() -> 2 lines
    - endnotesx() -> 42 lines
    - mermaidx() -> 2 lines
    - dotx() -> 2 lines
    - latexx() -> 2 lines
    - htmlx() -> 2 lines
    - rstx() -> 2 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvunits.py   | Total Lines: 141
    ================================================================================

    IMPORTS:
    - import importlib.util
    - import sys
    - from pathlib import Path
    - from rivtlib.unum.core import Unum, new_unit

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\__init__.py   | Total Lines: 60
    ================================================================================

    IMPORTS:

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\__main__.py   | Total Lines: 4
    ================================================================================

    IMPORTS:

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    ================================================================================


