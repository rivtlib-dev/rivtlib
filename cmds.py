# python #!
import fnmatch
import csv
import logging
import re
import sys
import warnings
from datetime import datetime, time
from io import StringIO
from pathlib import Path

import IPython
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
import tabulate
from PIL import Image
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import tags
from rivtlib.unit import *

tabulate.PRESERVE_WHITESPACE = True


# value table
hdraL = ["variable", "value", "[value]", "description"]
alignaL = ["left", "right", "right", "left"]
hdreL = ["variable", "value", "[value]", "description [eq. number]"]
aligneL = ["left", "right", "right", "left"]


class CmdV:
    """values commands that format to utf8 or reSt

        a = 1+1 | unit | reference (_[E])                = is command tag
        || EVAL | default |  dec1                       .csv
        || VALS | rel. pth |  dec1                      .csv
        || VCFG | rel. pth | rel. pth | dec1, dec2      .csv

    """

    blckevalL = []      # current value table
    eqL = []            # equation result table
    vtableL = []        # value table for export

    def __init__(self, labelD, folderD,  rivtD):
        """commands that format a utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.rivtD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        self.errlogP = folderD["errlogP"]

        baseS = self.labelD["baseS"]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + baseS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def vals(self):
        """declare variable values

        """
        locals().update(self.localD)
        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descripS = str(self.labelD["descS"])
        if unit1S.strip() != "-":
            cmdS = varS + "= " + valS + "*" + unit1S
        else:
            cmdS = varS + "= as_unum(" + valS + ")"

        exec(cmdS, globals(), locals())
        self.localD.update(locals())
        return [varS, valS, unit1S, unit2S, descripS]

    def evalmds(self):
        """assign value to equation

        :return: _description_
        :rtype: _type_
        """
        locals().update(self.localD)
        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descS = str(self.labelD["eqlabelS"])
        precI = int(self.labelD["descS"])  # trim result
        fmtS = "%." + str(precI) + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())

                val1U = eval(varS).cast_unit(eval(unit1S))
                val1U.set_format(value_format=fmtS, auto_norm=True)
                val2U = val1U.cast_unit(eval(unit2S))
                # print(f"{val1U=}")
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)

        spS = "Eq(" + varS + ",(" + valS + "))"
        mdS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        mdS = "\n" + mdS + "\n"
        eqL = [varS, valS, unit1S, unit2S, descS]

        print(mdS)                      # print equation

        subS = " "
        if self.labelD["subB"]:
            subS = self.vsub(eqL, precI, varS, val1U)
            print(subS)                  # print with substition

        self.localD.update(locals())
        return [eqL, mdS + "\n" + subS + "\n\n"]

    def eval(self):
        """import values from files

        """

        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        plenI = 2                       # number of parameters
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        valL = []
        fltfmtS = ""
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vL = len(vaL)
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["_ _", "_ _", "_ _", "Total"])  # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])

        rstS = self.vtable(valL, hdrL, "rst", alignL)

        # print(mdS + "\n")
        return rstS

    def eval2(self):
        """import data from files


            :return lineS: md table
            :rtype: str
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["cpath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self.vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

        return

    def evalrst(self):
        """ = assign result to equation

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string
        :rtype: string
        """
        locals().update(self.localD)
        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descS = str(self.labelD["eqlabelS"])
        precI = int(self.labelD["descS"])  # trim result
        fmtS = "%." + str(precI) + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())

                val1U = eval(varS).cast_unit(eval(unit1S))
                val1U.set_format(value_format=fmtS, auto_norm=True)
                val2U = val1U.cast_unit(eval(unit2S))
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)
        spS = "Eq(" + varS + ",(" + valS + "))"
        # symeq = sp.sympify(spS, _clash2, evaluate=False)
        # eqltxS = sp.latex(symeq, mul_symbol="dot")
        eqS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        indeqS = eqS.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"
        eqL = [varS, valS, unit1S, unit2S, descS]
        self.localD.update(locals())

        subS = "\n\n"
        if self.labelD["subB"]:              # replace variables with numbers
            subS = self.vsub(eqL, precI, varS, val1U) + "\n\n"

        assignL = [varS, str(val1U), unit1S, unit2S, descS]
        return [assignL, rstS + subS]

    def vsub(self, eqL, precI, varS, val1U):
        """substitute variables with values

        :param eqL: _description_
        :type eqL: _type_
        :param precI: _description_
        :type precI: _type_
        :param varS: _description_
        :type varS: _type_
        :param val1U: _description_
        :type val1U: _type_
        :return: _description_
        :rtype: _type_
        """

        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        # print(f"{symeq=}")
        symat = symeq.atoms(sp.Symbol)
        # print(f"{symat=}")
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            # print(f"{n1O=}")
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            # print(f"{n1U=}")
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            # print(f"{new_var=}")
            with sp.evaluate(False):
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
            # print(f"{symeq=}")
        out2 = sp.pretty(symeq, wrap_line=False)
        # print('out2a\n', out2)
        # symat1 = symeq.atoms(sp.Symbol)  # adjust character length
        # for n2 in symat1:
        #     orig_var = str(n2).replace("~", "")
        #     orig_var = orig_var.replace("|", "_")
        #     expr = eval(varL[1])
        #     if type(expr) == float:
        #         form = "{%." + str(precI) + "f}"
        #         symeval1 = form.format(eval(str(expr)))
        #     else:
        #         try:
        #             symeval1 = eval(
        #                 orig_var.__str__()).__str__()
        #         except:
        #             symeval1 = eval(orig_var.__str__()).__str__()
        #     out2 = out2.replace(n2.__str__(), symeval1)   # substitute
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        self.localD.update(locals())
        mdS = out3 + "\n\n"

        return mdS

    def vsub2(self, eqL, precI, varS, val1U):
        """substitute numbers for variables in printed output

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string
        :rtype: string
        """
        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        symat = symeq.atoms(sp.Symbol)
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            with sp.evaluate(False):                # sub values
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
        out2 = sp.pretty(symeq, wrap_line=False)
        # symat1 = symeq.atoms(sp.Symbol)
        # for n2 in symat1:
        #     orig_var = str(n2).replace("~", "")
        #     orig_var = orig_var.replace("|", "_")
        #     expr = eval(varL[1])
        #     if type(expr) == float:
        #         form = "{%." + str(precI) + "f}"
        #         symeval1 = form.format(eval(str(expr)))
        #     else:
        #         try:
        #             symeval1 = eval(
        #                 orig_var.__str__()).__str__()
        #         except:
        #             symeval1 = eval(orig_var.__str__()).__str__()
        #     out2 = out2.replace(n2.__str__(), symeval1)   # substitute
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        self.localD.update(locals())
        indeqS = out3.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"

        return rstS

    def vtable(self, tbL, hdrL, tblfmt, alignL):
        """write value table"""

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbL, headers=hdrL, tablefmt=tblfmt,
                showindex=False, colalign=alignL
            )
        )
        mdS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return mdS

        # self.calcS += mdS + "\n"
        # self.rivtD.update(locals())

    def atable2(self, tblL, hdreL, tblfmt, alignaL):
        """write assign table"""

        locals().update(self.rivtD)

        valL = []
        for vaL in tblL:
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            valL.append([varS, val1U, val2U, descripS])

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdreL,
                showindex=False,  colalign=alignaL))
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        # valP = Path(folderD["valsP"], folderD["valfileS"])
        # with open(valP, "w", newline="") as f:
        #     writecsv = csv.writer(f)
        #     writecsv.writerow(hdraL)
        #     writecsv.writerows(vtableL)

        self.localD.update(locals())
        print("\n" + mdS+"\n")
        return mdS

    def etable2(self, tblL, hdrvL, tblfmt, aligneL):
        """write eval table"""

        locals().update(self.rivtD)

        valL = []
        for vaL in tblL:
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + " * " + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            valL.append([varS, val1U, val2U, descripS])

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdrvL,
                showindex=False,  colalign=alignvL))
        utfS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.rivtD.update(locals())

        print("\n" + mdS+"\n")
        return utfS


