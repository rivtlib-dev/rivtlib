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

from rivtlib import rparse, rwrite
from rivtlib.rparam import *  # noqa: F403
from rivtlib.runits import *  # noqa: F403

logging.info(f"""rivt file : {folderD["rivtnS"]}""")
logging.info(f"""rivt path : {folderD["rivtP"]}""")

with open(rivtfP, "r") as f2:  # noqa: F405
    rivtS = f2.read()
with open(folderD["bakfP"], "w") as f3:  # noqa: F405
    f3.write(rivtS)
logging.info(f"""rivt backup : {folderD["bakfP"]}""")  # noqa: F405


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
    section strings to doc strings

    Args:
        sS (str): rivt section
        tS (str): section type (R,I,V,T,W,S)

    Calls:
        Section (class), section (method)

    Returns:
        sutfS (str): utf output
        srs2S (str): rst2pdf output
        srstS (str): reSt output
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

    msgS = "docs written"
    print("\n" + f"{msgS=}")
    sys.exit()
