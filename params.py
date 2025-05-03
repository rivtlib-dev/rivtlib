import os
import sys
from pathlib import Path
from fpdf import FPDF


"""folders and global dictionaries"""

rivN = "r000-x.py"
# input paths
baseS = rivN.split(".py")[0]
titleS = baseS.split("-")[1]
dnumS = baseS.split("-")[0][1:3]
projP = Path(os.path.dirname(curP))
bakP = Path(curP / ".".join((baseS, "bak")))
prfxS = baseS[0:7]
toolsP = Path(projP, "tools")
docsP = Path(projP, "docs")
insP = Path(curP / ("ins" + dnumS))
valsP = Path(curP / ("vals" + dnumS))
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
# global dicts
rivtD = {}
folderD = {}
for item in ["rivtP", "docsP", "readmeP", "reportP",
             "valsP", "insP", "errlogP", "styleP", "tempP"]:
    folderD[item] = eval(item)
labelD = {}
labelD = {
    "baseS": baseS,                         # file base name
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



def dicts(rivN, rivP, rivtP):
    """dictionaries of parameters

    Args:
        rivN (_type_): _description_
        rivP (_type_): _description_
        rivtP (_type_): _description_

    Returns:
        folderD (dict): dictionary of paths
        folderD (dict): dictionary of paths
        folderD (dict): dictionary of paths
    """

    # input paths
    baseS = rivN.split(".py")[0]
    titleS = baseS.split("-")[1]
    divnumS = baseS.split("-")[0][1:3]
    valN = baseS.split("-")[0]
    valN = valN.replace("r", "v", 1) + "-" + "qqqqqq" + ".csv"
    pdfN = baseS + ".pdf"
    rstpN = baseS + ".rst"
    rstN = baseS + ".rst"
    txtN = baseS + ".txt"
    prfxS = baseS[1:5]
    # input paths
    projP = Path(os.path.dirname(rivP))
    bakP = Path(rivP / ".".join((baseS, "bak")))
    toolsP = Path(projP, "tools")
    docsP = Path(projP, "docs")
    styleP = Path(docsP, "styles")
    # output paths
    pypathS = os.path.dirname(sys.executable)
    rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
    reportP = Path(projP, "docs")
    xrivtP = Path(projP, "xrivt")
    tempP = Path(rivP, "temp")
    errlogP = Path(tempP, "rivt-log.txt")
    valsP = Path(projP, "vals")
    valP = Path(valsP, valN)
    readmeP = Path(projP, "README.txt")
    ossP = Path(projP / "oss")
    pthS = " "
    labelD = {
        "rivN": rivN,                           # file name
        "divnumS": divnumS,                     # div number
        "baseS": baseS,                         # file base name
        "titleS": titleS,                       # document title
        "docnumS": prfxS,                       # doc number
        "sectS": "",                            # section title
        "secnumI": 0,                           # section number
        "widthI": 80,                           # print width
        "equI": 1,                              # equation number
        "tableI": 1,                            # table number
        "figI": 1,                              # figure number
        "valueI": 1,                            # value number
        "pageI": 1,                             # starting page number
        "noteL": [0],                           # footnote counter
        "footL": [1],                           # foot counter
        "descS": "2",                           # description or decimal places
        "headrS": "",                           # header string
        "footrS": "",                           # footer string
        "tocB": False,                          # table of contents
        "docstrB": False,                       # print doc strings
        "subB": False,                          # sub values in equations
        "valexpS": ""                           # list of values for export
        "coverS"
    }

    folderD = {}
    for item in ["rivP", "rivtP", "docsP", "readmeP", "reportP", "projP", "docsP",
                 "pthS", "rstN", "rstpN", "valN", "pdfN", "txtN", "errlogP",
                 "styleP",  "tempP", "valsP", ]:
        folderD[item] = eval(item)

    rivtpD = {}
    rivtvD = {}

    return folderD, labelD, rivtpD, rivtvD
