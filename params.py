"""parameter dictionaries and lists"""

import os
import sys
from pathlib import Path


def dicts(rivN, rivP, rivtP):
    """dictionaries of parameters

    Args:
        rivN (_type_): _description_
        curP (_type_): _description_
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
    projP = Path(os.path.dirname(rivP))
    bakP = Path(rivP / ".".join((baseS, "bak")))
    prfxS = baseS[1:5]
    toolsP = Path(projP, "tools")
    docsP = Path(projP, "docs")
    insP = Path(rivP / ("ins" + divnumS))
    valsP = Path(rivP / ("vals" + divnumS))

    # output paths
    pypath = os.path.dirname(sys.executable)  # rivt package path
    rivtpkgP = os.path.join(pypath, "Lib", "site-packages", "rivt")
    reportP = Path(projP, "reports")
    xrivtP = Path(projP, "xrivt")
    tempP = Path(projP, "temp")
    errlogP = Path(tempP, "rivt-log.txt")
    styleP = Path(projP, "docs", "pdf")
    valfileS = baseS.replace("riv", "val") + ".csv"
    readmeP = Path(projP, "README.txt")
    ossP = Path(projP / "oss")

    # global dicts
    rivtD = {}

    folderD = {}
    for item in ["rivtP", "docsP", "readmeP", "reportP", "projP",
                 "valsP", "insP", "errlogP", "styleP", "tempP"]:
        folderD[item] = eval(item)

    labelD = {
        "rivN": rivN,                           # file name
        "divnumS": divnumS,                     # div number
        "baseS": baseS,                         # file base name
        "titleS": titleS,                       # document title
        "docnumS": prfxS,                       # doc number
        "sectS": "",                            # section title
        "secnumI": 0,                           # section number
        "widthI": 80,                           # print width
        "equI": 0,                              # equation number
        "tableI": 0,                            # table number
        "figI": 0,                              # figure number
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

    return folderD, labelD, rivtD
