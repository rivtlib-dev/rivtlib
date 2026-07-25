#! python
"""
rivt API

usage:
    import rivtlib.rvapi as rv

API functions:
    rv.R(rS) - (Run) Execute markup and Python scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) External programs and shell scripts
    rv.D(rS) - (Docs) Publish formatted doc file
    rv.S(rS) - (Skip) Skip processing of section
    rv.X(rS) - (Exit) Exit processing of rivt file
where the argument rS is a triple quoted rivt string (utf-8)

Comment settings:
    # rc public=True; False  (default is False)

Globals:
    utfS (str): utf doc string
    rs2S (str): rstpdf doc string
    rstS (str): texpdf doc string
    lD (dict): formatting parameters
    fD (dict): fDer and file paths
    rivtD (dict): calculated values

Typing: Last letter of var name indicates type:
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
    T => path + file name (path)
"""

import argparse
import fnmatch
import logging
import os
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

import __main__
import rivtlib.rvunits as rvunit
from rivtlib import rvdoc, rvparse, rvshell, rvtext

# parse command line arguments
reptP = Path(os.getcwd())
# print(f"Current working directory: {reptP}")
try:
    rivtN = os.path.basename(__main__.__file__)
except Exception:
    rivtN = os.path.basename(__main__.__name__)

if fnmatch.fnmatch(rivtN, "rv[A-Z0-9][0-9][0-9]-*.py"):
    pass
else:
    print(f"""The rivt file name provided was {rivtN}""")
    print("""The file name must match rvDss-filename.py""")
    print("""where D is an alpha-numeric division label""")
    print("""and ss is a two-digit subdivision integer""")
    sys.exit()
args = ""
parser = argparse.ArgumentParser(description="Example script")
parser.add_argument("-t", "--ptype", default="---", help="file type")
parser.add_argument("-k", "--keep", default="false", help="keep rst")
args = parser.parse_args()
reptypeS = args.ptype
repkeepS = args.keep
# Basic paths
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
rbaseS = rivtN.split(".")[0]
bakN = rbaseS + ".bak"
reptpubN = rivtN.replace("rv", "rv-")
docnumS = rbaseS[0:6]
srcP = Path(reptP, "rvsrc")
publicP = Path(reptP, "_rivt-public")  # not used with rivtbooks
# Set paths and flags for report, book, or chapter
# print("--------------", reptP.name)
if reptP.name == "rivt-report":
    reptflagS = "doc"
    pubdocP = Path(reptP, "_published")
    storeP = Path(reptP, "_rvstor")
    rstdocsP = Path(reptP, "_rstdocs")
    pdfpubP = Path(pubdocP, "pdfdocs")
    txtdocsP = Path(pubdocP, "txtdocs")
    errlogN = docnumS + "log.txt"
    logsP = Path(storeP, "logs")
    dataP = Path(storeP, "data")
    scriptsP = Path(storeP, "scripts")
    errlogT = Path(logsP, errlogN)
    bakT = Path(logsP, bakN)
    rivtT = Path(reptP, rivtN)
    rvreadmeT = Path(reptP.parent, "README.txt")
    docreadmeT = Path(reptP, "_published", "readme", docnumS + "readme.txt")
    pubreadmeT = Path(publicP, "README.txt")
else:
    reptflagS = "chapter"
    pubdocP = Path(reptP.parent, "_published")
    rstdocsP = Path(reptP.parent, "_rstdocs")
    storeP = Path(reptP.parent, "_rvstor")
    txtdocsP = Path(pubdocP, "_txtdocs")
    pdfpubP = Path(pubdocP, "_pdfdocs")
    logsP = Path(storeP, "logs")
    errlogN = docnumS + "log.txt"
    errlogT = Path(logsP, errlogN)
    bakT = Path(logsP, bakN)
    rivtT = Path(reptP, rivtN)
    rvreadmeT = Path(reptP.parent, "README.txt")
    docreadmeT = Path(reptP.parent, "_rvstor", docnumS + "readme.txt")
    pubreadmeT = " "
# logs and backups
# print("-----------------------", reptflagS)
warnings.filterwarnings("ignore")
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + rbaseS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogT,
    filemode="w",
)
package_version = version("rivtlib")
verS = f"rivtlib version: {package_version}"
logging.info("Doc start")
logging.info(verS)
with open(rivtT, "r") as f2:
    rivtS = f2.read()
with open(bakT, "w") as f3:
    f3.write(rivtS)
