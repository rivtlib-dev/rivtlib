
rivtlib
========

.. code-block:: diff

    + NOTES:

    + See the steps outlined below for running an example file in a rivt CodeSpace.

    - rivtlib is alpha software. Some features are not complete and the program has bugs.

*rivt* is an open-source program for writing and assembling calculation
documents with a focus on reuse. The large ecosystem of engineering calculation
tools often requires assembly of their output into a single project document.
*rivt* is designed to write, assemble and link calculation documents into a
live, editable and testable format prior to publishing to a text, PDF or HTML
static format. 

The *rivt markup* language also facilitates conversion of any PDF or text
document into a live calculation document that can then be modified or extended.
Python knowledge is not required to use *rivt* but its capabilities are
increased when Python scientific and engineering libraries and scripts are used.
For further details refer to the `rivt user manual <https://rivt.info>`__.

The primary use case for *rivt* is producing clear, live calculation
documents that can be easily shared, reused and maintained. The table below 
compares limitations in current software programs that *rivt* is
designed to complement or replace.


**Software Comparison (commercial programs in italics)**

============= ============ ========= ======== ========== =========== ========== ========= ============= ===========
Program       Reprt [1]_   Ver [2]_  Txt [3]_  Priv [4]_ Units [5]_  Comp [6]_  C-P [7]_   Coll [8]_     Pub [9]_
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
.. [2] Native git version control
.. [3] Plain text input and output files
.. [4] Syntax control of private/public sections
.. [5] Calculation with dual units
.. [6] Forward and backward compatibility
.. [7] Cross-platform
.. [8] Collaboration support
.. [9] text, PDF and HTML documents from the same input file  


Run a rivt file in a rivt CodeSpace
---------------------------------------

.. code-block:: diff

    + When you fork or clone the rivtlib repository, you also get a devcontainer that will install rivt and open an example rivt file in a VSCode rivt environment. 
    
    Here are the steps to run the example rivt file in CodeSpaces:

    + 1. Open the rivtlib repository 




Modules - Summary
-------------------

::

    ================================================================================
    Total Project Line Count:  6035
    ================================================================================ 

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvapi.py   | Total Lines: 493
    ================================================================================

    IMPORTS:
    - import argparse
    - import fnmatch
    - import logging
    - import os
    - import string
    - import sys
    - import warnings
    - from importlib.metadata import version
    - from pathlib import Path
    - import __main__
    - import rivtlib.rvunits as rvunit
    - from rivtlib import rvdoc, rvparse, rvshell, rvtext

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - cmdhelp() -> 12 lines
    - doc_parse() -> 29 lines
    - R() -> 26 lines
    - I() -> 22 lines
    - V() -> 45 lines
    - T() -> 60 lines
    - D() -> 11 lines
    - S() -> 9 lines
    - X() -> 7 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvbook.py   | Total Lines: 327
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
    - from pathlib import Path
    - import __main__
    - import rvrepcfg as rvb

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - pdfx() -> 88 lines
    - txtx() -> 29 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvcmd.py   | Total Lines: 1284
    ================================================================================

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
        Class: Cmd (1261 lines total)
        └─ Method: __init__() -> 28 lines
        └─ Method: cmdx() -> 13 lines
        └─ Method: vdefine() -> 56 lines
        └─ Method: vassign() -> 113 lines
        └─ Method: vfunc() -> 115 lines
        └─ Method: vcompare() -> 123 lines
        └─ Method: wrap_pad() -> 15 lines
        └─ Method: get_image_time() -> 57 lines
        └─ Method: IMAGE() -> 62 lines
        └─ Method: IMAGE2() -> 85 lines
        └─ Method: TABLE() -> 85 lines
        └─ Method: VALTABLE() -> 101 lines
        └─ Method: VALDATA() -> 101 lines
        └─ Method: PYTHON() -> 81 lines
        └─ Method: FUNCTION() -> 83 lines
        └─ Method: TEXT() -> 92 lines

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
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvdoccfg.py   | Total Lines: 726
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
    - pdf_confpy() -> 145 lines
    - pdf_yamlS() -> 424 lines
    - html_templ() -> 41 lines
    - html_confpy() -> 81 lines
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvparse.py   | Total Lines: 406
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
        Class: Rs (384 lines total)
        └─ Method: __init__() -> 147 lines
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
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvreport.py   | Total Lines: 518
    ================================================================================

    IMPORTS:
    - import configparser
    - import glob
    - import logging
    - import os
    - import shutil
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
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvshell.py   | Total Lines: 93
    ================================================================================

    IMPORTS:
    - import glob
    - import os
    - import shutil
    - import subprocess
    - import textwrap
    - from pathlib import Path

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - run_shell() -> 85 lines
    ================================================================================
    
    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvtag.py   | Total Lines: 379
    ================================================================================

    IMPORTS:
    - import csv
    - import textwrap
    - from pathlib import Path
    - import docutils.parsers.rst.tableparser
    - import sympy as sp
    - import tabulate
    - from fastcore.utils import store_attr
    - from numpy import *
    - from sympy.abc import _clash2

    CLASSES & METHODS:
        Class: Tag (365 lines total)
        └─ Method: __init__() -> 23 lines
        └─ Method: taglx() -> 160 lines
        └─ Method: tagbx() -> 147 lines
        └─ Method: parse_simple_rst_table() -> 24 lines

    TOP-LEVEL FUNCTIONS:
    ================================================================================

    ================================================================================
    Module Name: C:\git\rivtlib-git\src\rivtlib\rvtext.py   | Total Lines: 266
    ================================================================================

    IMPORTS:
    - import ast
    - import io
    - import sys
    - import textwrap
    - from pathlib import Path
    - from docutils.core import publish_parts

    CLASSES & METHODS:

    TOP-LEVEL FUNCTIONS:
    - build_transcript() -> 67 lines
    - format_text() -> 166 lines
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


