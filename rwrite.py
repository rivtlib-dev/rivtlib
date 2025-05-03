import logging
import os
import subprocess
import time
import warnings
from pathlib import Path

from fpdf import FPDF

from templates.pdfcover import content, cover, mainpage


class CmdW:
    """
    write docs

    Commands:
        | DOC | rel. pth |  type, cover
        | REPORT | rel. pth |  type, cover
        | APPEND | rel. pth |  title
    """

    def __init__(self, folderD, labelD):
        """commands that format to utf and reSt"""

        self.folderD = folderD
        self.labelD = labelD
        self.cover = cover
        self.content = content
        self.mainpage = mainpage
        errlogP = folderD["errlogP"]
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def frontvar(self, titleS, subS, botS, imageS):
        """_summary_

        Args:
            folderD (_type_): _description_
            labelD (_type_): _description_
            titleS (_type_): _description_
        """

        tcovS = self.cover(titleS, subS, botS, imageS)
        tcontS = self.content(titleS)
        tmainS = self.mainpage()

        return tcovS, tcontS, tmainS

    def frontpg(self, tocS, tcovS, tcontS, tmainS):
        """assemble front pages"""

        match tocS:
            case "none":
                tcovS = " "
                tcontS = " "
            case "toc":
                tcovS = " "
            case "cover":
                pass
            case _:
                tcovS = " "
                tcontS = " "

        return tcovS + tcontS + tmainS

    def doctext(self):
        pass

    def docpdf2(self, rst2P, styleS):
        """_summary_"""

        pthP = Path(self.folderD["pthS"])
        # pthP = os.path.join(pthP, '')
        # print(f"{pthP=}")
        cmd1S = "rst2pdf " + "temp/" + self.folderD["rstpN"]  # input
        cmd2S = " -o ../" + str(rst2P) + self.folderD["pdfN"]  # output
        cmd3S = " --config=../docs/_styles/rst2pdf.ini"  # config
        cmd4S = " --stylesheets=" + styleS.strip() + ".yaml"
        cmdS = cmd1S + cmd2S + cmd3S + cmd4S
        # print("cmdS=", cmdS)
        subprocess.run(cmdS, shell=True, check=True)

        insP = Path(self.folderD["docsP"], "pdf2", self.folderD["pdfN"])
        # print(str(insP.as_posix()))
        msgS = "file written: " + str(insP)

        return msgS

    def docpdf(self):
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

        """

        startS = str(labelD["pageI"])
        doctitleS = str(labelD["doctitleS"])

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
        texf = texf.replace("x*x*x", "[" + labelD["docnumS"] + "]")
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

        global rstcalcS, _rstflagB

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

        """convert reST to tex file

        0. insert [i] data into model (see _genxmodel())
        1. read the expanded model
        2. build the operations ordered dictionary
        3. execute the dictionary and write the md-8 calc and Python file
        4. if the pdf flag is set re-execute xmodel and write the PDF calc
        5. write variable summary to stdout

        :param pdffileS: _description_
        :type pdffileS: _type_
        """

        global folderD

        style_path = folderD["styleP"]
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

    def dochtml(self):
        pass

    def reportpdf2(self):
        """



        My Report Title
        ################


        My SubTitle
        ************

        |
        |
        |
        |


        .. image:: /ins01/rivt01.png
        :width: 30%
        :align: center

        |
        |
        |
        |
        |



        .. class:: center

        **date and time**


        .. raw:: pdf

        PageBreak coverPage


        .. contents::



        .. raw:: pdf

        PageBreak mainPage


        """
        pass

    def reporthtml(self):
        """ """
        pass

    def reportpdf(self, rL):
        """skip info command for md calcs

        Command is executed only for docs in order to
        separate protected information for shareable calcs.

        Args:
            rL (list): parameter list
        """

        """
        try:
            filen1 = os.path.join(self.rpath, "reportmerge.txt")
            print(filen1)
            file1 = open(filen1, 'r')
            mergelist = file1.readlines()
            file1.close()
            mergelist2 = mergelist[:]
        except OSError:
            print('< reportmerge.txt file not found in reprt folder >')
            return
        calnum1 = self.pdffile[0:5]
        file2 = open(filen1, 'w')
        newstr1 = 'c | ' + self.pdffile + ' | ' + self.calctitle
        for itm1 in mergelist:
            if calnum1 in itm1:
                indx1 = mergelist2.index(itm1)
                mergelist2[indx1] = newstr1
                for j1 in mergelist2:
                    file2.write(j1)
                file2.close()
                return
        mergelist2.append("\n" + newstr1)
        for j1 in mergelist2:
            file2.write(j1)
        file2.close()
        return """
        pass

        # from values

        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()
        # write dictionary from value-string
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                val1U = val2U = array(eval(valS))
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:  # no units
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            mdS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"
            mdS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            print("\n" + mdS + "\n")  # pretty print equation
            self.calcS += "\n" + mdS + "\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:  # substitute into equation
                self._vsub(vL)
            else:  # write equation table
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
            locals().update(self.rivtD)
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())

        # update dictionary
        if vL[1].strip() == "sub":
            self.setcmdD["subB"] = True
        self.setcmdD["trmrI"] = vL[2].split(",")[0].strip()
        self.setcmdD["trmtI"] = vL[2].split(",")[1].strip()

        # assign values
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        exec("set_printoptions(precision=" + rprecS + ")")
        exec("Unum.set_format(value_format = '%." + rprecS + "f')")
        if len(vL) <= 2:  # equation
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "DC" and vL[1].strip() != "":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS).cast_unit(eval(unit1S))
                    valdec = ("%." + str(rprecS) + "f") % valU.number()
                    val1U = str(valdec) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                exec(cmdS, globals(), locals())
                # valU = eval(varS).cast_unit(eval(unit1S))
                # valdec = ("%." + str(rprecS) + "f") % valU.number()
                # val1U = str(valdec) + " " + str(valU.unit())
                val1U = eval(varS)
                val1U = val1U.simplify_unit()
                val2U = val1U
            rstS = vL[0]
            spS = "Eq(" + varS + ",(" + valS + "))"  # pretty print
            symeq = sp.sympify(spS, _clash2, evaluate=False)
            eqltxS = sp.latex(symeq, mul_symbol="dot")
            self.restS += "\n.. math:: \n\n" + "  " + eqltxS + "\n\n"
            eqS = sp.sympify(valS)
            eqatom = eqS.atoms(sp.Symbol)
            if self.setcmdD["subB"]:
                self._vsub(vL)
            else:
                hdrL = []
                valL = []
                hdrL.append(varS)
                valL.append(str(val1U) + "  [" + str(val2U) + "]")
                for sym in eqatom:
                    hdrL.append(str(sym))
                    symU = eval(str(sym))
                    valL.append(str(symU.simplify_unit()))
                alignL = ["center"] * len(valL)
                self._vtable([valL], hdrL, "rst", alignL, fltfmtS)
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + "  # equation" + "\n"
                # print(pyS)
                self.exportS += pyS
        elif len(vL) >= 3:  # value
            descripS = vL[2].strip()
            varS = vL[0].split("=")[0].strip()
            valS = vL[0].split("=")[1].strip()
            val1U = val2U = array(eval(valS))
            if vL[1].strip() != "" and vL[1].strip() != "-":
                unitL = vL[1].split(",")
                unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            else:
                cmdS = varS + "= " + "unum.as_unum(" + valS + ")"
                # print(f"{cmdS=}")
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                # val1U = str(valU.number()) + " " + str(valU.unit())
                val2U = valU
            self.valL.append([varS, val1U, val2U, descripS])
            if self.setcmdD["saveB"] == True:
                pyS = vL[0] + vL[1] + vL[2] + "\n"
                # print(pyS)
                self.exportS += pyS
        self.rivtD.update(locals())
        # print(self.rivtD)

        # write values to table
        tbl = "x"
        hdrL = "y"
        tlbfmt = "z"
        alignL = "true"
        fltfmtS = "x"
        locals().update(self.rivtD)
        rprecS = str(self.setcmdD["trmrI"])  # trim numbers
        tprecS = str(self.setcmdD["trmtI"])
        fltfmtS = "." + rprecS.strip() + "f"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        tableS = tabulate(
            tbl,
            tablefmt=tblfmt,
            headers=hdrL,
            showindex=False,
            colalign=alignL,
            floatfmt=fltfmtS,
        )
        output.write(tableS)
        rstS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        inrstS = ""
        self.restS += ":: \n\n"
        for i in rstS.split("\n"):
            inrstS = "  " + i
            self.restS += inrstS + "\n"
        self.restS += "\n\n"
        self.rivtD.update(locals())
