import configparser
import logging
import os
import subprocess
import sys
import warnings
from datetime import datetime
from pathlib import Path

from fastcore.utils import store_attr

import __main__


class Cmdp:
    """doc publish object

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

    def __init__(self, sS, fD, lD, cmdL, tagL, dutfS, drstS, dtxtS, rivtD):
        # region
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.rivtP = fD["rivtP"]
        errlogT = fD["errlogT"]
        self.confg = []

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
            | PUBLISH | doc name; - | text; html; pdf; texpdf
            | ATTACHPDF | rel. path | prepend;append

        Blocks:
            _[[METADATA]]
            _[[END]]

        Returns:
            msgS (str): completion message
        """
        # region
        msgS = ""
        ptempS = ""
        blockB = False
        self.blockS = """"""
        self.docnameS = " "
        for pS in self.spL:
            pL = pS[1:].split("|")
            if len(pL) > 0 and pL[0].strip() in self.cmdL:  #
                if pL[0].strip() == "PUBLISH":
                    typeS = str(pL[2].strip())
                    self.docnameS = str(pL[1].strip()).strip()
                    if self.docnameS == "-":
                        self.docnameS = self.fD["docnameS"]
                    dtypeS = typeS + ("x")
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                elif pL[0].strip() == "ATTACHPDF":
                    dtypeS = "attachpdfx"
                    self.pthS = pL[1].strip()
                    self.parS = pL[2].strip()
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                else:
                    pass
            if "_[[" in pS and ("_[[END]]" not in pS):  # block accumulate
                bsL = pS.split("]]")
                tagS = bsL[0].strip()
                if tagS in self.tagL:  # check list
                    # print(f"{tagS=}")
                    self.logging.info(f"block tag : {tagS}]]")
                    ptempS = tagS = bsL[0].strip()
                    self.blockS = """"""
                    blockB = True
                    continue
            if blockB and ("_[[END]]" in pS):  # block terminate
                if "METADATA" in ptempS:
                    ptempS = ""
                    obj = getattr(Cmdp, "metadatax")
                    msgS = obj(self)
                    self.blockS = """"""
                    continue
            if blockB:
                self.blockS += pS + "\n"
            else:  # everything else
                pass

        return msgS
        # endregion

    def htmlx(self):
        """write readme and sphinx-html files

        Returns:
            msgS (str): completion message

        """
        rvbaseS = self.fD["rbaseS"]
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".html"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        rvdocT = str(Path(self.fD["rivtpubP"], "docs", rvdocS))
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        htmlcmdS = f"sphinx-build -E -D root_doc={rvbaseS} {str(self.fD['rstdocsP'])} {self.fD['htmlpubP']} \n"
        try:
            result = subprocess.run(htmlcmdS, shell=True, check=True)
            if not result.returncode:
                print("\nhtml script executed")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        return (
            f"html doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )

        # add layout info
        # timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        # doctitleS = self.fD["rbaseS"]
        # authorS = self.rivD["metaD"]["authors"]
        # verS = "  v" + self.rivD["metaD"]["version"]
        # spaceS = "  |  "
        # headS = timeS + spaceS + authorS + spaceS + doctitleS + verS
        # headerS = f".. header::\n\n   {headS}\n"
        # self.drstS = headerS + self.drstS + "\n"

    def pdfx(self):
        """write readme and sphinx-pdf files

        Returns:
            msgS (str): completion message
        """
        # region
        rvbaseS = self.fD["rbaseS"]
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".pdf"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        rvdocT = str(Path(self.fD["rivtpubP"], "pdfdocs", rvdocS))
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        pdfcmdS = f"sphinx-build -E -b pdf -D root_doc={rvbaseS} {str(self.fD['rstdocsP'])} {self.fD['pdfpubP']} \n"
        try:
            result = subprocess.run(pdfcmdS, shell=True, check=True)
            if not result.returncode:
                print("\npdf script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        return (
            f"pdf doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )
        # endregion

        # # add layout info
        # timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        # doctitleS = self.fD["rbaseS"]
        # authorS = self.rivD["metaD"]["authors"]
        # verS = "  v" + self.rivD["metaD"]["version"]
        # spaceS = "  |  "
        # headS = timeS + spaceS + authorS + spaceS + doctitleS + verS
        # headerS = f".. header::\n\n   {headS}\n"
        # self.drstS = headerS + self.drstS + "\n"

        # versionS = "v-0"
        # rvfileS = self.fD["rbaseS"] + ".rst2"
        # rvdocS = self.fD["rbaseS"] + ".pdf"
        # rvfileT = str(Path(self.fD["rivtpubP"], rvfileS))
        # rvdocT = str(Path(self.fD["rivtpubP"], rvdocS))
        # timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        # doctitleS = "**" + self.docnameS + "**"
        # versionS = "v-" + self.versionS.strip()
        # authorS = self.authorS.strip()
        # footblkS = (
        #     doctitleS
        #     + "  **|**  "
        #     + authorS
        #     + "  **|**  "
        #     + timeS
        #     + "  **|**  "
        #     + versionS
        #     + "\n"
        # )
        # pageS = "   Page ###Page### of ###Total###"
        # imglogoS = " " + self.logopathS

        # imgS = (
        #     ".. |blklogo| image::"
        #     + imglogoS
        #     + "\n"
        #     + "   :width: 175px\n"
        #     + "   :alt: logo\n\n"
        # )
        # headS = ".. header::\n\n" + pageS + "\n\n"
        # footS = (
        #     ".. footer:: \n\n"
        #     + "   .. list-table::\n"
        #     + "      :class: foottable2\n"
        #     + "      :align: center\n"
        #     + "      :widths: 88 12\n"
        #     + " \n"
        #     + "      * - "
        #     + footblkS
        #     + "        - |blklogo|\n\n"
        # )
        # pgtemp = ".. contents:: " + self.docnameS + "\n   :depth: 2 \n\n "
        # self.drlabS = pgtemp + self.drlabS
        # self.drlabS = self.drlabS + "\n" + imgS + headS + footS
        # with open(rvfileT, "w", encoding="utf-8") as f5:
        #     f5.write(self.drlabS)
        # with open("README.txt", "w", encoding="utf-8") as f5:
        #     f5.write(self.dutfS)
        # iniP = str(Path(rvstyleP, "layout.ini"))
        # fontP = str(Path(rvstyleP, "fonts"))
        # yamlS = "rlabpdf.yaml"
        # cmd1S = "rst2pdf " + rvfileT  # input
        # cmd2S = " -o " + rvdocT  # output
        # cmd3S = " --config=" + iniP  # config
        # cmd4S = " --font-path=" + fontP  # fonts
        # cmd5S = " --stylesheet-path=" + rvstyleP  # style path
        # cmd6S = " --stylesheets=" + yamlS  # styles
        # rlabcmdS = cmd1S + cmd2S + cmd3S + cmd4S + cmd5S + cmd6S
        # print("rlabcmdS=", rlabcmdS)
        # sphinx-build -b pdf rstdocs pdfdocs
        # echo.Build finished. The PDF files are in pdfdocs

    def textx(self):
        """write readme and text files

        Returns:
            msgS (str): completion message
        """
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.fD["rivtpubP"], "txtdocs", rvdocS))
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
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        return (
            f"text doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )

    def metadatax(self):
        """read meta block as config file

        Returns:
            msgS (str): metadata read
        """

        self.configL = configparser.ConfigParser()
        self.configL.read_string(self.blockS)
        self.authorS = self.configL["doc"]["authors"]
        self.verS = self.configL["doc"]["version"]
        self.repoS = self.configL["doc"]["repo"]
        self.liceS = self.configL["doc"]["license"]
        self.f1_authorS = self.configL["doc"]["fork1_authors"]
        self.f1_verS = self.configL["doc"]["fork1_version"]
        self.f1_repoS = self.configL["doc"]["fork1_repo"]
        self.f1_liceS = self.configL["doc"]["fork1_license"]
        self.logopathS = self.configL["layout"]["logoname"]
        self.footerS = self.configL["layout"]["pdf_footer"]
        self.pagesizeS = self.configL["layout"]["pdf_pagesize"]
        self.marginS = self.configL["layout"]["pdf_margins"]
        self.rlabheaderS = self.configL["layout"]["pdf_header"]
        self.rlabcoverS = self.configL["layout"]["text_width"]

    def attachpdfx(self):
        """attach pdf or insert pdf as download file"""

        msgS = "attachment"
        return msgS

    def latexx(self):
        """Modify TeX file to avoid problems with escapes:

        -  Replace marker "aaxbb " inserted by rivt with
            \\hfill because it is not handled by reST).
        - Delete inputenc package
        - Modify section title and add table of contents

         write calc rSt file to d00_docs fDer

        Args:
            cmdS (str): [description]
            doctypeS ([type]): [description]
            stylefileS ([type]): [description]
            calctitleS ([type]): [description]
            startpageS ([type]): [description]

        convert reST to tex file

        0. insert [i] data into model (see _genxmodel())
        1. read the expanded model
        2. build the operations ordered dictionary
        3. execute the dictionary and write the md-8 calc and Python file
        4. if the pdf flag is set re-execute xmodel and write the PDF calc
        5. write variable summary to stdout

        :param pdffileS: _description_
        :type pdffileS: _type_

        """
        pypathS = os.path.dirname(sys.executable)
        rvstyleP = os.path.join(
            pypathS,
            "Lib",
            "site-packages",
            "rivtlib",
            "styles",
        )
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".html"

        #  # region
        #     startS = str(lD["pageI"])
        #     doctitleS = str(lD["doctitleS"])

        #     with open(tfileP, "r", encoding="md-8", errors="ignore") as f2:
        #         texf = f2.read()

        #     # modify "at" command
        #     texf = texf.replace(
        #         """\\begin{document}""",
        #         """\\renewcommand{\contentsname}{"""
        #         + doctitleS
        #         + "}\n"
        #         + """\\begin{document}\n"""
        #         + """\\makeatletter\n"""
        #         + """\\renewcommand\@dotsep{10000}"""
        #         + """\\makeatother\n""",
        #     )

        #     # add table of contents, figures and tables
        #     # texf = texf.replace("""\\begin{document}""",
        #     #                     """\\renewcommand{\contentsname}{""" + doctitleS
        #     #                     + "}\n" +
        #     #                     """\\begin{document}\n""" +
        #     #                     """\\makeatletter\n""" +
        #     #                     """\\renewcommand\@dotsep{10000}""" +
        #     #                     """\\makeatother\n""" +
        #     #                     """\\tableofcontents\n""" +
        #     #                     """\\listoftables\n""" +
        #     #                     """\\listoffigures\n""")

        #     texf = texf.replace("""inputenc""", """ """)
        #     texf = texf.replace("aaxbb ", """\\hfill""")
        #     texf = texf.replace("?x?", """\\""")
        #     texf = texf.replace(
        #         """fancyhead[L]{\leftmark}""",
        #         """fancyhead[L]{\\normalsize\\bfseries  """ + doctitleS + "}",
        #     )
        #     texf = texf.replace("x*x*x", "[" + lD["docnumS"] + "]")
        #     texf = texf.replace("""\\begin{tabular}""", "%% ")
        #     texf = texf.replace("""\\end{tabular}""", "%% ")
        #     texf = texf.replace(
        #         """\\begin{document}""",
        #         """\\begin{document}\n\\setcounter{page}{""" + startS + "}\n",
        #     )

        #     with open(tfileP, "w", encoding="md-8") as f2:
        #         f2.write(texf)

        #         # with open(tfileP, 'w') as texout:
        #         #    print(texf, file=texout)

        #         pdfD = {
        #             "xpdfP": Path(tempP, docbaseS + ".pdf"),
        #             "xhtmlP": Path(tempP, docbaseS + ".html"),
        #             "xrstP": Path(tempP, docbaseS + ".rst"),
        #             "xtexP": Path(tempP, docbaseS + ".tex"),
        #             "xauxP": Path(tempP, docbaseS + ".aux"),
        #             "xoutP": Path(tempP, docbaseS + ".out"),
        #             "xflsP": Path(tempP, docbaseS + ".fls"),
        #             "xtexmakP": Path(tempP, docbaseS + ".fdb_latexmk"),
        #         }

        #     _mod_tex(texfileP)

        #     pdfS = _gen_pdf(texfileP)

        #     pdfD = {
        #         "cpdfP": Path(_dpathP0 / ".".join([_cnameS, "pdf"])),
        #         "chtml": Path(_dpathP0 / ".".join([_cnameS, "html"])),
        #         "trst": Path(_dpathP0 / ".".join([_cnameS, "rst"])),
        #         "ttex1": Path(_dpathP0 / ".".join([_cnameS, "tex"])),
        #         "auxfile": Path(_dpathP0 / ".".join([_cnameS, ".aux"])),
        #         "omdile": Path(_dpathP0 / ".".join([_cnameS, ".out"])),
        #         "texmak2": Path(_dpathP0 / ".".join([_cnameS, ".fls"])),
        #         "texmak3": Path(_dpathP0 / ".".join([_cnameS, ".fdb_latexmk"])),
        #     }
        #     if stylefileS == "default":
        #         stylefileS = "pdf_style.sty"
        #     else:
        #         stylefileS == stylefileS.strip()
        #     style_path = Path(_dpathP0 / stylefileS)
        #     print("INFO: style sheet " + str(style_path))
        #     pythoncallS = "python "
        #     if sys.platform == "linux":
        #         pythoncallS = "python3 "
        #     elif sys.platform == "darwin":
        #         pythoncallS = "python3 "

        #     rst2xeP = Path(rivtpath / "scripts" / "rst2xetex.py")
        #     texfileP = pdfD["ttex1"]
        #     tex1S = "".join(
        #         [
        #             pythoncallS,
        #             str(rst2xeP),
        #             " --embed-stylesheet ",
        #             " --documentclass=report ",
        #             " --documentoptions=12pt,notitle,letterpaper ",
        #             " --stylesheet=",
        #             str(style_path) + " ",
        #             str(_rstfileP) + " ",
        #             str(texfileP),
        #         ]
        #     )

        #     os.chdir(_dpathP0)
        #     os.system(tex1S)
        #     print("INFO: tex file written " + str(texfileP))

        #     # fix escape sequences
        #     fnumS = _setsectD["fnumS"]
        #     with open(texfileP, "r", encoding="md-8", errors="ignore") as texin:
        #         texf = texin.read()
        #     texf = texf.replace("?x?", """\\""")
        #     texf = texf.replace(
        #         """fancyhead[L]{\leftmark}""",
        #         """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
        #     )
        #     texf = texf.replace("x*x*x", fnumS)
        #     texf = texf.replace("""\\begin{tabular}""", "%% ")
        #     texf = texf.replace("""\\end{tabular}""", "%% ")
        #     texf = texf.replace(
        #         """\\begin{document}""",
        #         """\\begin{document}\n\\setcounter{page}{""" + startpageS + "}\n",
        #     )

        #     # texf = texf.replace(
        #     #     """\\begin{document}""",
        #     #     """\\renewcommand{\contentsname}{"""
        #     #     + self.calctitle
        #     #     + "}\n"
        #     #     + """\\begin{document}"""
        #     #     + "\n"
        #     #     + """\\makeatletter"""
        #     #     + """\\renewcommand\@dotsep{10000}"""
        #     #     + """\\makeatother"""
        #     #     + """\\tableofcontents"""
        #     #     + """\\listoftables"""
        #     #     + """\\listoffigures"""
        #     # )

        #     time.sleep(1)
        #     with open(texfileP, "w", encoding="md-8") as texout:
        #         texout.write(texf)
        #     print("INFO: tex file updated")

        #     if doctypeS == "pdf":
        #         gen_pdf(texfileP)

        #     os._exit(1)

        #     # os.system('latex --version')
        #     os.chdir(tempP)
        #     texfS = str(pdfD["xtexP"])
        #     # pdf1 = 'latexmk -xelatex -quiet -f ' + texfS + " > latex-log.txt"
        #     pdf1 = "xelatex -interaction=batchmode " + texfS
        #     # print(f"{pdf1=}"")
        #     os.system(pdf1)
        #     srcS = ".".join([docbaseS, "pdf"])
        #     dstS = str(Path(reportP, srcS))
        #     shutil.copy(srcS, dstS)

        #     global fD

        #     style_path = fD["styleP"]
        #     # print(f"{style_path=}")
        #     # f2 = open(style_path)
        #     # f2.close

        #     pythoncallS = "python "
        #     if sys.platform == "linux":
        #         pythoncallS = "python3 "
        #     elif sys.platform == "darwin":
        #         pythoncallS = "python3 "

        #     rst2texP = Path(rivtP, "scripts", "rst2latex.py")
        #     # print(f"{str(rst2texP)=}")
        #     texfileP = Path(tempP, docbaseS + ".tex")
        #     rstfileP = Path(tempP, docbaseS + ".rst")

        #     with open(rstfileP, "w", encoding="md-8") as f2:
        #         f2.write(rstS)

        #     tex1S = "".join(
        #         [
        #             pythoncallS,
        #             str(rst2texP),
        #             " --embed-stylesheet ",
        #             " --documentclass=report ",
        #             " --documentoptions=12pt,notitle,letterpaper ",
        #             " --stylesheet=",
        #             str(style_path) + " ",
        #             str(rstfileP) + " ",
        #             str(texfileP),
        #         ]
        #     )
        #     logging.info(f"tex call:{tex1S=}")
        #     os.chdir(tempP)
        #     try:
        #         os.system(tex1S)
        #         time.sleep(1)
        #         logging.info(f"tex file written: {texfileP=}")
        #         print(f"tex file written: {texfileP=}")
        #     except SystemExit as e:
        #         logging.exception("tex file not written")
        #         logging.error(str(e))
        #         sys.exit("tex file write failed")

        #     """write pdf calc to reports fDer and open

        #     Args:
        #         texfileP (path): doc config fDer
        #     """

        #     global rstcalcS, _rstflagB

        #     os.chdir()
        #     time.sleep(1)  # cleanup tex files
        #     os.system("latexmk -c")
        #     time.sleep(1)

        #     pdfmkS = (
        #         "perl.exe c:/texlive/2020/texmf-dist/scripts/latexmk/latexmk.pl "
        #         + "-pdf -xelatex -quiet -f "
        #         + str(texfileP)
        #     )

        #     os.system(pdfmkS)
        #     print("\nINFO: pdf file written: " + ".".join([_cnameS, "pdf"]))

        #     dnameS = _cnameS.replace("c", "d", 1)
        #     docpdfP = Path(_dpathP / ".".join([dnameS, "pdf"]))
        #     doclocalP = Path(_dpathP0 / ".".join([_cnameS, "pdf"]))
        #     time.sleep(2)  # move pdf to doc fDer
        #     shutil.move(doclocalP, docpdfP)
        #     os.chdir(_dpathPcurP)
        #     print("INFO: pdf file moved to docs fDer", flush=True)
        #     print("INFO: program complete")

        #     cfgP = Path(_dpathP0 / "rv_cfg.txt")  # read pdf display program
        #     with open(cfgP) as f2:
        #         cfgL = f2.readlines()
        #         cfg1S = cfgL[0].split("|")
        #         cfg2S = cfg1S[1].strip()
        #     cmdS = cfg2S + " " + str(Path(_dpathP) / ".".join([dnameS, "pdf"]))
        #     # print(cmdS)
        #     subprocess.run(cmdS)

        #     os._exit(1)

        #     # clean temp files
        #     fileL = [
        #         Path(fileconfigP, ".".join([calcbaseS, "pdf"])),
        #         Path(fileconfigP, ".".join([calcbaseS, "html"])),
        #         Path(fileconfigP, ".".join([calcbaseS, "rst"])),
        #         Path(fileconfigP, ".".join([calcbaseS, "tex"])),
        #         Path(fileconfigP, ".".join([calcbaseS, ".aux"])),
        #         Path(fileconfigP, ".".join([calcbaseS, ".out"])),
        #         Path(fileconfigP, ".".join([calcbaseS, ".fls"])),
        #         Path(fileconfigP, ".".join([calcbaseS, ".fdb_latexmk"])),
        #     ]
        #     os.chdir(fileconfigP)
        #     tmpS = os.getcwd()
        #     if tmpS == str(fileconfigP):
        #         for f in fileL:
        #             try:
        #                 os.remove(f)
        #             except:
        #                 pass
        #         time.sleep(1)
        #         print("INFO: temporary Tex files deleted \n", flush=True)
        #    # endregion

        return (
            "tex pdf doc written: "
            + rvdocS
            + "\n"
            + "readme written: README.txt"
        )
