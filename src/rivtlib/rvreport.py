"""generate a rivt report

This module is called by the rivt-report.py file that contains
report settings.
"""

import configparser
import glob
import logging
import os
import sys
import warnings
from pathlib import Path

import __main__

rivtN = "abc"
rivtP = "adasf"
reptP = Path(os.getcwd())
rivtT = Path(reptP, rivtN)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
rbaseS = rivtN.split(".")[0]
reptPN = rivtN.replace("rv", "rv-")
docnumS = rbaseS[0:6]
bakN = rbaseS + ".bak"
errlogN = docnumS + "log.txt"
rootP = reptP.parent
publicP = Path(rootP, "_rivt-public")
storeP = Path(reptP, "_stored")
pubP = Path(reptP, "_published")
rstdocsP = Path(reptP, "_rstdocs")
srcP = Path(reptP, "src")
logsP = Path(storeP, "logs")
errlogT = Path(logsP, errlogN)
bakT = Path(logsP, bakN)
rivtT = Path(reptP, rivtN)
rivt_storedP = storeP

fD = {  # folders
    "errlogT": errlogT,
    "bakT": bakT,
    "pthS": " ",
    "srcnS": " ",
    "rivtN": rivtN,  # file name
    "rivtT": rivtT,  # full path name
    "reptP": Path(os.getcwd()),
    "rbaseS": rbaseS,  # file base name
    "reptfDN": os.path.dirname(reptP),
    "docP": Path(reptP, "rivtDocs"),
    "pdfN": rbaseS + ".pdf",
    "readmeT": Path(rivtP, "README.txt"),
    "rstdocsP": rstdocsP,
    "reptPubP": pubP,
    "pdfpubP": Path(pubP, "pdfdocs"),
    "htmlpubP": Path(pubP, "docs"),
    "publicT": Path(reptP, "public", reptPN),
    "srcP": srcP,
    "storeP": storeP,
    "valP": Path(srcP, "values"),
    "toolP": Path(srcP, "tools"),
    "styleP": Path(srcP, "styles"),
    "tempP": Path(srcP, "temp"),
}

rptlogT = Path(storeP, "logs", "reportlog.txt")

modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=rptlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")


def get_docs():
    """list of doc reports"""

    rst_folderP = fD["reptP"]
    rivtfL = glob.glob("rv???*.py", root_dir=rst_folderP)

    return rivtfL


def coverS(self):
    """
    cover page

    """

    # timeS = datetime.now().strftime("%Y-%m-%d")
    rvfileT = str(Path(self.fD["rstdocsP"], "_templates", "pdfcover.rst"))
    coverpgS = f"""
.. role:: big-text

|
|
        
.. image:: ../src/{self.coverlogo}
   :width: 600px
   :align: center

|
|
|


.. class:: center

    :big-text:`{self.docnameS}`

|
|
|
|
|
|

.. class:: center

   Attn: **{self.clientS}**

|

.. class:: center

   project: **{self.projrefS}**

   

.. raw:: pdf

   PageBreak mainPage
   SetPageCounter 1

   
"""

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(coverpgS)


inS = __main__.iniS
repD = {}
configL = configparser.ConfigParser()
configL.read_string(inS)
repD["cover"] = configL["report"]["cover"]
repD["coverlogo"] = configL["report"]["coverlogo"]
repD["title"] = configL["report"]["title"]
repD["subtitle"] = configL["report"]["subtitle"]
repD["client"] = configL["report"]["client"]
repD["projref"] = configL["report"]["projectref"]
repD["copyright"] = configL["report"]["copyright"]

with open(errlogT, "a") as f4:
    f4.write("write report: " + repD["title"] + "\n")
logging.info("Report : " + repD["title"])

rivtfL = get_docs()
print(rivtfL)

# run each file in list

for fS in rivtfL:
    fT = Path(rivtP, fS)
    rvcmd = f"python {fT} --none"
    exec(rvcmd)
