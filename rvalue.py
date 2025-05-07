import csv
import logging
import sys
import textwrap
import warnings

from io import StringIO
from pathlib import Path

import sympy as sp
import tabulate
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *  # noqa: F403
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import cmds, tags
from rivtlib.units import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True

"""
        elif stS == "V":
            self.cmdL = ["IMG", "IMG2", "VALUES"]
            self.tagsD = {
                "E]": "equation",
                "F]": "figure",
                "S]": "sympy",
                "L]": "slabel",
                "T]": "table",
                "H]": "hline",
                "P]": "page",
                ":=": "equals",
                "V]]": "valuesblk",
            }
"""


class CmdV:
    """value commands format to utf8 or reSt

    Commands:
        a = 1+1 | unit | reference
        | VALREAD | rel. pth |  dec1
    """

    def __init__(self, folderD, labelD, rivtpD, rivtvD):
        """commands that format a utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.rivtvD = rivtvD
        self.rivtpD = rivtpD
        self.folderD = folderD
        self.labelD = labelD

    def cmd_parse(self, cmdS, pthS, parS):
        """parse tagged line

        Args:
            cmdS (str): command
            pthS (str): path or equation string
            parS (str): command parameters

        Returns:
            utS: formatted utf string
        """

        # print(f"{cmdS=}")
        # print(f"{pthS=}")
        # print(f"{parS=}")

        cC = globals()["CmdV"](self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(self.rivtvD)
        return uS, rS, self.folderD, self.labelD, self.rivtpD, self.rivtvD

    def values(self, pthS, parS):
        """import values from csv files, update rivtD

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        if "_[V]" in parS.strip():  # table number
            vnumI = int(self.labelD["valueI"])
            fillS = str(vnumI).zfill(2)
            utitlnS = "\nValue Table " + fillS + " - " + parS.strip("_[V]")
            rtitlnS = "\n**Value Table " + fillS + " -** " + parS.strip("_[V]")
            self.labelD["valueI"] = vnumI + 1
        else:
            utitlnS = "\nValue Table  - " + parS.strip()
            rtitlnS = "\n**Value Table -** " + parS.strip()

        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + pthS + "]" + "\n\n"
        with open(insP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        # print(f"{readL=}")
        for iL in readL:  # add to valexp
            iS = ",".join(iL)
            self.labelD["valexpS"] += iS + "\n"
        tbL = []
        for vaL in readL:
            # print(f"{vaL=}")
            if len(vaL) < 4:
                continue
            eqS = vaL[0].strip()
            varS = vaL[0].split(":=")[0].strip()
            valS = vaL[0].split(":=")[1].strip()
            descripS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            dec1S, dec2S = vaL[4], vaL[5]
            self.rivtpD[varS] = valS, unit1S, unit2S, dec1S, dec2S
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [varS.cast_unit(eval(unit2S)) for varS in val1U]
                else:
                    eqS = varS + " = " + valS
                    try:
                        exec(eqS, globals(), self.rivtvD)
                    except ValueError as ve:
                        print(f"A ValueError occurred: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    valU = eval(varS, globals(), self.rivtvD)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                eqS = varS + " = " + valS
                exec(eqS, globals(), self.rivtD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])

        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        vC = CmdV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)  # format table
        r2S = rS

        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        pS = "[from file: " + pthS + "]" + "\n\n"
        uS = utitlnS + pS + uS + "\n"
        r2S = rtitlnS + pS + r2S + "\n"
        rS = rtitlnS + pS + rS + "\n"

        return uS, r2S

    def valtable(self, tbL, hdrL, alignL, tblfmt):
        """format table"""
        # print(f"{tbL=}")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL, tablefmt=tblfmt, headers=hdrL, showindex=False, colalign=alignL
            )
        )
        uS = r2S = rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return uS, r2S

    def equate(self, eqS, parS):
        """format equation ' = '

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        wI = self.labelD["widthI"]

        spS = eqS.strip()
        spS = spS.replace(":=", "=")
        refS = parS.split("|")[0].strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

        except:
            pass
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # utf
        lineS = textwrap.indent(lineS, "    ")
        refS = refS.rjust(self.labelD["widthI"])
        uS = refS + "\n" + lineS + "\n\n"
        # rst2
        r2S = "\n\n..  code:: \n\n\n" + refS + "\n" + lineS + "\n\n"
        # rst
        rS = ".. raw:: math\n\n   " + lineS + "\n"

        return uS, r2S

    def equtable(self, eqS, parS):
        """format equation table, update rivtD

        Args:
            eqS (_type_): _description_
            parS (_type_): _description_

        Returns:
            _type_: _description_
        """
        vaL = []
        wI = self.labelD["widthI"]
        eqS = eqS.strip()
        eqS = eqS.replace(":=", "=")
        refS = parS.split("|")
        varS = eqS.split("=")[0].strip()
        valS = eqS.split("=")[1].strip()
        descripS = refS[0].strip()
        unitL = refS[1].split(",")
        unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
        decL = refS[2].split(",")
        dec1S, dec2S = decL[0].strip(), decL[1].strip()
        if unit1S != "-":
            try:
                exec(eqS, globals(), self.rivtvD)
                # print(f"{self.rivtvD=}")
            except ValueError as ve:
                print(f"A ValueError occurred: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            try:
                exec(eqS, globals(), self.rivtD)
            except ValueError as ve:
                print(f"A ValueError occurred: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            valU = eval(varS, globals(), self.rivtD)
            val1U = str(valU)
            val2U = str(valU)
        eqxS = eqS.split("=")[1]
        symeqO = sp.sympify(eqxS, _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO) + 1
        tbl1L = []
        tbl2L = []
        hdr1L = []
        hdr1L.append(varS)
        for vS in symaO:
            hdr1L.append(str(vS))
        fmt1S = "%." + dec1S + "f"
        fmt2S = "%." + dec2S + "f"
        varU = eval(varS, globals(), self.rivtvD)
        varU.set_format(value_format=fmt1S, auto_norm=True)
        val1U = str(varU.cast_unit(eval(unit1S)))
        val2U = str(varU.cast_unit(eval(unit2S)))
        tbl1L.append(val1U)
        tbl2L.append(val2U)
        self.rivtpD[varS] = (val1U, unit1S, unit2S, dec1S, dec2S)
        for aO in symaO:
            # print(self.rivtpD)
            unit1S = self.rivtpD[str(aO)][1]
            unit2S = self.rivtpD[str(aO)][2]
            a1U = eval(str(aO), globals(), self.rivtvD)
            a1U.set_format(value_format=fmt2S, auto_norm=True)
            val1U = str(a1U.cast_unit(eval(unit1S)))
            a2U = eval(str(aO), globals(), self.rivtvD)
            a2U.set_format(value_format=fmt2S, auto_norm=True)
            val2U = str(a2U.cast_unit(eval(unit2S)))
            tbl1L.append(val1U)
            tbl2L.append(val2U)
        tblL = [tbl1L]
        tblL.append(tbl2L)
        alignL = []
        tblfmt = "rst"
        for nI in range(numvarI):
            alignL.append("center")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL, tablefmt=tblfmt, headers=hdr1L, showindex=False, colalign=alignL
            )
        )
        uS = output.getvalue()
        rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        refS = parS.split("|")
        eqS = eqS.replace("=", ":=")
        iS = eqS + "," + ",".join(refS)
        self.labelD["valexpS"] += iS + "\n"

        return uS, rS


class TagV:
    """format to utf8 or reSt

    Functions:
            _[E]                    equation
            _[F]                    figure
            _[T]                    table
            _[A]                    page
            _[[V]]                  values
            _[[Q]]                  quit
    """

    def __init__(self, folderD, labelD, rivtpD, rivtvD):
        """tags that format to utf and reSt"""
        self.rivtpD = rivtpD
        self.rivtvD = rivtvD
        self.folderD = folderD
        self.labelD = labelD
        # print(folderD)
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

    def tag_parse(self, tagcmdS, blockL):
        """parse a tagged line

        Args:
            tagcmd (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        tC = TagV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        uS, rS = functag(blockL)
        # print(f"{tcmdS=}")
        # print(self.rivtpD)
        # print(self.rivtvD)

        return uS, rS, self.folderD, self.labelD, self.rivtpD, self.rivtvD

    def valblock(self, blockL):
        """format values
        Args:
            blockL (list): _description_
        Returns:
            : _description_
        """
        vaL = []
        tbL = []
        # print(f"{blockL=}")
        for vaS in blockL:
            # print(f"{vaS=}")
            vaL = vaS.split("|")
            # print(f"{vaL=}")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if ":=" not in vaL[0]:
                continue
            eqS = vaL[0].strip()
            eqS = eqS.replace(":=", "=")
            varS = eqS.split("=")[0].strip()
            valS = eqS.split("=")[1].strip()
            descripS = vaL[1].strip()
            unitL = vaL[2].split(",")
            unit1S, unit2S = unitL[0], unitL[1]
            decL = vaL[3].split(",")
            dec1S, dec2S = decL[0], decL[1]
            if unit1S != "-":
                try:
                    exec(eqS, globals(), self.rivtvD)
                except ValueError as ve:
                    print(f"A ValueError occurred: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                valU = eval(varS, {}, self.rivtvD)
                val1U = str(valU.cast_unit(eval(unit1S)))
                val2U = str(valU.cast_unit(eval(unit2S)))
                # print(f"{self.rivtvD=}")
            else:
                cmdS = varS + " = " + valS
                exec(cmdS, globals(), self.rivtvD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])
            self.rivtpD[varS] = valS, unit1S, unit2S, dec1S, dec2S

        for vaS in blockL:
            vaL = vaS.split("|")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if "=" not in vaL[0]:
                continue
            iS = ",".join(vaL)
            self.labelD["valexpS"] += iS + "\n"

        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]

        vC = CmdV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)

        return uS + "\n", rS + "\n"
