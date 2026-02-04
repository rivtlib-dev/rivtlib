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
            foldD (dict): folders
            lablD (dict): labels
            rivD (dict): values
            rivL (list): values for export

        Vars:
            sS (str): rv.D API content substring
            uS (str): utf doc string
            r2S (str): rlabpdf doc string
            rS (str): reST doc string
    """

    def __init__(
        self,
        sS,
        foldD,
        lablD,
        cmdL,
        tagL,
        dutfS,
        drlabS,
        drstS,
        rivD,
    ):
        # region
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.rvlocalB = foldD["rvsingleB"]
        self.rivtP = foldD["rivtP"]
        errlogT = foldD["errlogT"]
        apilogT = foldD["apilogT"]
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
        with open(apilogT, "a") as f4:
            f4.write(self.sL[0] + "\n")
        self.logging.info("SECTION : " + self.sL[0])

        # endregion

    def cmdx(self):
        """parse commands and blocks in D API
        Commands:
            | PUBLISH | doc name; - | text; html; rlabpdf; texpdf
            | ATTACHPDF | rel. path | prepend;append

        Blocks:
            _[[METADATA]]
            _[[LAYOUT]]
            _[[END]]

        Returns:
            msgS (str): completion message
        """
        # region

        typeS = ""
        msgS = ""
        ptempS = ""
        blockB = False
        self.blockS = """"""
        self.docnameS = " "
        for pS in self.spL:
            pL = pS[1:].split("|")
            if len(pL) > 0 and pL[0].strip() in self.cmdL:
                if pL[0].strip() == "PUBLISH":
                    typeS = str(pL[2].strip())
                    self.docnameS = str(pL[1].strip()).strip()
                    if self.docnameS == "-":
                        self.docnameS = self.foldD["docnameS"]
                    self.stylefile = pL[1].strip()
                    dtypeS = typeS + ("x")
                    # print(dtypeS)
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
            if "_[[" in pS and ("_[[END]]" not in pS):  # block tags
                bsL = pS.split("]]")
                tagS = bsL[0].strip()
                if tagS in self.tagL:  # check list
                    # print(f"{tagS=}")
                    self.logging.info(f"block tag : {tagS}]]")
                    ptempS = tagS = bsL[0].strip()
                    textS = bsL[1].strip()
                    self.blockS = """"""
                    blockB = True
                    continue
            if blockB and ("_[[END]]" in pS):  # block accumulate
                if "LAYOUT" in ptempS:
                    ptempS = ""
                    obj = getattr(Cmdp, "layoutx")
                    msgS = obj(self)
                    self.blockS = """"""
                    continue
                elif "METADATA" in ptempS:
                    ptempS = ""
                    obj = getattr(Cmdp, "metadatax")
                    msgS = obj(self)
                    self.blockS = """"""
                    continue
            if blockB:
                self.blockS += pS + "\n"
                # print("vvvv", self.blockS)
            else:  # everything else
                pass

        return msgS
        # endregion

    def layoutx(self):
        """read layout block as config file

        Returns:
            msgS (str): completion message
        """

        self.configL = configparser.ConfigParser()
        self.configL.read_string(self.blockS)
        self.logopathS = self.configL["general"]["logopath"]
        self.footerS = self.configL["general"]["footer"]
        self.pagesizeS = self.configL["general"]["pagesize"]
        self.marginS = self.configL["general"]["margins"]
        self.headerS = self.configL["rlabpdf"]["header"]
        self.styleS = self.configL["rlabpdf"]["stylesheet"]
        self.coverS = self.configL["rlabpdf"]["cover"]

    def metadatax(self):
        print("metadata")

    def attachpdfx(self):
        """_summary_"""

        msgS = "attachment"
        return msgS

    def rlabpdfx(self):
        """write rst2pdf doc and readme file

        Returns:
            msgS (str): completion message
        """
        # region
        pypathS = os.path.dirname(sys.executable)
        rvstyleP = os.path.join(
            pypathS,
            "Lib",
            "site-packages",
            "rivtlib",
            "styles",
        )
        rvfileS = self.foldD["rbaseS"] + ".rst2"
        rvdocS = self.foldD["rbaseS"] + ".pdf"
        if self.rvlocalB:
            rvfileT = str(Path(self.foldD["rivtpub_P"], rvfileS))
            rvdocT = str(Path(self.foldD["rivtpub_P"], rvdocS))
            rvsrcP = Path(self.foldD["src_P"])
        else:
            rvfileT = str(Path(self.foldD["rivtpubP"], rvfileS))
            rvdocT = str(Path(self.foldD["rivtpubP"], rvdocS))
            rvsrcP = Path(self.foldD["srcP"])
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.docnameS
        authorS = self.rivD["metaD"]["authors"]
        verS = "  v" + self.rivD["metaD"]["version"]
        print("doc name:  ", doctitleS)

        footS = (
            "   |  "
            + " " * 30
            + timeS
            + "  |  "
            + authorS
            + "  |  "
            + doctitleS
            + verS
        )

        pageS = "   Page ###Page### of ###Total###"
        imglogoS = self.logopathS
        gsizeS = "\n      :width: 150px \n      :align: right\n\n"

        headfootS = (
            ".. header::\n\n"
            + pageS
            + "\n\n"
            + ".. footer:: \n\n"
            + "   .. image:: "
            + imglogoS
            + gsizeS
            + "\n\n"
        )

        pgtemp = ".. contents:: " + self.docnameS + "\n   :depth: 2 \n\n "
        # pgtemp = ".. raw:: pdf \n\n    PageBreak decoratedPage\n\n "
        self.drlabS = pgtemp + self.drlabS
        self.drlabS = self.drlabS + "\n" + headfootS

        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drlabS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        iniP = str(Path(rvstyleP, "layout.ini"))
        fontP = str(Path(rvstyleP, "fonts"))
        yamlS = "rlabpdf.yaml"
        cmd1S = "rst2pdf " + rvfileT  # input
        cmd2S = " -o " + rvdocT  # output
        cmd3S = " --config=" + iniP  # config
        cmd4S = " --font-path=" + fontP  # fonts
        cmd5S = " --stylesheet-path=" + rvstyleP  # style path
        cmd6S = " --stylesheets=" + yamlS  # styles
        rlabcmdS = cmd1S + cmd2S + cmd3S + cmd4S + cmd5S + cmd6S
        # print("rlabcmdS=", rlabcmdS)
        try:
            result = subprocess.run(rlabcmdS, shell=True, check=True)
            if not result.returncode:
                print("\nrst2pdf script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        except FileNotFoundError:
            print(f"Error: Script not found at {rvfileT}")

        return (
            "rlab pdf written: " + rvdocS + "\n" + "readme written: README.txt"
        )

    def htmlx(self):
        """write html doc and readme file

        Returns:
            msgS (str): completion message

        """
        pypathS = os.path.dirname(sys.executable)
        rvstyleP = os.path.join(
            pypathS, "Lib", "site-packages", "rivtlib", "styles"
        )

        rvfileS = self.foldD["rbaseS"] + ".rst"
        rvdocS = self.foldD["rbaseS"] + ".html"
        if self.rvlocalB:
            rvfileT = str(Path(self.foldD["rivtpub_P"], rvfileS))
            rvdocT = str(Path(self.foldD["rivtpub_P"], rvdocS))
        else:
            rvfileT = str(Path(self.foldD["rivtpubP"], rvfileS))
            rvdocT = str(Path(self.foldD["rivtpubP"], rvdocS))

        # add layout info
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        doctitleS = self.foldD["rbaseS"]
        authorS = self.rivD["metaD"]["authors"]
        verS = "  v" + self.rivD["metaD"]["version"]
        spaceS = "  |  "
        headS = timeS + spaceS + authorS + spaceS + doctitleS + verS
        headerS = f".. header::\n\n   {headS}"

        self.drstS = headerS + self.drstS + "\n"

        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        cmd4S = " --font-path="  # fonts
        cmd5S = " --stylesheet-path=" + os.path.join(rvstyleP, "singledoc.css")
        htmlS = "rst2html5" + cmd5S

        try:
            htmlcmdS = htmlS + " " + rvfileT + " " + rvdocT
            result = subprocess.run(htmlcmdS, shell=True, check=True)
            if not result.returncode:
                print("\nHTML script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        except FileNotFoundError:
            print(f"Error: Script not found at {rvfileT}")

        return (
            "html doc written: " + rvdocS + "\n" + "readme written: README.txt"
        )

    def textx(self):
        """write text doc and readme files

        Returns:
            msgS (str): completion message
        """
        rvdocS = self.foldD["rbaseS"] + ".txt"
        if self.rvlocalB:
            rvdocT = str(Path(self.foldD["rivtpub_P"], rvdocS))
        else:
            rvdocT = str(Path(self.foldD["rivtpubP"], rvdocS))

        verS = "  v" + self.rivD["metaD"]["version"]
        doctitleS = self.foldD["rbaseS"]
        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        authorS = self.rivD["metaD"]["authors"]
        borderS = "=" * 80
        hdlS = timeS + " | " + authorS + " | " + doctitleS + verS
        headS = "\n" + hdlS.rjust(80) + "\n" + borderS + "\n"
        self.dutfS = headS + "\n" + self.dutfS

        with open(rvdocT, "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        return (
            "text doc written: " + rvdocS + "\n" + "readme written: README.txt"
        )

    def texpdfx(self):
        """Modify TeX file to avoid problems with escapes:

        -  Replace marker "aaxbb " inserted by rivt with
            \\hfill because it is not handled by reST).
        - Delete inputenc package
        - Modify section title and add table of contents

         write calc rSt file to d00_docs folder

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
        rvfileS = self.foldD["rbaseS"] + ".rst"
        rvdocS = self.foldD["rbaseS"] + ".html"

        #  # region
        #     startS = str(lablD["pageI"])
        #     doctitleS = str(lablD["doctitleS"])

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
        #     texf = texf.replace("x*x*x", "[" + lablD["docnumS"] + "]")
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

        #     global foldD

        #     style_path = foldD["styleP"]
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

        #     """write pdf calc to reports folder and open

        #     Args:
        #         texfileP (path): doc config folder
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
        #     time.sleep(2)  # move pdf to doc folder
        #     shutil.move(doclocalP, docpdfP)
        #     os.chdir(_dpathPcurP)
        #     print("INFO: pdf file moved to docs folder", flush=True)
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
