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

if __name__ == "rivtlib.rparam":
    rivtT = Path(__main__.__file__)
    rivtN = rivtT.name
    patternS = "r[0-9][0-9][0-9]0-9]-*.py"
    if fnmatch.fnmatch(rivtN, patternS):
        rivtfP = Path(rivtP, rivtN)
else:
    print(f"""The rivt file name is - {rivtN} -. The file name must""")
    print("""match "rddss-anyname.py", where dd and ss are two-digit integers""")
    sys.exit()

# print(f"{rivtfP=}")
# print(f"{rivtP=}")
# print(f"{rivtnS=}")
# print(f"{__name__=}")
# print(f"{modnameS=}")

errlogT = Path(rivtP, "temp", "rivt-log.txt")
modnameS = __name__.split(".")[1]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=errlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")

# region - file paths
# read
pthS = " "
rbaseS = rivtN.split(".")[0]
prfxS = rivtN[0:5]
rnumS = rivtN[1:5]
dnumS = prfxS[1:3]
rnumS = rivtN[1:5]
divnumS = "d" + dnumS + "-"
rstnS = rbaseS + ".rst"
txtnS = rbaseS + ".txt"
pdfnS = rbaseS + ".pdf"
htmnS = rbaseS + ".html"
bakN = rbaseS + ".bak"
docP = Path(projP, "docs")
srcP = insP = Path(projP, "source")
styleP = Path(projP, "styles")
titleS = rivtN.split("-")[1]
# write
bakT = Path(rivtP, bakN)
rbakT = Path(rivtP, rbaseS + ".bak")
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
styleP = Path(projP, "docs", "style")
reportP = Path(projP, "docs", "report")
ossP = Path(projP / "rivtos")
valnS = prfxS.replace("r", "v")
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
    "rivtN": rivtT.name,
    "baseS": rbaseS,  # file base name
    "rivtP": Path(os.getcwd()),
    "projP": Path(os.path.dirname(rivtP)),
    "docP": Path(projP, "docs"),
    "bakT": Path(rivtP, bakN),
    "errlogT": Path(rivtP, "temp", "rivt-log.txt"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(projP, "README.txt"),
    "reportP": Path(projP, "docs", "report"),
    "styleP": Path(projP, "docs", "style"),
    "runP": Path(srcP, "r" + dnumS),
    "insP": Path(srcP, "i" + dnumS),
    "valP": Path(srcP, "v" + dnumS),
    "tooP": Path(srcP, "t" + dnumS),
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
    "colorS": "",  # section background color
    "valexpS": "",  # list of values for export
    "unitS": "M,M",  # units
}
# endregion

# region - values dict
rivtD = {}  # shared calculated values
# endregion
