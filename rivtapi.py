#! python
"""rivt API

import rivtlib.rivtapi as rv 

rv.R(rS) - (Run) Execute shell scripts 
rv.I(rS) - (Insert) Insert static text, math, images and tables
rv.V(rS) - (Values) Evaluate values and equations 
rv.T(rS) - (Tools) Execute Python functions and scripts 
rv.X(rS) - (eXclude) Skip string processing 
rv.W(rS) - (Write) Write formatted documents 

where rS is a triple quoted Python rivt-string 

Note: In the rivtlib code base variable types are identified by the last letter
of the variable name using the following convention:

A = array
B = boolean
C = class instance
D = dictionary
F = float
I = integer
L = list
P = path
S = string
"""

import __main__
import fnmatch
import logging
import os
import shutil
import sys
import time
import warnings
import IPython
from pathlib import Path
from configparser import ConfigParser
from pathlib import Path
from datetime import datetime, time

from rivtlib import parse
from rivtlib import folders

warnings.simplefilter(action="ignore", category=FutureWarning)

# rivt file path
curP = Path(os.getcwd())
if __name__ == "rivtlib.rivtapi":
    argfileS = Path(__main__.__file__)
    rivS = argfileS.name
    print(f"{argfileS=}")
    if fnmatch.fnmatch(rivS, "riv????-*.py"):
        rivP = Path(curP, rivS)
        print(f"{rivS=}")
        print(f"{curP=}")
    else:
        print(f"INFO     rivt file - {rivS}")
        print(f"INFO     The name must match 'rivddss-filename.py' where")
        print(f"INFO     dd and ss are two digit integers")
        sys.exit()
else:
    print(f"INFO  file path does not include a rivt file  - {curP}")
    sys.exit()

# initialize global variables
rstS = utfS = """"""  # rst and utf output strings
labelD = folderD = rivtD = {}  # label, folder and rivt dictionaries


def rivt_parse(mS, rS):
    """call parsing class for specified API function

    :param mS: rivt string method - R,I,V,T or X
    :param rS: rivt string
    :param utfS: utf output string
    :param rstS: rst output string
    :param labelD: label dictionary
    :param folderD: folder dictionary
    :param rivtD: rivt values dictionary      
    """

    global utfS, rstS, labelD, folderD, rivtD

    rL = rS.split()
    parseC = parse.RivtParse(mS, rL[0], folderD, labelD,  rivtD)
    xutfS, xrstS, labelD, folderD, rivtD = parseC.str_parse(rL[1:])

    # accumulate processed strings
    utfS += xutfS
    rstS += xrstS


def R(rS):
    """process Run string

        : param rS: run string
    """
    global utfS, rstS, labelD, folderD

    rivt_parse("R", rS)


def I(rS):
    """format Insert string

        : param rS: insert string
    """
    global utfS, rstS, labelD, folderD

    rivt_parse("I", rS)


def V(rS):
    """format Value string

        :param rS: value string
    """
    global utfS, rstS, labelD, folderD, rivtD

    locals().update(rivtD)
    rivt_parse("V", rS)
    rivtD.update(locals())


def T(rS):
    """process Tools string

        : param rS: tool string
    """

    locals().update(rivtD)
    rivt_parse("T", rS)
    rivtD.update(locals())


def W(rS):
    """write output files

    :param rS: write string
    """
    pass


def X(rS):
    """skip string - do not format
    """

    rL = rS.split("\n")
    print("\n skip section: " + rL[0] + "\n")
    pass
