#! python
"""
rivt API

usage:
    import rivLib.api as rv

API functions:
    rv.R(rS) - (Run) Execute shell scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) Execute Python scripts
    rv.D(rS) - (Docs) Write formatted document files
    rv.M(rS) - (Meta) Meta data for rivt file
    rv.S(rS) - (Skip) Skip processing of section
    rv.Q(rS) - (Quit) Exit processing of rivt file

where rS is a rivt section string - a triple quoted utf-8 string with a header
on the first line

Globals:
    utfS (str): utf doc string
    rstS (str): rstpdf doc string
    xstS (str): texpdf doc string
    lablD (dict): formatting labels
    foldD (dict): folder and file paths
    rivD (dict): calculated values

Last letter of var name indicates type:
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

import fnmatch
import logging
import os
import sys
import warnings
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

from rivLib import rvdoc, rvparse

import __main__

rivtP = Path(os.getcwd())
projP = Path(os.path.dirname(rivtP))
rivtT = Path(__main__.__file__)
rivtN = (rivtT.name).strip()
modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]

# print(f"{rivtT=}")
# print(f"{rivtN=}")
# print(f"{modnameS=}")
if fnmatch.fnmatch(rivtN, "rv[0-9][0-9][0-9][0-9]-*.py"):
    pass
else:
    print(f"""The rivt file name is  {rivtN} . The file name must""")
    print(
        """match "rvddss-anyname.py", where dd and ss are two-digit integers"""
    )
    sys.exit()

# input files
prfxS = rivtN[0:6]
rnumS = rivtN[2:6]
dnumS = prfxS[2:4]
# endregion

# region - file paths
# input files
pthS = " "
rbaseS = rivtN.split(".")[0]
divnumS = "d" + dnumS + "-"
rstnS = rbaseS + ".rst"
txtnS = rbaseS + ".txt"
pdfnS = rbaseS + ".pdf"
htmnS = rbaseS + ".html"
bakN = rbaseS + ".bak"
docP = Path(projP, "rivDocs")
srcP = Path(projP, "sources")
styleP = Path(projP, "styles")
titleS = rivtN.split("-")[1]

# output files
bakT = Path(rivtP, bakN)
rbakT = Path(rivtP, rbaseS + ".bak")
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
styleP = Path(projP, "style")
reportP = Path(projP, "rivDocs", "report")
ossP = Path(projP / "rivtos")
valN = prfxS.replace("rv", "v")
valP = Path(srcP, "v" + dnumS)

# print(f"{projP=}")
# print(f"{rivtP=}")
# print(f"{insP=}")
# print(f"{valsP=}")
# endregion

# region - folders dict
foldD = {
    "pthS": " ",
    "cmdP": srcP,
    "rivtT": rivtT,  # full path and name
    "rivtN": rivtT.name,  # file name
    "baseS": rbaseS,  # file base name
    "rivtP": Path(os.getcwd()),
    "projP": Path(os.path.dirname(rivtP)),
    "docP": Path(projP, "rivDocs"),
    "bakT": Path(rivtP, bakN),
    "errlogT": Path(rivtP, "error.log"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(projP, "README.txt"),
    "reportP": Path(projP, "rivDocs", "report"),
    "styleP": Path(projP, "rivDocs", "style"),
    "srcP": srcP,
    "localP": Path(os.getcwd()),
    "rstpN": rstnS,
    "pdfpN": pdfnS,
    "runP": Path(srcP, "r" + dnumS),
    "insP": Path(srcP, "i" + dnumS),
    "valP": Path(srcP, "v" + dnumS),
    "tooP": Path(srcP, "t" + dnumS),
    "valN": valN,
    "srcnS": "",
}
# endregion
# region - labels dict
lablD = {
    "divnumS": divnumS,  # div number
    "docnumS": prfxS,  # doc number
    "titleS": titleS,  # document title
    "sectS": "",  # section title
    "secnumI": 0,  # section number
    "widthI": 80,  # print width
    "equI": 1,  # equation number
    "tableI": 1,  # table number
    "figI": 1,  # figure number
    "pageI": 1,  # starting page number
    "noteL": [0],  # endnote counter
    "descS": "ref",  # description
    "deciI": 2,  # decimals
    "headrS": "",  # header string
    "footrS": "",  # footer string
    "folderaliaS": "rvsource",  # folder alias
    "unitS": "M,M",  # units
    "valexpS": "",  # list of values for export
    "publicB": False,  # public section
    "printB": True,  # print section to doc
    "tocB": False,  # table of contents
    "subB": False,  # sub values in equations
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "none",  # topic background color
}
# endregion

# region - values dict
rivD = {}  # shared calculated values
# endregion


# region - logging and backup
errlogT = Path(rivtP, prfxS + "-log.txt")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogT,
    filemode="w",
)

warnings.filterwarnings("ignore")
logging.info(f"""rivt file : {foldD["rivtN"]}""")
logging.info(f"""rivt file path : {foldD["rivtP"]}""")

try:
    package_version = version("rivLib")
    verS = f"rivLib version: {package_version}"
except Exception as e:
    verS = f"Could not retrieve version for rivLib: {e}"

print("   ")
print("----------------------------------------------------------")
print(verS)
print(f"rivt file: {rivtN}")
print(f"rivt file path: {rivtP}")
print("----------------------------------------------------------")
print("   ")


# write backup file
with open(foldD["rivtT"], "r") as f2:  # noqa: F405
    rivtS = f2.read()
with open(foldD["bakT"], "w") as f3:  # noqa: F405
    f3.write(rivtS)
logging.info(f"""rivt backup : {foldD["bakT"]}""")  # noqa: F405
# endregion


# initialize doc strings
dutfS = ""
drsrS = ""
drstS = ""
dhtmS = ""


def cmdhelp():
    """command line help"""

    print()
    print("Run rivt file on command line with:                     ")
    print()
    print("     python rvddss-filename.py                             ")
    print()
    print("Where dd and ss are two digit integers.                    ")
    print("See User Manual at https://rivt.info for details           ")
    sys.exit()


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
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    sL = sS.split("\n")
    secC = rvparse.Section(tS, sL, foldD, lablD, rivD)
    sutfS, srs2S, srstS, foldD, lablD, rivD, rivL = secC.content(tagL, cmdL)
    # accumulate doc strings
    dutfS += sutfS
    drs2S += srs2S
    drstS += srstS

    return dutfS, drs2S, drstS, rivL


def R(rS):
    """Run shell command
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["WIN", "OSX", "LINUX"]
    tagL = []
    dutfS, drs2S, drstS, rivL = doc_parse(rS, "R", tagL, cmdL)


