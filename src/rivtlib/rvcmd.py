# python #!
import csv
import sys
import textwrap
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import sympy as sp
import tabulate
from fastcore.utils import store_attr
from IPython.display import display as _display
from PIL import Image
from sympy.abc import _clash2

import rivtlib.rvunits as rvunit
from rivtlib.rvunits import *  # noqa: F403
from rivtlib.unum.core import Unum

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """reads, writes and formats files

    Methods:

     API        Command                                                  RW     File Types
    ---------  ------------------------------------------------------- ----- ----------------------
    rv.R        | SHELL | relative path | *wait;nowait*                   R     *.sh*
    rv.V,I      | IMAGE | relative path |  scale, caption, num;nonum      R     *.png, .jpg*
    rv.V,I      | IMAGE2 | relative path | s1, s2, c1, c2, n1, n2         R     *.png, jpg*
    rv.V,I      | TABLE | relative path | width, l;c;r, title, num;nonum  R     *csv, txt, xlsx*
    rv.V,I      | TEXT | relative path |  *text;literal*; code            R     *txt, code*
    rv.V,T      | PYTHON | relative path | *rivt*; nmspace                R     *py*
    rv.T        | MARKUP | relative path | label                          R     *html*   *tex*
    rv.V        | VALTABLE | relative path | width, title, num;nonum      R     *csv, txt, xlsx*
    rv.V        a ==: 1*IN  | unit1, unit2, decimal | ref                 W     define value
    rv.V        b <=: a + 3*FT | unit1, unit2, decimal | ref              W     assign value
    rv.V        c :=: func1(x,y) | unit1, unit2, decimal | ref            W     function value
    rv.V        b < a | true text, false text, decimal | ref              W     compare value
    """

    def __init__(self, stS, fD, lD, rivD, rivL, parL):
        """command object

        Args:
            fD (dict): folders
            lD (dict): labels
            rivD (dict): values
            rivL (list): values for export
            parL ( list): parameter list

        Vars:
            uS (str): utf string
            rS (str): rst string
            tS (str): text string
        """
        # region
        store_attr()
        # unicode switch
        if stS == "V":
            sp.init_printing(use_unicode=False)
        else:
            sp.init_printing(use_unicode=True)

        self.fileS = parL[1].strip()
        self.parS = parL[2].strip()
        self.uS = ""
        self.r2s = ""
        self.rs = ""
        self.insP = Path(fD["rivtP"], "_src/", self.fileS)
        self.inspS = str(self.insP.as_posix())
        rvunitD = vars(rvunit)
        self.rivD = rivD | rvunitD
        # endregion

    def cmdx(self, cmdS):
        """call command

        Args:
            cmdS (str): command keyword

        Returns:
            uS, rS, tS, lS, fD, lD, rivD, rivL
        """
        method = getattr(self, cmdS)
        method()

        return self.mD

    def vdefine(self, deqS):
        """define value ==:

            a ==: .5 * 2*IN | unit1, unit2, decimal | ref

            collects successive rows until hitting a blank

        Returns:
            self.mD, tbL

        """
        # region
        tbL = []
        vaL = deqS.split("|")
        eqS = vaL[0].strip()
        eqS = eqS.replace(" ==: ", " = ")
        varS = eqS.split("=")[0].strip()
        unitL = vaL[1].split(",")
        unit1S, unit2S, dec1S = (
            unitL[0].strip(),
            unitL[1].strip(),
            unitL[2].strip(),
        )
        descripS = vaL[2].strip()
        exvS = ",".join((eqS, unit1S, unit2S, dec1S, descripS))
        self.rivL.append(exvS)
        try:
            exec(eqS, globals(), self.rivD)
        except ValueError as ve:
            print(f"A ValueError occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=False, unitless="")
        valU = eval(varS, {}, self.rivD)
        if type(valU) is Unum:
            val2S = str(valU.cast_unit(eval(unit2S)))
            val1U = valU.cast_unit(eval(unit1S))
            if val1U.number() == 1.0:
                val1S = str((1 + 10**-10) * val1U)
            else:
                val1S = str(valU.cast_unit(eval(unit1S)))
        else:
            val1S = str(valU)
            val2S = str(valU)
        self.rivD[varS] = valU  # rivt dictionary
        tbL = [varS, val1S, val2S, descripS]  # append row

        self.mD = {
            "uS": self.uS,
            "rS": self.rS,
            "tS": self.tS,
            "lS": self.lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivD": self.rivD,
            "rivL": self.rivL,
        }

        return self.mD, tbL

        # endregion

    def vassign(self, aeqS):
        """assign value <=:

            a <=: b + 2 | unit1, unit2, decimal | ref

        Returns:
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        lpL = aeqS.split("|")
        eqS = lpL[0]
        eqS = eqS.replace(" <=: ", " = ").strip()
        unit1S, unit2S, dec1S = lpL[1].split(",")
        unit1S, unit2S, dec1S = unit1S.strip(), unit2S.strip(), dec1S.strip()
        refS = lpL[2].strip()
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=True, unitless="")
        # print(dir(Unum.set_format))
        # wI = self.lD["widthI"]

        # symbolic equation eval
        spL = eqS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        if unit1S != "-":
            exec(eqS, globals(), self.rivD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivD)
        valU = eval(spL[0], globals(), self.rivD)
        self.rivD[spL[0]] = valU

        # result tables
        hdr1L = []
        tbl1L = []
        hdr1L.append(spL[0])
        hdr1L.append("[" + spL[0] + "]")
        hdr1L.append("reference")
        alignL = ["center", "center", "center"]
        tblfmt = "rst"
        tblL = [tbl1L]
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append(str(val1U))
        tbl1L.append(str(val2U))
        tbl1L.append(refS)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                headers=hdr1L,
                showindex=False,
                colalign=alignL,
            )
        )
        uS = output.getvalue()
        r2S = output.getvalue() + "\n"
        rS = output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()
        # values table
        tbl2L = []
        hdr2L = []
        alignL = []
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO)
        for vS in symaO:
            hdr2L.append(str(vS))
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivD)
            tbl2L.append(str(a1U))
        alignL = []
        tbl2L = [tbl2L]
        tblfmt = "rst"
        for nI in range(numvarI):
            alignL.append("center")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbl2L,
                tablefmt=tblfmt,
                headers=hdr2L,
                showindex=False,
                colalign=alignL,
            )
        )
        uS += "\n" + output.getvalue()
        rS += "\n" + output.getvalue()
        tS += "\n" + output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        # rivL append - for export
        ex2S = spL[0].strip() + " = " + str(val1U)
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivL.append(exvS)
        self.mD = {
            "uS": self.uS,
            "rS": self.rS,
            "tS": self.tS,
            "lS": self.lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivD": self.rivD,
            "rivL": self.rivL,
        }

        return self.mD

        # endregion

    def vfunc(self, feqS):
        """format function and assign value

            equation tag  <=:
            a :=: b + 2 | unit1, unit2, decimal | ref

        Returns:
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        lpL = feqS.split("|")
        eqS = lpL[0]
        eqS = eqS.replace(" :=: ", " = ").strip()
        unit1S, unit2S, dec1S = lpL[1].split(",")
        unit1S, unit2S, dec1S = unit1S.strip(), unit2S.strip(), dec1S.strip()
        refS = lpL[2].strip()
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=True, unitless="")
        # print(dir(Unum.set_format))
        # wI = self.lD["widthI"]

        # symbolic equation
        spL = eqS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        refS = refS.rjust(self.lD["widthI"])
        if unit1S != "-":
            exec(eqS, globals(), self.rivD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivD)

        # rivD append
        valU = eval(spL[0], globals(), self.rivD)
        self.rivD[spL[0]] = valU
        # result table
        hdr1L = []
        tbl1L = []
        hdr1L.append(spL[0])
        hdr1L.append("[" + spL[0] + "]")
        hdr1L.append("reference")
        alignL = ["center", "center"]
        tblfmt = "rst"
        tblL = [tbl1L]
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append(str(val1U))
        tbl1L.append(str(val2U))
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                headers=hdr1L,
                showindex=False,
                colalign=alignL,
            )
        )
        uS = output.getvalue()
        r2S = output.getvalue() + "\n"
        rS = output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()

        # rivL append
        ex2S = spL[0].strip() + " = " + str(val1U)
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivL.append(exvS)

        self.mD = {
            "uS": self.uS,
            "rS": self.rS,
            "tS": self.tS,
            "lS": self.lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivD": self.rivD,
            "rivL": self.rivL,
        }

        return self.mD

    # endregion

    def vcompare(self, compS, opS):
        """compare values

            comparison operators-a space around the operator is required
            < ,  > ,  != ,  == ,  <= ,  >=

            a < b  | unit, dec, true text, false text | ref

        Returns:
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        lpL = compS.split("|")
        eqS = lpL[0].strip()
        unitS, decS, trueS, falseS = lpL[1].split(",")
        unitS, decS, trueS, falseS = (
            unitS.strip(),
            decS.strip(),
            trueS.strip(),
            falseS.strip(),
        )
        refS = lpL[2].strip()
        decS = "%." + decS + "f"
        Unum.set_format(value_format=decS, auto_norm=True, unitless="")
        # symbolic equation
        spL = eqS.split(opS)
        spS = eqS
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        refS = refS.rjust(self.lD["widthI"])
        eqr2S = refS + "\n"
        eqrS = (
            ".. raw:: html\n\n" + '   <p align="right">' + refS + "</p> +\n\n"
        )
        # values table
        tblfmt = "rst"
        alignL = ["center", "center", "center"]
        hdrL = [spL[0], opS, spL[1]]
        valU = eval(spL[0], globals(), self.rivD)
        # print(self.rivD)
        val1U = valU.cast_unit(eval(unitS))
        valU = eval(spL[1], globals(), self.rivD)
        val2U = valU.cast_unit(eval(unitS))
        val1L = [val1U, opS, val2U]
        val2L = [val1U / val2U, "ratio", val2U / val1U]
        tblL = [val1L, val2L]
        # tabulate
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                headers=hdrL,
                showindex=False,
                colalign=alignL,
            )
        )
        stdS = "\n" + output.getvalue()
        uS = "\n" + output.getvalue()
        r2S = "\n" + output.getvalue() + "\n"
        rS = "\n" + output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()
        # compare
        resultB = eval(eqS, {}, self.rivD)
        chkS = ""
        if resultB:
            chkS = "\033[92m" + trueS + "\033[00m"
            chktxtS = trueS
            chkrS = ":compgreen:`" + trueS + "`"
        else:
            chkS = "\033[91m" + falseS + "\033[00m"
            chktxtS = falseS
            chkrS = ":compred:`" + falseS + "`"
        stdS += "\n" + chkS.rjust(self.lD["widthI"]) + "\n"
        uS += "\n" + chktxtS.rjust(self.lD["widthI"]) + "\n"
        r2S += "\n.. role:: compred\n\n.. role:: compgreen\n\n"
        r2S += "\n.. class:: align-right\n\n   " + chkrS + "\n"
        rS += (
            "\n"
            + ".. raw:: html\n\n"
            + '   <p align="right">'
            + chkS
            + "</p> \n\n"
        )

        self.mD = {
            "uS": self.uS,
            "rS": self.rS,
            "tS": self.tS,
            "lS": self.lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivD": self.rivD,
            "rivL": self.rivL,
        }

        return self.mD, stdS

        # endregion

    def IMAGE(self):
        """insert image

        | IMAGE | rel. path file | caption, scale, num;nonum
        """
        # region
        parL = self.parS.split(",")
        capS = parL[0].strip()
        scS = parL[1].strip()
        figS = parL[2].strip()
        if figS == "num":
            numS = str(self.lD["tableI"])
            self.lD["tableI"] = int(numS) + 1
            lablS = "<b>Table " + numS + "</b> "
        else:
            lablS = ""
        if capS == "-":
            capS = ""
        lablS = lablS + capS + " "
        try:
            img1 = Image.open(self.inspS)
            _display(img1)
            self.uS = lablS
        except Exception:
            self.uS = lablS

        self.uS = "\n" + self.uS + " [file: " + self.fileS + " ] \n"
        self.tS = "\n Image: " + self.uS + "\n"
        self.rS = (
            "\n\n.. image:: "
            + self.inspS
            + "\n"
            + "   :width: "
            + scS
            + "%"
            + "\n"
            + "   :align: center"
            + "\n\n\n"
            + ".. raw:: html \n\n"
            + "   "
            + '<p align="center">'
            + lablS
            + "\n"
        )
        self.lS = (
            "\n\n.. image:: "
            + self.inspS
            + "\n"
            + "   :width: "
            + scS
            + "%"
            + "\n"
            + "   :align: center"
            + "\n\n\n"
            + ".. raw:: html \n\n"
            + "   "
            + '<p align="center">'
            + lablS
            + "\n"
        )

        # endregion

    def IMAGE2(self):
        """insert side by side images

        |IMG2| rel. pth, rel. pth | sf1, sf2, c1, c2 (_[F])
        """
        # region
        # print(f"{parS=}")
        parL = self.parS.split(",")
        fileL = self.pthS.split(",")
        file1P = Path(fileL[0])
        file2P = Path(fileL[1])
        cap1S = parL[0].strip()
        cap2S = parL[1].strip()
        scale1S = parL[2].strip()
        scale2S = parL[3].strip()
        figS = "Fig. "
        if parL[2] == "_[F]":
            numS = str(self.lD["fnum"])
            self.lD["fnum"] = int(numS) + 1
            figS = figS + numS + cap1S

        self.uS = "<" + cap1S + " : " + str(file1P) + "> \n"
        self.r2s = (
            "\n.. image:: "
            + self.pthS
            + "\n"
            + "   :scale: "
            + scale1S
            + "%"
            + "\n"
            + "   :align: center"
            + "\n\n"
        )
        # endregion

    def TABLE(self):
        """insert table

        | TABLE | rel. path | col width, l;c;r, title (_[T])
        """
        # region
        # print(f"{pthS=}")

        lineS = self.strpS
        tnumI = int(self.lD["tableI"])
        self.lD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.tabuS = "\nTable " + str(tnumI) + ": " + lineS
        self.tabr2s = "\n<b>Table " + fillS + "</b>: " + lineS
        self.tabrs = "\n**Table " + fillS + "**: " + lineS

        parL = self.parS.split(",")
        titleS = " "
        parL = self.parS.split(",")
        capS = parL[0].strip()
        scS = parL[1].strip()
        tabS = parL[2].strip()
        if tabS == "num":
            numS = str(self.lD["figI"])
            self.lD["fnum"] = int(numS) + 1
            lablS = "<b>Fig. " + numS + "</b> "
        else:
            lablS = ""
        if capS == "-":
            capS = ""
        lablS = lablS + capS + " "

        self.strpS = titleS.strip()
        self.cT()
        fiS = " [file: " + self.fileS + "]" + "\n\n"
        utlS = titleS + fiS  # file path text
        rtlS = xtlS = titleS + fiS
        extS = self.insP.suffix  # file extension
        maxwI = int(parL[0].strip())  # max col. width
        alnS = parL[1].strip()  # col. alignment
        rowL = eval(parL[3].strip())  # rows
        if len(rowL) == 0:
            pass
        alignD = {
            "s": "",
            "d": "decimal",
            "c": "center",
            "r": "right",
            "l": "left",
        }
        readL = []
        if extS == "csv":  # read csv file
            with open(self.inspS, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # print(f"{row=}")
                    if row and row[0].startswith("#"):
                        continue
                    else:
                        readL.append(row)
        elif extS == "xlsx":  # read xls file
            pDF1 = pd.read_excel(self.pthS, header=None)
            readL = pDF1.values.tolist()
        else:
            pass
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        alignS = alignD[alnS]
        output.write(
            tabulate.tabulate(
                readL,
                tablefmt="rst",
                headers="firstrow",
                numalign="decimal",
                maxcolwidths=maxwI,
                stralign=alignS,
            )
        )
        uS = rS = output.getvalue()
        sys.stdout = old_stdout

        self.uS = utlS + uS + "\n"
        self.r2s = rtlS + rS + "\n"
        self.rs = xtlS + rS + "\n"
        # endregion

    def TEXT(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        insP = Path(self.fD["srcP"], self.pthS)
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.r2s = fileS
        self.rs = fileS
        # endregion

    def VALTABLE(self):
        """read file and insert values

        | VALTABLE | relative path | title, rows
        """
        # region
        parL = self.parS.split(",")
        titleS = parL[0].strip()
        fiS = " [file: " + self.fileS + "]" + "\n\n"
        tnumI = int(self.lD["tableI"])
        self.lD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        if titleS[0:1] == "--":
            titleS = fiS
            utlS = "\n" + fiS
            rtlS = "\n" + fiS
            xtlS = "\n" + fiS
        else:
            titleS = titleS + fiS
            utlS = "\nTable " + fillS + ": " + titleS
            rtlS = "\n**Table " + fillS + "**: " + titleS
            xtlS = "\n**Table " + fillS + "**: " + titleS
        sliceS = parL[1].strip()
        with open(self.insP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        # extract rows
        sliceS = parL[1].strip()
        sliceL = sliceS.split(":")
        if sliceL[1].strip() == "0":
            sliceO = slice(int(sliceL[0]), len(readL))
        else:
            sliceO = slice(int(sliceL[0]), int(sliceL[1]))
        readL = readL[sliceO]
        # print(f"{readL=}")
        tbL = []
        for vaL in readL:
            # print(f"{vaL=}")
            if len(vaL) != 5:
                continue
            eqS = vaL[0].strip()
            varS = vaL[0].split("=")[0].strip()
            valS = vaL[0].split("=")[1].strip()
            unit1S, unit2S = vaL[1], vaL[2]
            dec1S, descripS = vaL[3].strip(), vaL[4].strip()
            decS = "%." + dec1S + "f"
            Unum.set_format(value_format=decS, auto_norm=True, unitless="")
            # print(dir(Unum.set_format))
            # wI = self.lD["widthI"]
            if unit1S != "-":
                if isinstance(eval(valS), list):
                    val1U = np.array(eval(valS)) * eval(unit1S)
                    val2U = [varS.cast_unit(eval(unit2S)) for varS in val1U]
                else:
                    eqS = varS + " = " + valS
                    try:
                        exec(eqS, globals(), self.rivD)
                    except ValueError as ve:
                        print(f"A ValueError occurred: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    valU = eval(varS, globals(), self.rivD)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                eqS = varS + " = " + valS
                exec(eqS, globals(), self.rivD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])
        # print("tbl", tbL)
        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colalign=alignL,
            )
        )
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        self.uS = utlS + outS + "\n"
        self.r2s = rtlS + outS + "\n"
        self.rs = xtlS + outS + "\n"
        # endregion

    def PYTHON(self):
        """execute Python script

        | PYTHON | rel. path | namespace, docstrings
        """
        # region
        # print(f"{readL=}")
        namespaceS = "rivtO"

        fileP = Path(self.fD["rivtP"], self.fileS)
        with open(fileP, "r") as f10:
            pyscriptS = f10.read()
        if namespaceS == "rivtO":
            exec(pyscriptS, globals(), self.rivD)
        else:
            exec(pyscriptS, globals(), namespaceS)

        fiS = "**[ Python file read:** " + self.fileS + " **]**" + "\n\n"
        fiuS = "[ Python file read: " + self.fileS + " ]" + "\n\n"
        self.uS = fiuS + "\n"
        self.r2s = fiS + "\n"
        self.rs = fiS + "\n"

        # endregion

    def LATEX(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")

    def WIN(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.fD["reptfDP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.r2s = fileS
        self.rs = fileS
        # endregion

    def OSX(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.fD["reptfDP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.r2s = fileS
        self.rs = fileS
        # endregion

    def LINUX(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.fD["reptfDP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.r2s = fileS
        self.rs = fileS
        # endregion
