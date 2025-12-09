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

     API        Command                                                RW   File Types
    ---------  ------------------------------------------------------- --- -----------------
    rv.R        | LINUX | relative path | *wait;nowait*                 R     *.sh*
    rv.R        | MACOS | relative path | *wait;nowait*                 R     *.sh*
    rv.R        | WIN | relative path   | *wait;nowait*                 R     *.bat, .cmd*
    rv.I, V     | IMAGE | relative path |  scale, caption (_[I])        R     *.png, .jpg*
    rv.I, V     | IMAGE2 | relative path | s1, s2, c1, c2 (_[I])        R     *.png, jpg*
    rv.I, V     | TABLE | relative path | width, l;c;r, title           R     *csv, txt, xlsx*
    rv.I, V     | TEXT | relative path |  *normal;literal* ;code        R     *txt, code*
    rv.V        | VALUES | relative path | label (_[T])                 R     *csv*
    rv.V       a := 1*IN  | unit1, unit2, decimal | descrip (_[E])[1]   W     define a value
    rv.V       b <= a + 3*FT | unit1, unit2, decimal | descrip (_[E])   W     assign a value
    rv.V       c <= func1(x,y) | unit1, unit2, decimal | descrip (_[E]) W     assign a value
    rv.V, T     | PYTHON | relative path | *rv-space*; userspace        R     *py*
    rv.T        | HTML | relative path | label                          R     *html*
    rv.T        | LATEX | relative path | label                         R     *tex*
    rv.D        | ATTACH | relative path | cover_page_title             W     *pdf*
    rv.D        | PUBLISH | relative path | *pdf;pdftex;text;html*      W     *pdf, html, txt*

    """

    def __init__(self, foldD, lablD, rivD, rivL, parL):
        """command object

        Args:
            foldD (dict): folders
            lablD (dict): labels
            rivD (dict): values
            rivL (list): values for export

        Vars:
            uS (str): utf string
            r2S (str): rst2pdf string
            rS (str): reST string
        """
        # region
        store_attr()
        self.fileS = parL[1].strip()
        self.parS = parL[2].strip()
        self.uS = ""
        self.r2s = ""
        self.rs = ""
        self.insP = Path(foldD["rivtP"], self.fileS)
        self.inspS = str(self.insP.as_posix())
        # endregion

    def cmdx(self, cmdS):
        """parse section

        Args:
            cmdS (str): command keyword
        Returns:
            uS, rS, xS, foldD, lablD, rivD, rivL
        """
        # region
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.r2s,
            self.rs,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )
        # endregion

    def vassign(self, aeqS):
        """format equation and assign value

            equation tag  <=
            a <= b + 2 | unit1, unit2, decimal | ref

        Returns:
            uS, r2S, rS, foldD, lablD, rivD, rivL
        """
        # region
        tbl1L = []
        hdr1L = []
        lpL = aeqS.split("|")
        eqS = lpL[0]
        eqS = eqS.replace("<=", "=").strip()
        unit1S, unit2S, dec1S = lpL[1].split(",")
        unit1S, unit2S, dec1S = unit1S.strip(), unit2S.strip(), dec1S.strip()
        refS = lpL[2].strip()
        decS = "%." + dec1S + "f"
        Unum.set_format(value_format=decS, auto_norm=True, unitless="")
        # print(dir(Unum.set_format))
        # wI = self.lablD["widthI"]

        # equation
        spL = eqS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        eq1S = sp.pretty(sp.sympify(sp.simplify(spS), _clash2, evaluate=False))
        eq1S = textwrap.indent(eq1S, "    ")
        if "_[E]" in refS:
            refS = refS.replace("_[E]", "")
            enumI = int(self.lablD["equI"])
            self.lablD["equI"] = enumI + 1
            fillS = " [Eq " + str(enumI) + "]"
            refS = refS + fillS
            refS = refS.rjust(self.lablD["widthI"]) + "\n"
            self.uS = refS + "\n"
            self.r2s = refS + "\n"
            self.rs = refS + "\n"
        else:
            refS = refS.rjust(self.lablD["widthI"])

        uS = "\n" + refS + "\n" + eq1S + "\n\n"
        if unit1S != "-":
            exec(eqS, globals(), self.rivD)
        else:
            cmdS = spL[0] + " = " + spL[1]
            exec(cmdS, globals(), self.rivD)

        r2S = "\n\n..  code:: \n\n\n" + refS + "\n" + eqS + "\n\n"
        rS = ".. raw:: math\n\n   " + eqS + "\n"

        # rivD append
        valU = eval(spL[0], globals(), self.rivD)
        self.rivD[spL[0]] = valU

        # equation and table elements
        symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO) + 3
        hdr1L.append(spL[0])
        hdr1L.append("[" + spL[0] + "]")
        hdr1L.append("|")
        for vS in symaO:
            hdr1L.append(str(vS))
        # print("header----------", hdr1L)

        # eval value
        val1U = valU.cast_unit(eval(unit1S))
        val2U = valU.cast_unit(eval(unit2S))
        tbl1L.append(str(val1U))
        tbl1L.append(str(val2U))
        # print(f"{valU=}")
        # print("table--------------", tbl1L)

        # rivL append
        ex2S = spL[0].strip() + " = " + str(val1U)
        exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
        self.rivL.append(exvS)
        # loop over variables
        tbl1L.append("|")
        for aO in symaO:
            a1U = eval(str(aO), globals(), self.rivD)
            tbl1L.append(str(a1U))
            # print(aO, a1U, tbl1L)

        # write table
        alignL = []
        tblL = [tbl1L]
        tblfmt = "rst"
        for nI in range(numvarI):
            alignL.append("center")
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
        uS += output.getvalue()
        r2S += output.getvalue()
        rS += output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return (
            uS,
            r2S,
            rS,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )

    # endregion

    def vdefine(self, valS):
        """define value :=

            a := .5 * 2*IN | unit1, unit2, decimal | ref

        Returns:
            uS, r2S, rS, foldD, lablD, rivD, rivL

        """

        # region
        tbL = []
        vaL = valS.split("|")
        # print(f"{valS=}")
        # print(f"{vaL=}")
        eqS = vaL[0].strip()
        eqS = eqS.replace(":=", "=")
        varS = eqS.split("=")[0].strip()
        valS = eqS.split("=")[1].strip()
        unitL = vaL[1].split(",")
        unit1S, unit2S, dec1S = (
            unitL[0].strip(),
            unitL[1].strip(),
            unitL[2].strip(),
        )
        descripS = vaL[2].strip()
        # rivL append
        exvS = ",".join((eqS, unit1S, unit2S, dec1S, descripS))
        self.rivL.append(exvS)
        # rivD append
        try:
            exec(eqS, globals(), self.rivD)
        except ValueError as ve:
            print(f"A ValueError occurred: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        # format
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
        # print(f"{self.rivtvD=}")
        self.rivD[varS] = valU  # rivt dictionary
        tbL = [varS, val1S, val2S, descripS]  # append row

        return (
            self.uS,
            self.r2s,
            self.rs,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
            tbL,
        )

        # export value table
        # endregion

    def cF(self):
        """number figure"""
        # region
        lineS = self.strpS
        fnumI = int(self.lablD["figI"])
        self.lablD["figI"] = fnumI + 1
        self.uS = "Fig. " + str(fnumI) + " -" + lineS
        self.r2s = "**Fig. " + str(fnumI) + " -** " + lineS
        self.rs = "**Fig. " + str(fnumI) + " -** " + lineS
        # endregion

    def cT(self):
        """number table"""
        # region
        lineS = self.strpS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.r2s = "\n**Table " + fillS + "**: " + lineS
        self.rs = "\n**Table " + fillS + "**: " + lineS
        # endregion

    def cE(self):
        """number equation"""
        # region
        lineS = self.strpS
        enumI = int(self.lablD["equI"])
        self.lablD["equI"] = enumI + 1
        fillS = "\n" + "Eq. " + str(enumI)
        self.uS = fillS + " - " + lineS
        fillS = "**Eq " + str(enumI) + "**"
        self.r2s = lineS + " - " + fillS + "\n"
        self.rs = lineS + " - " + fillS + "\n"
        # endregion

    def IMAGE(self):
        """insert image

        | IMG | rel. path file | scale factor, caption (_[F])
        """
        # region
        parL = self.parS.split(",")
        scS = parL[0].strip()
        capS = " "
        if "_[F]" in parL[1] or capS[0:1] != "--":
            capS = parL[1].replace("_[F]", " ")
        elif capS[0:1] != "--":
            capS = " "
        self.strpS = capS.strip()
        self.cF()
        try:
            img1 = Image.open(self.inspS)
            _display(img1)
        except Exception:
            pass

        self.uS = self.uS + " [file: " + self.fileS + " ] \n"
        self.r2s = self.rs = (
            "\n\n.. image:: "
            + self.inspS
            + "\n"
            + "   :width: "
            + scS
            + "% \n"
            + "   :align: center \n\n\n"
            + ".. class:: center \n\n"
            + capS
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
            numS = str(self.lablD["fnum"])
            self.lablD["fnum"] = int(numS) + 1
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

        parL = self.parS.split(",")
        titleS = " "
        if "_[T]" in parL[2] or titleS[0:1] != "--":
            titleS = parL[2].replace("_[T]", " ")
        elif titleS[0:1] != "--":
            titleS = " "
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
        insP = Path(self.foldD["srcP"], self.pthS)
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.r2s = fileS
        self.rs = fileS
        # endregion

    def VALUES(self):
        """read file and insert values

        | VALUE | relative path | title (_[T])
        """
        # region
        parL = self.parS.split(",")
        titleS = " "
        if "_[T]" in parL[0] or titleS[0:1] != "--":
            titleS = parL[0].replace("_[T]", " ").strip()
        elif titleS[0:1] != "--":
            titleS = " "
        self.strpS = titleS.strip()
        self.cT()
        fiS = " [file: " + self.fileS + "]" + "\n\n"
        utlS = titleS + fiS
        rtlS = xtlS = titleS + fiS

        with open(self.insP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
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
            # wI = self.lablD["widthI"]
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
        parL = self.parS.split(",")
        namespaceS = parL[0]

        fileP = Path(self.foldD["rivtP"], self.fileS)
        with open(fileP, "r") as f10:
            pyscriptS = f10.read()
        if namespaceS == "rivt":
            exec(pyscriptS, globals(), self.rivD)
        else:
            exec(pyscriptS, globals(), namespaceS)

        fiS = " [file: " + self.fileS + "]" + "\n\n"

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
        insP = Path(self.foldD["reptfoldP"])
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
        insP = Path(self.foldD["reptfoldP"])
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
        insP = Path(self.foldD["reptfoldP"])
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
