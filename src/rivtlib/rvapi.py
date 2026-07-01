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
import glob
import logging
import os
import shutil
import subprocess
import sys
import warnings
from importlib.metadata import version
from pathlib import Path

import __main__
import rivtlib.rvunits as rvunit
from rivtlib import rvdoc, rvmarkup, rvparse

# parse command line arguments
reptP = Path(os.getcwd())
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
print("--------------", reptP.name)
if reptP.name == "rivt-report":
    reptflagS = "doc"
    rstdocsP = Path(reptP, "_rstdocs")
    txtdocsP = Path(reptP, "_published", "txtdocs")
    pubdocP = Path(reptP, "_published")
    pdfpubP = Path(pubdocP, "pdfdocs")
    storeP = Path(reptP, "rv_stor")
    errlogN = docnumS + "log.txt"
    logsP = Path(storeP, "logs")
    errlogT = Path(logsP, errlogN)
    bakT = Path(logsP, bakN)
    rivtT = Path(reptP, rivtN)
    rvreadmeT = Path(reptP.parent, "README.txt")
    docreadmeT = Path(reptP, "_published", "readme", docnumS + "readme.txt")
    pubreadmeT = Path(publicP, "README.txt")
else:
    reptflagS = "chapter"
    pubdocP = " "
    rstdocsP = Path(reptP.parent, "_rstdocs")
    txtdocsP = Path(reptP.parent, "_txtdocs")
    pdfpubP = Path(reptP.parent, "_pdfdocs")
    storeP = Path(reptP.parent, "_rvstor")
    logsP = Path(storeP, "logs")
    errlogN = docnumS + "log.txt"
    errlogT = Path(logsP, errlogN)
    bakT = Path(logsP, bakN)
    rivtT = Path(reptP, rivtN)
    rvreadmeT = Path(reptP.parent, "README.txt")
    docreadmeT = Path(reptP.parent, "_rvstor", docnumS + "readme.txt")
    pubreadmeT = " "
# logs and backups
print("-----------------------", reptflagS)
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
    "privB": "True",  # do not write to public
    "docB": "True",  # add to doc
    "mergeB": "False",  # merge to prev section
    "autocfgB": "True",  # config format from metadata
    "runtypeS": "",  # type for rv.R
    "reptflagS": reptflagS,  # rivt-report, rivtbook or chapter
    "cntflgI": 0,  # counter flag - skips transition for first section
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
    if tyS == "R":
        dutfS += conC.sutfS
        drstS += conC.srstS
        dtxtS += conC.stxtS
        return dutfS, dtxtS, drstS
    sutfS, stxtS, srstS, fD, lD, rivtD = conC.content(tyS, tagL, cmdL)
    if tyS == "I" or tyS == "V":
        if lD["docB"] == "True":
            dutfS += sutfS
            drstS += srstS
            dtxtS += stxtS
    else:
        pass

    return dutfS, dtxtS, drstS


def R(rS):
    """Run API - Evaluate and insert scripts

        types - specified in header
        --------------------------
        endnotes
        rst
        python
        html
        latex - require texlive cli
        mermaid - requires mermaid cli
        dot - requires graphviz cli

    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD, rivtD

    cmdL = []
    tagL = []
    tagbL = []
    tagL = tagL + tagbL
    dutfS, dtxtS, drstS = doc_parse(rS, "R", tagL, cmdL)
    r1S = rS.split("\n", 1)[1]
    uS, tS, rS = rvmarkup.typex(lD, r1S)
    dutfS += uS
    dtxtS += tS
    drstS += rS


def I(rS):  # noqa: E743
    """Insert API
    Insert static files e.g. tables, images and text

    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD

    cmdL = [
        "IMAGE",  # insert image from file
        "IMAGE2",  # insert adjacent images from file
        "TEXT",  # format text from file
        "TABLE",  # insert table from file
    ]
    tagL = [
        "G",  # glossary term
        "S",  # section link
        "U",  # url link
        "D",  # download link
        "R",  # right justify
        "C",  # center bold
        "B",  # bold line
        "M",  # ascii math
        "L",  # LaTeX math
        "V",  # var value
        "T",  # table label
        "#",  # footnote
    ]
    tagbL = [
        "TEXT",  # format text
        "TABLE",  # format inline rst and write to csv
        "END",  # end
    ]
    tagL = tagL + tagbL
    dutfS, dtxtS, drstS = doc_parse(rS, "I", tagL, cmdL)


