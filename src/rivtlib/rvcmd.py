# python #!
import csv
import re
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

from rivtlib.rvunits import *  # noqa: F403
from rivtlib.unum.core import Unum

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """reads, writes and formats files

    Methods:

     API        Command                                                  File Types
    ---------  ------------------------------------------------------- ---------------------
    rv.R        | SHELL | relative path | os, *wait;nowait*               *.sh*
    rv.V,I      | IMAGE | relative path |  scale, caption, num;non        *.png, .jpg*
    rv.V,I      | IMAGE2 | relative path | s1, s2, c1, c2, n1, n2         *.png, jpg*
    rv.V,I      | TABLE | relative path | width, l;c;r, title, num;non    *csv, txt, xlsx*
    rv.V        | PYTHON | relative path | *rivt*; nmspace                *py*
    rv.V        | VALTABLE | relative path | width, title, num;non        *csv, txt, xlsx*
    rv.V        a ==: 1*IN  | unit1, unit2, decimal | ref                 define value
    rv.V        b <=: a + 3*FT | unit1, unit2, decimal | ref              assign value
    rv.V        c :=: func1(x,y) | unit1, unit2, decimal | ref            function value
    rv.V        b < a | unit, decimal, true text, false text | ref        compare value
    rv.T        | MARKUP | relative path | type
    rv.D        | ATTACHPDF
    rv.D        | PUBLISH
    """

    def __init__(self, stS, fD, lD, rivtD, rivL, parL):
        """command object

        Args:
            fD (dict): folders
            lD (dict): labels
            rivtD (dict): values
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
        self.file2L = parL[1].split(",")
        self.parS = parL[2].strip()
        self.insP = Path(fD["rivtP"], self.fileS)
        self.inspS = str(self.insP.as_posix())
        self.uS = ""
        self.rS = ""
        self.tS = ""
        self.lS = ""
        self.lD = lD
        self.rivL = rivL
        self.rivtD = rivtD
        self.wI = self.lD["widthI"]
        # endregion

    def cmdx(self, cmdS):
        """call command

        Args:
            cmdS (str): command keyword

        Returns:
            uS, rS, tS, lS, fD, lD, rivtD, rivL
        """
        method = getattr(self, cmdS)
        method()

        return self.mD

    def vdefine(self, deqS):
        """define value ==:

            a ==: .5 * 2*IN | unit1, unit2, decimal | ref

            collects successive rows until hitting a blank;
            table is written in rvparse module

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
        # rivt store
        descripS = vaL[2].strip()
        exvS = ",".join((eqS, unit1S, unit2S, dec1S, descripS))
        self.rivL.append(exvS)
        try:
            exec(eqS, globals(), self.rivtD)
        except ValueError as ve:
            print(f"A ValueError occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=False, unitless="")
        valU = eval(varS, {}, self.rivtD)
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
        self.rivtD[varS] = valU  # rivt dictionary
        tbL = [varS, val1S, val2S, descripS]  # append row

        return tbL, self.rivtD, self.rivL

        # endregion

    def vassign(self, aeqS):
        """assign value <=:

            a <=: b + 2 | unit1, unit2, decimal | ref

        Returns:
            uS, rS, tS, fD, lD, rivtD, rivL
        """

        # region
        self.enumI = int(self.lD["equI"])
        self.enumI += 1
        self.lD["equI"] = self.enumI
        self.enumS = str(self.enumI)

        lpL = aeqS.split("|")
        eqS = lpL[0]
        eqS = eqS.replace(" <=: ", " = ").strip()
        unit1S, unit2S, dec1S = lpL[1].split(",")
        unit1S, unit2S, dec1S = unit1S.strip(), unit2S.strip(), dec1S.strip()
        refS = lpL[2].strip()
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=True, unitless="")
        # print(dir(Unum.set_format))
        spL = eqS.split("=")  # ============== symbolic equation
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # text
        eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
        toptS = chr(9484) + "  Eq-" + self.enumS + " | " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
        # rest
        eq1S = textwrap.indent(eq1S, "           ")
        erS = "\n**Eq. " + self.enumS + ":**  " + refS + "\n"
        eqrS = "\n|\n" + erS + "\n.. code-block:: text \n\n" + eq1S + "\n\n"
        if unit1S != "-":  # =================== rivtD
            exec(eqS, globals(), self.rivtD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivtD)
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        tbl1L = []  # =================== result tables
        alignL = ["center", "center", "center"]
        tblfmt = "rst"
        tblL = [tbl1L]
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append("**" + spL[0] + " = " + str(val1U) + "**")
        tbl1L.append("[" + spL[0] + "]" + " = " + str(val2U))
        tbl1L.append("**" + refS.strip() + "**")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                showindex=False,
                colalign=alignL,
            )
        )
        uS = eqtS + "\n" + output.getvalue() + "\n"
        tS = eqtS + "\n" + output.getvalue() + "\n"
        rS = eqrS + "\n" + output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()
        tbl2L = []  # ============ values table
        hdr2L = []
        alignL = []
        print("spL", spL)
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO)
        for vS in symaO:
            hdr2L.append(str(vS))
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivtD)
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
        lS = ""
        sys.stdout = old_stdout
        sys.stdout.flush()
        # rivL append - for export
        ex2S = spL[0].strip() + " = " + str(val1U)
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivL.append(exvS)
        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivtD": self.rivtD,
            "rivL": self.rivL,
        }
        return self.mD
        # endregion

    def vfunc(self, feqS):
        """format function and assign value

            equation tag  <=:
            a :=: b + 2 | unit1, unit2, decimal | ref

        Returns:
            uS, r2S, rS, fD, lD, rivtD, rivL
        """
        # region
        self.enumI = int(self.lD["equI"])
        self.enumI += 1
        self.lD["equI"] = self.enumI
        self.enumS = str(self.enumI)

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
        spL = eqS.split("=")  # ============== symbolic equation
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # text
        eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
        toptS = chr(9484) + " Eq-" + self.enumS + ": " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n\n"
        # rest
        eq1S = textwrap.indent(eq1S, "           ")
        erS = "\n**Eq. " + self.enumS + ":**  " + refS + "\n"
        eqrS = erS + "\n.. code-block:: text \n\n" + eq1S + "\n\n"
        if unit1S != "-":  # =================== rivtD
            exec(eqS, globals(), self.rivtD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivtD)
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        tbl2L = []  # ============ argument table
        hdr2L = []
        alignL = []
        funcS = spL[1].strip()
        matchO = re.search(r"\(.*\)", funcS)
        matchS = matchO.group()
        syO = sp.sympify(matchS)
        symeqO = sp.sympify(syO, _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO)
        for vS in symaO:
            hdr2L.append(str(vS))
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivtD)
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
        uS = eqtS + "\n" + output.getvalue() + "\n"
        tS = eqtS + "\n" + output.getvalue() + "\n"
        rS = eqrS + "\n" + output.getvalue() + "\n"
        sys.stdout = old_stdout
        sys.stdout.flush()
        tbl1L = []  # =================== result tables
        alignL = ["center", "center", "center"]
        tblfmt = "rst"
        tblL = [tbl1L]
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append("**" + spL[0] + " = " + str(val1U) + "**")
        tbl1L.append("[" + spL[0] + "]" + " = " + str(val2U))
        tbl1L.append(refS)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                showindex=False,
                colalign=alignL,
            )
        )
        uS += "\n" + output.getvalue() + "\n"
        tS += "\n" + output.getvalue() + "\n"
        rS += "\n" + output.getvalue() + "\n"
        lS = " "
        sys.stdout = old_stdout
        sys.stdout.flush()
        # rivL append
        ex2S = spL[0].strip() + " = " + str(val1U)
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivL.append(exvS)

        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivtD": self.rivtD,
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
            uS, rS, tS, fD, lD, rivtD, rivL
        """
        # region
        self.enumI = int(self.lD["equI"])
        self.enumI += 1
        self.lD["equI"] = self.enumI
        self.enumS = str(self.enumI)

        lpL = compS.split("|")
        eqS = lpL[0].strip()
        spL = lpL[0].split(opS)
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
        eq1S = sp.pretty(sp.sympify(eqS, _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        # text  == symbolic equation
        eqxS = textwrap.indent(eqS, chr(9474) + "     ")
        toptS = chr(9484) + "  Eq-" + self.enumS + " | " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
        # rest
        eq1S = textwrap.indent(eq1S, "           ")
        erS = "\n**Eq." + self.enumS + " |** " + refS + "\n"
        eqrS = erS + "\n.. code-block:: text \n\n" + eq1S + "\n\n"

        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        tblfmt = "rst"
        alignL = ["center", "center", "center", "center", "center"]
        hdrL = [spL[0], spL[1], "ratio", "check", "reference"]
        # print(self.rivtD)
        # compare

        resultB = eval(eqS, {}, self.rivtD)
        if resultB:
            chkS = trueS
        else:
            chkS = falseS

        valU = eval(spL[0], globals(), self.rivtD)
        val1U = valU.cast_unit(eval(unitS))
        valU = eval(spL[1], globals(), self.rivtD)
        val2U = valU.cast_unit(eval(unitS))
        val1L = [val1U, val2U, val1U / val2U, chkS, refS]
        tblL = [val1L]
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
        uS = eqtS + "\n" + output.getvalue() + "\n"
        tS = eqtS + "\n" + output.getvalue() + "\n"
        rS = eqrS + "\n" + output.getvalue() + "\n"
        lS = ""
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
            "lD": self.lD,
            "fD": self.fD,
            "rivtD": self.rivtD,
            "rivL": self.rivL,
        }

        return self.mD
        # endregion

    def IMAGE(self):
        """insert image

        | IMAGE | rel. path file | caption, scale, num;non
        """
        # region
        lablS = ""
        parL = self.parS.split(",")
        capS = parL[0].strip()
        scS = parL[1].strip()
        figS = parL[2].strip()
        try:
            img1 = Image.open(self.inspS)
            _display(img1)
        except Exception:
            pass
        if capS == "--":
            capS = ""
        if figS == "num":
            numS = str(self.lD["figI"])
            self.lD["figI"] = int(numS) + 1
            lablS = "Fig. " + numS + " - "
        else:
            lablS = ""
        lablS = lablS + capS + " "
        uS = "\n" + lablS + " [file: " + self.fileS + " ] \n"
        tS = "\n" + lablS + "\n"
        rS = f"""
