"""generate rivtbook report

The module is called by the make-rivtbook.py script file.
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
rstdocsP = Path(bookP, "_rstdocs")  # rst folder
storeP = Path(bookP, "_rvstor")
logsP = Path(storeP, "logs")
rptlogT = Path(storeP, "logs", "reportlog.txt")
rvreadmeT = Path(bookP, "README.txt")
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


print("\n||||||||||||||||| folders included in book")
for s in bookfL:
    print("rivtbook folder:", s)
print("||||||||||||||||||| \n\n")
for file_path in rstdocsP.glob("*.rst"):
    try:
        file_path.unlink()
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")
print("\n||||||||||||||||| rst files deleted\n\n")

# -------------------- get report settings from rivt-report.py
setS = os.getenv("bookset")
configL = configparser.ConfigParser()
configL.read_string(setS)

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
    print("||||||||||||||||||| report cover page written")
    rvb.pdf_yamlS()
    print("||||||||||||||||||| report yaml file written")
    rvb.pdf_confpy()
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

    tocinS = "\n"
    for item in [rstL]:
        tocinS += textwrap.indent(item, "") + "\n"
    tocrS = toc1S.replace("[replace]", tocinS)
    rvindxT = str(Path(repD["rstdocsP"], "index.rst"))

    preamS = insS + imgS + headS + footS + tocrS
    with open(rvindxT, "w", encoding="utf-8") as f5:
        f5.write(preamS)

    print("||||||||||||||||||| book - running sphinx-pdf ")
    curP = Path(os.getcwd())
    os.chdir(curP.parent)
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc=index {str(rstdocsP)} {str(pdfpubP)} \n"
    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print(f"||||||||||||||||||| book - pdf written: {short_p} \n")
    except subprocess.CalledProcessError as e:
        print(f"||||||||||||||||||| Error executing script: {e}")
        print("Stderr:", e.stderr)

    return " "
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


# ---------- loop over folders in book - get doc title from PUBLISH
doctitleS = " "
dochdrL = []  # for html
# strtdocS = rivtfL[0]
# strtdocT = Path(bookP, strtdocS)
for dirS in bookfL:
    bkdivP = Path(bookP, dirS)
    pypathS = os.path.dirname(sys.executable)
    bookPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
    pdfpubP = Path(bookP, "_pdfdocs")
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
    dochdrS = [bookfS.replace(".py", ".rst"), doctitleS]
    repD["doctitleS"] = doctitleS
    repD["rvbaseS"] = bookfS.split(".py")[0].strip()
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    # -------------------------------------- generate rst file and logs
    script_dir = Path(frstT).resolve().parent
    os.chdir(script_dir)
    print("\n||| generate rst : ", short_p, "\n")
    print("\n||| cwd : ", os.getcwd(), "\n")
    result = subprocess.run(
        ["python", frstT, "-t", "none", "-k", "true"], text=True
    )
    errlogT = Path(logsP, bookfS[0:7] + "log.txt")
    with open(errlogT, "a") as f1:
        f1.write(f">> rst << generated from: {frstT}\n")
    logging.info(f">> rst << generated from: {frstT}\n")
    print(f"||||||||||||| >> rst << file generated from: {frstT}\n")
    print("result from subprocess", result)
# ----------------------------------------------------- write pdf - book
rstfiL = []
bookrstL = glob.glob("rv???-*.rst", root_dir=rstdocsP)
for fS in bookrstL:
    rstfiL.append(fS)
    rsttabL = ["    " + tS for tS in rstfiL]
rsttabL = "\n".join(rsttabL)
print("--------------- write pdf report")
pubT = Path(bookP, "_pdfdocs", repD["repfile"].strip())
msgS = pdfx(rsttabL)
print(f"||||||||||||| pdfx: {msgS}")
# ------------------------------------- write readme - book
reptitleS = repD["repfile"]
versionS = repD["version"]
authorS = repD["authors"]
toctxtS = "Table of Contents\n==================\n"
for item in dochdrL:
    it = item[0]
    toctxtS += it[2] + "." + str(int(it[3:5])) + "  " + item[1] + "\n"
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
logging.info("|||||||||| README book : " + repD["title"])
print(f"||||||||||||| README book written:  {short_p}")
