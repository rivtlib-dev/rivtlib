"""generate rivtbook report

This module is called by the make-rivtbook.py script file.
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
from pathlib import Path

import __main__

# -------------------- make list of rivtbook folders
bookP = os.getcwd()  # root of rivtbook folders
bookfL = glob.glob("bk*-*", root_dir=bookP)
bookfL.sort()
# -------------------- redefine paths for rivtbook
rstdocsP = Path(bookP, "_rstdocs")  # rst folder
storeP = Path(bookP, "_rvstor")
logsP = Path(storeP, "logs")
rptlogT = Path(storeP, "logs", "reportlog.txt")
rvreadmeT = Path(bookP, "README.txt")
timeS = datetime.now().strftime("%Y-%m-%d")
txtpubP = Path(bookP, "_txtdocs")

modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=rptlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")


print("\n\033[33m||||||||||||||||| folders included in book\033[0m")
for s in bookfL:
    print("\033[33mrivtbook folder:\033[0m", s)
print("\033[33m||||||||||||||||||| \n\n\033[0m")
for file_path in rstdocsP.glob("*.rst"):
    try:
        file_path.unlink()
        print(f"\033[33mDeleted: {file_path}\033[0m")
    except OSError as e:
        print(f"\033[31mError deleting {file_path}: {e}\033[0m")
print("\033[33m||||||||||||| rst files deleted\n\n\033[0m")

# -------------------- get report settings from rivt-report.py
setS = os.getenv("bookset")
configL = configparser.ConfigParser()
configL.read_string(setS)

# Dictionary of config settings
repD = {}
repD["rstdocsP"] = rstdocsP
repD["regen"] = configL["process"]["regen_pdf"]
repD["auto"] = configL["process"]["auto_cfg"]
repD["verbose"] = configL["process"]["book_verbose"]
repD["repfile"] = configL["book"]["book_filename"]
repD["exclude"] = configL["book"]["exclude"]
repD["version"] = configL["book"]["version"]
repD["title"] = configL["layout"]["title"]
repD["subtitle"] = configL["layout"]["subtitle"]
repD["client"] = configL["layout"]["client"]
repD["projref"] = configL["layout"]["project_ref"]
repD["authors"] = configL["layout"]["authors"]
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
get_typeS = repD["repfile"].split(".")[-1].strip()

# -------------------- import rvrepcfg .py file
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import rvrepcfg as rvb  # noqa: E402

# --------------------- add dictionaries to rvb
for key, value in repD.items():
    rvb.repD[key] = value


def pdfx(rstL):
    """write pdf report

    Returns:
        msgS (str): completion message
    """
    # region - pdfx
    repdocT = Path(pdfpubP, repD["repfile"])
    parts = Path(repdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    rvb.pdf_coverS()
    print("\033[33m||||||||||||||||||| report cover page written\033[0m")
    rvb.pdf_yamlS()
    print("\033[33m||||||||||||||||||| report yaml file written\033[0m")
    rvb.pdf_confpy()
    print("\033[33m||||||||||||||||||| report conf file written\033[0m")
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

    tocinS = "\n"
    for item in [rstL]:
        tocinS += textwrap.indent(item, "") + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))

    preamS = insS + imgS + headS + footS + tocrS
    with open(rvindxT, "w", encoding="utf-8") as f5:
        f5.write(preamS)

    print("\033[33m||||||||||||||||||| book - running sphinx-pdf \033[0m")
    curP = Path(os.getcwd())
    os.chdir(curP.parent)
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(pdfpubP)} \n"
    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print(
                f"\033[34m||||||||||||||||||| book - pdf written: {short_p} \033[0m\n"
            )
    except subprocess.CalledProcessError as e:
        print(f"\033[33m||||||||||||||||||| Error executing script: {e}\033[0m")
        print(f"\033[33mStderr:\033[0m {e.stderr}")

    return " "
    # endregion


def txtx(txtfL):
    """write text rivtbook

    Returns:
        msgS (str): completion message
    """
    # region - txtx
    rvrepT = Path(bookP, "_txtdocs", repD["repfile"])
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
    with open(rvrepT, "w", encoding="utf-8") as f5:
        for fname in txtfL:
            fnameT = Path(txtpubP, fname)
            with open(fnameT, "r", encoding="utf-8") as infile:
                f5.write(infile.read())
    with open(rvrepT, "r", encoding="utf-8") as f1:
        content = f1.read()
    with open(rvrepT, "w", encoding="utf-8") as f2:
        f2.write(headS + "\n" + toctxtS + "\n\n" + content)
    parts = Path(rvrepT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"\033[33mtext rivtbook written: {short_p}\033[0m\n"
    # endregion


# ---------- loop over folders in book - get doc title from PUBLISH
doctitleS = " "
dochdrL = []  # for txt
# strtdocS = rivtfL[0]
# strtdocT = Path(bookP, strtdocS)``
for dirS in bookfL:
    bkdivP = Path(bookP, dirS)
    pypathS = os.path.dirname(sys.executable)
    bookPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
    pdfpubP = Path(bookP, "_pdfdocs")
    txtpubP = Path(bookP, "_txtdocs")
    srcP = Path(bkdivP, "rvsrc")
    bookfS = glob.glob("rv???-*.py", root_dir=bkdivP)[0]
    frstT = Path(bkdivP, bookfS)
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
    dochdrL.append(f"{bookfS[2:5]} - {doctitleS}")
    repD["doctitleS"] = doctitleS
    repD["rvbaseS"] = bookfS.split(".py")[0].strip()
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    # -------------------------------------- generate rst file and logs
    if get_typeS == "pdf":
        script_dir = Path(frstT).resolve().parent
        os.chdir(script_dir)
        print("\n\033[33m||| write rst : \033[0m", short_p, "\n")
        print("\n\033[33m||| cwd : \033[0m", os.getcwd(), "\n")
        result = subprocess.run(
            ["python", frstT, "-t", "none", "-k", "true"], text=True
        )
        print(
            f"\033[33m||||||||||||| >> rst << rivtbook chapter generated: {frstT}\033[0m\n"
        )
    elif get_typeS == "txt":
        script_dir = Path(frstT).resolve().parent
        os.chdir(script_dir)
        print("\n\033[33m||| write txt : \033[0m", short_p, "\n")
        print("\n\033[33m||| cwd : \033[0m", os.getcwd(), "\n")
        result = subprocess.run(
            ["python", frstT, "-t", "txt", "-k", "true"], text=True
        )
        print(
            f"\033[33m|||||||||||||| >> txt << rivtbook chapter generated: {frstT}\033[0m\n"
        )
    print("\033[33mresult from subprocess\033[0m", result)
    errlogT = Path(logsP, bookfS[0:7] + "log.txt")
    with open(errlogT, "a") as f1:
        f1.write(f"\033[33m>> {get_typeS} << generated from: {frstT}\033[0m\n")
    logging.info(f">> {get_typeS} << generated from: {frstT}\n")
# ----------------------------------------------------- write pdf - book
if get_typeS == "pdf":
    rstfiL = []
    bookrstL = glob.glob("rv???-*.rst", root_dir=rstdocsP)
    for fS in bookrstL:
        rstfiL.append(fS)
        rsttabL = ["    " + tS for tS in rstfiL]
    rsttabL = "\n".join(rsttabL)
    print("\033[33m||||||||||||| write pdf rivtbook\033[0m")
    pubT = Path(bookP, "_pdfdocs", repD["repfile"].strip())
    msgS = pdfx(rsttabL)
    print(f"\033[33m||||||||||||| pdf rivtbook: {msgS}\033[0m")
elif get_typeS == "txt":
    print("\033[33m||||||||||||| write text rivtbook\033[0m")
    pubT = Path(bookP, "_txtdocs", repD["repfile"].strip())
    txt_folderP = Path(bookP, "_txtdocs")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)
    txtfL.sort()
    msgS = txtx(txtfL)
    print(f"\033[33m||||||||||||| txt rivtbook:  {msgS}\033[0m")
# ------------------------------------- write readme - book
reptitleS = repD["repfile"]
versionS = repD["version"]
authorS = repD["authors"]
toctxtS = "rivtbook Table of Contents\n===================================\n\n"
for item in dochdrL:
    toctxtS += item + "\n"
borderS = "=" * 80
hdlS = repD["title"] + " v-" + versionS + " | " + authorS + " | " + timeS
headS = "\n" + borderS + "\n| rivtbook | " + hdlS + "\n" + borderS + "\n\n"
rtxtS = headS
rme_folderP = Path(bookP, "_rvstor")
rdfL = glob.glob("rv???-*.txt", root_dir=rme_folderP)
rdfL.sort()
with open(rvreadmeT, "w", encoding="utf-8") as outfile:
    for fname in rdfL:
        readT = Path(bookP, "_rvstor", fname)
        with open(readT, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
            outfile.write("\n")
# insert header and toc into readme
with open(rvreadmeT, "r", encoding="utf-8") as f2:
    content = f2.read()
with open(rvreadmeT, "w", encoding="utf-8") as f1:
    f1.write(headS + "\n" + toctxtS + "\n\n" + content)
# with open(, "w", encoding="utf-8") as f3:
parts = Path(rvreadmeT).parts[-3:]  # Take last 3 segments
short_p = ".../" + "/".join(parts)
logging.info(f"|||||||||| README book : {repD['title']}")
print(f"\033[33m||||||||||||| README book written:  {short_p}\033[0m")
