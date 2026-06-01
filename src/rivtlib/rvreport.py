"""generate rivt report

The module is called by the rivt-report.py script file.
"""

import configparser
import glob
import logging
import os
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
htmlpubP = Path(pubP, "docs")
pdfpubP = Path(pubP, "pdfdocs")
txtpubP = Path(pubP, "txtdocs")
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
repD["repfile"] = configL["settings"]["rept_filename"]
repD["regen"] = configL["settings"]["regen_pdf"]
repD["exclude"] = configL["settings"]["exclude"]
repD["auto"] = configL["settings"]["rivt_cfg"]
repD["title"] = configL["format"]["title"]
repD["subtitle"] = configL["format"]["subtitle"]
repD["client"] = configL["format"]["client"]
repD["projref"] = configL["format"]["project_ref"]
repD["authors"] = configL["reformatport"]["authors"]
repD["version"] = configL["format"]["version"]
repD["copyright"] = configL["format"]["copyright"]
repD["runlogo"] = configL["format"]["running_logo"]
repD["runlabel"] = configL["format"]["running_label"]
repD["coverlogo"] = configL["format"]["coverlogo"]
repD["logosize"] = configL["format"]["coverlogo_size"]
repD["pdfpage"] = configL["format"]["pdf_pagesize"]
repD["pdfmargin"] = configL["format"]["pdf_margins"]
repD["pdflink"] = configL["format"]["pdf_link"]
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
    rvr.html_confpy()
    print("html_conf.py file written")
    rvr.html_index()
    print("html_index file written")

    timeS = datetime.now().strftime("%Y-%m-%d")

    rvdateS = f"""
<!-- _templates/rv-date.html -->
<div class="footer-item">
    <p class="rvdate">
        {timeS}
    </p>
</div>
"""
    rvdateT = str(Path(rstdocsP, "_static", "rv-date.html"))
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
    rvauthT = str(Path(rstdocsP, "_static", "rv-author.html"))
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
    rvtitleT = str(Path(rstdocsP, "_static", "rv-title.html"))
    with open(rvtitleT, "w", encoding="utf-8") as f2:
        f2.write(rvtitleS)

    rvdateS = f"""
<!-- _templates/rv-date.html -->
<div class="footer-item">
<p class="rvdate">
    {timeS}
</p>
</div>
"""
    rvdateT = str(Path(rstdocsP, "_static", "rv-date.html"))
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
    rvauthT = str(Path(rstdocsP, "_static", "rv-author.html"))
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
    rvtitleT = str(Path(rstdocsP, "_static", "rv-title.html"))
    with open(rvtitleT, "w", encoding="utf-8") as f2:
        f2.write(rvtitleS)
    # ------------ append div tocs to index.rst
    tocinS = "\n"
    toc1S = """

.. toctree::
    :hidden:
    :maxdepth: 3

[replace]
    
"""
    groupL = [list(g) for k, g in groupby(rstfiL, key=lambda x: x[2])]
    indxtocL = [sublist[0] for sublist in groupL]
    for item in indxtocL:
        tocinS = tocinS + "    " + item + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))
    with open(rvindxT, "a", encoding="utf-8") as f5:
        f5.write(tocrS)
    # -------------- write subdiv tocs to docs
    toc2S = """
.. toctree::
    :hidden:
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
        with open(fpT, "a") as f1:
            f1.write(tocrS)
    # --------------- insert section header
    for item in dochdrL:
        docS = item[0]
        titleS = item[1]
        docT = Path(rstdocsP, docS)
        divS = docS[2]
        hdrS = f"D.{divS} {titleS} \n" + "=" * 70 + "\n\n"
        with open(docT, "r", encoding="utf-8") as f1:
            content = f1.read()
        with open(docT, "w", encoding="utf-8") as f2:
            f2.write(hdrS + content)

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

    # region - pdfx
    repdocT = Path(pdfpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    rvr.pdf_coverS()
    print("cover page written")
    rvr.pdf_yamlS()
    print("yaml file written")
    rvr.pdf_confpy()
    print("conf file written")
    # ------------ write div tocs to index.rst
    tocinS = "\n"
    toc1S = """

.. toctree::
    :hidden:

    pdfcover.rst    

    
.. toctree::
    :hidden:
    :maxdepth: 3

[replace]
    
