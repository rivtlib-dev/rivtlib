"""generate a rivt report

This module is called by the rivt-report.py file that contains
report settings.
"""

import configparser
import glob
import logging
import os
import shutil
import subprocess
import sys
import warnings
from datetime import datetime
from pathlib import Path

import rvrepcfg as rvr

import __main__

rvr.pdf_coverS()

reptP = os.getcwd()
rivtP = os.path.dirname(reptP)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
publicP = Path(rivtP, "_rivt-public")
storeP = Path(reptP, "_stored")
pubP = Path(reptP, "_published")
rstdocsP = Path(reptP, "_rstdocs")
pdfpubP = Path(pubP, "pdfdocs")
htmlpubP = Path(pubP, "docs")

srcP = Path(reptP, "src")
logsP = Path(storeP, "logs")
rivt_storedP = storeP
rptlogT = Path(storeP, "logs", "reportlog.txt")
timeS = datetime.now().strftime("%Y-%m-%d")

rivtfL = glob.glob("rv???*.py", root_dir=reptP)
rivtfL.sort()

# shutil.rmtree(path)

inS = __main__.iniS
repD = {}
configL = configparser.ConfigParser()
configL.read_string(inS)
repD["repname"] = configL["report"]["repname"]
repD["title"] = configL["report"]["title"]
repD["regen"] = configL["report"]["regen"]
repD["exclude"] = configL["report"]["exclude"]
repD["cover"] = configL["report"]["cover"]
repD["coverlogo"] = configL["report"]["coverlogo"]
repD["logosize"] = configL["report"]["coverlogo_size"]
repD["subtitle"] = configL["report"]["subtitle"]
repD["client"] = configL["report"]["client"]
repD["authors"] = configL["report"]["authors"]
repD["version"] = configL["report"]["version"]
repD["projref"] = configL["report"]["projectref"]
repD["copyright"] = configL["report"]["copyright"]
repD["runlogo"] = configL["report"]["running_logo"]
repD["runlabel"] = configL["report"]["running_label"]
repD["pdfpage"] = configL["report"]["pdf_pagesize"]
repD["pdfmargin"] = configL["report"]["pdf_margins"]
repD["pdflink"] = configL["report"]["pdf_link"]
repD["clearpub"] = configL["report"]["clean_publish"]


reprsN = (repD["repname"].replace(".pdf", ".rst")).strip()
freprstT = Path(rstdocsP, reprsN)


modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=rptlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")