def V(rS):
    """Values API
    Args:
        rS (str): rivt string
    """
    global dutfS, dtxtS, drstS, fD, lD, rivtD, vdescD

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
        "IMAGE",  # image from file
        "IMAGE2",  # adjacent images frome files
        "TABLE",  # table from file
        "VALTABLE",  # value table from file
        "PYTHON",  # execute Python file
        "FUNCTION",  # evaluate function
        " ==: ",  # define value
        " <=: ",  # assign value
        " :=: ",  # assign function value
    ]
    tagL = [
        "R",  # right justify
        "C",  # center bold
        "B",  # bold line of text
        "M",  # math format
        "L",  # LaTeX format
        "V",  # var value
        "C",  # bold center text
        "T",  # table label
    ]
    tagbL = [
        "ARGS",
    ]
    tagL = tagL + tagbL
    dutfS, dtxtS, drstS = doc_parse(rS, "V", tagL, cmdL)


def T(rS):
    """Tools API
    Execute shell commands

    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD

    rL = rS.split("\n", 1)
    fileS = lD["toolprfx"] + str(lD["secnumI"]) + ".txt"
    fileP = Path(fD["storeP"], fileS)
    with open(fileP, "w") as file1:
        file1.write("\n".join(rL[1:]))

    blkB = False
    blkS = ""
    rvL = rS.split("\n")
    for lS in rvL[1:]:
        lS = lS[4:]
        # print(lS)
        if lS[:8] == "| COPY |":
            reptS = str(fD["reptP"])
            if "-rvsrc-" in lS:
                lS = lS.replace("-rvsrc-", reptS + "/rvsrc")
            lcL = lS.split("|")
            srcP = str(Path(os.path.expandvars(lcL[2].strip())))
            destP = str(Path(os.path.expandvars(lcL[3].strip())))
            fileS = lcL[4].strip()
            source_pattern = str(Path(srcP, fileS))
            print("\n---| COPY | ---")
            print(f"from: {source_pattern}")
            print(f"to: {destP}")
            for fpath in glob.glob(source_pattern):
                shutil.copy(fpath, destP)
            print(f"---| COPIED |--- {fileS} from {srcP} to {destP}")
        elif lS[:9] == "--- | SHELL | -----":
            lcL = lS.split("|")
            cmdS = lcL[3].strip()
            srcP = Path(fD["reptP"], lcL[2].strip(), cmdS)
            cmdS = f'"{str(srcP)}"'
            try:
                # This will block until finished or raise  error
                print(
                    "\n-----------------| Run shell command |------------------\n"
                )
                print(f"{cmdS}")
                print("........\n")
                result = subprocess.run(cmdS, shell=True, check=True)
                print("\n shell message: ", result)
                print(
                    "\n--------- | Shell command finished |------------------\n"
                )
            except subprocess.CalledProcessError as e:
                print(
                    f"--------------- | Command failed with exit code {e.returncode}"
                )
        elif "_[[WRITE]]" in lS:
            blkB = True  # tag flag
            wfS = lS.split("]]")[1].strip()
            writeP = Path(fD["reptP"], wfS)
            continue
        else:
            if blkB:
                if "_[[END]]" in lS:
                    try:
                        subS = eval(blkS, globals(), rivtD)
                    except Exception:
                        subS = blkS
                    with open(writeP, "w") as f2:
                        f2.write(subS)
                    print(f"File {wfS} written to: {fD['reptP']}")
                    blkB = False
                    blkS = ""
                    continue
                blkS += lS + "\n"
                continue
            pass


def D(rS):
    """Doc API
    Publish doc files as .txt, .pdf, .html

    Args:
        rS (str): rivt string
    """
    global dutfS, drstS, dtxtS, fD, lD, rivtD
    wrtdoc = rvdoc.Cmdp(rS, fD, lD, dutfS, drstS, dtxtS)
    print(f"{wrtdoc.cmdx()}")
    print("\n>>>>>>>>>>>>>>>>>>> End of rivt file\n\n")
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
    """Exit rivt file processing

    Args:
        rS (str): rivt string
    """
    shL = rS.split("\n")
    logging.info("exit rivt file at: " + shL[0])
    print("\n[" + shL[0].strip() + "] : rivtlib exit " + "\n")
    sys.exit()
