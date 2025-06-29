"""
File paths and labels
"""

import fnmatch
import logging
import os
import sys
import warnings
from pathlib import Path

import __main__

rivtP = Path(os.getcwd())
projP = Path(os.path.dirname(rivtP))
modnameS = __name__.split(".")[1]

if __name__ == "rivtlib.rvparam":
    rivtT = Path(__main__.__file__)
    rivtN = rivtT.name
    patternS = "r[0-9][0-9][0-9]0-9]-*.py"
    if fnmatch.fnmatch(rivtN, patternS):
        rivtfP = Path(rivtP, rivtN)
else:
    print(f"""The rivt file name is - {rivtN} -. The file name must""")
    print("""match "rddss-anyname.py", where dd and ss are two-digit integers""")
    sys.exit()

# print(f"{rivtT=}")
# print(f"{__name__=}")
# print(f"{modnameS=}")

# input files
prfxS = rivtN[0:6]
rnumS = rivtN[2:6]
dnumS = prfxS[2:4]

errlogT = Path(projP, "temp", prfxS + "-log.txt")
modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")

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
docP = Path(projP, "rivtdocs")
srcP = Path(projP, "sources")
styleP = Path(projP, "styles")
titleS = rivtN.split("-")[1]

# output files
bakT = Path(rivtP, bakN)
rbakT = Path(rivtP, rbaseS + ".bak")
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
styleP = Path(projP, "style")
reportP = Path(projP, "rivtdocs", "report")
ossP = Path(projP / "rivtos")
valN = prfxS.replace("rv", "v")

# read/write
valP = Path(srcP, "v" + dnumS)

# print(f"{projP=}")
# print(f"{rivtP=}")
# print(f"{insP=}")
# print(f"{valsP=}")
# endregion

# region - folders dict
folderD = {
    "pthS": " ",
    "rivtT": rivtT,  # full path and name
    "rivtN": rivtT.name,  # file name
    "baseS": rbaseS,  # file base name
    "rivtP": Path(os.getcwd()),
    "projP": Path(os.path.dirname(rivtP)),
    "docP": Path(projP, "rivtdocs"),
    "bakT": Path(rivtP, bakN),
    "errlogT": errlogT,
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(projP, "README.txt"),
    "reportP": Path(projP, "rivtdocs", "report"),
    "styleP": Path(projP, "rivtdocs", "style"),
    "srcP": srcP,
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
labelD = {
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
    "noteL": [0],  # footnote counter
    "footL": [1],  # foot counter
    "descS": "2",  # description or decimal places
    "headrS": "",  # header string
    "footrS": "",  # footer string
    "tocB": False,  # table of contents
    "docstrB": False,  # print doc strings
    "subB": False,  # sub values in equations
    "rvtosB": False,  # open-source rivt flag
    "valexpS": "",  # list of values for export
    "unitS": "M,M",  # units
    "colorL": ["red", "blue", "yellow", "green", "gray"],  # pallete
    "colorS": "none",  # background color
}
# endregion

# region - values dict
rivtD = {}  # shared calculated values
# endregion
