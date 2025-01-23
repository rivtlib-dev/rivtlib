#! python
"""rivt API

import rivtlib.api as rv 

rS is a triple quoted utf-8 string 
rv.R(rS) - (Run) Execute shell scripts 
rv.I(rS) - (Insert) Insert static text, math, images and tables
rv.V(rS) - (Values) Evaluate values and equations 
rv.T(rS) - (Tools) Execute Python functions and scripts 
rv.W(rS) - (Write) Write formatted documents 
rv.X(rS) - (eXclude) Skip string processing 

The rivtlib code base uses variable types identified by the last letter
of the variable name:

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
from pathlib import Path
from datetime import datetime, time
from rivtlib import folders
from rivtlib import parse


warnings.simplefilter(action="ignore", category=FutureWarning)
rstS = utfS = """"""  # initialize rst and utf output strings
labelD = folderD = rivtD = {}  # initialize label, folder and rivt dictionaries


def rivt_parse(mS, rS):
    """call parsing class for specified API function

    :param mS: rivt string method - R,I,V,T,W or X
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
    utfS += xutfS  # accumulate utf output strings
    rstS += xrstS  # accumulate rst output strings


def R(rS):
    """process Run string

        : param rS: rivt string - run 
    """
    global utfS, rstS, labelD, folderD
    rivttxt = rivt_parse("R", rS)
    print(rivttxt)


def I(rS):
    """format Insert string

        : param rS: rivt string - insert 
    """
    global utfS, rstS, labelD, folderD
    rivttxt = rivt_parse("I", rS)
    print(rivttxt)


def V(rS):
    """format Value string

        :param rS: rivt string - value
    """
    global utfS, rstS, labelD, folderD, rivtD
    locals().update(rivtD)
    rivttxt = rivt_parse("V", rS)
    rivtD.update(locals())
    print(rivttxt)


def T(rS):
    """process Tools string

        : param rS: rivt string - tools
    """
    global utfS, rstS, labelD, folderD, rivtD
    locals().update(rivtD)
    rvttxt = rivt_parse("T", rS)
    rivtD.update(locals())
    print(rivttxt)


def W(rS):
    """write output files

    :param rS: write string
    """
    rivt_parse("W", rS)


def X(rS):
    """skip string - do not format
    """

    rL = rS.split("\n")
    print("\n skip section: " + rL[0] + "\n")
    pass
