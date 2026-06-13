"""generate rivt report

The module is called by the rivt-report.py script file.
"""

import configparser
import glob
import logging
import os
import subprocess
import sys
import textwrap
import warnings
from datetime import datetime
from itertools import groupby
from pathlib import Path

import __main__

# -------------------- import rvrepcfg .py file
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import rvrepcfg as rvr  # noqa: E402

# -------------------- get report settings from rivt-report.py
setS = os.getenv("reportset")
configL = configparser.ConfigParser()
configL.read_string(setS)

# -------------------- make list of rivt files
reptP = os.getcwd()
rivtfL = glob.glob("rv???*.py", root_dir=reptP)
rivtfL.sort()
print("\n||||||||||||||||| rivt files included in report")
for s in rivtfL:
    print("rivt file:", s)
print("||||||||||||||||||| \n\n")
rstdocsP = Path(reptP, "_rstdocs")
print("\n||||||||||||||||| rst files deleted")
for file_path in rstdocsP.glob("*.rst"):
    try:
        file_path.unlink()
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
print("||||||||||||||||||| \n\n")

# Paths
rivtP = os.path.dirname(reptP)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
srcP = Path(reptP, "rvsrc")
storeP = Path(reptP, "rv_stor")
publicP = Path(rivtP, "_rivt-public")
pubP = Path(reptP, "_published")
htmlpubP = Path(pubP, "docs")
pdfpubP = Path(pubP, "pdfdocs")
txtpubP = Path(pubP, "txtdocs")
logsP = Path(storeP, "logs")
rivt_storedP = storeP
rptlogT = Path(storeP, "logs", "reportlog.txt")
timeS = datetime.now().strftime("%Y-%m-%d")

# Dictionaries
repD = {}
repD["rstdocsP"] = rstdocsP
repD["repfile"] = configL["settings"]["rept_filename"]
repD["regen"] = configL["settings"]["regen_pdf"]
repD["exclude"] = configL["settings"]["exclude"]
repD["auto"] = configL["settings"]["auto_cfg"]
repD["verbose"] = configL["settings"]["rep_verbose"]
repD["title"] = configL["format"]["title"]
repD["subtitle"] = configL["format"]["subtitle"]
repD["client"] = configL["format"]["client"]
repD["projref"] = configL["format"]["project_ref"]
repD["authors"] = configL["format"]["authors"]
repD["version"] = configL["format"]["version"]
repD["copyright"] = configL["format"]["copyright"]
repD["runlogo"] = configL["format"]["running_logo"]
repD["runlabel"] = configL["format"]["running_label"]
repD["coverlogo"] = configL["format"]["coverlogo"]
repD["logosize"] = configL["format"]["coverlogo_size"]
repD["pdfpage"] = configL["format"]["pdf_pagesize"]
repD["pdfmargin"] = configL["format"]["pdf_margins"]
repD["pdflink"] = configL["format"]["pdf_link"]
repD["toc_level"] = configL["format"]["toc_level"]
repD["repfilebase"] = repD["repfile"].split(".")[0]

modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=rptlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")


def pdfx(rstL):
    """write pdf report

    Returns:
        msgS (str): completion message
    """
    # region - pdfx
    repdocT = Path(pdfpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    rvr.pdf_coverS()
    print("||||||||||||||||||| report cover page written")
    rvr.pdf_yamlS()
    print("||||||||||||||||||| report yaml file written")
    rvr.pdf_confpy()
    print("||||||||||||||||||| report conf file written")
    # -------------------------- append div tocs to index.rst
    timeS = datetime.now().strftime("%Y-%m-%d")
    headblkS = f"""**{repD["title"]}** - v{repD["version"]} |s| |s| |s| |s|  **###Section###**"""
    foot1blkS = f"""{timeS} |s| |s| |s| **|** |s| |s| |s| {repD["authors"]}"""
    foot2blkS = f"""**{repD["runlabel"]}**"""
    imgS = f"""
.. |blklogo| image:: ./_static/{repD["runlogo"]}
   :height: 100px
   :alt: logo


"""
    headS = f"""
.. header::
    .. list-table::
        :class: header-box
        :align: left
        :widths: 90 10
        
        * - {headblkS}
          - p. **###Page###**   

          
"""

    footS = f"""
.. footer:: 
    .. list-table::
        :class: footer-box
        :align: left
        :widths: 84 22 16
        
        * - {foot1blkS}        
          - {foot2blkS}        
          - |blklogo|                  
"""

    toc1S = """
    
.. toctree::
    :maxdepth: 1

[replace]
    
"""

    insS = ".. |s| unicode:: 0xA0 \n\n\n"

    # groupL = [list(g) for k, g in groupby(rstfiL, key=lambda x: x[2])]
    # indxtocL = [sublist[0] for sublist in groupL]
    # for item in indxtocL:
    #     tocinS = tocinS + "    " + item + "\n"
    tocinS = "\n"
    for item in [rstL]:
        tocinS += textwrap.indent(item, "") + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))

    preamS = insS + imgS + headS + footS + tocrS
    with open(rvindxT, "w", encoding="utf-8") as f5:
        f5.write(preamS)

    print("||||||||||||||||||| run sphinx-pdf")
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(pdfpubP)} \n"

    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print(f"||||||||||||||||||| pdf file written: {short_p} \n")
    except subprocess.CalledProcessError as e:
        print(f"||||||||||||||||||| Error executing script: {e}")
        print("Stderr:", e.stderr)

    return " "
    # endregion


