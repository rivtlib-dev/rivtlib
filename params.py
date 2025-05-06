import os
import sys
from pathlib import Path

"""folders and global dictionaries"""

rivtP = Path(os.getcwd())
rivtN = "not found"
# input paths
baseS = rivtN.split(".py")[0]
titleS = baseS.split("-")[1]
dnumS = baseS.split("-")[0][1:3]
projP = Path(os.path.dirname(rivtP))
bakP = Path(rivtP / ".".join((baseS, "bak")))
prfxS = baseS[0:7]
toolsP = Path(projP, "tools")
docsP = Path(projP, "docs")
insP = Path(rivtP / ("ins" + dnumS))
valsP = Path(rivtP / ("vals" + dnumS))
print(f"{insP=}")
print(f"{valsP=}")
# output paths
reportP = Path(projP, "reports")
xrivtP = Path(projP, "xrivt")
tempP = Path(projP, "temp")
pypath = os.path.dirname(sys.executable)  # rivt package path
rivtpkgP = os.path.join(pypath, "Lib", "site-packages", "rivt")
errlogP = Path(tempP, "rivt-log.txt")
styleP = Path(projP, "docs", "pdf")
valfileS = baseS.replace("riv", "val") + ".csv"
readmeP = Path(projP, "README.txt")
print(f"{projP=}")
print(f"{rivtP=}")

# input paths
pthS = " "
rivbaseS = rivtnS.split(".py")[0]
titleS = rivbaseS.split("-")[1]
divnumS = rivbaseS.split("-")[0][1:3]
valN = rivbaseS.split("-")[0]
valN = valN.replace("r", "v", 1) + "-" + "qqqqqq" + ".csv"
pdfN = rivbaseS + ".pdf"
rstpN = rivbaseS + ".rst"
rstN = rivbaseS + ".rst"
txtN = rivbaseS + ".txt"
prfxS = rivbaseS[1:5]
projP = Path(os.path.dirname(rivtP))
bakP = Path(rivtP / ".".join((rivbaseS, "bak")))
toolsP = Path(projP, "tools")
docsP = Path(projP, "docs")
styleP = Path(docsP, "styles")
# output paths
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
reportP = Path(projP, "docs")
xrivtP = Path(projP, "xrivt")
tempP = Path(rivtP, "temp")
errlogP = Path(tempP, "rivt-log.txt")
valsP = Path(projP, "vals")
valP = Path(valsP, valN)
readmeP = Path(projP, "README.txt")
ossP = Path(projP / "oss")


def dicts(rivtnS, rivtP, rivtfP):
    """dictionaries of parameters

    Args:
        rivtS (str): rivt file name
        rivtP (str): rivt file path
        rivtfP (str): rivt file full path

    Returns:
        folderD (dict): dictionary of paths
        lablelD (dict): dictionary of paths
        rivtD (dict): dictionary of paths
    """

    rivtvD = {}  # rivt values dictionary

    folderD = {}
    for item in [
        "rivP",
        "rivtP",
        "docsP",
        "readmeP",
        "reportP",
        "projP",
        "docsP",
        "pthS",
        "rstN",
        "rstpN",
        "valN",
        "pdfN",
        "txtN",
        "errlogP",
        "styleP",
        "valsP",
        "rivtP",
        "valsP",
        "insP",
        "styleP",
        "tempP",
    ]:
        folderD[item] = eval(item)

    labelD = {
        "rivN": rivtN,  # file name
        "divnumS": divnumS,  # div number
        "baseS": baseS,  # file base name
        "titleS": titleS,  # document title
        "docnumS": prfxS,  # doc number
        "sectS": "",  # section title
        "secnumI": 0,  # section number
        "widthI": 80,  # print width
        "equI": 1,  # equation number
        "tableI": 1,  # table number
        "figI": 1,  # figure number
        "valueI": 1,  # value number
        "pageI": 1,  # starting page number
        "noteL": [0],  # footnote counter
        "footL": [1],  # foot counter
        "descS": "2",  # description or decimal places
        "headrS": "",  # header string
        "footrS": "",  # footer string
        "tocB": False,  # table of contents
        "docstrB": False,  # print doc strings
        "subB": False,  # sub values in equations
        "valexpS": ""  # list of values for export
        "baseS": baseS,  # file base name
        "titleS": titleS,  # document title
        "docnumS": prfxS,  # doc number
        "sectS": "",  # section title
        "secnumI": 0,  # section number
        "widthI": 80,  # print width
        "equI": 1,  # equation number
        "tableI": 1,  # table number
        "figI": 1,  # figure number
        "pageI": 1,  # starting page number
        "noteL": [0],  # footnote counter
        "footL": [1],  # foot counter
        "unitS": "M,M",  # units
        "descS": "2",  # description or decimal places
        "headrS": "",  # header string
        "footrS": "",  # footer string
        "tocB": False,  # table of contents
        "docstrB": False,  # print doc strings
        "subB": False,  # sub values in equations
    }

    return folderD, labelD, rivtvD
