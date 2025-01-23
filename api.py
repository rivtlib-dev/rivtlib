#! python
"""rivt API


rv.R(rS) - (Run) Execute shell scripts 
rv.I(rS) - (Insert) Insert static text, math, images and tables
rv.V(rS) - (Values) Evaluate values and equations 
rv.T(rS) - (Tools) Execute Python functions and scripts 
rv.W(rS) - (Write) Write formatted documents 
rv.X(rS) - (eXclude) Skip string processing 

The API is intialized with 

             import rivtlib.api as rv 

and rS is a triple quoted utf-8 string. The rivtlib code base uses variable
types identified with the last letter of a variable name:

A = array
B = boolean
C = class instance
D = dictionary
F = float
I = integer
L = list
N = file name
P = path
S = string
"""

import fnmatch
import logging
import os
import shutil
import sys
import time
import warnings
import IPython
from pathlib import Path
from datetime import datetime, time
from rivtlib import folders
from rivtlib import parse
# from rivtlib import write

rstS = utfS = """"""  # initialize rst and utf doc strings
labelD = folderD = rivtD = {}  # initialize dictionaries
warnings.simplefilter(action="ignore", category=FutureWarning)


def rivt_parse(tS, rS):
    """call parsing class with specified API function

    Globals:
        utfS
        rstS
        labelD (dict): label dictionary
        folderD: folder dictionary
        rivtD: rivt values dictionary 

    Args:
        tS (str): section type R,I,V,T,W or X
        rS (str): rivt string
    """
    global utfS, rstS, labelD, folderD, rivtD
    rL = rS.split("\n")
    # parse header string
    parseC = parse.RivtParse(rL[0], tS, folderD, labelD,  rivtD)
    # parse section string
    xutfS, xrstS, labelD, folderD, rivtD = parseC.str_parse(rL[1:])
    print(xutfS)
    utfS += xutfS  # accumulate utf output strings
    rstS += xrstS  # accumulate rst output strings


def R(rS):
    """process Run string

        Args:
            rS (str): rivt string - run 
    """
    global utfS, rstS, labelD, folderD
    rivt_parse("R", rS)


def I(rS):
    """format Insert string

        : param rS: rivt string - insert 
    """
    global utfS, rstS, labelD, folderD
    rivt_parse("I", rS)


def V(rS):
    """format Value string

        :param rS: rivt string - value
    """
    global utfS, rstS, labelD, folderD, rivtD
    locals().update(rivtD)
    rivt_parse("V", rS)
    rivtD.update(locals())


def T(rS):
    """process Tools string

        : param rS: rivt string - tools
    """
    global utfS, rstS, labelD, folderD, rivtD
    locals().update(rivtD)
    rivt_parse("T", rS)
    rivtD.update(locals())


def W(rS):
    """write output files

    :param rS: rivt string - write 
    """
    pass


def X(rS):
    """skip rivt string - do not process or format
    """

    rL = rS.split("\n")
    print("\n X func - skip section: " + rL[0] + "\n")