def htmlx():
    """write html report

    Returns:
        msgS (str): completion message

    """

    # region - htmlx
    rvr.html_confpy()
    print("||||||||||||||||||| html_conf.py file written")
    rvr.html_index()
    print("||||||||||||||||||| html_index file written")
    timeS = datetime.now().strftime("%Y-%m-%d")
    # html classes
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
    :maxdepth: 2

[replace]
    
"""
    tocinS = ""  # key on div number and take first one
    groupL = [list(g) for k, g in groupby(rstfiL, key=lambda x: x[2])]
    indxtocL = [sublist[0] for sublist in groupL]
    for item in indxtocL:
        tocinS = tocinS + "    " + item + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))
    with open(rvindxT, "a", encoding="utf-8") as f5:
        f5.write(tocrS)
    # -------------- write subdiv tocs to second doc
    toc2S = """
.. toctree::
    :hidden:
    :maxdepth: 2

[replace]
    
"""
    # collect other docs
    indxsubtocL = [sublist[1:] for sublist in groupL]
    idx = 0
    for fS in indxtocL:
        tocinS = ""
        for item in indxsubtocL[idx]:
            tocinS = tocinS + "    " + item + "\n"
            tocrS = toc2S.replace("[replace]", tocinS)
        fpT = Path(rstdocsP, fS)
        with open(fpT, "a") as f1:
            f1.write(tocrS)
        idx += 1
    # --------------- insert section header
    # for item in dochdrL:
    #     docS = item[0]
    #     titleS = item[1]
    #     docT = Path(rstdocsP, docS)
    #     divS = docS[2]
    #     # hdrS = f"D.{divS} {titleS} \n" + "=" * 70 + "\n\n"
    #     # with open(docT, "r", encoding="utf-8") as f1:
    #     #     content = f1.read()
    #     # with open(docT, "w", encoding="utf-8") as f2:
    #     #     f2.write(hdrS + content)

    print("||||||||||||||||||| run sphinx-html")
    htmlcmdS = f"sphinx-build -E -D root_doc=index {rstdocsP} {htmlpubP} \n"
    try:
        result = subprocess.run(htmlcmdS, shell=True, check=True)
        if not result.returncode:
            print("||||||||||||||||||| html script executed")
    except subprocess.CalledProcessError as e:
        print(f"||||||||||||||||||| Error executing script: {e}")
        print("Stderr:", e.stderr)

    repdocT = Path(htmlpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"file written: {short_p} \n"
    # endregion


def txtx(txtfL):
    """write text report

    Returns:
        msgS (str): completion message
    """
    # region - txtx
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


# ---------------------------------------loop over files in report
doctitleS = " "  # ------------ get publish params for each py file
dochdrL = []  # for html
strtdocS = rivtfL[0]
strtdocT = Path(reptP, strtdocS)
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
    # -------------------------------------- types
    get_typeS = repD["repfile"].split(".")[-1].strip()
    if get_typeS == "txt":
        print("\n|||||||||||||| generate txt file for report: ", short_p, "\n")
        result = subprocess.run(  # -------------- from txt list generate doc
            ["python", frstT, "-t", "txt", "-k", "true"], text=True
        )
    elif get_typeS == "pdf" or get_typeS == "html":
        print("\n|||||||||||||| generate rst file : ", short_p, "\n")
        result = subprocess.run(  # -------------- from rst list gen rst
            ["python", frstT, "-t", "none", "-k", "true"], text=True
        )
    else:
        pass
    # ------------------------------------------------------- write logs
    errlogT = Path(logsP, frstS[0:7] + "log.txt")
    with open(errlogT, "a") as f1:
        f1.write(f">>{get_typeS}<< generated from: {frstT}\n")
    logging.info(f">>{get_typeS}<< generated from: {frstT}\n")
    print(f"|||||||||||||{get_typeS}<< file generated from: {frstT}\n")
    print("result from subprocess", result)
    # ----------------------------------------------------- write report
# generate list of rst files
rstfiL = []
for fS in rivtfL:
    rstfiL.append(fS.replace(".py", ".rst"))
rsttabL = ["    " + tS for tS in rstfiL]
rsttabL = "\n".join(rsttabL)
if get_typeS == "txt":
    """write text report"""
    print("||||||||||||| write text report")
    pubT = Path(pubP, "txtdocs", repD["repfile"].strip())
    txt_folderP = Path(pubP, "txtdocs")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = txtx(txtfL)
    print(f"||||||||||||| txtx:  {msgS}")
elif get_typeS == "pdf":
    """write pdf report"""
    print("--------------- write pdf report")
    pubT = Path(pubP, "pdfdocs", repD["repfile"].strip())
    msgS = pdfx(rsttabL)
    print(f"||||||||||||| pdfx: {msgS}")
elif get_typeS == "html":
    """write html report"""
    print("--------------- write html report")
    pubT = Path(pubP, "docs", repD["repfile"].strip())
    msgS = htmlx()
    print(f"||||||||||||| htmlx: {msgS}")
else:
    pass
# ------------------------------------- write readme report
reptitleS = repD["repfile"]
versionS = repD["version"]
authorS = repD["authors"]
toctxtS = "Table of Contents\n==================\n"
for item in dochdrL:
    it = item[0]
    toctxtS += it[2] + "." + str(int(it[3:5])) + "  " + item[1] + "\n"
borderS = "=" * 80
hdlS = repD["title"] + " v-" + versionS + " | " + authorS + " | " + timeS
headS = "\n" + borderS + "\n| rivt | " + hdlS + "\n" + borderS + "\n\n"
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
logging.info("|||||||||| README report : " + repD["title"])
print(f"||||||||||||| README report written:  {short_p}")
