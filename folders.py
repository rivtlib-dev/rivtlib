"""register folder structure"""

import __main__
import os
import sys
import fnmatch
from configparser import ConfigParser
from pathlib import Path

docS = "x.py"
docP = "/"

# check rivt file coming from IDE
curP = Path(os.getcwd())
rivtP = curP
print(f"{__name__=}")
if __name__ == "rivtlib.folders":
    argfileP = Path(__main__.__file__)
    print(f"{argfileP=}")
    rivN = argfileP.name
    if fnmatch.fnmatch(rivN, "r????-*.py"):
        rivP = Path(curP, rivN)
        print(f"{rivN=}")
        print(f"{curP=}")
    else:
        print(f"INFO     rivt file - {rivN}")
        print(f"INFO     The name must match 'rddss-filename.py' where")
        print(f"INFO     dd and ss are two digit integers")
        sys.exit()
else:
    print(f"INFO  file path does not include a rivt file  - {curP}")
    sys.exit()


# files and paths
baseS = rivN.split(".py")[0]
titleS = baseS.split("-")[1]
projP = os.path.dirname(curP)
bakP = curP / ".".join((baseS, "bak"))
prfxS = baseS[0:7]
toolsP = Path(projP, "data")
docsP = Path(projP, "docs")
print(f"{projP=}")

# output paths
reportP = Path(projP, "reports")
xrivtP = Path(projP, "xrivt")
tempP = Path(projP, "temp")
pypath = os.path.dirname(sys.executable)  # rivt package path
rivtpkgP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(tempP, "rivt-log.txt")
styleP = Path(projP, "reports", "pdf")
valfileS = baseS.replace("riv", "val") + ".csv"
readmeP = Path(projP, "README.txt")

# config file
print(f"{Path(projP, 'rivt-config.ini')=}")
config = ConfigParser()
config.read(Path(projP, "rivt-config.ini"))
headS = config.get('report', 'title')
footS = config.get('utf', 'foot1')

# global dictionaries and strings
rivtS = """"""                              # rivt input string
utfS = """"""                               # utf-8 output string
rmeS = """"""                               # readme output string
xremS = """"""                              # redacted readme string
rstS = """"""                               # reST output string
declareS = """"""                           # declares output string
assignS = """"""                            # assigns output string
rivtD = {}                                  # rivt object dictionary
folderD = {}                                # folder dictionary
for item in ["rivtP", "docsP", "readmeP", "reportP",
             "valfileS", "errlogP", "styleP", "tempP"]:
    folderD[item] = eval(item)
labelD = {
    "titleS": titleS,                       # document title
    "docnumS": prfxS,                       # doc number
    "sectS": "",                            # section title
    "secnumI": 0,                           # section number
    "widthI": 80,                           # print width
    "equI": 1,                              # equation number
    "tableI": 1,                            # table number
    "figI": 1,                              # figure number
    "pageI": 1,                             # starting page number
    "noteL": [0],                           # footnote counter
    "footL": [1],                           # foot counter
    "unitS": "M,M",                         # units
    "descS": "2",                           # description or decimal places
    "headrS": "",                           # header string
    "footrS": "",                           # footer string
    "tocB": False,                          # table of contents
    "docstrB": False,                       # print doc strings
    "subB": False                           # sub values in equations
}
