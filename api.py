#! python
"""rivt API
API is implemented with :

    import rivtlib.api as rv

API functions :

    rv.R(sS) - (Run) Execute shell scripts
    rv.I(sS) - (Insert) Insert static text, math, images and tables
    rv.V(sS) - (Values) Evaluate values and equations
    rv.T(sS) - (Tools) Execute Python functions and scripts
    rv.W(sS) - (Write) Write formatted documents
    rv.S(sS) - (Skip) Skip string processing of that string

where sS is a triple quoted, indented, utf-8 section string. This rivtlib code
base uses the last letter of a variable name to indicate the variable types as
follows:

Variable type suffix:

    A = array
    B = boolean
    C = class instance
    D = dictionary
    F = float
    I = integer
    L = list
    N = file name only
    P = path
    S = string
"""

import fnmatch
import os
import sys
import logging
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path

import __main__
from rivtlib import log_check, parse, rwrite
from rivtlib.units import *  # noqa: F403

# get rivt file and path
rivtP = Path(os.getcwd())
rivtnS = "not found"
projP = Path(os.path.dirname(rivtP))

if __name__ == "rivtlib.api":
    rivtP = Path(__main__.__file__)
    rivtnS = rivtP.name
    patternS = "r[0-9][0-9][0-9]0-9]-*.py"
    if fnmatch.fnmatch(rivtnS, patternS):
        rivtfP = Path(rivtP, rivtnS)
else:
    print(f"""The rivt file name is - {rivtnS} -. The file name pattern must""")
    print("""match "rddss-anyname.py", where dd and ss are two-digit integer""")
    sys.exit()

# initialize logging
modnameS = __name__.split(".")[1]
log_check.log_bak(rivtfP, modnameS, folderD)

# print(f"{rivtfP=}")
# print(f"{rivtN=}")
# print(f"{__name__=}")
# print(f"{modnameS=}")

# output strings
rstS = """"""  # cumulative rest string
utfS = """"""  # cumulative utf string
xtfS = """"""  # cumulative tex string
srstS = """"""  # reSt section string
sutfS = """"""  # utf section string
xrstS = """"""  # reSt-tex section string

# write backup doc file
with open(rivtfP, "r") as f2:
    rivtS = f2.read()
with open(folderD["bakP"], "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup: [{bakshortP}]""")
print(" ")


def doc_hdr():
    # init file - (headings and doc overrides)

    hdutfS = ""
    hdrstS = ""
    hdrxtS = ""

    timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")

    config = ConfigParser()
    config.read(Path(projP, "rivt-doc.ini"))
    headS = config.get("report", "title")
    footS = config.get("utf", "foot1")

    titleL = rivtnS.split("-")[1]  # subdivision title
    titleS = titleL[1].split(".")[0]
    titleS = titleS.title()
    borderS = "=" * 80

    dnumS = (titleL[0].split("r"))[1]
    hdutfS = timeS + "\n" + headS + "\n" + borderS + "\n"
    utfS += hdutfS + "\n"

    utfS += sutfS  # accumulate doc strings
    rstS += srstS
    xtfS += xrstS

    return utfS, rstS, xstS


def doc_parse(sS, tS, tagL, cmdL):
    """
    parses section strings to doc strings

    Globals:
        utfS (str): utf doc string
        rstS (str): rst2pdf doc string
        xstS (str): latex doc string
        labelD (dict): formatting labels
        folderD (dict): folder and file paths
        rivtD (dict): calculated values

    Args:
        sS (str): rivt section
        tS (str): section type (R,I,V,T,W,S)

    Calls:
        RivtParse (class)
        parse_sec (method)

    Returns:
        utfS (str): utf output
        rstS (str): reSt output
    """

    global utfS, rstS, xstS, folderD, labelD, rivtD

    sL = sS.split("\n")  # convert section to list
    secC = parse.Section(tS, sL, labelD)
    sutfS, srstS, sxstS, folderD, labelD, rivtD = secC.section(
        tagL, cmdL, folderD, labelD, rivtD
    )
    utfS += sutfS  # accumulate doc strings
    rstS += srstS
    xstS += sxstS

    return utfS, rstS, xstS


def R(sS):
    """convert Run string

    Args:
        sS (str): section string
    """

    global utfS, rstS, xstS, folderD, labelD, rivtD

    cmdL = ["IMG"]
    tagL = ["E]"]

    utfS, rstS, xstS = doc_parse(sS, "R", tagL, cmdL)


def I(sS):  # noqa: E743
    """convert Insert string

    Args:
        sS (str): section string
    """

    global utfS, rstS, xstS, folderD, labelD, rivtD

    cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
    tag1 = ["#]", "C]", "D]", "E]", "F]", "S]", "L]", "T]", "H]", "P]", "U]"]
    tag2 = ["B]]", "C]]", "I]]", "L]]", "X]]"]
    tagL = tag1 + tag2

    utfS, rstS, xstS = doc_parse(sS, "I", tagL, cmdL)


def V(sS):
    """convert Value string

    Args:
        sS (str): section string
    """

    global utfS, rstS, xstS, folderD, labelD, rivtD

    cmdL = ["IMG", "IMG2", "VALUES"]
    tagL = ["E]", "F]", "S]", "Y]", "T]", "H]", "P]", ":=", "[V]]"]

    utfS, rstS, xstS = doc_parse(sS, "V", tagL, cmdL)


def T(sS):
    """convert Tools string

    Args:
        sS (str): section string
    """

    global utfS, rstS, xstS, folderD, labelD, rivtD

    cmdL = ["IMG"]
    tagL = ["E]"]

    utfS, rstS, xstS = doc_parse(sS, "T", tagL, cmdL)


def S(sS):
    """skip section string - no processing

    Args:
        sS (str): section string
    """

    shL = sS.split("|")
    print("\n Section skipped: " + shL[0] + "\n")


def W(sS):
    """write doc files

    Args:
        sS (str): section string
    """
    global utfS, rstS, xsts, folderD, labelD, rivtD

    rivtL = rivtS.split("\n")
    # 1. remove W function write that rivt temp file and execute
    # 2. execute rest of file and process doc temp files through W commands
    for lS in rivtL:
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
                if typeS == "pdf":
                    rfrontS = docC.frontpg(tocS, tcovS, tcontS, tmainS)
                    rstS = rfrontS + "\n" + rstS
                    with open(txtP, "w", encoding="utf-8") as file:
                        file.write(utfS)
                    with open(sStP, "w", encoding="utf-8") as file:
                        file.write(rstS)
                    msgS = docC.docpdf2(pthS, styleS)
                elif typeS == "pdfx":
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
        else:
            pass

    print("\n" + f"{msgS=}")
    sys.exit()