def htmlx():
    """write html report

    Returns:
        msgS (str): completion message

    """

    htmlindex()
    print("html index page written")
    yamlS()
    print("yaml written")
    confpy()
    print("conf.py file written")

    srcS = Path(reptP, repD["coverlogo"])
    destS = Path(rstdocsP, "_static", "img")
    shutil.copy(srcS, destS)
    srcS = Path(reptP, repD["runlogo"])
    shutil.copy(srcS, destS)
    timeS = datetime.now().strftime("%Y-%m-%d")

    rvdateS = f"""
<!-- _templates/rv-date.html -->
<div class="footer-item">
<p class="rvdate">
    {timeS}
</p>
</div>
"""
    rvdateT = str(Path(rstdocsP, "_templates", "rv-date.html"))
    with open(rvdateT, "w", encoding="utf-8") as f2:
        f2.write(rvdateS)

    rvauthS = f"""
<!-- _templates/rv-author.html -->
<div class="footer-item">
<p class="rvauthor">
    {repD["authors"]}
</p>
</div>
"""
    rvauthT = str(Path(rstdocsP, "_templates", "rv-author.html"))
    with open(rvauthT, "w", encoding="utf-8") as f2:
        f2.write(rvauthS)

    rvtitleS = f"""
<!-- _templates/rv-title.html -->
<div class="footer-item">
<p class="rvtitle">
    {repD["title"]}  v.{repD["version"]} 
</p>
</div>
"""
    rvtitleT = str(Path(rstdocsP, "_templates", "rv-title.html"))
    with open(rvtitleT, "w", encoding="utf-8") as f2:
        f2.write(rvtitleS)

    htmlcmdS = f"sphinx-build -E -D root_doc=index {rstdocsP} {htmlpubP} \n"
    try:
        result = subprocess.run(htmlcmdS, shell=True, check=True)
        if not result.returncode:
            print("\nhtml script executed")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print("Stderr:", e.stderr)

    repdocT = Path(htmlpubP, repD["repname"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"file written: {short_p} \n"


def pdfx():
    """write pdf report

    Returns:
        msgS (str): completion message
    """

    # region

    pdfcoverS()
    print("cover page written")
    pdfindex()
    print("index page written")
    yamlS()
    print("yaml file written")
    confpy()
    print("conf file written")

    print("run pdf sphinx")
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(htmlpubP)} \n"

    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print("\npdf script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print("Stderr:", e.stderr)

    repdocT = Path(pdfpubP, repD["repname"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    return f"pdf file written: {short_p} \n"
    # endregion


def textx():
    """write text report

    Returns:
        msgS (str): completion message
    """
    self.confpy()  # update conf.py
    rvdocS = self.fD["rbaseS"] + ".txt"
    rvdocT = str(Path(self.fD["reptPubP"], "txtdocs", rvdocS))
    timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
    doctitleS = self.docnameS
    versionS = "v-" + self.verS.strip()
    authorS = self.authorS.strip()

    borderS = "=" * 80
    hdlS = doctitleS + " | " + authorS + " | " + timeS + " | " + versionS
    headS = "\n" + hdlS + "\n" + borderS + "\n"
    self.dutfS = headS + "\n" + self.dutfS

    with open(rvdocT, "w", encoding="utf-8") as f5:
        f5.write(self.dutfS)
    with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
        f5.write(self.dutfS)

    parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"file written: {short_p} \n"


def get_readme():
    """list of doc reports"""

    rme_folderP = Path(pubP, "readme")
    rdfL = glob.glob("rv???*.txt", root_dir=rme_folderP)
    rdfL.sort()

    return rdfL


# generate rst for each rivt file in list
print("\n\nrivt files included in report\n---------------------------")
for s in rivtfL:
    print("rivt file:", s)
print("---------------------------\n\n")
for frstS in rivtfL:
    frstT = Path(reptP, frstS)
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    print("\nrun file: ", short_p, "\n")
    subprocess.run(["python", frstT, "-t none"])
    errlogT = Path(logsP, frstS[0:7] + "log.txt")
with open(errlogT, "a") as f1:
    f1.write("write rst for each rivt file: " + repD["title"] + "\n")
logging.info("write rst files: " + repD["title"])
# ------------ convert list from .py to .rst
rstfiL = []
for fS in rivtfL:
    rstfiL.append(fS.replace(".py", ".rst"))
rsttabL = ["    " + tS for tS in rstfiL]
rsttabL = "\n".join(rsttabL)
# -------------------- write readme report
reptitleS = repD["repname"]
versionS = repD["version"]
authorS = repD["authors"]
borderS = "=" * 80
hdlS = reptitleS + " | " + authorS + " | " + timeS + " | " + versionS
headS = "\n" + hdlS + "\n" + borderS + "\n\n"
readmeT = Path(rivtP, "README.txt")
rtxtS = headS
rtxtL = get_readme()
with open(readmeT, "w") as outfile:
    outfile.write(headS)
    for fname in rtxtL:
        readT = Path(pubP, "readme", fname)
        with open(readT) as infile:
            outfile.write(infile.read())
            outfile.write("\n")
# with open(, "w", encoding="utf-8") as f3:
parts = Path(readmeT).parts[-3:]  # Take last 3 segments
short_p = ".../" + "/".join(parts)
print("\nREADME report written: ", short_p, "\n")
logging.info("README report : " + repD["title"])
# ------------------------- write report
get_typeS = repD["repname"].split(".")[-1].strip()
if get_typeS == "text":
    """write text report"""
    pubT = Path(pubP, "txtdocs", repD["repname"].strip())
    txt_folderP = Path(pubP, "_doctext")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = textx()
    print(msgS)
elif get_typeS == "pdf":
    """write pdf report"""
    pubT = Path(pubP, "pdfdocs", repD["repname"].strip())
    print("write pdf report")
    print("----------------")
    msgS = pdfx()
    print(msgS)
elif get_typeS == "html":
    """write html report"""
    pubT = Path(pubP, "docs", repD["repname"].strip())
    print("write html report")
    msgS = htmlx()
    print(msgS)
else:
    pass
