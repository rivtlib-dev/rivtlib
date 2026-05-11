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

    def __init__(self, stS, fD, lD, rivtD, rivL, parL, vardescD):
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
        sp.init_printing(use_unicode=True)
        # if stS == "V":
        #     sp.init_printing(use_unicode=False)
        # else:
        #     sp.init_printing(use_unicode=True)

        self.fileS = parL[1].strip()
        self.file2L = parL[1].split(",")
        self.parS = parL[2].strip()
        self.insP = Path(fD["rivtP"], self.fileS)
        self.inspS = str(self.insP.as_posix())
        self.uS = ""
        self.rS = ""
        self.tS = ""
        self.lS = ""
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
        self.vardescD[varS] = descripS
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
        self.rivtD[varS] = valU  # add to rivt dictionary
        tbL = [varS, val1S, val2S, descripS]  # append row

        return tbL, self.rivtD, self.rivL, self.vardescD
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
        self.vardescD[spL[0].strip()] = refS
        # text
        eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
        toptS = chr(9484) + "  Eq-" + self.enumS + " | " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
        # rest
        eq1S = textwrap.indent(eq1S, "           ")
        erS = "\n\n**Eq. " + self.enumS + ":**  " + refS + "\n"
        if unit1S != "-":  # =================== rivtD
            exec(eqS, globals(), self.rivtD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivtD)
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        eq2S = sp.pretty(sp.sympify(spL[0], _clash2, evaluate=False))  # results
        tbl1L = []  # ============ values table
        tbl2L = []
        hdr2L = []
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        for vS in symaO:
            vS = sp.pretty(sp.sympify(vS, _clash2, evaluate=False))
            hdr2L.append(str(vS))
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivtD)
            tbl2L.append(str(a1U))
        dL = []
        for aO in symaO:
            dL.append(self.vardescD[str(aO)])
        tblL = self.wrap_pad(dL)
        tbl1L = list(zip(*tblL))
        lnS = chr(8212) * 5
        lnL = (lnS,) * len(tbl1L[0])
        tbl1L.insert(0, lnL)
        tbl2L = [tbl2L]
        tbl3L = tbl2L + tbl1L
        tblfmt = "rst"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbl3L,
                tablefmt=tblfmt,
                headers=hdr2L,
                showindex=False,
                colglobalalign="left",
            )
        )
        outputL = output.getvalue().split("\n")[1:]
        outputS = "\n".join(outputL).replace("=", chr(8212))
        eqrS = (
            "\n|\n"
            + erS
            + "\n.. code-block:: text \n\n"
            + eq1S
            + "\n\n           "
            + f"{eq2S} = {val1U}     [{eq2S}] = {val2U}   | {refS.strip()}\n\n"
            + textwrap.indent(outputS, "           ")
        )
        uS = tS = "\n" + eqtS + output.getvalue()
        rS = "\n" + eqrS + "\n\n"
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
        return self.mD, self.vardescD
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
        spL = eqS.split("=")  # ============== symbolic equation
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        self.vardescD[spL[0].strip()] = refS
        # text
        eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
        toptS = chr(9484) + "  Eq-" + self.enumS + " | " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
        # rest
        eq1S = textwrap.indent(eq1S, "           ")
        erS = "\n\n**Eq. " + self.enumS + ":**  " + refS + "\n"
        # rst
        self.vardescD[spL[0].strip()] = refS
        if unit1S != "-":  # =================== rivtD
            exec(eqS, globals(), self.rivtD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivtD)
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        eq2S = sp.pretty(sp.sympify(spL[0], _clash2, evaluate=False))  # results
        tbl1L = []  # ============ values table
        tbl2L = []
        hdr2L = []
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO)
        for vS in symaO:
            vS = sp.pretty(sp.sympify(vS, _clash2, evaluate=False))
            hdr2L.append(str(vS))
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivtD)
            tbl2L.append(str(a1U))
        dL = []
        for aO in symaO:
            dL.append(self.vardescD[str(aO)])
        tblL = self.wrap_pad(dL)
        tbl1L = list(zip(*tblL))
        lnS = chr(8212) * 5
        lnL = (lnS,) * len(tbl1L[0])
        tbl1L.insert(0, lnL)
        tbl2L = [tbl2L]
        tbl3L = tbl2L + tbl1L
        tblfmt = "rst"
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbl3L,
                tablefmt=tblfmt,
                headers=hdr2L,
                showindex=False,
                colglobalalign="left",
            )
        )
        outputL = output.getvalue().split("\n")[1:]
        outputS = "\n".join(outputL).replace("=", chr(8212))
        eqrS = (
            "\n|\n"
            + erS
            + "\n.. code-block:: text \n\n"
            + eq1S
            + "\n\n           "
            + f"{eq2S} = {val1U}     [{eq2S}] = {val2U}   | {refS.strip()}\n\n"
            + textwrap.indent(outputS, "           ")
        )
        uS = tS = "\n" + eqtS + output.getvalue()
        rS = "\n" + eqrS + "\n\n"
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
        return self.mD, self.vardescD
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
        # text  == symbolic
        eqxS = textwrap.indent(eqS, chr(9474) + "     ")
        toptS = chr(9484) + "  Eq-" + self.enumS + " | " + refS + "\n"
        eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
        # ====== rivtD
        valU = eval(spL[0], globals(), self.rivtD)
        self.rivtD[spL[0]] = valU
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
        term1S = sp.pretty(sp.sympify(spL[0].strip(), _clash2, evaluate=False))
        term2S = sp.pretty(sp.sympify(spL[1].strip(), _clash2, evaluate=False))
        tblfmt = "rst"
        hdrL = [term1S, term2S, "ratio", "check", "reference"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL,
                tablefmt=tblfmt,
                headers=hdrL,
                showindex=False,
                colglobalalign="left",
            )
        )
        equS = ""
        equL = output.getvalue().split("\n")
        for ln in equL:
            ln = chr(9646) + " " + ln
            equS += ln + "\n"
        uS = tS = eqtS + "\n" + equS + "\n"
        lS = ""
        eq3S = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # rest  == symbolic and table
        erS = "|\n\n**Eq." + self.enumS + ":** " + refS + "\n"
        outputL = output.getvalue().split("\n")[1:]
        outputS = "\n".join(outputL).replace("=", chr(8212))
        erS = "\n\n**Eq. " + self.enumS + ":**  " + refS + "\n"
        eq3S = ""
        eq3L = outputS.split("\n")
        for ln in eq3L:
            ln = "  " + chr(9646) + " " + ln
            eq3S += ln + "\n"
        rS = (
            "\n|\n"
            + erS
            + "\n.. code-block:: text \n\n  "
            + chr(9646)
            + " "
            + eq1S.strip()
            + "\n  "
            + chr(9646)
            + "\n"
            + eq3S
        )

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
            lablS = "**Fig. " + numS + "** - "
            lablxS = "Fig. " + numS + " - "
        else:
            lablS = ""
        lablS = lablS + capS + " "
        bordS = " " * 10 + "-" * 40 + "\n"
        uS = tS = bordS + lablxS + " [file: " + self.fileS + " ] \n" + bordS
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
            labl1S = "**Fig. " + num1S + " -** " + cap1S + " "
            labl1xS = "Fig. " + num1S + " - " + cap1S + " "
        else:
            labl1S = ""
        if fig2S == "num":
            num2S = str(self.lD["figI"])
            self.lD["figI"] = int(num2S) + 1
            labl2S = "**Fig. " + num2S + " -** " + cap2S + " "
            labl2xS = "Fig. " + num2S + " - " + cap2S + " "
        else:
            labl2S = ""

        bordS = " " * 10 + "-" * 40 + "\n"
        uS = bordS + f"{labl1xS} | {labl2xS}  \nfiles: {self.fileS}\n" + bordS
        tS = bordS + f"{labl1xS} | {labl2xS}  \nfiles: {self.fileS}\n" + bordS

        rS = f"""
.. list-table::
    :widths: {scale1S} {scale2S}
    :header-rows: 0

    * - .. figure:: {insp1S}
            :width: 100%

            {labl1S}
     
      - .. figure:: {insp2S}
            :width: 100%
            
            {labl2S}
                     
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
        rowL = eval(parL[3].strip())  # rows
        if len(rowL) == 0:
            pass
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
        output.write(
            tabulate.tabulate(
                readL,
                tablefmt="rst",
                headers="firstrow",
                numalign="decimal",
                maxcolwidths=maxwI,
                colglobalalign="left",
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
            rtlS = "|\n\n**Table " + fillS + "**: " + titlerS
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
        for ln in readL:
            symS = str(ln[0].split("=")[0].strip())
            self.vardescD[symS] = ln[4].strip()
        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colglobalalign="left",
            )
        )
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        uS = utlS + outS + "\n\n"
        rS = rtlS + outS + "\n\n"
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

        return self.mD, self.vardescD

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
        titleS = self.parS.strip() + " from file: " + fuS
        titlerS = self.parS.strip() + " from file: **" + fuS + "**\n\n"
        if titleS[0:2] == "--":
            utlS = xtlS = "from file: " + fuS + "\n"
            rtlS = "from file: **" + fuS + "**\n\n"
        else:
            utlS = xtlS = "\nTable " + fillS + ": " + titleS
            rtlS = "\n**Table " + fillS + "**: " + titlerS
        tblfmt = "rst"
        hdrvL = ["Function", "Docstring"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colglobalalign="left",
            )
        )
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        uS = tS = utlS + "\n" + outS + "\n"
        rS = rtlS + "\n" + outS + "\n"
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

    def wrap_pad(self, sentences, width=25):
        # Step 1: Wrap all sentences into lists of lines
        wrapped_data = [textwrap.wrap(s, width=width) for s in sentences]

        # Step 2: Identify the maximum number of lines
        max_height = max(len(lines) for lines in wrapped_data)

        # Step 3: Pad shorter sentences with empty lines to match max_height
        padded_data = []
        for lines in wrapped_data:
            # Create a copy and add empty strings until length matches max_height
            padded = lines + ["-"] * (max_height - len(lines))
            padded_data.append(padded)

        return padded_data
