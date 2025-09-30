import logging
import os
import subprocess
import time
import warnings
from pathlib import Path
from reportlab.lib.utils import ImageReader
from configparser import ConfigParser

import __main__

# from templates.pdfcover import content, cover, mainpage --


class Cmdd:
    """publish object

    commands:
        DOC - write doc
        APPEND - append pdf to doc

    syntax:
        |DOC| rel. path | doc type
        |ATTACH| rel. path | title

    """

    def __init__(self, foldD, lablD, sS, cmdL, drs2S):
        """Write object
        Args:
            foldD (dict): folders
            lablD (dict): labels
            sS (str): section text
        """
        # region
        self.foldD = foldD
        self.lablD = lablD
        self.sS = sS  # section string
        self.cmdL = cmdL  # commands
        self.pthS = ""
        self.parS = ""
        self.contentS = drs2S

        errlogP = Path(foldD["rivtP"], "temp", "rivt-log.txt")
        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
        self.logging = logging

        sL = sS.split("\n")  # unprocessed lines
        spL = []
        # strip leading spaces and comments from section
        for slS in sL[1:]:
            if len(slS) < 5:
                continue
            if "#" in slS:
                continue
            if len(slS.strip()) > 0:
                spL.append(slS[4:])

        self.spL = spL  # preprocessed list
        self.logging.info("SECTION : P")
        # endregion

    def cmdpx(self):
        """parse commands in P section
        Commands:
            |DOC| rel. style pth | type, init file
            |APPEND| rel. src pth | divider; nodivider

        Returns:
            msgS (str): completion message
        """
        # region
        typeS = ""
        msgS = ""

        for pS in self.spL:
            pL = pS[1:].split("|")
            if len(pL) > 0 and pL[0].strip() in self.cmdL:
                if pL[0].strip() == "DOC":
                    typeS = str(pL[1].strip())
                    self.parS = pL[2].strip()
                    dtypeS = typeS + ("x")
                    # print(dtypeS)
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                elif pL[0].strip() == "ATTACH":
                    typeS = "attach"
                    self.pthS = pL[1].strip()
                    self.parS = pL[2].strip()
                    dtypeS = typeS + ("x")
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                else:
                    pass
            else:
                pass

        return msgS
        # endregion

    def attachx(self):
        """_summary_"""
        # region

        msgS = "attachment"
        return msgS

        # endregion

    def textx(self):
        """write text doc file

        Returns:
            msgS (str): completion message
        """
        pass

    def rstpdfx(self):
        """write rstpdf doc file

        Returns:
            msgS (str): completion message
        """
        # region

        fileS = self.foldD["rstpN"]
        fileP = Path(self.foldD["projP"], "temp", fileS)
        with open(fileP, "w", errors="ignore") as f1:
            f1.write(self.contentS)
        self.yamlP = Path(self.foldD["projP"], "rivDocs/styles/rstpdf.yaml")
        self.iniP = Path(self.foldD["projP"], "rivDocs/styles/rivt.ini")

        cmd1S = "rst2pdf " + "../temp/" + self.foldD["rstpN"]  # input
        cmd2S = " -o ../rivDocs/rstpdf/" + self.foldD["pdfN"]  # output
        cmd3S = " --config=../styles/rstpdf.ini"  # config
        cmd4S = " --stylesheets=../styles/rstpdf.yaml"  # styles
        cmdS = cmd1S + cmd2S + cmd3S + cmd4S
        # print("cmdS=", cmdS)
        subprocess.run(cmdS, shell=True, check=True)
        outS = "/rivDocs/rstpdf/" + self.foldD["pdfN"]
        msgS = "doc written: " + outS
        return msgS
        # endregion

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
        # region
        startS = str(lablD["pageI"])
        doctitleS = str(lablD["doctitleS"])

        with open(tfileP, "r", encoding="md-8", errors="ignore") as f2:
            texf = f2.read()

        # modify "at" command
        texf = texf.replace(
            """\\begin{document}""",
            """\\renewcommand{\contentsname}{"""
            + doctitleS
            + "}\n"
            + """\\begin{document}\n"""
            + """\\makeatletter\n"""
            + """\\renewcommand\@dotsep{10000}"""
            + """\\makeatother\n""",
        )

        # add table of contents, figures and tables
        # texf = texf.replace("""\\begin{document}""",
        #                     """\\renewcommand{\contentsname}{""" + doctitleS
        #                     + "}\n" +
        #                     """\\begin{document}\n""" +
        #                     """\\makeatletter\n""" +
        #                     """\\renewcommand\@dotsep{10000}""" +
        #                     """\\makeatother\n""" +
        #                     """\\tableofcontents\n""" +
        #                     """\\listoftables\n""" +
        #                     """\\listoffigures\n""")

        texf = texf.replace("""inputenc""", """ """)
        texf = texf.replace("aaxbb ", """\\hfill""")
        texf = texf.replace("?x?", """\\""")
        texf = texf.replace(
            """fancyhead[L]{\leftmark}""",
            """fancyhead[L]{\\normalsize\\bfseries  """ + doctitleS + "}",
        )
        texf = texf.replace("x*x*x", "[" + lablD["docnumS"] + "]")
        texf = texf.replace("""\\begin{tabular}""", "%% ")
        texf = texf.replace("""\\end{tabular}""", "%% ")
        texf = texf.replace(
            """\\begin{document}""",
            """\\begin{document}\n\\setcounter{page}{""" + startS + "}\n",
        )

        with open(tfileP, "w", encoding="md-8") as f2:
            f2.write(texf)

            # with open(tfileP, 'w') as texout:
            #    print(texf, file=texout)

            pdfD = {
                "xpdfP": Path(tempP, docbaseS + ".pdf"),
                "xhtmlP": Path(tempP, docbaseS + ".html"),
                "xrstP": Path(tempP, docbaseS + ".rst"),
                "xtexP": Path(tempP, docbaseS + ".tex"),
                "xauxP": Path(tempP, docbaseS + ".aux"),
                "xoutP": Path(tempP, docbaseS + ".out"),
                "xflsP": Path(tempP, docbaseS + ".fls"),
                "xtexmakP": Path(tempP, docbaseS + ".fdb_latexmk"),
            }

        _mod_tex(texfileP)

        pdfS = _gen_pdf(texfileP)

        pdfD = {
            "cpdfP": Path(_dpathP0 / ".".join([_cnameS, "pdf"])),
            "chtml": Path(_dpathP0 / ".".join([_cnameS, "html"])),
            "trst": Path(_dpathP0 / ".".join([_cnameS, "rst"])),
            "ttex1": Path(_dpathP0 / ".".join([_cnameS, "tex"])),
            "auxfile": Path(_dpathP0 / ".".join([_cnameS, ".aux"])),
            "omdile": Path(_dpathP0 / ".".join([_cnameS, ".out"])),
            "texmak2": Path(_dpathP0 / ".".join([_cnameS, ".fls"])),
            "texmak3": Path(_dpathP0 / ".".join([_cnameS, ".fdb_latexmk"])),
        }
        if stylefileS == "default":
            stylefileS = "pdf_style.sty"
        else:
            stylefileS == stylefileS.strip()
        style_path = Path(_dpathP0 / stylefileS)
        print("INFO: style sheet " + str(style_path))
        pythoncallS = "python "
        if sys.platform == "linux":
            pythoncallS = "python3 "
        elif sys.platform == "darwin":
            pythoncallS = "python3 "

        rst2xeP = Path(rivtpath / "scripts" / "rst2xetex.py")
        texfileP = pdfD["ttex1"]
        tex1S = "".join(
            [
                pythoncallS,
                str(rst2xeP),
                " --embed-stylesheet ",
                " --documentclass=report ",
                " --documentoptions=12pt,notitle,letterpaper ",
                " --stylesheet=",
                str(style_path) + " ",
                str(_rstfileP) + " ",
                str(texfileP),
            ]
        )

        os.chdir(_dpathP0)
        os.system(tex1S)
        print("INFO: tex file written " + str(texfileP))

        # fix escape sequences
        fnumS = _setsectD["fnumS"]
        with open(texfileP, "r", encoding="md-8", errors="ignore") as texin:
            texf = texin.read()
        texf = texf.replace("?x?", """\\""")
        texf = texf.replace(
            """fancyhead[L]{\leftmark}""",
            """fancyhead[L]{\\normalsize  """ + calctitleS + "}",
        )
        texf = texf.replace("x*x*x", fnumS)
        texf = texf.replace("""\\begin{tabular}""", "%% ")
        texf = texf.replace("""\\end{tabular}""", "%% ")
        texf = texf.replace(
            """\\begin{document}""",
            """\\begin{document}\n\\setcounter{page}{""" + startpageS + "}\n",
        )

        # texf = texf.replace(
        #     """\\begin{document}""",
        #     """\\renewcommand{\contentsname}{"""
        #     + self.calctitle
        #     + "}\n"
        #     + """\\begin{document}"""
        #     + "\n"
        #     + """\\makeatletter"""
        #     + """\\renewcommand\@dotsep{10000}"""
        #     + """\\makeatother"""
        #     + """\\tableofcontents"""
        #     + """\\listoftables"""
        #     + """\\listoffigures"""
        # )

        time.sleep(1)
        with open(texfileP, "w", encoding="md-8") as texout:
            texout.write(texf)
        print("INFO: tex file updated")

        if doctypeS == "pdf":
            gen_pdf(texfileP)

        os._exit(1)

        # os.system('latex --version')
        os.chdir(tempP)
        texfS = str(pdfD["xtexP"])
        # pdf1 = 'latexmk -xelatex -quiet -f ' + texfS + " > latex-log.txt"
        pdf1 = "xelatex -interaction=batchmode " + texfS
        # print(f"{pdf1=}"")
        os.system(pdf1)
        srcS = ".".join([docbaseS, "pdf"])
        dstS = str(Path(reportP, srcS))
        shutil.copy(srcS, dstS)

        global foldD

        style_path = foldD["styleP"]
        # print(f"{style_path=}")
        # f2 = open(style_path)
        # f2.close

        pythoncallS = "python "
        if sys.platform == "linux":
            pythoncallS = "python3 "
        elif sys.platform == "darwin":
            pythoncallS = "python3 "

        rst2texP = Path(rivtP, "scripts", "rst2latex.py")
        # print(f"{str(rst2texP)=}")
        texfileP = Path(tempP, docbaseS + ".tex")
        rstfileP = Path(tempP, docbaseS + ".rst")

        with open(rstfileP, "w", encoding="md-8") as f2:
            f2.write(rstS)

        tex1S = "".join(
            [
                pythoncallS,
                str(rst2texP),
                " --embed-stylesheet ",
                " --documentclass=report ",
                " --documentoptions=12pt,notitle,letterpaper ",
                " --stylesheet=",
                str(style_path) + " ",
                str(rstfileP) + " ",
                str(texfileP),
            ]
        )
        logging.info(f"tex call:{tex1S=}")
        os.chdir(tempP)
        try:
            os.system(tex1S)
            time.sleep(1)
            logging.info(f"tex file written: {texfileP=}")
            print(f"tex file written: {texfileP=}")
        except SystemExit as e:
            logging.exception("tex file not written")
            logging.error(str(e))
            sys.exit("tex file write failed")

        """write pdf calc to reports folder and open

        Args:
            texfileP (path): doc config folder
        """

        global rstcalcS, _rstflagB

        os.chdir()
        time.sleep(1)  # cleanup tex files
        os.system("latexmk -c")
        time.sleep(1)

        pdfmkS = (
            "perl.exe c:/texlive/2020/texmf-dist/scripts/latexmk/latexmk.pl "
            + "-pdf -xelatex -quiet -f "
            + str(texfileP)
        )

        os.system(pdfmkS)
        print("\nINFO: pdf file written: " + ".".join([_cnameS, "pdf"]))

        dnameS = _cnameS.replace("c", "d", 1)
        docpdfP = Path(_dpathP / ".".join([dnameS, "pdf"]))
        doclocalP = Path(_dpathP0 / ".".join([_cnameS, "pdf"]))
        time.sleep(2)  # move pdf to doc folder
        shutil.move(doclocalP, docpdfP)
        os.chdir(_dpathPcurP)
        print("INFO: pdf file moved to docs folder", flush=True)
        print("INFO: program complete")

        cfgP = Path(_dpathP0 / "rv_cfg.txt")  # read pdf display program
        with open(cfgP) as f2:
            cfgL = f2.readlines()
            cfg1S = cfgL[0].split("|")
            cfg2S = cfg1S[1].strip()
        cmdS = cfg2S + " " + str(Path(_dpathP) / ".".join([dnameS, "pdf"]))
        # print(cmdS)
        subprocess.run(cmdS)

        os._exit(1)

        # clean temp files
        fileL = [
            Path(fileconfigP, ".".join([calcbaseS, "pdf"])),
            Path(fileconfigP, ".".join([calcbaseS, "html"])),
            Path(fileconfigP, ".".join([calcbaseS, "rst"])),
            Path(fileconfigP, ".".join([calcbaseS, "tex"])),
            Path(fileconfigP, ".".join([calcbaseS, ".aux"])),
            Path(fileconfigP, ".".join([calcbaseS, ".out"])),
            Path(fileconfigP, ".".join([calcbaseS, ".fls"])),
            Path(fileconfigP, ".".join([calcbaseS, ".fdb_latexmk"])),
        ]
        os.chdir(fileconfigP)
        tmpS = os.getcwd()
        if tmpS == str(fileconfigP):
            for f in fileL:
                try:
                    os.remove(f)
                except:
                    pass
            time.sleep(1)
            print("INFO: temporary Tex files deleted \n", flush=True)
            # endregion

    def htmlx(self):
        # region
        pass
        # end region
