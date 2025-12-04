#! python
"""
rivt API

usage:
    import rivtlib.rvapi as rv

API functions:
    rv.R(rS) - (Run) Execute shell scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) Execute Python scripts
    rv.D(rS) - (Docs) Publish formatted doc file
    rv.S(rS) - (Skip) Skip processing of section
    rv.X(rS) - (Exit) Exit processing of rivt file

where the argument rS is a triple quoted utf-8 string (rivt string)

Settings:
    rv_authD (dict): author information
    rv_localB (bool): True - reads and writes to local directory

Globals:
    utfS (str): utf doc string
    rstS (str): rstpdf doc string
    xstS (str): texpdf doc string
    lablD (dict): formatting parameters
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
    N => file name (string)
    O => object
    P => path
    S => string
    T => path + file name
"""

import fnmatch
import logging
import os
import sys
import warnings
from datetime import datetime
from importlib.metadata import version
from pathlib import Path

import __main__
from rivtlib import rvparse

rv_localB = False
rv_authD = {}
from rivtmeta import *  # noqa: E402, F403

# region - rivt file name and paths
# set metadata variables
rivtP = Path(os.getcwd())
reptP = Path(os.path.dirname(rivtP))
rivtT = Path(__main__.__file__)
rivtN = (rivtT.name).strip()
modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")

if fnmatch.fnmatch(rivtN, "rv[A-Z0-9][0-9][0-9]-*.py"):
    pass
else:
    print(f"""The rivt file name provided was {rivtN}""")
    print("""The file name must match  rvDss-anyname.py""")
    print("""where D is a capital alpha-numeric division label""")
    print("""and ss is a two-digit subdivision integer""")
    sys.exit()
# endregion

# region - file names
rbaseS = rivtN.split(".")[0]
rivtpN = rivtN.replace("rv", "rv-")
docnumS = rbaseS[0:6]
rstN = rbaseS + ".rst"
txtN = rbaseS + ".txt"
pdfN = rbaseS + ".pdf"
htmlN = rbaseS + ".html"
bakN = rbaseS + ".bak"
apilogN = docnumS + "api.txt"
errlogN = docnumS + "chk.log"
# endregion

# region - file paths
publicP = Path(rivtP, "public")
srcP = Path(rivtP, "src")
storeP = Path(rivtP, "store")
pubP = Path(rivtP, "publish")
logsP = Path(storeP, "logs")
# endregion

if rv_localB:
    errlogT = Path(rivtP, errlogN)
    apilogT = Path(rivtP, apilogN)
    bakT = Path(rivtP, bakN)
else:
    errlogT = Path(logsP, errlogN)
    apilogT = Path(logsP, apilogN)
    bakT = Path(logsP, bakN)

# region - folders dict
rivD = {}  # shared calculated values
foldD = {
    "pthS": " ",
    "srcnS": " ",
    "rivtN": rivtT.name,  # file name
    "baseS": rbaseS,  # file base name
    "rivtP": Path(os.getcwd()),
    "reptfoldN": os.path.dirname(rivtP),
    "docP": Path(rivtP, "rivDocs"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(rivtP, "README.txt"),
    "publishP": Path(rivtP, "publish"),
    "publish_P": Path(rivtP),
    "publicT": Path(rivtP, "public", rivtpN),
    "public_T": Path(rivtP, rivtpN),
    "srcP": srcP,
    "storeP": storeP,
    "valP": Path(srcP, "values"),
    "toolP": Path(srcP, "tools"),
    "styleP": Path(srcP, "styles"),
    "tempP": Path(srcP, "temp"),
    "val_P": rivtP,
    "style_P": rivtP,
    "tool_P": rivtP,
    "temp_P": rivtP,
    "errlogT": errlogT,
    "apilogT": apilogT,
    "bakT": bakT,
}
lablD = {
    "rvtypeS": "",  # section type,
    "divS": rbaseS[2:3],  # div number
    "sdivS": rbaseS[3:5],
    "docnumS": rbaseS[0:6],  # doc number
    "docnameS": rbaseS[6:].replace("-", " "),  # document name
    "replablS": reptP.name[5:],
    "valprfx": rbaseS[0:6].replace("rv", "v"),
    "sectS": "",  # section title
    "secnumI": 0,  # section number
    "widthI": 80,  # print width
    "equI": 1,  # equation number
    "tableI": 1,  # table number
    "figI": 1,  # figure number
    "pageI": 1,  # starting page number
    "noteL": [0],  # endnote counter
    "descS": "ref",  # value description
    "deciI": 2,  # decimals
    "headrS": "",  # header string
    "footrS": "",  # footer string
    "aliaS": "rvsource",  # folder alias
    "unitS": "M,M",  # units
    "valexpS": "",  # list of values for export
    "publicB": False,  # public section
    "printB": True,  # print section to doc
    "mergeB": False,
    "apiB": True,
    "tocB": False,  # table of contents
    "subB": False,  # sub values in equations
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "none",  # topic background color
}
# endregion

# region - logs
warnings.filterwarnings("ignore")
try:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename=errlogT,
        filemode="w",
    )
except Exception:
    pass
logging.info("Doc start")

# write backup file
with open(rivtT, "r") as f2:  # noqa: F405
    rivtS = f2.read()
try:
    with open(bakT, "w") as f3:  # noqa: F405
        f3.write(rivtS)
    logging.info(f"""rivt backup : {bakT}""")  # noqa: F405
