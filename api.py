#! python
""" rivt API
The API is intialized with

    import rivtlib.api as rv

API Functions:

    rv.R(rS) - (Run) Execute shell scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) Execute Python functions and scripts
    rv.X(rS) - (eXclude) Skip string processing
    rv.W(rS) - (Write) Write formatted documents
    rv.Q(rS) - (Quit) Exit rivt processing

where rS is a triple quoted utf-8 string. The rivtlib code base uses
variable types identified with the last letter of a variable name:

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

import __main__
from pathlib import Path
from datetime import datetime, time
from configparser import ConfigParser
import warnings
import os
import logging
import fnmatch
import sys
from rivtlib.units import *
from rivtlib import params, parse, write

# from rivtlib import write

global utfS, rstS, folderD, labelD, rivtpD, rivtvD

curP = Path(os.getcwd())
rivP = curP
if __name__ == "rivtlib.api":
    rivtP = Path(__main__.__file__)
    rivN = rivtP.name
    if fnmatch.fnmatch(rivN, "r????-*.py"):
        rivtP = Path(rivP, rivN)
        folderD, labelD, rivtpD, rivtvD = params.dicts(rivN, rivP, rivtP)
else:
    print(f"INFO     rivt file - {rivN}")
    print(f"INFO     The name must match 'rddss-filename.py' where")
    print(f"INFO     dd and ss are two digit integers")
    sys.exit()

# print(f"{rivtP=}")
# print(f"{curP=}")
# print(f"{rivN=}")
# print(f"{__name__=}")

# initialize logging
modnameS = __name__.split(".")[1]
# print(f"{modnameS=}")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS +
    "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=folderD["errlogP"],
    filemode="w",
)
warnings.filterwarnings("ignore")
# warnings.simplefilter(action="ignore", category=FutureWarning)

# read init file
config = ConfigParser()
config.read(Path(folderD["projP"], "rivt-config.ini"))
headS = config.get('report', 'title')
footS = config.get('utf', 'foot1')

# initialize strings, config
rstS = """"""
utfS = """"""
xrstS = """"""
xutfS = """"""
timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")
titleL = rivN.split("-")                           # subdivision title
titleS = titleL[1].split(".")[0]
titleS = titleS.title()
dnumS = (titleL[0].split('r'))[1]
headS = "[" + dnumS + "]  " + titleS.strip()
bordrS = labelD["widthI"] * "="
hdutfS = "\n" + headS + "\n" + bordrS + "\n" + timeS
hdrstS = "\n" + headS + "\n" + bordrS + "\n" + timeS
hdrstS = hdrstS + "\n\n\n" + ".. contents::" + "\n\n\n"
print(hdutfS)                                      # stdout subdivision heading
utfS += hdutfS + "\n"
rstS += hdrstS + "\n"


def rivt_parse(rS, tS):
    """parse and accumulate a rivt string

    Globals:
        utfS (str): accumulated utf text string
        rstS (str): accumulated reSt text string
        labelD (dict): labels
        folderD (dict): folders
        rivtD (dict): values

    Args:
        rS (str): rivt string
        tS (str): section type is R,I,V,T,W or X

    Calls:
        RivtParse (class)
        parse_str (method)

    Returns:
        None
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    rL = rS.split("\n")
    parseC = parse.RivtParse(tS)
    xutfS, xrstS, folderD, labelD, rivtpD, rivtvD = parseC.parse_str(
        rL, folderD, labelD, rivtpD, rivtvD)

    if tS == "W":
        return utfS, rstS, xutfS
    else:
        utfS += xutfS       # accumulate output strings
        rstS += xrstS
        return utfS, rstS


def R(rS):
    """ process Run string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "R")


def I(rS):
    """ format Insert string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "I")


def V(rS):
    """ format Value string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "V")


def T(rS):
    """ process Tools string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "T")


def W(rS):
    """ write output files

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    txtP = Path(folderD["tempP"], folderD["txtN"])
    rstP = Path(folderD["tempP"], folderD["rstpN"])
    pdfP = Path(folderD["tempP"], folderD["pdfN"])

    utfS, rstS, msgS = rivt_parse(rS, "W")

    with open(txtP, 'w', encoding="utf-8") as file:
        file.write(utfS)
    with open(rstP, 'w', encoding="utf-8") as file:
        file.write(rstS)

    print("-"*labelD["widthI"])
    print(msgS)
    print("file written: " + str(txtP))
    print("file written: " + str(rstP))
    print("file written: " + str(pdfP))

    sys.exit()


def X(rS):
    """ skip rivt string - no processing

    Args:
        rS (str): rivt string
    """

    rL = rS.split("|")
    print("\n X func - section skipped: " + rL[0] + "\n")


def Q():

    print("<<<<< exit rivtlib >>>>>")
    sys.exit()