.. figure:: {self.inspS}
    :width: {scS}%
    :align: center

    {lablS}
    
"""
        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lD": self.lD,
            "rivL": self.rivL,
            "rivtD": self.rivtD,
        }
        # endregion

    def IMAGE2(self):
        """insert side by side images

        |IMG2| rel. pth, rel. pth | sf1, sf2, c1, c2 (_[F])
        """
        # region
        # print(f"{parS=}")

        file1S = self.file2L[0].strip()
        file2S = self.file2L[1].strip()
        ins1P = Path(self.fD["rivtP"], file1S)
        ins2P = Path(self.fD["rivtP"], file2S)
        insp1S = str(ins1P.as_posix())
        insp2S = str(ins2P.as_posix())

        parL = self.parS.split(",")
        cap1S = parL[0].strip()
        cap2S = parL[1].strip()
        scale1S = parL[2].strip()
        scale2S = parL[3].strip()
        fig1S = parL[4].strip()
        fig2S = parL[5].strip()

        try:
            img1 = Image.open(self.inspS)
            _display(img1)
        except Exception:
            pass
        if cap1S == "--":
            cap1S = ""
        if cap2S == "--":
            cap2S = ""
        if fig1S == "num":
            num1S = str(self.lD["figI"])
            self.lD["figI"] = int(num1S) + 1
            labl1S = "Fig. " + num1S + " - "
        else:
            labl1S = ""
        if fig2S == "num":
            num2S = str(self.lD["figI"])
            self.lD["figI"] = int(num2S) + 1
            labl2S = "Fig. " + num2S + " - "
        else:
            labl2S = ""

        labl1S = labl1S + cap1S + " "
        labl2S = labl2S + cap2S + " "

        uS = f"{labl1S} | {labl2S} files: {self.fileS}\n"
        tS = f"{labl1S} | {labl2S}\n"

        rS = f"""
