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

# -------------------- make list of rivt files
reptP = os.getcwd()
rivtfL = glob.glob("rv???*.py", root_dir=reptP)
rivtfL.sort()
rstdocsP = Path(reptP, "_rstdocs")
print("\n\033[34m||||||||||||||||| rivt files included in report\033[0m")
for s in rivtfL:
    print("\033[34mrivt file:\033[0m", s)
print("\033[34m||||||||||||||||||| \033[0m\n\n")

for file_path in rstdocsP.glob("*.rst"):
    try:
        file_path.unlink()
        print(f"\033[34mDeleted: {file_path}\033[0m")
    except OSError as e:
        print(f"\033[34mError deleting {file_path}: {e}\033[0m")
print("\n\033[34m||||||||||||||||| rst files deleted\033[0m\n\n")


# -------------------- get report settings from rivt-report.py
setS = os.getenv("reportset")
configL = configparser.ConfigParser()
configL.read_string(setS)

# Dictionaries
repD = {}
repD["rstdocsP"] = rstdocsP
repD["repfile"] = configL["report"]["rept_filename"]
repD["exclude"] = configL["report"]["exclude"]
repD["regen"] = configL["process"]["regen_pdf"]
repD["auto"] = configL["process"]["auto_cfg"]
repD["verbose"] = configL["process"]["rep_verbose"]
repD["title"] = configL["layout"]["title"]
repD["subtitle"] = configL["layout"]["subtitle"]
repD["client"] = configL["layout"]["client"]
repD["projref"] = configL["layout"]["project_ref"]
repD["authors"] = configL["layout"]["authors"]
repD["version"] = configL["layout"]["version"]
repD["copyright"] = configL["layout"]["copyright"]
repD["runlogo"] = configL["layout"]["running_logo"]
repD["runlabel"] = configL["layout"]["running_label"]
repD["coverlogo"] = configL["layout"]["coverlogo"]
repD["logosize"] = configL["layout"]["coverlogo_size"]
repD["pdfpage"] = configL["layout"]["pdf_pagesize"]
repD["pdfmargin"] = configL["layout"]["pdf_margins"]
repD["pdflink"] = configL["layout"]["pdf_link_underline"]
repD["linkcolor"] = configL["layout"]["pdf_link_color"]
repD["toc_level"] = configL["layout"]["toc_level"]
repD["repfilebase"] = repD["repfile"].split(".")[0]

# -------------------- import rvrepcfg .py file
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import rvrepcfg as rvr  # noqa: E402

# --------------------- add dictionaries to rvr
for key, value in repD.items():
    rvr.repD[key] = value

# Paths
rootP = os.path.dirname(reptP)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
srcP = Path(reptP, "rvsrc")
storeP = Path(reptP, "rv_stor")
publicP = Path(rootP, "_rivt-public")
pubP = Path(reptP, "_published")
htmlpubP = Path(pubP, "docs")
pdfpubP = Path(pubP, "pdfdocs")
txtpubP = Path(pubP, "txtdocs")
logsP = Path(storeP, "logs")
rivt_storedP = storeP
rptlogT = Path(storeP, "logs", "reportlog.txt")
timeS = datetime.now().strftime("%Y-%m-%d")

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
    print("\033[34m||||||||||||||||||| report cover page written\033[0m")
    rvr.pdf_yamlS()
    print("\033[34m||||||||||||||||||| report yaml file written\033[0m")
    rvr.pdf_confpy()
    print("\033[34m||||||||||||||||||| report conf file written\033[0m")
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

    print("\033[34m||||||||||||||||||| run sphinx-pdf\033[0m")
    pdfcmdS = f"\033[34msphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(pdfpubP)} \033[0m\n"

    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print(
                f"\033[34m||||||||||||||||||| pdf file written: {short_p} \033[0m\n"
            )
    except subprocess.CalledProcessError as e:
        print(f"\033[34m||||||||||||||||||| Error executing script: {e}\033[0m")
        print("\033[34mStderr:\033[0m", e.stderr)

    return " "
    # endregion


def htmlx():
    """write html report

    Returns:
        msgS (str): completion message

    """

    # region - htmlx
    rvr.html_confpy()
    print("\033[34m||||||||||||||||||| html_conf.py file written\033[0m")
    rvr.html_index()
    print("\033[34m||||||||||||||||||| html_index file written\033[0m")
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

    print("\033[34m||||||||||||||||||| run sphinx-html\033[0m")
    htmlcmdS = f"\033[34msphinx-build -E -D root_doc=index {rstdocsP} {htmlpubP} \033[0m\n"
    try:
        result = subprocess.run(htmlcmdS, shell=True, check=True)
        if not result.returncode:
            print("\033[34m||||||||||||||||||| html script executed\033[0m")
    except subprocess.CalledProcessError as e:
        print(f"\033[34m||||||||||||||||||| Error executing script: {e}\033[0m")
        print("\033[34mStderr:\033[0m", e.stderr)

    repdocT = Path(htmlpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"\033[34mfile written\033[0m: {short_p} \n"
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
    hdlS = (
        "| rivt report | "
        + repD["title"]
        + " | "
        + authorS
        + " | "
        + versionS
        + " | "
        + timeS
    )
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
    return f"\033[34mtext report written: {short_p} \033[0m\n"
    # endregion


# ---------- loop over folders in book get doc title from PUBLISH
doctitleS = " "
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
        print(
            "\n\033[34m|||||||||||||| generate txt file for report: \033[0m",
            short_p,
            "\n",
        )
        result = subprocess.run(  # -------------- from txt list generate doc
            ["python", frstT, "-t", "txt", "-k", "true"], text=True
        )
    elif get_typeS == "pdf" or get_typeS == "html":
        print(
            "\n\033[34m|||||||||||||| generate rst file : \033[0m",
            short_p,
            "\n",
        )
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
    print(
        f"\033[34m||||||||||||| >>{get_typeS}<< file generated from: {frstT}\033[0m\n"
    )
    print("\033[34mresult from subprocess\033[0m", result)
# ----------------------------------------------------- write report
# generate list of rst files
rstfiL = []
for fS in rivtfL:
    rstfiL.append(fS.replace(".py", ".rst"))
rsttabL = ["    " + tS for tS in rstfiL]
rsttabL = "\n".join(rsttabL)
if get_typeS == "txt":
    """write text report"""
    print("\033[34m||||||||||||| write text report\033[0m")
    pubT = Path(pubP, "txtdocs", repD["repfile"].strip())
    txt_folderP = Path(pubP, "txtdocs")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = txtx(txtfL)
    print(f"\033[34m||||||||||||| txtx:  {msgS}\033[0m")
elif get_typeS == "pdf":
    """write pdf report"""
    print("\033[34m--------------- write pdf report\033[0m")
    pubT = Path(pubP, "pdfdocs", repD["repfile"].strip())
    msgS = pdfx(rsttabL)
    print(f"\033[34m||||||||||||| pdfx: {msgS}\033[0m")
elif get_typeS == "html":
    """write html report"""
    print("\033[34m--------------- write html report\033[0m")
    pubT = Path(pubP, "docs", repD["repfile"].strip())
    msgS = htmlx()
    print(f"\033[34m||||||||||||| htmlx: {msgS}\033[0m")
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
headS = "\n" + borderS + "\n| rivt report | " + hdlS + "\n" + borderS + "\n\n"
readmeT = Path(rootP, "README.txt")
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
logging.info("\033[34m|||||||||| README report : \033[0m" + repD["title"])
print(f"\033[34m||||||||||||| README report written:  {short_p}\033[0m")
