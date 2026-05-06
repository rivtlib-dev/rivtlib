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
rivtP = Path(os.getcwd())
reptP = Path(os.path.dirname(rivtP))
try:
    rivtN = os.path.basename(__main__.__file__)
except Exception:
    rivtN = os.path.basename(__main__.__name__)
rivtT = Path(rivtP, rivtN)
print(rivtN, rivtT)
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")

if fnmatch.fnmatch(rivtN, "rv[A-Z0-9][0-9][0-9]-*.py"):
    pass
else:
    print(f"""The rivt file name provided was {rivtN}""")
    print("""The file name must match rvDss-filename.py""")
    print("""where D is an alpha-numeric division label""")
    print("""and ss is a two-digit subdivision integer""")
    sys.exit()

rbaseS = rivtN.split(".")[0]
rivtpN = rivtN.replace("rv", "rv-")
docnumS = rbaseS[0:6]
bakN = rbaseS + ".bak"
errlogN = docnumS + "log.txt"
rootP = rivtP.parent
publicP = Path(rootP, "_rivt-public")
storeP = Path(rivtP, "_stored")
pubP = Path(rivtP, "_published")
rstdocsP = Path(rivtP, "_rstdocs")
srcP = Path(rivtP, "src")
logsP = Path(storeP, "logs")
errlogT = Path(logsP, errlogN)
bakT = Path(logsP, bakN)
rivtT = Path(rivtP, rivtN)
# endregion

# region - logs and comment variables
rvpubB = False
with open(rivtT, "r") as f1:  # noqa: F405
    rivtL = f1.readlines()
for lnS in rivtL:
    if lnS[0:4] == "# rv":
        if "setpublic" and "True" in lnS:
            rvpubB = True
# print(f"={rvpubB}")
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
rivtD = {}
rvunitD = vars(rvunit)
rivtD = rivtD | rvunitD
metaD = {}  # metadata
fD = {  # folders
    "errlogT": errlogT,
    "bakT": bakT,
    "rvpubB": rvpubB,
    "pthS": " ",
    "srcnS": " ",
    "rivtN": rivtN,  # file name
    "rivtT": rivtT,  # full path name
    "rivtP": Path(os.getcwd()),
    "rbaseS": rbaseS,  # file base name
    "reptfDN": os.path.dirname(rivtP),
    "docP": Path(rivtP, "rivtDocs"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(rivtP, "README.txt"),
    "rstdocsP": rstdocsP,
    "rivtpubP": pubP,
    "pdfpubP": Path(pubP, "pdfdocs"),
    "htmlpubP": Path(pubP, "docs"),
    "publicT": Path(rivtP, "public", rivtpN),
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
    "sdivS": rbaseS[3:5],  # subdiv
    "docnameS": rbaseS[6:].replace("-", " "),  # document name
    "replablS": reptP.name[5:],
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
    "publicB": False,  # public section
    "showB": True,  # print section to doc
    "mergeB": False,
    "apiB": True,
    "tocB": False,  # table of contents
    "subB": False,  # sub values in equations
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "none",  # topic background color
    "widthI": 80,  # print width
}
# endregion

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
    conC = rvparse.Rs(tyS, rsL, fD, lD, rivtD, rivtL)
    sutfS, srstS, stxtS, fD, lD, rivtD = conC.content(tyS, tagL, cmdL)
    dutfS += sutfS
    drstS += srstS
    dtxtS += stxtS

    return dutfS, drstS, dtxtS


def R(rS):
    """Run shell command
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    cmdL = ["SHELL"]  # commands from file
    tagL = []
    tagbL = [
        "SHELL",  # run commands
        "END",  # end
        "NEWPAGE",  # new page
    ]
    tagL = tagbL + tagL
    dutfS, drstS, dtxtS = doc_parse(rS, "R", tagL, cmdL)


def I(rS):  # noqa: E743
    """Insert static source
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    cmdL = [
        "IMAGE",  # insert image from file
        "IMAGE2",  # insert adjacent images from file
        "TABLE",  # insert table from file
        "TEXT",  # insert text from filoe
    ]
    tagL = [
        "C",  # center text
        "R",  # right justify text
        "B",  # bold text
        "I",  # italic text
        "M",  # math
        "L",  # LaTeX math
        "#",  # footnote
        "G",  # glossary
        "S",  # section link
        "U",  # url link
        "V",  # var value
        "E",  # equation label
        "T",  # table label
        "F",  # figure label
    ]
    tagbL = [
        "INDENT",  # indent
        "ITALIC",  # indent and italicize
        "ENDNOTES",  # note description
        "TABLE",  # note description
        "TEXT",  # format text
        "TOPIC",  # topic
        "END",  # end
    ]
    tagL = tagL + tagbL
    dutfS, drstS, dtxtS = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values calculate
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
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
        "V",  # var value
        "E",  # equation label
        "T",  # table label
        "F",  # figure label
        "B",  # bold text
        "I",  # italic text
    ]
    tagbL = [
        "PYTHON",  # execute Python script
        "END",  # end
    ]
    tagL = tagL + tagbL
    dutfS, drstS, dtxtS = doc_parse(rS, "V", tagL, cmdL)


def T(rS):
    """Markup tools
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    cmdL = [
        "MARKUP",  # execute script file
    ]
    tagL = []
    tagbL = [
        "MARKUP",  # execute script
        "END",  # end
    ]
    tagL = tagL + tagbL

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
    wrtdoc = rvdoc.Cmdp(rS, fD, lD, rivtD, dutfS, drstS, dtxtS)
    msgS = wrtdoc.cmdx()
    print(f"{msgS}")
    sys.exit()


def S(rS):
    """Skip rivt string processing
    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS

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
