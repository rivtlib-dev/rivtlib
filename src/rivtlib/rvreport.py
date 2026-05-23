"""generate rivt report

The module is called by the rivt-report.py script file.
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
from itertools import groupby
from pathlib import Path

import __main__

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import rvrepcfg as rvr  # noqa: E402

reptP = os.getcwd()
rivtfL = glob.glob("rv???*.py", root_dir=reptP)
rivtfL.sort()
print("\n\nrivt files included in report\n---------------------------")
for s in rivtfL:
    print("rivt file:", s)
print("---------------------------\n\n")

rivtP = os.path.dirname(reptP)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
srcP = Path(reptP, "rvsrc")
storeP = Path(reptP, "rv_stor")
publicP = Path(rivtP, "_rivt-public")
pubP = Path(reptP, "_published")
rstdocsP = Path(reptP, "_rstdocs")
pdfpubP = Path(pubP, "pdfdocs")
htmlpubP = Path(pubP, "docs")
logsP = Path(storeP, "logs")
rivt_storedP = storeP
rptlogT = Path(storeP, "logs", "reportlog.txt")
timeS = datetime.now().strftime("%Y-%m-%d")


# shutil.rmtree(path)


repD = {}
repD["rstdocsP"] = rstdocsP

inS = __main__.iniS
configL = configparser.ConfigParser()
configL.read_string(inS)
repD["repfile"] = configL["report"]["rept_filename"]
repD["regen"] = configL["report"]["regen"]
repD["exclude"] = configL["report"]["exclude"]
repD["keep"] = configL["report"]["keep_files"]
repD["auto"] = configL["report"]["auto_cfg"]
repD["title"] = configL["report"]["title"]
repD["subtitle"] = configL["report"]["subtitle"]
repD["coverlogo"] = configL["report"]["coverlogo"]
repD["logosize"] = configL["report"]["coverlogo_size"]
repD["client"] = configL["report"]["client"]
repD["projref"] = configL["report"]["project_ref"]
repD["authors"] = configL["report"]["authors"]
repD["version"] = configL["report"]["version"]
repD["copyright"] = configL["report"]["copyright"]
repD["runlogo"] = configL["report"]["running_logo"]
repD["runlabel"] = configL["report"]["running_label"]
repD["pdfpage"] = configL["report"]["pdf_pagesize"]
repD["pdfmargin"] = configL["report"]["pdf_margins"]
repD["pdflink"] = configL["report"]["pdf_link"]

repD["repfilebase"] = repD["repfile"].split(".")[0]

rvr.repD = repD

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

    # region - htmlx
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

    repdocT = Path(htmlpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    return f"file written: {short_p} \n"
    # endregion


def pdfx():
    """write pdf report

    Returns:
        msgS (str): completion message
    """

    repdocT = Path(pdfpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    rvr.pdf_coverS()
    print("cover page written")
    rvr.pdf_yamlS()
    print("yaml file written")
    rvr.pdf_confpy()
    print("conf file written")

    # ------------ write tocs to index.rst
    tocinS = "\n"
    toc1S = """

.. toctree::
    :hidden:

    pdfcover.rst    

    
.. toctree::
    :maxdepth: 3

[replace]
    
"""
    groupL = [list(g) for k, g in groupby(rstfiL, key=lambda x: x[2])]
    indxtocL = [sublist[0] for sublist in groupL]
    for item in indxtocL:
        tocinS = tocinS + "    " + item + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    print("*****xxx", tocrS)

    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))
    with open(rvindxT, "w", encoding="utf-8") as f5:
        f5.write(tocrS)

    # -------------- write tocs to subdivisions
    toc2S = """
.. toctree::
    :maxdepth: 2

[replace]
    
"""

    for item in groupL:
        tocinS = "\n"
        fL = item[1:]
        for iS in fL:
            tocinS += tocinS + "    " + iS + "\n"
        tocrS = toc2S.replace("[replace]", tocinS)
        fpT = Path(rstdocsP, item[0])
        print("*******yyy", tocrS)
        with open(fpT, "a") as f1:
            f1.write(tocrS)

    print("run sphinx-pdf")
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(pdfpubP)} \n"

    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print(f"pdf file written: {short_p} \n")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print("Stderr:", e.stderr)

    return " "
    # endregion


def textx():
    """write text report

    Returns:
        msgS (str): completion message
    """

    # region - testx
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
    # endregion


def get_readme():
    """list of doc reports"""

    # region - readme
    rme_folderP = Path(pubP, "readme")
    rdfL = glob.glob("rv???*.txt", root_dir=rme_folderP)
    rdfL.sort()

    return rdfL
    # endregion


# ------------ generate rst for each rivt file in list from type none
doctitleS = " "
for frstS in rivtfL:
    frstT = Path(reptP, frstS)
    with open(frstT, "r", encoding="utf-8") as f1:
        fL = f1.readlines()
        for lS in fL:
            if len(lS) > 0:
                if "| PUBLISH |" in lS:
                    pL = lS[5:].split("|")
                    doctitleS = str(pL[1].strip()).strip()
                    if doctitleS == "--":
                        doctitleS = " "
                    else:
                        doctitleS = str(pL[1]).strip()
    repD["doctitleS"] = doctitleS
    repD["rvbaseS"] = frstS.split(".py")[0].strip()
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    print("\nrun file: ", short_p, "\n")
    subprocess.run(["python", frstT, "-t none"])

    errlogT = Path(logsP, frstS[0:7] + "log.txt")
with open(errlogT, "a") as f1:
    f1.write("write rst for each rivt file: " + repD["title"] + "\n")
logging.info("write rst files: " + repD["title"])
# -------------- convert list from .py to .rst
rstfiL = []
for fS in rivtfL:
    rstfiL.append(fS.replace(".py", ".rst"))
rsttabL = ["    " + tS for tS in rstfiL]
rsttabL = "\n".join(rsttabL)
# ------------- write readme report
reptitleS = repD["repfile"]
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
get_typeS = repD["repfile"].split(".")[-1].strip()
if get_typeS == "text":
    """write text report"""
    pubT = Path(pubP, "txtdocs", repD["repfile"].strip())
    txt_folderP = Path(pubP, "_doctext")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = textx()
    print(msgS)
elif get_typeS == "pdf":
    """write pdf report"""
    pubT = Path(pubP, "pdfdocs", repD["repfile"].strip())
    print("write pdf report")
    print("----------------")
    msgS = pdfx()
    print(msgS)
elif get_typeS == "html":
    """write html report"""
    pubT = Path(pubP, "docs", repD["repfile"].strip())
    print("write html report")
    msgS = htmlx()
    print(msgS)
else:
    pass
