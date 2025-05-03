#! python
"""rivt API
The API is intialized with

    import rivtlib.api as rv

API Functions:

    rv.R(rS) - (Run) Execute shell scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) Execute Python functions and scripts
    rv.W(rS) - (Write) Write formatted documents
    rv.S(rS) - (Skip) Skip string processing of that string

where rS is a triple quoted, indented, utf-8 string. This rivtlib code base uses
the last letter of a variable name to indicate the variable types as follows:

A = array
B = boolean
C = class instance
D = dictionary
F = float
I = integer
L = list
N = file name only
P = file path only (abs or rel)
PF = path and file name
S = string
"""

import fnmatch
import os
import sys
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path

import __main__
from rivtlib import log_check, params, parse, rwrite
from rivtlib.units import *  # noqa: F403

global utfS, rstS, folderD, labelD, rivtpD, rivtvD

rivtP = Path(os.getcwd())
rivtN = "not found"
if __name__ == "rivtlib.api":
    rivtP = Path(__main__.__file__)
    rivtN = rivtP.name
    patternS = "r[0-9][0-9][0-9]0-9]-*.py"
    if fnmatch.fnmatch(rivtN, patternS):
        rivtFP = Path(rivtP, rivtN)
        folderD, labelD, rivtpD, rivtvD = params.dicts(rivtN, rivtP, rivtFP)
else:
    print(f"-  The rivt file name is !! {rivtN} !!. The file name must match the")
    print("""-   pattern"rddss-anyname.py , where dd and ss are two-digit integers""")
    sys.exit()

# print(f"{rivtP=}")
# print(f"{rivP=}")
# print(f"{rivN=}")
# print(f"{__name__=}")

# initialize logging
modnameS = __name__.split(".")[1]
# print(f"{modnameS=}")
log_check.log_rivt(rivtP, modnameS, folderD)

# read doc init file
config = ConfigParser()
config.read(Path(folderD["projP"], "rivt-doc.ini"))
headS = config.get("report", "title")
footS = config.get("utf", "foot1")

# initialize strings, config
rstS = """"""
utfS = """"""
xrstS = """"""
xutfS = """"""
timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")
titleL = rivtN.split("-")  # subdivision title
titleS = titleL[1].split(".")[0]
titleS = titleS.title()
dnumS = (titleL[0].split("r"))[1]
headS = "[" + dnumS + "]  " + titleS.strip()
bordrS = labelD["widthI"] * "="
time1S = timeS.rjust(labelD["widthI"])
hdutfS = time1S + "\n" + headS + "\n" + bordrS + "\n"
# stdout subdivision heading
print(hdutfS)
utfS += hdutfS + "\n"


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
        rL, folderD, labelD, rivtpD, rivtvD
    )
    utfS += xutfS  # accumulate output strings
    rstS += xrstS
    return utfS, rstS


def R(rS):
    """process Run string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "R")


def I(rS):
    """format Insert string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "I")


def V(rS):
    """format Value string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "V")


def T(rS):
    """process Tools string

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(rS, "T")


def W(rS):
    """write output files

    Args:
        rS (str): rivt string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    rsL = rS.split("\n")
    for lS in rsL:
        cmdS = ""
        # print(f"{lS[:2]=}")
        if len(lS) == 0:
            continue
        if lS[0] == "#":
            continue
        elif lS[:2] == "||":
            cL = lS[2:].split("|")
            # print(cL)
            cmdS = cL[0].strip()
            pthS = cL[1].strip()
            parS = cL[2].strip()

            # rstP = Path(folderD["rivP"], "temp", folderD["rstN"])
            # pdf2P = Path(folderD["tempP"], folderD["pdfN"])

            # print(f"{rstP=}")
            # print(f"{cmdS=}")
            # print(f"{pthS=}")
            # print(f"{parS=}")

            msgS = "end of file "
            if cmdS == "APPEND":
                pass
            elif cmdS == "PREPEND":
                pass
            elif cmdS == "COVER":
                titleS = pthS
                subS = parS
                botS = cL[3].strip()
                imgS = cL[4].strip()
                docC = rwrite.CmdW(folderD, labelD)
                tcovS, tcontS, tmainS = docC.frontvar(titleS, subS, botS, imgS)
                # print(tcovS, tcontS, tmainS)
            elif cmdS == "DOC":
                parL = parS.split(",")
                typeS = parL[0].strip()
                tocS = parL[1].strip()
                styleS = parL[2].strip()
                txtP = Path(folderD["docsP"], "text", folderD["txtN"])
                rstP = Path(folderD["tempP"], folderD["rstN"])
                docC = rwrite.CmdW(folderD, labelD)
                if typeS == "pdf2":
                    rfrontS = docC.frontpg(tocS, tcovS, tcontS, tmainS)
                    rstS = rfrontS + "\n" + rstS
                    with open(txtP, "w", encoding="utf-8") as file:
                        file.write(utfS)
                    with open(rstP, "w", encoding="utf-8") as file:
                        file.write(rstS)
                    msgS = docC.docpdf2(pthS, styleS)
                elif typeS == "pdf":
                    rfrontS = docC.coverpg(tocS)
                    msgS = docC.docpdf()
                elif typeS == "html":
                    rfrontS = docC.coverpg(tocS)
                    msgS = docC.dochtml()
                elif typeS == "text":
                    rfrontS = docC.coverpg(tocS)
                    msgS = docC.doctext()
                else:
                    pass
                tcovS = " "
                tcontS = " "
                tmainS = " "
                rfrontS = " "
                # print(f"{rfrontS=}")
            elif cmdS == "REPORT":
                if typeS == "pdf2":
                    rfrontS = docC.coverpg(parL[1].strip(), parL[2].strip())
                    msgS = docC.reportpdf2()
                elif parL[0].strip() == "rstpdf":
                    rfrontS = docC.coverpg(parL[1].strip(), parL[2].strip())
                    msgS = docC.reportpdf()
                elif parL[0].strip() == "rsthtml":
                    rfrontS = docC.coverpg(parL[1].strip(), parL[2].strip())
                    msgS = docC.reporthtml()
                else:
                    pass
        else:
            pass

    print("\n" + f"{msgS=}")
    sys.exit()


def S(rS):
    """skip rivt string - no processing

    Args:
        rS (str): rivt string
    """

    rL = rS.split("|")
    print("\n Section skipped: " + rL[0] + "\n")
