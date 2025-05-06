#! python
"""rivt API
The API is intialized with

    import rivtlib.api as rv

The API functions are:

    rv.R(sS) - (Run) Execute shell scripts
    rv.I(sS) - (Insert) Insert static text, math, images and tables
    rv.V(sS) - (Values) Evaluate values and equations
    rv.T(sS) - (Tools) Execute Python functions and scripts
    rv.W(sS) - (Write) Write formatted documents
    rv.S(sS) - (Skip) Skip string processing of that string

where sS is a triple quoted, indented, utf-8 string. This rivtlib code base uses
the last letter of a variable name to indicate the variable types as follows:

Variable type suffix:

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
    print(f"- The rivt file name is - {rivtN} -. The file name must match the")
    print("""- pattern "rddss-anyname.py" , where dd and ss are two-digit integer""")
    sys.exit()

# initialize logging
modnameS = __name__.split(".")[1]
log_check.log_bak(rivtFP, modnameS, folderD)

# print(f"{rivtFP=}")
# print(f"{rivN=}")
# print(f"{__name__=}")
# print(f"{modnameS=}")

# initialize strings
rstS = """"""  # cumulative rest string
utfS = """"""  # cumulative utf string
xrstS = """"""  # api function string - rest
xutfS = """"""  # api function string - utf
timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")
titleL = rivtN.split("-")  # subdivision title
titleS = titleL[1].split(".")[0]
titleS = titleS.title()
dnumS = (titleL[0].split("r"))[1]
headS = "[" + dnumS + "]  " + titleS.strip()
bordsS = labelD["widthI"] * "="
time1S = timeS.rjust(labelD["widthI"])
# read init file - for doc overrides
config = ConfigParser()
config.read(Path(folderD["projP"], "rivt-doc.ini"))
headS = config.get("report", "title")
footS = config.get("utf", "foot1")
# subdivision heading - for stdoout
hdutfS = time1S + "\n" + headS + "\n" + bordsS + "\n"
utfS += hdutfS + "\n"
# print(hdutfS)


def rivt_parse(sS, tS):
    """
    parse section strings to doc strings and accumulate

    Globals:
        utfS (str): utf doc
        rStS (str): reSt doc
        labelD (dict): labels for formatting
        folderD (dict): folder and file paths
        rivtvD (dict): calculation values
        rivtpD (dict): printing parameters

    Args:
        sS (str): rivt section
        tS (str): section type (R,I,V,T,W or S)

    Calls:
        RivtParse (class)
        parse_sec (method)

    Returns:
        utfS (str): utf output
        rstS (str): reSt output
    """

    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    rL = sS.split("\n")
    parseC = parse.RivtParse(tS)
    xutfS, xrstS, folderD, labelD, rivtpD, rivtvD = parseC.parse_sec(
        rL, folderD, labelD, rivtpD, rivtvD
    )
    # accumulate doc strings
    utfS += xutfS
    rstS += xrstS

    return utfS, rstS


def R(sS):
    """
    process Run string

    Args:
        sS (str): section string
    """

    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(sS, "R")


def I(sS):
    """
    format Insert string

    Args:
        sS (str): section string
    """

    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(sS, "I")


def V(sS):
    """
    format Value string

    Args:
        sS (str): section string
    """

    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(sS, "V")


def T(sS):
    """
    process Tools string

    Args:
        sS (str): section string
    """

    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    utfS, rstS = rivt_parse(sS, "T")


def W(sS):
    """
    write output files

    Args:
        sS (str): section string
    """
    global utfS, rstS, folderD, labelD, rivtpD, rivtvD

    sSL = sS.split("\n")
    for lS in sSL:
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
            pasS = cL[2].strip()

            # sStP = Path(folderD["rivP"], "temp", folderD["sStN"])
            # pdf2P = Path(folderD["tempP"], folderD["pdfN"])

            # print(f"{sStP=}")
            # print(f"{cmdS=}")
            # print(f"{pthS=}")
            # print(f"{pasS=}")

            msgS = "end of file "
            if cmdS == "APPEND":
                pass
            elif cmdS == "PREPEND":
                pass
            elif cmdS == "COVER":
                titleS = pthS
                subS = pasS
                botS = cL[3].strip()
                imgS = cL[4].strip()
                docC = rwrite.CmdW(folderD, labelD)
                tcovS, tcontS, tmainS = docC.frontvar(titleS, subS, botS, imgS)
                # print(tcovS, tcontS, tmainS)
            elif cmdS == "DOC":
                parL = pasS.split(",")
                typeS = parL[0].strip()
                tocS = parL[1].strip()
                styleS = parL[2].strip()
                txtP = Path(folderD["docsP"], "text", folderD["txtN"])
                sStP = Path(folderD["tempP"], folderD["sStN"])
                docC = rwrite.CmdW(folderD, labelD)
                if typeS == "pdf2":
                    rfrontS = docC.frontpg(tocS, tcovS, tcontS, tmainS)
                    rstS = rfrontS + "\n" + rstS
                    with open(txtP, "w", encoding="utf-8") as file:
                        file.write(utfS)
                    with open(sStP, "w", encoding="utf-8") as file:
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
                elif parL[0].strip() == "sStpdf":
                    rfrontS = docC.coverpg(parL[1].strip(), parL[2].strip())
                    msgS = docC.reportpdf()
                elif parL[0].strip() == "sSthtml":
                    rfrontS = docC.coverpg(parL[1].strip(), parL[2].strip())
                    msgS = docC.reporthtml()
                else:
                    pass
        else:
            pass

    print("\n" + f"{msgS=}")
    sys.exit()


def S(sS):
    """skip section string - no processing

    Args:
        sS (str): section string
    """

    rL = sS.split("|")
    print("\n Section skipped: " + rL[0] + "\n")
