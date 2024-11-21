"""parse rivtlib folder structure"""


from pathlib import Path
import os
import fnmatch

docS = "x.py"
docP = "/"


def get_riv_files(cur_dirP):
    """list of rivt files
    """

    docpathP = Path(os.getcwd())
    for fileS in os.listdir(docpathP):
        # print(fileS)
        if fnmatch.fnmatch(fileS, "riv????-*.py"):
            docfileS = fileS
            docP = Path(docpathP, docfileS)
            # print(docP)
            break
    if docfileS == "xx":
        print("INFO     rivt file not found")
        exit()


# files and paths
baseS = docS.split(".py")[0]
titleS = baseS.split("-")[1]
projP = docP
bakP = docP / ".".join((baseS, "bak"))
prfxS = baseS[0:7]
dataP = Path(projP, "data")
toolsP = Path(projP, "tools")

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
config = ConfigParser()
config.read(Path(projP, "config.ini"))
headS = config.get('format', 'header')
footS = config.get('format', 'footer')

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
for item in ["rivtP", "dataP", "readmeP", "reportP",
             "dataP", "valfileS", "errlogP", "styleP", "tempP"]:
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
