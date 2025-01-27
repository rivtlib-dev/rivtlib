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

import logging
import warnings
from configparser import ConfigParser
from pathlib import Path

from rivtlib import parse
from rivtlib.folders import *

# from rivtlib import write

# read config file
config = ConfigParser()
config.read(Path(projP, "rivt-config.ini"))
headS = config.get('report', 'title')
footS = config.get('utf', 'foot1')

modnameS = __name__.split(".")[1]
# print(f"{modnameS=}")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS +
    "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogP,
    filemode="w",
)
warnings.filterwarnings("ignore")
# warnings.simplefilter(action="ignore", category=FutureWarning)


def rivt_parse(rS, tS):
    """parse rivt string and print doc text

    Globals:
        utfS (str): accumulating utf text string 
        rstS (str): acculating restr text string
        labelD (dict): label dictionary
        folderD (dict): folder dictionary
        rivtD (dict): rivt values dictionary 

    Args:
        tS (str): section type R,I,V,T,W or X
        rS (str): rivt string
    """
    global utfS, rstS, labelD, folderD, rivtD
    rL = rS.split("\n")

    # pass header and initialize class
    parseC = parse.RivtParse(rL[0], tS, folderD, labelD,  rivtD)

    # parse section string
    xutfS, xrstS, labelD, folderD, rivtD = parseC.str_parse(rL[1:])

    # print doc text
    print(xutfS)

    # accumulate output strings
    utfS += xutfS
    rstS += xrstS


def R(rS):
    """process Run string

    Globals:
        utfS
        rstS
        labelD (dict): label dictionary
        folderD: folder dictionary
        rivtD: rivt values dictionary 

        Args:
            rS (str): rivt string - run 
    """
    global utfS, rstS, labelD, folderD, rivtD
    rivt_parse(rS, "R")


def I(rS):
    """format Insert string

        : param rS: rivt string - insert 
    """
    global utfS, rstS, labelD, folderD
    rivt_parse(rS, "I")


def V(rS):
    """format Value string

        :param rS: rivt string - value
    """
    global utfS, rstS, labelD, folderD, rivtD
    locals().update(rivtD)
    rivt_parse(rS, "V")
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
