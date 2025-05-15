import fnmatch
import os
import sys
from pathlib import Path

import __main__

"""
File and label parameters 

    Labels (dict)
    ==============

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


    Commands (list)
    ================

    | IMG  | rel. pth | caption, scale, ([_F])        .png, .jpg
    | IMG2  | rel. pth | c1, c2, s1, s2, ([_F])       .png, .jpg
    | TEXT | rel. pth |  plain; rivt                  .txt
    | TABLE | rel. pth | col width, l;c;r ([_T])      .csv, .txt, .xls
    | VALUES | rel. pth | col width, l;c;r            .csv, .txt, .xls
    || PUBLISH | rel. pth | txt, pdf, pdfx, html
    || PREPEND | rel. pth | num; nonum                .pdf
    || APPEND | rel. pth | num; nonum                 .pdf


    tags (dictionary)
    ==================
    _[C]     center
    _[D]     descrip
    _[E]     equation
    _[#]     foot
    _[F]     figure
    _[S]     sympy
    _[L]     sympy label
    _[T]     table
    _[H]     hline
    _[P]     page
    _[U]     url
     :=      equals
    _[[B]]   bldindblk
    _[[C]]   codeblk
    _[[I]]   italindblk
    _[[L]]   literalblock
    _[[X]]   latexblk
    _[[V]]   valuesblk
    _[[Q]


"""

rivtP = Path(os.getcwd())
projP = Path(os.path.dirname(rivtP))
modnameS = __name__.split(".")[1]

if __name__ == "rivtlib.rparam":
    rivtfP = Path(__main__.__file__)
    rivtnS = rivtfP.name
    patternS = "r[0-9][0-9][0-9]0-9]-*.py"
    if fnmatch.fnmatch(rivtnS, patternS):
        rivtfP = Path(rivtP, rivtnS)
else:
    print(f"""The rivt file name is - {rivtnS} -. The file name pattern must""")
    print("""match "rddss-anyname.py", where dd and ss are two-digit integers""")
    sys.exit()

# print(f"{rivtfP=}")
# print(f"{rivtP=}")
# print(f"{rivtnS=}")
# print(f"{__name__=}")
# print(f"{modnameS=}")


# read file paths
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
baknS = rbaseS + "bak"
docP = Path(projP, "doc")
bakfP = Path(rivtP, baknS)
divnumS = "d" + dnumS + "-"
srcP = insP = Path(projP, "src")
insP = Path(srcP, "ins")
toolsP = Path(srcP, "vls")
styleP = Path(docP, "styles")
titleS = rivtnS.split("-")[1]


# write file paths
rbakP = Path(rivtP, rbaseS + ".bak")
pypathS = os.path.dirname(sys.executable)
rivtpkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
tempP = Path(rivtP, "temp")
errlogP = Path(tempP, "rivt-log.txt")
styleP = Path(projP, "doc", "style")
reportP = Path(projP, "report")
readmeP = Path(projP, "README.txt")
reportP = Path(projP, "docs")
ossP = Path(projP / "oss")
valnS = prfxS.replace("r", "v")

# read/write paths
valP = Path(srcP, "v" + dnumS)

# print(f"{projP=}")
# print(f"{rivtP=}")
# print(f"{insP=}")
# print(f"{valsP=}")

rivtD = {}  # calculated values

folderD = {}  # folders
for item in [
    "docP",
    "bakfP",
    "errlogP",
    "insP",
    "pthS",
    "projP",
    "pdfnS",
    "rivtP",
    "readmeP",
    "reportP",
    "styleP",
    "tempP",
    "rivtnS",
    "rstnS",
    "txtnS",
    "valnS",
    "valP",
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
