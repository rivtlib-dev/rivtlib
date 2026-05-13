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

import fnmatch
import logging
import os
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

import __main__
import rivtlib.rvunits as rvunit
from rivtlib import rvdoc, rvparse

# region - top level rivt files
reptP = Path(os.getcwd())
rivtP = Path(os.path.dirname(reptP))
try:
    rivtN = os.path.basename(__main__.__file__)
except Exception:
    rivtN = os.path.basename(__main__.__name__)
rivtT = Path(reptP, rivtN)
print(rivtN, rivtT)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")

if fnmatch.fnmatch(rivtN, "rv[A-Z0-9][0-9][0-9]-*.py"):
    pass
else:
    print(f"""The rivt file name provided was {rivtN}""")
    print("""The file name must match rvDss-filename.py""")
    print("""where D is an alpha-numeric division label""")
    print("""and ss is a two-digit subdivision integer""")
    sys.exit()

rbaseS = rivtN.split(".")[0]
reptPN = rivtN.replace("rv", "rv-")
docnumS = rbaseS[0:6]
bakN = rbaseS + ".bak"
errlogN = docnumS + "log.txt"
rootP = reptP.parent
publicP = Path(rootP, "_rivt-public")
storeP = Path(reptP, "_stored")
pubP = Path(reptP, "_published")
rstdocsP = Path(reptP, "_rstdocs")
srcP = Path(reptP, "src")
logsP = Path(storeP, "logs")
errlogT = Path(logsP, errlogN)
bakT = Path(logsP, bakN)
rivtT = Path(reptP, rivtN)
rivt_storedP = storeP
# endregion

# region - logs
try:
    package_version = version("rivtlib")
    verS = f"rivtlib version: {package_version}"
except Exception as e:
    verS = f"rivtlib version not available: {e}"

warnings.filterwarnings("ignore")
try:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-8s  " + rbaseS + "   %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename=errlogT,
        filemode="w",
    )
except Exception:
    pass
logging.info("Doc start")
logging.info(verS)
# write backup file
with open(rivtT, "r") as f2:  # noqa: F405
    rivtS = f2.read()
try:
    with open(bakT, "w") as f3:  # noqa: F405
        f3.write(rivtS)
    logging.info(f"""rivt backup : {bakT}""")  # noqa: F405
except Exception:
    pass
# end region