class CmdW:
    """
        write commands

        || WRITE | rel. pth |  dec1                      .csv
        || REPORT | rel. pth | rel. pth | dec1, dec2     .csv

    """
    pass


class Cmd:
    """
        insert commands that format to utf8 or reSt

        || APPEND | rel. pth | num; nonum                      .pdf
        || TEXT | rel. pth |  plain; rivt                      .txt
        || TABLE | rel. pth | col width, l;c;r                 .csv, .txt, .xls
        || IMG  | rel. pth | caption, scale, (**[_F]**)        .png, .jpg
        || IMG2  | rel. pth | c1, c2, s1, s2, (**[_F]**)       .png, .jpg

    """

    def __init__(self,  folderD, labelD):
        """commands that format to utf and reSt

        """
        self.folderD = folderD
        self.labelD = labelD
        # print(folderD)
        errlogP = folderD["errlogP"]
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def cmd_parse(self, cmdS, pthS, parS):
        """parse a tagged line

        Args:
            cmdS (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        cC = globals()['Cmd'](self.folderD, self.labelD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(f"{cmdS=}")
        # print(f"{pthS=}")
        # print(f"{parS=}")

        return uS, rS

    def deflabel(self, labelS, numS):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        self.labelD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

    def append(self):
        """_summary_
        """
        pass

    def img(self, pthS, parS):
        """ insert image from file

        Args:
            pthS (str): relative file path
            parS (str): parameters

        Returns:
            uS (str): formatted utf string
            rS (str): formatted reSt string
        """
        # print(f"{parS=}")
        parL = parS.split(",")
        fileP = Path(pthS)
        capS = parL[0]
        scS = parL[1].strip()
        scF = float(scS)
        figS = ""
        if len(parL) == 3:
            if parL[2] == "_[F]":
                numS = self.labelD["fnum"]
                figS = self.deflabel(capS, numS)
        try:
            img1 = Image.open(pthS)
            img1 = img1.resize((int(img1.size[0]*scF), int(img1.size[1]*scF)))
            _display(img1)
        except:
            pass
        uS = "< " + capS + " : " + str(fileP) + " > \n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :scale: "
              + scS + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )
        print(uS)
        return uS, rS

    def img2(self, pthS, parS):
        """ insert side by side images from files

        Args:
            pthS (str): relative file path
            parS (str): parameters

        Returns:
            uS (str): formatted utf string
            rS (str): formatted reSt string
        """
        # print(f"{parS=}")
        parL = parS.split(",")
        fileL = pthS.split(",")
        file1P = Path(fileL[0])
        file2P = Path(fileL[1])
        cap1S = parL[0].strip()
        cap2S = parL[1].strip()
        scale1S = parL[2].strip()
        scale2S = parL[3].strip()
        figS = ""
        if len(parL) == 5:
            if parL[2] == "_[F]":
                numS = self.labelD["fnum"]
                figS = self.deflabel(capS, numS)
        try:
            img1 = Image.open(pthS)
            _display(img1)
        except:
            pass
        uS = "<" + capS + " : " + str(fileP) + "> \n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :scale: "
              + scale1S + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )
        print(uS)
        return uS, rS


    # def combine_images_side_by_side(image_path1, image_path2, output_path):
    #     """Combines two images horizontally side by side.

    # Args:
    #     image_path1: Path to the first image.
    #     image_path2: Path to the second image.
    #     output_path: Path to save the combined image.
    # """
    # try:
    #     img1 = Image.open(image_path1)
    #     img2 = Image.open(image_path2)

    #     new_width = img1.width + img2.width
    #     new_height = max(img1.height, img2.height)

    #     new_img = Image.new('RGB', (new_width, new_height), 'white')

    #     new_img.paste(img1, (0, 0))
    #     new_img.paste(img2, (img1.width, 0))

    #     new_img.save(output_path)
    #     print(f"Combined image saved to: {output_path}")

    # except FileNotFoundError:
    #     print("Error: One or both image files not found.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # if __name__ == '__main__':
    #     combine_images_side_by_side('image1.jpg', 'image2.jpg', 'combined_image.jpg')


    def table(self, pthS, parS):
        """insert table from csv, xlsx or reSt file

        """

        uS = rS = """"""
        alignD = {"s": "", "d": "decimal", "c": "center", "r": "right", "l": "left"}
        pthS = pthS.split(":")                            # strip rows
        pthP = Path(pthS[0])
        parL = parS.split(",")
        maxwI = int(parL[0])
        keyS = parL[1].strip()
        alignS = alignD[keyS]
        extS = pthP.suffix[1:]
        readL = []
        #print(f"{extS=}")
        if extS == "csv":                                  # read csv file
            with open(pthP, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    #print(f"{row=}")
                    if row and row[0].startswith('#'):
                        #print(f"{row=}")
                        continue
                    else:
                        readL.append(row)
        elif extS == "xlsx":                               # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(f"{self.cmdS} not evaluated: {extS} file not processed")
            return

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate.tabulate(
            readL,
            tablefmt="rst",
            headers="firstrow",
            numalign="decimal",
            maxcolwidths=maxwI,
            stralign=alignS))

        uS = rS = output.getvalue()
        sys.stdout = old_stdout

        print(uS)
        return uS, rS

    def text(self):
        """insert text from file

        || text | folder | file | type

        :param lineS: string block

        """
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated:  \
                                    {plenI} parameters required")
            return
            if self.paramL[0] == "data":
                folderP = Path(self.folderD["dataP"])
            else:
                folderP = Path(self.folderD["dataP"])
                fileP = Path(self.paramL[1].strip())
                pathP = Path(folderP / fileP)
                txttypeS = self.paramL[2].strip()
                extS = pathP.suffix
                with open(pathP, "r", encoding="md-8") as f1:
                    txtfileS = f1.read()
                with open(pathP, "r", encoding="md-8") as f2:
                    txtfileL = f2.readlines()
                j = ""
            if extS == ".txt":
                # print(f"{txttypeS=}")
                if txttypeS == "plain":
                    print(txtfileS)
                    return txtfileS
                elif txttypeS == "code":
                    pass
                elif txttypeS == "rivttags":
                    xtagC = parse.RivtParseTag(
                        self.folderD, self.labelD,  self.localD)
                    xmdS, self.labelD, self.folderD, self.localD = xtagC.md_parse(
                        txtfileL)
                    return xmdS
                elif extS == ".html":
                    mdS = self.txthtml(txtfileL)
                    print(mdS)
                    return mdS
            elif extS == ".tex":
                soupS = self.txttex(txtfileS, txttypeS)
                print(soupS)
                return soupS
            elif extS == ".py":
                pass