logging.info(f"""rivt backup : {bakT}""")
# region - folder and label dictionaries
vdescD = {}
rivtD = {}
rvunitD = vars(rvunit)
rivtD = rivtD | rvunitD  # add units to dictionary
metaD = {}  # metadata
fD = {
    "rivtN": rivtN,  # file name
    "rivtT": rivtT,  # full path name
    "reptP": reptP,
    "rbaseS": rbaseS,  # file base name
    "errlogT": errlogT,
    "bakT": bakT,
    "pthS": " ",
    "srcnS": " ",
    "pdfN": rbaseS + ".pdf",
    "rvreadmeT": rvreadmeT,
    "pubreadmeT": pubreadmeT,
    "docreadmeT": docreadmeT,
    "rstdocsP": rstdocsP,
    "txtdocsP": txtdocsP,
    "reptpubP": pubdocP,
    "srcP": srcP,
    "storeP": storeP,
    "pdfpubP": pdfpubP,
    "htmlpubP": Path(pubdocP, "docs"),  # not used with rivtbooks
    "publicT": Path(reptP, "public", reptpubN),  # not used with rivtbooks
}
lD1 = {
    "rvtypeS": "",  # section type r,i,v,t,d
    "reptypeS": reptypeS,  # default pub type
    "repkeepS": repkeepS,  # default keep rst files
    "doctypeS": "txt",  # default doc
    "docnumS": rbaseS[0:6],  # doc number
    "sdivI": int(rbaseS[3:5]),  # subdiv number
    "secnumI": 0,  # section number
    "divS": rbaseS[2],  # div character
    "valprfx": rbaseS[0:6].replace("rv", "v"),
    "toolprfx": rbaseS[0:6].replace("rv", "t"),
    "sectS": "",  # section title
    "equI": 0,  # equation number
    "tableI": 1,  # table number
    "figI": 1,  # figure number
    "pageI": 1,  # starting page number
    "noteI": 0,  # endnote counter
    "descS": "ref",  # value description
    "deciI": 2,  # decimals
    "valexpS": "",  # list of values for export
    "argsname": "",  # name of argument dictionary
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "white",  # topic background color
    "reptflagS": reptflagS,  # rivt-report, rivtbook or chapter
    "cntflgI": 0,  # counter flag - skips transition for first section
    "privB": "True",  # do not write to public
    "docB": "True",  # add to doc
    "mergeB": "False",  # merge to prev section
    "storeB": "False",  # write section to _rvstor
    "autocfgB": "True",  # config format from metadata
    "runtypeS": "",  # type for rv.T
}
# defaults for rivt file comment settings
lD2 = {
    "widthI": 80,
    "privateB": "True",
    "notagB": "True",
}
lD = lD1 | lD2
# settings from rivt file comment settings
lnL = []
with open(rivtT, "r") as f1:
    rivtL = f1.readlines()
for lnS in rivtL:
    if lnS[0:4] == "# rv":
        lnL = lnS.split(";")
        lnL = lnL[0].split("=")
        if lnL[0].strip() == "set_width":
            lD["widthI"] = int(lnL[1].strip())
        elif lnL[0].strip() == "no_tag":
            lD["notagB"] = lnL[1].capitalize.strip()
        elif lnL[0].strip() == "private":
            lD["privateB"] = lnL[1].capitalize.strip()
        else:
            pass
# initialize doc strings
dutfS = ""  # doc utf string
dtxtS = ""  # doc text string
dlatS = ""  # doc latex string
dcmdS = ""  # doc command string
# doc rst string
drstS = """ 
.. raw:: pdf

   PageBreak

      
"""


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


def doc_parse(rS, tyS, tagL, cmdL):
    """convert section string to doc string
    Args:
        rS (str): section string
        tyS (str): section type (R,I,V,T,W,S)
        tagL (list): tag list
        cmdL (list): command list
    Calls:
        Rs (class), content (method)
    Returns:
        sutfS (str): utf output
        srstS (str): rest output
        stxtS (str): text output
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    rsL = rS.split("\n")
    conC = rvparse.Rs(tyS, rsL, fD, lD, rivtD, rivtL, vdescD)
    if tyS == "R" or tyS == "T":
        return conC.sutfS, conC.stxtS, conC.srstS
    elif tyS == "I" or tyS == "V":
        sutfS, stxtS, srstS, fD, lD, rivtD = conC.content(tyS, tagL, cmdL)
        if lD["docB"] == "True":
            dutfS += sutfS
            drstS += srstS
            dtxtS += stxtS
    else:
        pass

    return dutfS, dtxtS, drstS


tagsL = [
    "R",  # right justify
    "C",  # center bold
    "B",  # bold text
    "M",  # math format
    "L",  # LaTeX format
    "V",  # var value
    "T",  # table label
    "U",  # url link
    "S",  # section link
    "D",  # download link
    "G",  # glossary term
    "#",  # footnote
]


def R(rS):
    """Run shell commands

    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD

    cmdL = [
        "COPY",  # copy file from source to target
        "SHELL",  # execute shell command
    ]

    tagbL = [
        "WRITE",  # write text block to rvsrc/data
    ]
    tagL = tagbL
    sutfS, stxtS, srstS = doc_parse(rS, "R", tagL, cmdL)
    r1S = rS.split("\n", 1)[1]
    uS, tS, rS, lS = rvshell.run_shell(r1S, lD, fD, rivtD)
    sutfS += uS
    stxtS += tS
    srstS += rS
    dutfS += sutfS
    dtxtS += stxtS
    drstS += srstS


