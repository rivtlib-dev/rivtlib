#! python
"""rivt API
API implemented with :

import rivtlib.rapi as rv

API functions:
    rv.R(sS) - (Run) Execute shell scripts
    rv.I(sS) - (Insert) Insert static text, math, images and tables
    rv.V(sS) - (Values) Evaluate values and equations
    rv.T(sS) - (Tools) Execute Python functions and scripts
    rv.W(sS) - (Write) Write formatted documents
    rv.S(sS) - (Skip) Skip string processing of that string

Globals:
    utfS (str): utf doc string
    rstS (str): rst2pdf doc string
    xstS (str): latex doc string
    labelD (dict): formatting labels
    folderD (dict): folder and file paths
    rivtD (dict): calculated values

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

import sys
import logging
from datetime import datetime
from pathlib import Path

from rivtlib import rcheck, rparse, rwrite
from rivtlib.rparam import *  # noqa: F403
from rivtlib.runits import *  # noqa: F403

logging.info(f"""rivt file : {folderD["rivtnS"]}""")
logging.info(f"""rivt path : {folderD["rivtP"]}""")


def doc_hdr():
    """_summary_

    Returns:
        _type_: _description_
    """
    # init file - (headings and doc overrides)

    dutfS = ""
    drs2S = ""
    drstS = ""

    # config = ConfigParser()
    # config.read(Path(projP, "rivt-doc.ini"))
    # headS = config.get("report", "title")
    # footS = config.get("utf", "foot1")

    titleL = rivtnS.split("-")  # subdivision title
    titleS = titleL[1].split(".")[0]
    dnumS = titleL[0].split("r")[1]
    headS = dnumS + "   " + titleS

    timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")
    borderS = "=" * 80
    dutfS = "\n\n" + timeS + "   " + headS + "\n" + borderS + "\n"

    print(dutfS)  # STDOOUT doc heading
    dutfS = dutfS  # accumulate doc strings
    drs2S = dutfS
    drstS = dutfS

    return dutfS, drs2S, drstS


def doc_parse(sS, tS, tagL, cmdL):
    """
    parses section strings to doc strings

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

    global dutfS, drs2S, drstS, folderD, labelD, rivtD

    sL = sS.split("\n")
    secC = rparse.Section(tS, sL, folderD, labelD, rivtD)
    sutfS, srs2S, srstS, folderD, labelD, rivtD, rivtL = secC.section(tagL, cmdL)

    # accumulate doc strings
    dutfS += sutfS
    drs2S += srs2S
    drstS += srstS

    return dutfS, drs2S, drstS, rivtL


def rivt_bak(rivtfP):
    """write rivt backup file"""
    with open(rivtfP, "r") as f2:
        rivtS = f2.read()
    with open(folderD["bakfP"], "w") as f3:
        f3.write(rivtS)
    logging.info(f"""rivt backup : {folderD["bakfP"]}""")


rivt_bak(rivtfP)  # rivt backup file


dutfS, drs2S, drstS = doc_hdr()  # doc header


def R(sS):
    """convert Run string

    Args:
        sS (str): section string
    """

    global dutfS, drs2S, drstS, folderD, labelD, rivtD


def I(sS):  # noqa: E743
    """convert Insert string

    Args:
        sS (str): section string
    """

    global dutfS, drs2S, drstS, folderD, labelD, rivtD

    cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
    tag1 = ["#]", "C]", "D]", "E]", "F]", "S]", "L]", "T]", "H]", "P]", "U]"]
    tag2 = ["B]]", "C]]", "I]]", "L]]", "X]]"]
    tagL = tag1 + tag2

    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "I", tagL, cmdL)


def V(sS):
    """convert Value string

    Args:
        sS (str): section string
    """

    global dutfS, drs2S, drstS, folderD, labelD, rivtD

    cmdL = ["IMG", "IMG2", "VALUE"]
    tagL = ["E]", "F]", "S]", "Y]", "T]", "H]", "P]", ":=", "[V]]"]

    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "V", tagL, cmdL)

    fileS = folderD["valnS"] + "-" + str(labelD["secnumI"]) + ".csv"
    fileP = Path(folderD["valP"], fileS)
    with open(fileP, "w") as file1:
        file1.write("\n".join(rivtL))


def T(sS):
    """convert Tools string

    Args:
        sS (str): section string
    """

    global dutfS, drs2S, drstS, folderD, labelD, rivtD


def S(sS):
    """skip section string - no processing

    Args:
        sS (str): section string
    """

    shL = sS.split("|")
    print("\n[" + shL[0] + "] : section skipped " + "\n")


def W(sS):
    """write doc files

    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD

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