except Exception:
    pass

# api log
try:
    package_version = version("rivtlib")
    verS = f"rivtlib version: {package_version}"
except Exception as e:
    verS = f"Could not retrieve version for rivtlib: {e}"
if rv_localB:
    apilogT = Path(rivtP, apilogN)
else:
    apilogT = Path(logsP, apilogN)
f4 = open(apilogT, "w")
f4.write("API log: " + rivtN + "\n")
f4.write("-------------------\n")
f4.write("Meta Data\n")
f4.write("-------------------\n")
f4.write(f"""rivtlib version : {verS}\n""")
f4.write(f"""rivt file : {foldD["rivtN"]}\n""")
f4.write(f"""rivt file path : {foldD["rivtP"]}\n""")
for key, value in rv_authD.items():
    f4.write(f"{key}\t{value}\n")


# initialize doc strings
dutfS = ""
drsrS = ""
drstS = ""
dhtmS = ""
rv_localB = False


cmdS = ""
# read content

# print(cmdS)
localsD = locals()
exec(cmdS, globals(), localsD)
try:
    authD = localsD["rv_authD"]
except Exception:
    pass
try:
    if localsD["rv_localB"]:
        foldD["localdirB"] = True
except Exception:
    pass

authS = "v" + authD["version"]
headS = "   " + lablD["docnameS"]
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
# end region


def cmdhelp():
    """command line help"""

    print()
    print("Run rivt file on command line with:                     ")
    print()
    print("     python rvDss-filename.py                           ")
    print()
    print("Where D is a capital alpha-numeric division label       ")
    print("and ss is a two digit subdivision integer.              ")
    print("See User Manual at https://rivt.info for details        ")
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
        srsrS (str): rst2pdf output
        srstS (str): reSt output
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    sL = sS.split("\n")
    secC = rvparse.Section(tS, sL, foldD, lablD, rivD)
    sutfS, srsrS, srstS, foldD, lablD, rivD, rivL = secC.content(tagL, cmdL)
    # accumulate doc strings
    dutfS += sutfS
    drsrS += srsrS
    drstS += srstS

    return dutfS, drsrS, drstS, rivL


def R(rS):
    """Run shell command
    Args:
        sS (str): section string
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["WIN", "OSX", "LINUX"]
    tagL = []
    dutfS, drsrS, drstS, rivL = doc_parse(rS, "R", tagL, cmdL)


def I(rS):  # noqa: E743
    """Insert static source
    Args:
        rS (str): rivt string
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["IMAGE", "IMAGE2", "TABLE", "TEXT"]
    tagL = [
        "#]",
        "C]",
        "R]",
        "E]",
        "I]",
        "T]",
        "A]",
        "L]",
        "S]",
        "D]",
        "U]",
        "-----",
        "=====",
    ]
    tagbL = ["B]]", "C]]", "I]]", "L]]", "X]]"]
    tagL = tagL + tagbL
    dutfS, drsrS, drstS, rivL = doc_parse(rS, "I", tagL, cmdL)

    apiS = "[rv.I] " + rS.split("\n")[0]
    f4.write(apiS + "\n")


def V(rS):
    """Values calculate
    Args:
        sS (str): section string
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["IMAGE", "IMAGE2", "TABLE", "VALUE", ":=", "<="]
    tagL = [
        "#]",
        "C]",
        "R]",
        "E]",
        "I]",
        "T]",
        "S]",
        "D]",
        "U]",
        "-----",
        "=====",
    ]

    dutfS, drsrS, drstS, rivL = doc_parse(rS, "V", tagL, cmdL)

    apiS = "[rv.V] " + rS.split("\n")[0]
    f4.write(apiS + "\n")


def T(rS):
    """Python and Markup Tools
    Args:
        sS (str): section string
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    cmdL = ["PYTHON", "LATEX", "HTML", "RST"]
    tagL = []
    dutfS, drsrS, drstS, rivL = doc_parse(rS, "T", tagL, cmdL)


def D(rS):
    """Publish Doc files

    Writes docs as .txt, .pdf (reportLab or tex) and .html

    Args:
        sS (str): section string
    """
    global dutfS, drsrS, drstS, dhtmS, foldD, lablD, rivD
    # config = ConfigParser()
    # config.read(Path(reptfoldP, "rivt-doc.ini"))
    # headS = config.get("report", "title")
    # footS = config.get("utf", "foot1")
    print(drsrS)
    cmdL = ["DOC", "ATTACH"]
    wrtdoc = rvdoc.Cmdp(foldD, lablD, rS, cmdL, drsrS)
    mssgS = wrtdoc.cmdpx()
    print("\n" + f"{mssgS}")
    apiS = "[rv.D] " + rS.split("\n")[0]
    f4.write(apiS + "\n")
    f4.close()
    sys.exit()


def S(rS):
    """skip section string - not processed
    Args:
        sS (str): section string
    """
    shL = rS.split("\n")
    print("\n[" + shL[0].strip() + "] : section skipped " + "\n")
    apiS = "[rv.S] " + rS.split("\n")[0]
    f4.write(apiS + "\n")


def Q(rS):
    """exit rivtlib processing
    Args:
        rS (str): section string
    """
    shL = rS.split("\n")
    print("\n[" + shL[0].strip() + "] : rivtlib exit " + "\n")
    apiS = "[rv.Q] " + rS.split("\n")[0]
    f4.write(apiS + "\n")
    f4.close()
    sys.exit()