def I(rS):  # noqa: E743
    """Insert static source
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
    tagL = ["#]", "C]", "D]", "E]", "F]", "S]", "L]", "T]", "H]", "P]", "U]"]
    tagbL = ["B]]", "C]]", "I]]", "L]]", "X]]"]
    tagL = tagL + tagbL
    dutfS, drs2S, drstS, rivL = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values calculate
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["IMG", "IMG2", "TABLE", "VALUE"]
    tagL = ["E]", "F]", "S]", "Y]", "T]", "H]", "P]", "[V]]", ":=", "="]
    dutfS, drs2S, drstS, rivL = doc_parse(rS, "V", tagL, cmdL)
    # write values file
    fileS = foldD["valN"] + "-" + str(lablD["secnumI"]) + ".csv"
    fileP = Path(foldD["valP"], fileS)
    with open(fileP, "w") as file1:
        file1.write("\n".join(rivL))


def T(rS):
    """Tools in Python
    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["PYTHON", "LATEX"]
    tagL = []
    dutfS, drs2S, drstS, rivL = doc_parse(rS, "T", tagL, cmdL)


def D(rS):
    """Write doc files

    Writes docs as .txt, .pdf (reportLab or tex) and .html

    Args:
        sS (str): section string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD
    # config = ConfigParser()
    # config.read(Path(projP, "rivt-doc.ini"))
    # headS = config.get("report", "title")
    # footS = config.get("utf", "foot1")
    print(drs2S)
    cmdL = ["DOC", "ATTACH"]
    wrtdoc = rvdoc.Cmdp(foldD, lablD, rS, cmdL, drs2S)
    mssgS = wrtdoc.cmdpx()
    print("\n" + f"{mssgS}")
    sys.exit()


def M(rS):
    """rivt file meta data
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivD

    cmdS = ""
    for iS in rS.split("\n")[1:]:
        cmdS += iS[4:] + "\n"
    # print(cmdS)

    localsD = locals()
    exec(cmdS, globals(), localsD)
    authD = localsD["rv_authD"]
    authS = "av-" + authD["version"]
    headS = "   " + str(rivtN)
    timeS = datetime.now().strftime("%Y-%m-%d | %I:%M%p")
    borderS = "=" * 80
    lenI = len(timeS + "   " + headS)
    sutfS = (
        "\n\n"
        + timeS
        + "   "
        + headS
        + authS.rjust(80 - lenI)
        + "\n"
        + borderS
        + "\n"
    )

    print(sutfS)  # STDOUT doc header
    logging.info("Doc start")


def S(rS):
    """skip section string - not processed
    Args:
        sS (str): section string
    """
    shL = rS.split("\n")
    print("\n[" + shL[0].strip() + "] : section skipped " + "\n")


def Q(rS):
    """exit rivLib processing
    Args:
        rS (str): section string
    """
    shL = rS.split("\n")
    print("\n[" + shL[0].strip() + "] : rivLib exit " + "\n")
    sys.exit()
