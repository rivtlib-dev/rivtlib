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
        # region
        # shutil.rmtree(path)
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.reptP = fD["reptP"]
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
        self.docnameS = " "
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
                    self.docnameS = str(pL[1].strip()).strip()
                    if self.docnameS == "--":
                        self.docnameS = " "
                    else:
                        self.docnameS = str(pL[1]).strip()
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
                    obj(self)
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
        self.projrefS = self.configL["layout"]["projectref"]
        self.clientS = self.configL["layout"]["client"]
        self.pdfmarginS = self.configL["layout"]["pdf_margins"]
        self.linkB = self.configL["layout"]["pdf_link_underline"]
        self.titleS = self.configL["layout"]["title"]
        self.subtitleS = self.configL["layout"]["subtitle"]

    def attachpdfx(self):
        """attach pdf or insert pdf as download file"""

        msgS = "attachment"
        return msgS

    def htmlx(self):
        """write html doc

        Returns:
            msgS (str): completion message

        """
        rvd.html_confpy(self, self.fD)  # write conf.py
        rvd.html_coverS(self, self.fD)  # write cover page
        rvd.html_insert(self, self.fD, self.lD)  # write templates

        # write rst file
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        self.docnameS = f"**| D.{self.lD['divS']} |** " + self.docnameS
        self.drstS = f"{self.docnameS}\n" + "=" * 80 + "\n\n" + self.drstS
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)

        rvdocS = self.fD["rbaseS"] + ".html"
        htmldocS = self.fD["htmlpubP"]
        rstdocS = self.fD["rstdocsP"]
        rvbaseS = self.fD["rbaseS"]
        rvdocT = str(Path(self.fD["reptPubP"], "docs", rvdocS))

        htmlcmdS = (
            f"sphinx-build -E -D root_doc={rvbaseS} {rstdocS} {htmldocS} \n"
        )
        try:
            result = subprocess.run(htmlcmdS, shell=True, check=True)
            if not result.returncode:
                print("\nhtml script executed")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)

        parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        return f"file written: {short_p} \n"

    def pdfx(self):
        """write pdf doc

        Returns:
            msgS (str): completion message
        """
        # region
        rvd.pdf_confpy(self, self.fD)  # write conf.py
        rvd.pdf_coverS(self, self.fD)  # write cover page
        rvd.pdf_yamlS(self, self.fD)  # write yaml file
        rvd.pdf_insert(self, self.fD, self.lD)  # write templates

        pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc={self.fD['rbaseS']} {str(self.fD['rstdocsP'])} {self.fD['pdfpubP']} \n"
        try:
            result = subprocess.run(pdfcmdS, shell=True, check=True)
            if not result.returncode:
                print("\npdf script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)

        rvdocS = self.fD["rbaseS"] + ".pdf"
        rvdocT = str(Path(self.fD["reptPubP"], "pdfdocs", rvdocS))
        parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        return f"file written: {short_p} \n"

        # endregion

    def textx(self):
        """write readme and text doc

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
        return f"file written: {short_p} \n" + "file written: .../README.txt"

    def nonex(self):
        """write readme and rst doc"""

        self.confpy()  # update conf.py
        self.yamlS()  # update yaml file
        rvfileS = self.fD["rbaseS"] + ".rst"
        rstfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        self.docnameS = f"**| D.{self.lD['divS']} |** " + self.docnameS
        self.drstS = f"{self.docnameS}\n" + "=" * 80 + "\n\n" + self.drstS
        with open(rstfileT, "w", encoding="utf-8") as f:
            f.write(self.drstS)
            f.flush()  # Forces data out of Python's buffer
            os.fsync(f.fileno())  # Forces the OS to write to disk
        parts = Path(rstfileT).parts[-3:]  # Take last 3 segments
        short_p = ".../" + "/".join(parts)
        return f"file written: {short_p} \n" + "file written: .../README.txt"
