"""
write docs
"""

import configparser
import logging
import os
import subprocess
import warnings
from datetime import datetime
from pathlib import Path

import rvdoccfg as rvd
from fastcore.utils import store_attr

import __main__


class Cmdp:
    """publish doc or report

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
        # shutil.rmtree(path)
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.reptP = fD["reptP"]
        self.reptPubP = fD["reptpubP"]
        errlogT = fD["errlogT"]
        self.confg = []
        self.rvbaseS = fD["rbaseS"]
        self.authorS = " "
        self.verS = " "
        self.copyS = " "
        self.repoS = " "
        self.licenS = " "
        self.f1_authorrs = " "
        self.f1_verS = " "
        self.f1_repoS = " "
        self.f1_liceS = " "
        self.coverlogo = " "
        self.logosize = " "
        self.runlogo = " "
        self.runlabelS = " "
        self.pdfpageS = " "
        self.projrefS = " "
        self.clientS = " "
        self.pdfmarginins = " "
        self.linkB = " "
        self.titleS = " "
        self.subtitleS = " "
        self.privateS = " "
        self.keepS = " "
        self.autoS = " "

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
        warnings.filterwarnings("ignore")
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

        # write README
        with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        with open(self.fD["rvreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        # parse Doc API
        for pS in self.spL:
            if len(pS) > 0:
                if pS[0:11] == "| PUBLISH |":
                    pL = pS[5:].split("|")
                    self.doctitleS = str(pL[1].strip()).strip()
                    if self.doctitleS == "--":
                        self.doctitleS = " "
                    else:
                        self.doctitleS = str(pL[1]).strip()
                    # set doc type
                    typeS = str(pL[2].strip())
                    if typeS not in ["text", "html", "pdf", "none"]:
                        print(
                            "Doc type must be: text, html or pdf \n"
                            "Type is set to default: text"
                        )
                        typeS = "text"
                    if self.lD["ptypeS"] != "--":
                        typeS = self.lD["ptypeS"]
                    dtypeS = typeS + ("x")
                    # call doc functions
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                    print(msgS)
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

        return "\nend of rivt file\n"
        # endregion

    def metadatax(self):
        """read meta blockfor config parameters

        Returns:
            msgS (str): metadata read
        """
        # region - metadata
        self.configL = configparser.ConfigParser()
        self.configL.read_string(self.blockS)
        self.authorS = self.configL["doc"]["authors"]
        self.verS = self.configL["doc"]["version"]
        self.copyS = self.configL["doc"]["copyright"]
        self.repoS = self.configL["doc"]["repo"]
        self.licenS = self.configL["doc"]["license"]
        self.f1_authorS = self.configL["doc"]["fork1_authors"]
        self.f1_verS = self.configL["doc"]["fork1_version"]
        self.f1_repoS = self.configL["doc"]["fork1_repo"]
        self.f1_liceS = self.configL["doc"]["fork1_license"]
        self.coverlogo = self.configL["layout"]["coverlogo"]
        self.logosize = self.configL["layout"]["coverlogo_size"]
        self.runlogo = self.configL["layout"]["runninglogo"]
        self.runlabelS = self.configL["layout"]["runninglabel"]
        self.pdfpageS = self.configL["layout"]["pdf_pagesize"]
        self.projrefS = self.configL["layout"]["project_ref"]
        self.clientS = self.configL["layout"]["client"]
        self.pdfmarginS = self.configL["layout"]["pdf_margins"]
        self.linkB = self.configL["layout"]["pdf_link_underline"]
        self.titleS = self.configL["layout"]["title"]
        self.subtitleS = self.configL["layout"]["subtitle"]
        self.privateS = self.configL["process"]["private_heading"]
        self.keepS = self.configL["process"]["keep_files"]
        self.autoS = self.configL["process"]["auto_cfg"]
        # endregion

    def attachpdfx(self):
        """attach pdf or insert pdf as download file"""

        msgS = "attachment"
        return msgS

    def pdf_insert(self):
        """insert pdf header"""

        # region - insert pdf header
        doctitleS = f"**|D.{self.lD['divS']}|** " + self.doctitleS
        timeS = datetime.now().strftime("%Y-%m-%d")
        headblkS = (
            f"""{doctitleS} - v{self.verS} |s| |s| |s| |s|  **###Section###**"""
        )
        foot1blkS = f"""{timeS} |s| |s| |s| **|** |s| |s| |s| {self.authorS}"""
        foot2blkS = f"""**{self.runlabelS}**"""

        imgS = f"""
.. |blklogo| image:: ../{self.runlogo}
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

        drstS = ".. |s| unicode:: 0xA0 \n\n\n" + imgS + headS + footS

        return drstS

    def htmlx(self):
        """write html doc

        Returns:
            msgS (str): completion message

        """
        # region - htmlx
        rvd.html_confpy(self, self.fD)  # write conf.py
        rvd.html_templ(self, self.fD)  # write templates

        # write rst file
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        self.doctitleS = f"**| D.{self.lD['divS']} |** " + self.doctitleS
        self.drstS = f"{self.doctitleS}\n" + "=" * 80 + "\n\n" + self.drstS
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
            if not result.returncode:
                pass
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)

        # write README
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.reptPubP, "txtdocs", rvdocS))
        borderS = "-" * self.lD["widthI"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.doctitleS
        versionS = "v-" + self.verS.strip()
        authorS = self.authorS.strip()
        hdlS = doctitleS + " | " + authorS + " | " + versionS + " | " + timeS
        headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n"
        dutfS = headS + "\n" + self.dutfS

        with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)
        with open(self.fD["rvreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)

        parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        print(f"\nHTML doc written to {short_p}")

        return f"\nThe README doc is in: {self.fD['rivtfldN']}"
        # endregion

    def pdfx(self):
        """write pdf doc

        Returns:
            msgS (str): completion message
        """
        # region - pdfx
        rvd.pdf_confpy(self, self.fD)  # write conf.py
        rvd.pdf_coverS(self, self.fD)  # write cover page
        rvd.pdf_yamlS(self, self.fD)  # write yaml file

        inS = self.pdf_insert()
        rstdP = Path(self.fD["rstdocP"], self.fD["rbaseS"] + ".rst")
        with open(rstdP, "r") as f1:
            contentS = f1.read()
        with open(rstdP, "w") as f2:
            f2.write(inS + contentS)

        with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        rvdocS = self.fD["rbaseS"] + ".pdf"
        rvdocT = str(Path(self.reptPubP, "pdfdocs", rvdocS))
        parts = Path(rvdocT).parts[-4:-1]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)

        pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc={self.fD['rbaseS']} {str(self.fD['rstdocsP'])} {self.fD['pdfpubP']} \n"
        try:
            result = subprocess.run(pdfcmdS, shell=True, check=True)
            if not result.returncode:
                print(f"\nPDF doc written to {short_p}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)

        # write README
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.reptPubP, "txtdocs", rvdocS))
        borderS = "-" * self.lD["widthI"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.doctitleS
        versionS = "v-" + self.verS.strip()
        authorS = self.authorS.strip()
        hdlS = doctitleS + " | " + authorS + " | " + versionS + " | " + timeS
        headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n"
        dutfS = headS + "\n" + self.dutfS

        with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)
        with open(self.fD["rvreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)

        return " "
        # endregion

    def txtx(self):
        """write text doc and README

        Returns:
            msgS (str): completion message
        """

        # region - textx
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.reptPubP, "txtdocs", rvdocS))
        borderS = "-" * self.lD["widthI"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.doctitleS
        versionS = "v-" + self.verS.strip()
        authorS = self.authorS.strip()
        hdlS = doctitleS + " | " + authorS + " | " + versionS + " | " + timeS
        headS = "\n" + borderS + "\n" + hdlS + "\n" + borderS + "\n"
        dtxtS = headS + "\n" + self.dtxtS
        dutfS = headS + "\n" + self.dutfS

        with open(rvdocT, "w", encoding="utf-8") as f5:
            f5.write(dtxtS)
        with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)
        with open(self.fD["rvreadmeT"], "w", encoding="utf-8") as f5:
            f5.write(dutfS)

        parts = Path(rvdocT).parts[-4:-1]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        return (
            f"The text doc is in : {short_p} \n\n"
            + f"The README doc is in: {self.fD['rivtfldN']}"
        )
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

        return f"nonex - rst file written: {short_p} \n"
        # endregion