.. list-table::
    :widths: {scale1S} {scale2S}
    :header-rows: 0

    * - .. figure:: {insp1S}
            :width: 100%

            {cap1S}
     
      - .. figure:: {insp2S}
            :width: 100%
            
            {cap2S}
                     
"""

        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lD": self.lD,
            "rivL": self.rivL,
            "rivtD": self.rivtD,
        }
        # endregion

    def TABLE(self):
        """insert table

        | TABLE | rel. path | title,width,r1:r2,l;c;r,num;non
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

        | VALTABLE | relative path | title, rows, num;non
        """
        # region
        fuS = self.fileS
        parL = self.parS.split(",")
        titleS = parL[0].strip()
        tnumI = int(self.lD["tableI"])
        self.lD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        titleS = parL[0].strip() + " from file: " + fuS + "\n"
        titlerS = parL[0].strip() + " from file: **" + fuS + "**\n\n"
        if titleS[0:2] == "--":
            utlS = xtlS = "from file: " + fuS + "\n"
            rtlS = "from file: **" + fuS + "**\n\n"
        else:
            utlS = xtlS = "\nTable " + fillS + ": " + titleS
            rtlS = "\n**Table " + fillS + "**: " + titlerS
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
                        exec(eqS, globals(), self.rivtD)
                    except ValueError as ve:
                        print(f"A ValueError occurred: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    valU = eval(varS, globals(), self.rivtD)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                eqS = varS + " = " + valS
                exec(eqS, globals(), self.rivtD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])
        # print("tbl", tbL)
        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "left", "left", "left"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colglobalalign=alignL,
                headersalign=alignL,
            )
        )
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        uS = utlS + outS + "\n"
        rS = rtlS + outS + "\n"
        tS = xtlS + outS + "\n"
        lS = ""

        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
            "lD": self.lD,
            "rivL": self.rivL,
            "rivtD": self.rivtD,
        }

        return self.mD

        # endregion

    def PYTHON(self):
        """execute Python script

        | PYTHON | rel. path | reference
        """
        # region
        # print(f"{readL=}")
        fuS = self.fileS
        tnumI = int(self.lD["tableI"])
        self.lD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        fileP = Path(self.fD["rivtP"], self.fileS)
        with open(fileP, "r") as f10:
            pyscriptS = f10.read()
        exec(pyscriptS, globals(), self.rivtD)
        tbL = []
        funcL = []
        docstrL = []
        docflg = False
        pyscriptL = pyscriptS.split("\n")
        for s in pyscriptL:
            if docflg:
                s = s.replace('"""', "")
                docstrL.append(s)
                docflg = False
            if s[0:3] == "def":
                s = s.replace("def", "")
                s = s[:-1]
                funcL.append(s)
                docflg = True
        tbL = zip(funcL, docstrL)
        titleS = self.parS.strip() + " from file: " + fuS + "\n"
        titlerS = self.parS.strip() + " from file: **" + fuS + "**\n\n"
        if titleS[0:2] == "--":
            utlS = xtlS = "from file: " + fuS + "\n"
            rtlS = "from file: **" + fuS + "**\n\n"
        else:
            utlS = xtlS = "\nTable " + fillS + ": " + titleS
            rtlS = "\n**Table " + fillS + "**: " + titlerS
        tblfmt = "rst"
        hdrvL = ["Function", "Docstring"]
        alignL = ["left", "left"]
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
        uS = utlS + "\n" + outS + "\n"
        rS = rtlS + "\n" + outS + "\n"
        tS = xtlS + "\n" + outS + "\n"
        lS = ""

        self.mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
            "lD": self.lD,
            "rivL": self.rivL,
            "rivtD": self.rivtD,
        }

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