def I(rS):  # noqa: E743
    """Insert API
    Insert static files e.g. tables, images and text

    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD

    tagbL = [
        "TABLE",  # format inline rst and write to csv
        "ENDNOTES",  # list footnote references in order
        "WRITE",  # write text block to rvsrc/data
        "END",  # end
    ]
    cmdL = [
        "IMAGE",  # insert image from file
        "IMAGE2",  # insert adjacent images from file
        "TEXT",  # insert text from file and format
        "TABLE",  # insert table from file
    ]
    tagL = tagsL + tagbL
    dutfS, dtxtS, drstS = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values API
    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD, rivtD, vdescD

    tagbL = [
        "ARGS",  # argument dictionary for function
        "TABLE",  # format inline rst and write to csv
        "ENDNOTES",  # list footnote references in order
        "TEXT",  # insert text from fileand format
        "WRITE",  # write text block to rvsrc/data
        "END",  # end
    ]
    compL = [
        " < ",
        " > ",
        " != ",
        " == ",
        " <= ",
        " >= ",
        "<",
        ">",
        "!=",
        "==",
        "<=",
        ">=",
    ]
    cmdL = [
        compL,  # comparisons
        "IMAGE",  # image
        "IMAGE2",  # adjacent images
        "PYTHON",  # read functions
        "TABLE",  # table from file
        "VALTABLE",  # value table from rvsrc/data
        "VALDATA",  # value table from stored file
        "TEXT",  # insert text and format
        " ==: ",  # define value
        " <=: ",  # assign value
        " :=: ",  # assign function value
    ]

    tagL = tagsL + tagbL
    dutfS, dtxtS, drstS = doc_parse(rS, "V", tagL, cmdL)


def T(rS):
    """Text API - reads and processes scripts

    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD, rivtD

    typeL = [
        "bold",  # bold text with indent
        "endnote",  # list of endnotes in order
        "indent",  # format literal with indent
        "italic",  # italic text with indent
        "note",  # note in box
        "rst",  # format restructured text
        "text",  # format literal
        "wrap",  # wrap with indent
        "latex",  # include in pdf
        "html",  # include in html
        "latex",  # requires texlive cli
        "mermaid",  # requires mermaid cli
        "dot",  # requires graphviz cli
        "subpython",  # substitute into python code block
    ]
    tagL = []
    cmdL = []
    hS = rS.split("\n", 1)[0]
    hL = hS.split("|")
    r1S = rS.split("\n", 1)[1]
    try:
        typeS = hL[3].strip()
        if typeS in typeL:
            lD["rvtypeS"] = typeS
        else:
            print(
                f"\033[31m{typeS} is not a valid type for rv.T() - type reset to 'text'\033[0m"
            )
            typeS = "text"
    except Exception:
        typeS = "text"
    try:
        fileS = hL[2].strip()
    except Exception:
        fileS = ""
    try:
        fileP = Path(srcP, "scripts", fileS)
        with open(fileP, "r") as f1:
            r2S = f1.read()
    except Exception:
        r2S = ""
    sutfS, stxtS, srstS = doc_parse(rS, "T", tagL, cmdL)
    uS, tS, rS, lS = rvtext.format_text(typeS, r1S, r2S, fileS, lD, fD, rivtD)
    print(uS + "\n")

    sutfS += uS
    stxtS += tS
    srstS += rS

    dutfS += sutfS
    dtxtS += stxtS
    drstS += srstS


def D(rS):
    """Doc API
    Publish doc files as .txt, .pdf, .html

    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    wrtdoc = rvdoc.Cmdp(rS, fD, lD, dutfS, drstS, dtxtS)
    print(f"{wrtdoc.cmdx()}")
    print("\n\033[32m>>>>>>>>>>>>>>>>>>> End of rivt file\033[0m\n\n")
    sys.exit()


def S(rS):
    """Skip rivt string processing

    Args:
        rS (str): rivt string
    """
    shL = rS.split("\n")
    logging.info("section skipped at: " + shL[0])
    print("\n[" + shL[0].strip() + "] : section skipped " + "\n")


def X():
    """Exit rivt file processing

    Args:
        rS (str): rivt string
    """
    logging.info("exit rivt file with rv.X()")
    print("\n\033[31m------------------------------------------------\033[0m")
    print("\n\033[31mrivtlib exited with rv.X()\033[0m")
    print("\n\033[31m------------------------------------------------\033[0m")
    sys.exit()
