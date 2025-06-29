#! python
"""rivt API

usage:
    import rivtlib.api as rv

API functions:
    rv.R(sS) - (Run) Execute shell scripts
    rv.I(sS) - (Insert) Insert static text, math, images and tables
    rv.V(sS) - (Values) Evaluate values and equations
    rv.T(sS) - (Tools) Execute Python scripts
    rv.W(sS) - (Write) Write formatted document files
    rv.S(sS) - (Skip) Skip processing of that section

where sS is a section string - triple quoted, header line, indented, utf-8.

Globals:
    utfS (str): utf doc string
    rstS (str): rst2pdf doc string
    xstS (str): latex doc string
    labelD (dict): format labels
    folderD (dict): folder and file paths
    rivtD (dict): calculated values

rivtlib variables use the last letter of the var name to indicate type:
    A => array
    B => boolean
    C => class instance
    D => dictionary
    F => float
    I => integer
    L => list
    N => file name
    O => object
    P => path
    S => string
    T => total path (includes file)

"""

import logging
import sys
from datetime import datetime
from pathlib import Path

from rivtlib.rvunits import *  # noqa: F403
from rivtlib.rvparam import *  # noqa: F403
from rivtlib import rvparse

from . import rvcmdpub

logging.info(f"""rivt file : {folderD["rivtN"]}""")
logging.info(f"""rivt path : {folderD["rivtP"]}""")

with open(folderD["rivtT"], "r") as f2:  # noqa: F405
    rivtS = f2.read()
with open(folderD["bakT"], "w") as f3:  # noqa: F405
    f3.write(rivtS)
logging.info(f"""rivt backup : {folderD["bakT"]}""")  # noqa: F405


def doc_hdr():
    """generate document header

    Returns:
        str: doc string header
    """
    # init file - (headings and doc overrides)

    dutfS = ""
    drs2S = ""
    drstS = ""
    # config = ConfigParser()
    # config.read(Path(projP, "rivt-doc.ini"))
    # headS = config.get("report", "title")
    # footS = config.get("utf", "foot1")
    titleL = rivtN.split("-")  # subdivision title
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
    """section string to doc string
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
    secC = rvparse.Section(tS, sL, folderD, labelD, rivtD)
    sutfS, srs2S, srstS, folderD, labelD, rivtD, rivtL = secC.section(tagL, cmdL)
    # accumulate doc strings
    dutfS += sutfS
    drs2S += srs2S
    drstS += srstS

    return dutfS, drs2S, drstS, rivtL


def R(sS):
    """Run shell command
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD
    cmdL = ["WIN", "OSX", "LINUX"]
    tagL = []
    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "R", tagL, cmdL)


def I(sS):  # noqa: E743
    """Insert static source
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD
    cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
    tag1L = ["#]", "C]", "D]", "E]", "F]", "S]", "L]", "T]", "H]", "P]", "U]"]
    tag2L = ["B]]", "C]]", "I]]", "L]]", "X]]"]
    tagL = tag1L + tag2L
    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "I", tagL, cmdL)


def V(sS):
    """Values calculate
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD
    cmdL = ["IMG", "IMG2", "VALUE"]
    tagL = ["E]", "F]", "S]", "Y]", "T]", "H]", "P]", "[V]]", ":="]
    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "V", tagL, cmdL)
    fileS = folderD["valN"] + "-" + str(labelD["secnumI"]) + ".csv"
    fileP = Path(folderD["valP"], fileS)
    with open(fileP, "w") as file1:
        file1.write("\n".join(rivtL))


def T(sS):
    """Tools in Python
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD
    cmdL = ["SCRIPT"]
    tagL = []
    dutfS, drs2S, drstS, rivtL = doc_parse(sS, "T", tagL, cmdL)


def P(sS):
    """Write doc files

    Writes docs as .txt, .pdf (from reportab or tex) and .html

    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, folderD, labelD, rivtD

    wrtdoc = rvcmdpub.Cmdw(folderD, labelD, sS)
    msgS = wrtdoc.cmdwx()
    print("\n" + f"{msgS}")
    sys.exit()


def S(sS):
    """skip section string - not processed
    Args:
        sS (str): section string
    """
    shL = sS.split("|")
    print("\n[" + shL[0] + "] : section skipped " + "\n")


# begin doc generation - returns doc as txt, rst2 and rst string
dutfS, drs2S, drstS = doc_hdr()
