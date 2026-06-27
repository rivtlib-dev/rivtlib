"""
write docs
"""

import configparser
import glob
import logging
import os
import shutil
import subprocess
import warnings
from datetime import datetime
from pathlib import Path

import rvdoccfg as rvd
from fastcore.utils import store_attr

import __main__


class Cmdp:
    """publish doc

    Args:
        Args:
            fD (dict): fDers
            lD (dict): labels
            rivD (dict): values
            rivL (list): values for export

        Vars:
            sS (str): rv.D API content substring
            uS (str): utf doc string
            r2S (str): rlabpdf doc string
            rS (str): reST doc string
    """

    def __init__(self, sS, fD, lD, dutfS, drstS, dtxtS):

        # region - init
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.reptP = fD["reptP"]
        self.reptPubP = fD["reptpubP"]
        errlogT = fD["errlogT"]
        self.rvbaseS = fD["rbaseS"]
        self.rstdocsP = fD["rstdocsP"]
        self.reptypeS = lD["reptypeS"]
        self.repkeepS = lD["repkeepS"]
        self.confg = []
        self.authorS = " "
        self.verS = " "
        self.copyrightS = " "
        self.repoS = " "
        self.licenS = " "
        self.f1_authorrs = " "
        self.f1_verS = " "
        self.f1_repoS = " "
        self.f1_licenS = " "
        self.coverlogo = " "
        self.logosize = " "
        self.runlogo = " "
        self.runlabelS = " "
        self.pdfpageS = " "
        self.projrefS = " "
        self.clientS = " "
        self.pdfmarginins = " "
        self.linkB = " "
        self.doctitleS = " "
        self.subtitleS = " "
        self.privateS = " "
        self.autoS = " "

        warnings.filterwarnings("ignore")
        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  "
            + modnameS
            + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogT,
            filemode="w",
        )
        self.logging = logging

        # strip leading spaces and comments from section
        sL = sS.split("\n")  # unprocessed lines
        spL = []
        for slS in sL[1:]:
            if len(slS) < 5:
                continue
            if len(slS.strip()) > 0:
                spL.append(slS[4:])
        self.spL = spL  # preprocessed list
        with open(errlogT, "a") as f4:
            f4.write(self.sL[0] + "\n")
        self.logging.info("SECTION : " + self.sL[0])
        # copy images
        if lD["reptflagS"] == "doc":
            src_P = str(Path(fD["reptP"], "img", "*.*"))
            destP = str(Path(fD["rstdocsP"], "_static"))
            for fileP in glob.glob(src_P):
                shutil.copy(fileP, destP)
        elif lD["reptflagS"] == "chapter":
            src_P = str(Path(fD["reptP"], "img", "*.*"))
            destP = str(Path(fD["rstdocsP"], "_static"))
            for fileP in glob.glob(src_P):
                shutil.copy(fileP, destP)

        # clean rst files
        if lD["repkeepS"].strip() == "true":
            pass
        elif lD["repkeepS"].strip() == "false":
            rstdocsP = fD["rstdocsP"]
            for file_path in rstdocsP.glob("*.rst"):
                try:
                    file_path.unlink()
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")
        # endregion

    def cmdx(self):
        """parse commands and blocks in Doc API
        Commands:
            | PUBLISH | doc name; -- | text; html; pdf;
            | ATTACHPDF | rel. path | prepend;append

        Blocks:
            _[[METADATA]]
            _[[END]]

        Returns:
            msgS (str): completion message
        """
        # region
        blockB = False
        self.blockS = """"""
        self.doctitleS = " "
        uS = rS = tS = lS = ""
        # parse Doc API
        for pS in self.spL:
            if len(pS) > 0:
                if pS[0:11] == "| PUBLISH |":
                    pL = pS[5:].split("|")
                    if self.doctitleS == "--":
                        self.doctitleS = " "
                    else:
                        self.doctitleS = pL[1].strip()
                    # set doc type
                    print(
                        "reptypeS -------------------- | ", self.lD["reptypeS"]
                    )
                    if self.lD["reptypeS"] != "---":
                        typeS = self.lD["reptypeS"]
                    else:
                        typeS = str(pL[2].strip())
                    if typeS not in ["txt", "html", "pdf", "none"]:
                        print("Doc type must be: txt, html or pdf \n")
                    dtypeS = typeS + ("x")
                    print("dtypeS -------------------- | ", dtypeS)
                    continue
                elif pS[0:13] == "| ATTACHPDF |":
                    dtypeS = "attachpdfx"
                    self.pthS = pL[1].strip()
                    self.parS = pL[2].strip()
                    obj = getattr(Cmdp, dtypeS)
                    obj(self)
                    continue
                elif "_[[" in pS and ("_[[END]]" not in pS):  # block start
                    bsL = pS.split("]]")
                    tagS = bsL[0][3:].strip()
                    if tagS == "METADATA":
                        # print(f"{tagS=}")
                        self.logging.info(f"block tag : {tagS}]]")
                        self.blockS = """"""
                        blockB = True
                        continue
                elif blockB and ("_[[END]]" in pS):  # block terminate
                    if tagS == "METADATA":
                        obj = getattr(Cmdp, "metadatax")
                        obj(self)
                        self.blockS = """"""
                        continue
                elif blockB:
                    self.blockS += pS + "\n"
                    continue
                else:  # everything else
                    pass
            uS += pS
            rS += pS
            tS += pS
            lS += pS
        # call publish function
        obj = getattr(Cmdp, dtypeS)
        msgS = obj(self)
        print(msgS)

        rme_msgS = self.docreadme()
        print(rme_msgS)

        return "------------------ End of doc processing"
        # endregion

    def metadatax(self):
        """read meta block for config parameters

        Returns:
            msgS (str): metadata read
        """
        # region - metadata
        self.configL = configparser.ConfigParser()
        self.configL.read_string(self.blockS)
        self.authorS = self.configL["doc"]["authors"]
        self.verS = self.configL["doc"]["version"]
        self.copyrightS = self.configL["doc"]["copyright"]
        self.repoS = self.configL["doc"]["repo"]
        self.licenS = self.configL["doc"]["license"]
        self.f1_authorS = self.configL["doc"]["fork1_authors"]
        self.f1_verS = self.configL["doc"]["fork1_version"]
        self.f1_repoS = self.configL["doc"]["fork1_repo"]
        self.f1_licenS = self.configL["doc"]["fork1_license"]
        self.coverlogo = self.configL["layout"]["coverlogo"]
        self.coverpageB = self.configL["layout"]["coverpage"]
        self.logosize = self.configL["layout"]["coverlogo_size"]
        self.runlogo = self.configL["layout"]["runninglogo"]
        self.runlabelS = self.configL["layout"]["runninglabel"]
        self.pdfpageS = self.configL["layout"]["pdf_pagesize"]
        self.projrefS = self.configL["layout"]["project_ref"]
        self.clientS = self.configL["layout"]["client"]
        self.pdfmarginS = self.configL["layout"]["pdf_margins"]
        self.linkB = self.configL["layout"]["pdf_link_underline"]
        self.subtitleS = self.configL["layout"]["subtitle"]
        self.doc_verbose = self.configL["process"]["doc_verbose"]
        self.auto_cfg = self.configL["process"]["auto_cfg"]
        self.toc_level = self.configL["layout"]["toc_level"]
        # endregion

    def attachpdfx(self):
        """attach pdf or insert pdf as download file"""

        msgS = "attachment"
        return msgS

    def pdfx(self):
        """write pdf doc

        Returns:
            msgS (str): completion message
        """
        # region - pdfx
        rvd.pdf_confpy(self, self.fD)  # write conf.py
        rvd.pdf_yamlS(self, self.fD)  # write yaml file
        inS = self.pdf_insert()
        rstdP = Path(self.fD["rstdocsP"], self.fD["rbaseS"] + ".rst")
        with open(rstdP, "w", encoding="utf-8") as f2:
            f2.write(inS + self.drstS)
        rvdocS = self.fD["rbaseS"] + ".pdf"
        rvdocT = str(Path(self.reptPubP, "pdfdocs", rvdocS))
        parts = Path(rvdocT).parts[-4:-1]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)

        pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc={self.fD['rbaseS']} {str(self.fD['rstdocsP'])} {self.fD['pdfpubP']} \n"
        try:
            result = subprocess.run(pdfcmdS, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            result = f"[Error executing script]: {e}"
        # print("------------ | ", result)
        return f"\n ------------------   PDF doc written to  | {short_p}"
        # endregion

    def pdf_insert(self):
        """insert pdf header"""

        # region - insert pdf header
        timeS = datetime.now().strftime("%Y-%m-%d")
        headblkS = f"""**{self.doctitleS}** - v{self.verS} |s| |s| |s| |s|  **###Section###**"""
        foot1blkS = f"""{timeS} |s| |s| |s| **|** |s| |s| |s| {self.authorS}"""
        foot2blkS = f"""**{self.runlabelS}**"""

        imgS = f"""
.. |blklogo| image:: ./_static/{self.runlogo}
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
        # endregion

        # region pdf-cover page
        coverpgS = f"""
.. role:: btext
   :class: big-text

.. role:: mtext
    :class: medium-text

.. role:: stext
    :class: small-text

|
|
|
|
        
.. image:: _static/{self.coverlogo}
   :width: {self.logosize}%
   :align: center

|
|
|
|
|

.. rst-class:: center

    :mtext:`{self.subtitleS}`

|

.. rst-class:: center

    :btext:`{self.doctitleS}`
    
|
|
|
|
|


.. rst-class:: center

    :mtext:`{self.clientS}`

|

.. rst-class:: center

    :stext:`{self.projrefS}`

   """

        instocS = f"""
.. raw:: pdf

   PageBreak noHead
      
**{self.doctitleS}** - v{self.verS}

--------------------

|

.. contents:: Table of Contents
  :depth: {self.toc_level}

  
.. raw:: pdf
 
   PageBreak mainPage
   SetPageCounter 1

"""
        # endregion

        insrstS = (
            ".. |s| unicode:: 0xA0 \n\n\n" + imgS + headS + footS + instocS
        )
        if self.coverpageB.capitalize() == "True":
            insrstS = (
                ".. |s| unicode:: 0xA0 \n\n\n"
                + imgS
                + headS
                + footS
                + coverpgS
                + instocS
            )
        else:
            pass

        return insrstS

    def htmlx(self):
        """write html doc

        Returns:
            msgS (str): completion message

        """
        # region - htmlx
        rvd.html_confpy(self, self.fD)  # write conf.py
        rvd.html_templ(self, self.fD)  # write templates
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        doctitleS = f"**{self.doctitleS}**"
        # doctitleS = f"**| {self.lD['divS']}.{sdivS} |** " + self.doctitleS
        self.drstS = f"{doctitleS}\n" + "=" * 80 + "\n\n" + self.drstS
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        rvdocS = self.fD["rbaseS"] + ".html"
        htmldocS = self.fD["htmlpubP"]
        rstdocS = self.fD["rstdocsP"]
        rvbaseS = self.fD["rbaseS"]
        rvdocT = str(Path(self.reptPubP, "docs", rvdocS))

        htmlcmdS = (
            f"sphinx-build -E -D root_doc={rvbaseS} {rstdocS} {htmldocS} \n"
        )
        try:
            result = subprocess.run(htmlcmdS, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)

        parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)

        print("---------- | ", result)
        return f"HTML doc written to -------------- | {short_p}"

        # endregion

    def txtx(self):
        """write text doc

        Returns:
            msgS (str): completion message
        """
        # region - txtx
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.reptPubP, "txtdocs", rvdocS))
        borderS = "-" * self.lD["widthI"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.doctitleS
        versionS = "v-" + self.verS.strip()
        authorS = self.authorS.strip()
        doctitleS = self.doctitleS
        hdlS = doctitleS + " | " + authorS + " | " + versionS + " | " + timeS
        headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n"
        dtxtS = headS + "\n" + self.dtxtS
        with open(rvdocT, "w", encoding="utf-8") as f5:
            f5.write(dtxtS)

        parts = Path(rvdocT).parts[-4:-1]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        return f"text doc written to -------------- | {short_p}"
        # endregion

    def nonex(self):
        """write report rst doc

        Returns:
            msgS (str): completion message

        """
        # region - nonex
        rvfileS = self.fD["rbaseS"] + ".rst"
        rstfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        with open(rstfileT, "w", encoding="utf-8") as f:
            f.write(self.drstS)

        parts = Path(rstfileT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)

        return f"rst file written for doc --------------- | : {short_p}"
        # endregion

    def docreadme(self):
        """write doc readme to root and public"""

        borderS = "-" * self.lD["widthI"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.doctitleS
        versionS = "v-" + self.verS.strip()
        authorS = self.authorS.strip()
        hdlS = (
            "| rivt | "
            + doctitleS
            + " | "
            + authorS
            + " | "
            + versionS
            + " | "
            + timeS
        )
        headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n"
        dutfS = headS + "\n" + self.dutfS

        with open(self.fD["docreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)
        with open(self.fD["rvreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)
        # with open(self.fD["publreadmeT"], "w", encoding="utf-8") as f5:
        #     f5.write(dutfS)

        parts = Path(self.fD["docreadmeT"]).parts[-4:-1]  # Take last 3 segments
        short_p1 = ".../" + "/".join(parts)
        parts = Path(self.fD["rvreadmeT"]).parts[-3:-1]  # Take last 2 segments
        short_p2 = ".../" + "/".join(parts)
        return (
            f"README.txt written to -------------- |  {short_p1}\n"
            + f"README.txt written to -------------- |  {short_p2}"
        )