# region - dictionaries
vdescD = {}
rivtD = {}
rvunitD = vars(rvunit)
rivtD = rivtD | rvunitD
metaD = {}  # metadata
fD = {  # folders
    "errlogT": errlogT,
    "bakT": bakT,
    "pthS": " ",
    "srcnS": " ",
    "rivtN": rivtN,  # file name
    "rivtT": rivtT,  # full path name
    "reptP": Path(os.getcwd()),
    "rbaseS": rbaseS,  # file base name
    "reptfDN": os.path.dirname(reptP),
    "docP": Path(reptP, "rivtDocs"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(rivtP, "README.txt"),
    "rstdocsP": rstdocsP,
    "reptPubP": pubP,
    "pdfpubP": Path(pubP, "pdfdocs"),
    "htmlpubP": Path(pubP, "docs"),
    "publicT": Path(reptP, "public", reptPN),
    "srcP": srcP,
    "storeP": storeP,
    "valP": Path(srcP, "values"),
    "toolP": Path(srcP, "tools"),
    "styleP": Path(srcP, "styles"),
    "tempP": Path(srcP, "temp"),
}
lD = {  # labels
    "rbaseS": rbaseS,  # section type r,i,v,t,d
    "rvtypeS": "",  # section type r,i,v,t,d
    "docnumS": rbaseS[0:6],  # doc number
    "divS": rbaseS[2:3],  # div number
    "sdivS": str(int(rbaseS[3:5])),  # subdiv
    "docnameS": rbaseS[6:].replace("-", " "),  # document name
    "replablS": rivtP.name[5:],
    "valprfx": rbaseS[0:6].replace("rv", "v"),
    "sectS": "",  # section title
    "secnumI": 0,  # section number
    "equI": 0,  # equation number
    "tableI": 1,  # table number
    "figI": 1,  # figure number
    "pageI": 1,  # starting page number
    "noteL": [0],  # endnote counter
    "descS": "ref",  # value description
    "deciI": 2,  # decimals
    "headrS": "",  # header string
    "footrS": "",  # footer string
    "aliaS": "rvsource",  # fDer alias
    "unitS": "M,M",  # units
    "valexpS": "",  # list of values for export
    "showB": True,  # print section to doc
    "mergeB": False,
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "none",  # topic background color
    "cntflgI": 0,
    "addtagB": False,  # add API tag
    "rvpubB,": False,  # public section
    "widthI": 80,  # print width
}
# endregion

# comment settings
with open(rivtT, "r") as f1:  # noqa: F405
    rivtL = f1.readlines()
for lnS in rivtL:
    if lnS[0:4] == "# rv":
        if "setpublic" and ("True" in lnS or "true" in lnS):
            lD["rvpubB"] = True
        if "setwidth" in lnS:
            lD["widthI"] = int(lnS.split("=")[1])
        if "addtag" and ("True" in lnS or "true" in lnS):
            lD["addtagB"] = True


# initialize doc strings
dutfS = ""
drstS = ""
dtxtS = ""
dlatS = ""
dcmdS = ""


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
    sutfS, srstS, stxtS, fD, lD, rivtD = conC.content(tyS, tagL, cmdL)
    dutfS += sutfS
    drstS += srstS
    dtxtS += stxtS

    return dutfS, drstS, dtxtS


def R(rS):
    """Run scripts and insert markup
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    cmdL = [
        "MARKUP",  # execute script file
    ]
    tagL = []
    tagbL = [
        "PYTHON",  # Python script
        "MARKUP",  # format block
        "END",  # end
    ]

    tagL = tagbL + tagL

    blkB = False
    blkS = ""
    lL = rS.split("\n")
    for lS in lL:
        if blkB:  # tag flag
            if "[[END]]" in lS:
                blkB = False
                exec(blkS, globals(), rivtD)
                blkS = ""
                continue
            blkS += lS.strip()
            continue
        for subS in tagL:  # tags
            if subS in lS:
                blkB = True
                continue
        for subS in cmdL:
            pass


def I(rS):  # noqa: E743
    """Insert static source
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD

    cmdL = [
        "IMAGE",  # insert image from file
        "IMAGE2",  # insert adjacent images from file
        "TABLE",  # insert table from file
        "TEXT",  # insert text from filoe
    ]
    tagL = [
        "C",  # bold center text
        "M",  # ascii math
        "L",  # LaTeX math
        "#",  # footnote
        "G",  # glossary term
        "S",  # section link
        "U",  # url link
        "D",  # download link
        "V",  # var value
        "T",  # table label
        "F",  # figure label
    ]
    tagbL = [
        "TABLE",  # format and write to csv
        "TOPIC",  # topic
        "BOX",  # draw box
        "END",  # end
    ]
    tagL = tagL + tagbL
    dutfS, drstS, dtxtS = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values calculate
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD, vdescD

    compL = [" < ", " > ", " != ", " == ", " <= ", " >= "]
    cmdL = [
        "IMAGE",  # image from file
        "IMAGE2",  # adjacent image files
        "TABLE",  # table from file
        "VALTABLE",  # value table from file
        "PYTHON",  # execute Python file
        " ==: ",  # define value
        " <=: ",  # assign value
        " :=: ",  # assign value
        compL,  # comparisons
    ]
    tagL = [
        "M",  # math format
        "L",  # LaTeX format
        "V",  # var value
        "F",  # figure label
        "C",  # bold center text
        "T",  # table label
    ]
    tagbL = []
    tagL = tagL + tagbL
    dutfS, drstS, dtxtS = doc_parse(rS, "V", tagL, cmdL)


def T(rS):
    """Execute external programs
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    cmdL = ["SHELL"]  # commands from file
    tagL = []
    tagbL = [
        "SHELL",  # run commands
        "END",  # end
    ]
    tagL = tagL + tagbL
    dutfS, drstS, dtxtS = doc_parse(rS, "T", tagL, cmdL)

    blkB = False
    blkS = ""
    lL = rS.split("\n")
    for lS in lL:
        if blkB:  # tag flag
            if "[[END]]" in lS:
                blkB = False
                exec(blkS, globals(), rivtD)
                blkS = ""
                continue
            blkS += lS.strip()
            continue
        for subS in tagL:  # tags
            if subS in lS:
                blkB = True
                continue
        for subS in cmdL:
            pass


def D(rS):
    """Publish doc files as .txt, .pdf  and .html
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    wrtdoc = rvdoc.Cmdp(rS, fD)
    msgS = wrtdoc.cmdx()
    print(f"{msgS}")
    sys.exit()


def S(rS):
    """Skip rivt string processing
    Args:
        rS (str): rivt string
    """
    shL = rS.split("\n")
    logging.info("section skipped at: " + shL[0])
    print("\n[" + shL[0].strip() + "] : section skipped " + "\n")


def X(rS):
    """exit rivt file processing
    Args:
        rS (str): rivt string
    """
    shL = rS.split("\n")
    logging.info("exit rivt file at: " + shL[0])
    print("\n[" + shL[0].strip() + "] : rivtlib exit " + "\n")
    sys.exit()
