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

Doc comment settings:
    # rc singledoc: True; False  (default is False)


Globals:
    utfS (str): utf doc string
    rs2S (str): rstpdf doc string
    rstS (str): texpdf doc string
    lablD (dict): formatting parameters
    foldD (dict): folder and file paths
    rivtD (dict): calculated values

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
from rivtlib import rvdoc, rvparse

# region - rivt file name and paths
rivtP = Path(os.getcwd())
reptP = Path(os.path.dirname(rivtP))
rivtN = os.path.basename(__main__.__file__)
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
apilogN = docnumS + "api.txt"
errlogN = docnumS + "log.txt"
publicP = Path(rivtP, "public")
srcP = Path(rivtP, "src")
storeP = Path(rivtP, "store")
pubP = Path(rivtP, "publish")
logsP = Path(storeP, "logs")
# endregion

# region - rivt file flags
prflagB = False
rvsingleB = False
with open(rivtT, "r") as f1:  # noqa: F405
    rivtL = f1.readlines()
for lnS in rivtL:
    if lnS[0:4] == "# rv":
        if "singledoc" and "True" in lnS:
            rvsingleB = True

# print(f"={rvsingleB}")

if rvsingleB:
    errlogT = Path(rivtP, errlogN)
    apilogT = Path(rivtP, apilogN)
    bakT = Path(rivtP, bakN)
    rivtT = Path(rivtP, rivtN)
else:
    errlogT = Path(logsP, errlogN)
    apilogT = Path(logsP, apilogN)
    bakT = Path(logsP, bakN)
    rivtT = Path(rivtP, rivtN)
try:
    package_version = version("rivtlib")
    verS = f"rivtlib version: {package_version}"
except Exception as e:
    verS = f"rivtlib version not available: {e}"
# endregion

# region - logs
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
# api log
with open(apilogT, "w") as f4:
    f4.write("API log: " + rivtN + "\n")
    f4.write("---------------------------------------\n")
# end region

# region - dictionaries
rivtD = {
    "metaD": {
        "authors": " - ",
        "version": " - ",
        "email": " - ",
        "repo": " - ",
        "license": " - ",
        "fork1": [" - "],
        "fork2": [" - "],
    },
}
metaD = {}  # metadata
foldD = {  # folders
    "errlogT": errlogT,
    "apilogT": apilogT,
    "bakT": bakT,
    "rvsingleB": rvsingleB,
    "pthS": " ",
    "srcnS": " ",
    "rivtN": rivtN,  # file name
    "rivtT": rivtT,  # full path name
    "rivtP": Path(os.getcwd()),
    "rbaseS": rbaseS,  # file base name
    "reptfoldN": os.path.dirname(rivtP),
    "docP": Path(rivtP, "rivDocs"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(rivtP, "README.txt"),
    "rivtpubP": Path(rivtP, "publish"),
    "rivtpub_P": Path(rivtP),
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
}
lablD = {  # dictionary of labels
    "rvtypeS": "",  # section type r,i,v,t,d
    "docnumS": rbaseS[0:6],  # doc number
    "divS": rbaseS[2:3],  # div number
    "sdivS": rbaseS[3:5],  # subdiv
    "docnameS": rbaseS[6:].replace("-", " "),  # document name
    "replablS": reptP.name[5:],
    "valprfx": rbaseS[0:6].replace("rv", "v"),
    "sectS": "",  # section title
    "secnumI": 0,  # section number
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
drs2S = ""
drstS = ""
dhtmS = ""
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


def doc_parse(rS, tS, tagL, cmdL):
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
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
    rsL = rS.split("\n")
    conC = rvparse.Rs(tS, rsL, foldD, lablD, rivtD, prflagB, rivtL)
    sutfS, srs2S, srstS, foldD, lablD, rivtD = conC.content(tS, tagL, cmdL)
    dutfS += sutfS
    drs2S += srs2S
    drstS += srstS
    return dutfS, drs2S, drstS


def R(rS):
    """Run shell command
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
    cmdL = ["SHELL"]  # commands from file
    tagL = []
    tagbL = [
        "[SHELL]]",  # run commands
        "[END]]",  # end
        "[NEWPAGE]]",  # new page
    ]
    tagL = tagbL + tagL
    dutfS, drs2S, drstS = doc_parse(rS, "R", tagL, cmdL)


def I(rS):  # noqa: E743
    """Insert static source
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
    cmdL = [
        "IMAGE",  # insert image from file
        "IMAGE2",  # insert adjacent images from file
        "TABLE",  # insert table from file
        "TEXT",  # insert text from filoe
    ]
    tagL = [
        "C]",  # center text
        "R]",  # right justify text
        "M]",  # math
        "L]",  # LaTeX math
        "#]",  # footnote
        "G]",  # glossary
        "S]",  # section link
        "D]",  # doc link
        "U]",  # url link
        "V]",  # var value
        "E]",  # equation label
        "T]",  # table label
        "F]",  # figure label
    ]
    tagbL = [
        "[INDENT]]",  # indent
        "[ITALIC]]",  # indent and italicize
        "[ENDNOTES]]",  # note description
        "[TEXT]]",  # format text
        "[TOPIC]]",  # topic
        "[END]]",  # end
        "[NEWPAGE]]",  # new page
    ]
    tagL = tagL + tagbL
    dutfS, drs2S, drstS = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values calculate
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
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
        "V]",  # var value
        "E]",  # equation label
        "T]",  # table label
        "F]",  # figure label
    ]
    tagbL = [
        "[PYTHON]]",  # execute Python script
        "[END]]",  # end
        "[NEWPAGE]]",  # new page
    ]
    tagL = tagL + tagbL
    dutfS, drs2S, drstS = doc_parse(rS, "V", tagL, cmdL)


def T(rS):
    """Python and Markup Tools
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
    cmdL = [
        "PYTHON",  # execute Python file
        "MARKUP",  # execute script file
    ]
    tagL = []
    tagbL = [
        "[PYTHON]]",  # execute Python script
        "[MARKUP]]",  # execute script
        "[END]]",  # end
        "[NEWPAGE]]",  # new page
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
    """Publish Doc files

    Writes docs as .txt, .pdf (reportLab or tex) and .html

    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS, foldD, lablD, rivtD
    # config = ConfigParser()
    # config.read(Path(reptfoldP, "rivt-doc.ini"))
    # headS = config.get("report", "title")
    # footS = config.get("utf", "foot1")
    cmdL = ["PUBLISH", "PDFATTACH"]
    tagbL = ["[LAYOUT]]", "[METADATA]]"]
    tagL = []
    tagL = tagL + tagbL
    wrtdoc = rvdoc.Cmdp(
        rS, foldD, lablD, cmdL, tagL, dutfS, drs2S, drstS, rivtD
    )
    mssgS = wrtdoc.cmdx()
    print("\n" + f"{mssgS}")
    sys.exit()


def S(rS):
    """skip rivt string processing
    Args:
        rS (str): rivt string
    """
    global dutfS, drs2S, drstS, dhtmS

    shL = rS.split("\n")
    sutfS = srsrS = srstS = (
        "\n[" + shL[0].strip() + "] : section skipped " + "\n"
    )
    print(sutfS)
    dutfS += sutfS
    drs2S += srsrS
    drstS += srstS


def X(rS):
    """exit rivt file processing
    Args:
        rS (str): rivt string
    """
    shL = rS.split("\n")
    logging.info("exit rivt file at: " + shL[0])
    print("\n[" + shL[0].strip() + "] : rivtlib exit " + "\n")
    sys.exit()