"""
    groupL = [list(g) for k, g in groupby(rstfiL, key=lambda x: x[2])]
    indxtocL = [sublist[0] for sublist in groupL]
    for item in indxtocL:
        tocinS = tocinS + "    " + item + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))
    with open(rvindxT, "w", encoding="utf-8") as f5:
        f5.write(tocrS)
    # -------------- append subdiv tocs to rst docs
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


def textx(txtfL):
    """write text report

    Returns:
        msgS (str): completion message
    """

    # region - textx

    rvrepT = Path(txtpubP, repD["repfile"])
    timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
    versionS = repD["version"]
    authorS = repD["authors"]

    borderS = "=" * 80
    hdlS = repD["title"] + " | " + authorS + " | " + versionS + " | " + timeS
    headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n\n"

    toctxtS = "Table of Contents\n==================\n"
    for item in dochdrL:
        itm = item[0]
        toctxtS += itm[2] + "." + str(int(itm[3:5])) + "  " + item[1] + "\n"
    with open(rvrepT, "w") as f5:
        for fname in txtfL:
            fnameT = Path(txtpubP, fname)
            with open(fnameT) as infile:
                f5.write(infile.read())
    with open(rvrepT, "r") as f1:
        content = f1.read()
    with open(rvrepT, "w") as f2:
        f2.write(headS + "\n" + toctxtS + "\n\n" + content)
    parts = Path(rvrepT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"text report written: {short_p} \n"
    # endregion


rmfileS = str(Path(rstdocsP, "*.rst"))
for f in glob.glob(rmfileS):
    os.remove(f)
# ------------ generate rst for each rivt file in list from type none
doctitleS = " "
dochdrL = []  # for html
firstdocS = rivtfL[0]
firstdocT = Path(reptP, firstdocS)
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
    dochdrL.append([frstS.replace(".py", ".rst"), doctitleS])
    repD["doctitleS"] = doctitleS
    repD["rvbaseS"] = frstS.split(".py")[0].strip()
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    # ----------------- run batch rivt files
    get_typeS = repD["repfile"].split(".")[-1].strip()
    if get_typeS == "txt":
        print("\ngemerate txt file for report: ", short_p, "\n")
        subprocess.run(["python", frstT, "-t text"])
        # -------------- write logs
        errlogT = Path(logsP, frstS[0:7] + "log.txt")
        with open(errlogT, "a") as f1:
            f1.write("txt written for each rivt file: " + repD["title"] + "\n")
        logging.info("txt files written: " + repD["title"])
    elif get_typeS == "pdf" or get_typeS == "html":
        print("\ngenerate rst file report: ", short_p, "\n")
        subprocess.run(["python", frstT, "-t none"])
        # -------------- write logs
        errlogT = Path(logsP, frstS[0:7] + "log.txt")
        with open(errlogT, "a") as f1:
            f1.write("rst written for each rivt file: " + repD["title"] + "\n")
        logging.info("rst files written: " + repD["title"])
        # -------------- convert list from .py to .rst
        rstfiL = []
        for fS in rivtfL:
            rstfiL.append(fS.replace(".py", ".rst"))
        rsttabL = ["    " + tS for tS in rstfiL]
        rsttabL = "\n".join(rsttabL)
# ------------------------------------- write readme report
reptitleS = repD["repfile"]
versionS = repD["version"]
authorS = repD["authors"]
toctxtS = "Table of Contents\n==================\n"
for item in dochdrL:
    it = item[0]
    toctxtS += it[2] + "." + str(int(it[3:5])) + "  " + item[1] + "\n"
borderS = "=" * 80
hdlS = repD["title"] + " | " + authorS + " | " + versionS + " | " + timeS
headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n\n"
readmeT = Path(rivtP, "README.txt")
rtxtS = headS
rme_folderP = Path(pubP, "readme")
rdfL = glob.glob("rv???-*.txt", root_dir=rme_folderP)
rdfL.sort()
with open(readmeT, "w") as outfile:
    for fname in rdfL:
        readT = Path(pubP, "readme", fname)
        with open(readT) as infile:
            outfile.write(infile.read())
            outfile.write("\n")
with open(readmeT, "r") as f2:
    content = f2.read()
with open(readmeT, "w") as f1:
    f1.write(headS + "\n" + toctxtS + "\n\n" + content)
# with open(, "w", encoding="utf-8") as f3:
parts = Path(readmeT).parts[-3:]  # Take last 3 segments
short_p = ".../" + "/".join(parts)
print("\nREADME report written: ", short_p, "\n")
logging.info("README report : " + repD["title"])
# ------------------------- write report
if get_typeS == "txt":
    """write text report"""
    print("write text report")
    print("----------------")
    pubT = Path(pubP, "txtdocs", repD["repfile"].strip())
    txt_folderP = Path(pubP, "txtdocs")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = txtx(txtfL)
    print(msgS)
elif get_typeS == "pdf":
    """write pdf report"""
    print("write pdf report")
    print("----------------")
    pubT = Path(pubP, "pdfdocs", repD["repfile"].strip())
    msgS = pdfx()
    print(msgS)
elif get_typeS == "html":
    """write html report"""
    print("write html report")
    print("----------------")
    pubT = Path(pubP, "docs", repD["repfile"].strip())
    msgS = htmlx()
    print(msgS)
else:
    pass
