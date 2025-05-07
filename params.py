import os
import sys
from pathlib import Path

"""folders and global dictionaries"""

rivtP = Path(os.getcwd())
rivtnS = "not found"
projP = Path(os.path.dirname(rivtP))

# read paths
pthS = " "
rbaseS = rivtnS.split(".")[0]
prfxS = rivtnS[0:5]
rnumS = rivtnS[1:5]
dnumS = prfxS[1:3]
rnumS = rivtnS[1:5]
rstnS = rbaseS + ".rst"
txtnS = rbaseS + ".txt"
pdfnS = rbaseS + ".pdf"
htmnS = rbaseS + ".html"
divnumS = "d" + dnumS + "-"
valnS = prfxS.replace("r", "v") + ".csv"
docP = Path(projP, "doc")
srcP = insP = Path(projP, "src")
insP = Path(srcP, "ins")
valsP = Path(srcP, "vls")
toolsP = Path(srcP, "vls")
styleP = Path(docP, "styles")
titleS = rivtnS.split("-")[1]

# write paths
rbakP = Path(rivtP, rbaseS + ".bak")
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
tempP = Path(rivtP, "temp")
errlogP = Path(tempP, "rivt-log.txt")
styleP = Path(projP, "doc", "style")
reportP = Path(projP, "report")
readmeP = Path(projP, "README.txt")
reportP = Path(projP, "docs")
valsP = Path(projP, "vals")
ossP = Path(projP / "oss")

# print(f"{projP=}")
# print(f"{rivtP=}")
# print(f"{insP=}")
# print(f"{valsP=}")

rivtvD = {}  # calculated values

folderD = {}  # folders
for item in [
    "docsP",
    "errlogP",
    "insP",
    "pthS",
    "projP",
    "pdfN",
    "rivtP",
    "rivtfP",
    "rstN",
    "rstpN",
    "readmeP",
    "reportP",
    "styleP",
    "styleP",
    "tempP",
    "txtN",
    "valN",
    "valsP",
    "valsP",
]:
    folderD[item] = eval(item)

labelD = {}  # parameters and labels
labelD = {
    "baseS": rbaseS,  # file base name
    "rivtnS": rivtnS,  # file name
    "divnumS": divnumS,  # div number
    "docnumS": prfxS,  # doc number
    "titleS": titleS,  # document title
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
    "valexpS": "",  # list of values for export
    "unitS": "M,M",  # units
}
