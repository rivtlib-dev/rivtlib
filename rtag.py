#
import logging
import sys
import textwrap
import warnings
from datetime import datetime, time
from io import StringIO
from pathlib import Path

import sympy as sp
import tabulate
from numpy import *  # noqa: F403
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib.runits import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """
<<<<<<< HEAD
    tag formatting
=======
    formatting tags
>>>>>>> 9792e999fd29be05bdd949c5d1f3e270d1eb7642


    blocks:
    hexcolor _[[B]]   bldindblk
    hexcolor _[[C]]   codeblk
    hexcolor _[[I]]   italindblk
    hexcolor _[[L]]   literalblock
    hexcolor _[[X]]   latexblk
    title  _[[V]]     valuesblk
    _[[Q]]

    try:
        valN = folderD["valN"]  # value export file
        valN = valN.replace("qqqqqq", str(snumI))
        valsP = folderD["valsP"]
        valP = Path(valsP, valN)
        folderD["valP"] = valP
    except:
        pass
    # print(strL)
    # print(f"{self.tS=}")




        tC = Tag(self.folderD, self.labelD)
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        uS, rS = functag(lineS)

    """

    def __init__(self, folderD, labelD, rivtD):
        """
        format tags - utf and reSt

        folderD (_type_): _description_
        labelD (_type_): _description_
        rivtD (_type_): _description_

        """
        self.folderD = folderD
        self.labelD = labelD
        self.rivtD = rivtD
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

    def linetag(self, tagS, lineS, rivtL):
        """format line tags

        text        _[C]    center
        text        _[D]    footnote description
        label       _[E]    equation label
        text        _[#]    footnote
        caption     _[F]    figure caption
        equation    _[S]    sympy
        equation    _[Y]    sympy with label
        title       _[T]    table title
        url, label  _[U]    url
        a := 1       :=     evaluate equation
        _[-----]            horizontal line
        _[=====]            new page

        Args:
            tagS (str): tag symbol
            lineS (str): line from rivt section

        Returns:
            tuple : formatted doc strings
        """

        if tagS == "C]":
            """ center a line """
            uS = lineS.center(int(self.labelD["widthI"])) + "\n"
            r2S = lineS.center(int(self.labelD["widthI"])) + "\n"
            rS = "\n::\n\n" + lineS.center(int(self.labelD["widthI"])) + "\n"

        elif tagS == "D]":
            """ footnote description """
            ftnumI = self.labelD["noteL"].pop(0)

            uS, r2S, rS = "[" + str(ftnumI) + "] " + lineS

        elif tagS == "E]":
            """ equation label """
            enumI = int(self.labelD["equI"])
            self.labelD["equI"] = enumI + 1
            fillS = "E" + str(enumI).zfill(2)
            uS = fillS + " - " + lineS

            fillS = "**E" + str(enumI).zfill(2) + "**"
            rS = r2S = lineS + " - " + fillS + "\n"

        elif tagS == "F]":
            """ figure caption"""
            fnumI = int(self.labelD["figI"])
            self.labelD["figI"] = fnumI + 1

            uS = r2S = rS = "Fig. " + str(fnumI) + " - " + lineS + "\n"

        elif tagS == "#]":
            """ footnote number """
            ftnumI = self.labelD["footL"].pop(0)
            self.labelD["noteL"].append(ftnumI + 1)
            self.labelD["footL"].append(ftnumI + 1)

            uS = r2S = rS = lineS.replace("*]", "[" + str(ftnumI) + "]")

        elif tagS == "S]":
            """ format equation with sympy """
            spS = lineS.strip()
            try:
                spL = spS.split("=")
                spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            except:
                pass
            lineS = sp.pretty(sp.sympify(sp.simplify(spS), _clash2, evaluate=False))

            uS = textwrap.indent(lineS, "     ")
            r2S = "\n\n.. code:: \n\n\n" + uS + "\n\n"
            rS = ".. raw:: math\n\n   " + uS + "\n"

        elif tagS == "Y]":
            """ format and label equation with sympy """
            spS = lineS.strip()
            try:
                spL = spS.split("=")
                spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            except:
                pass
            lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

            uS = textwrap.indent(lineS, "     ")
            r2S = "\n\n.. code:: \n\n\n" + uS + "\n\n"
            rS = ".. raw:: math\n\n   " + lineS + "\n"

        elif tagS == "T]":
            """ format table title """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            fillS = str(tnumI).zfill(2)
            uS = "\nTable " + str(tnumI) + ": " + lineS
            r2S = "\n**Table " + fillS + "**: " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS

        elif tagS == "U]":
            """ format url """
            lineL = self.lineS.split(",")
            uS = r2S = rS = ".. _" + lineL[0] + ": " + lineL[1]

        elif tagS[:5] == "------":
            """ format horizontal line """
            uS = "-" * 80
            r2S = "-" * 80
            rS = "-" * 80

        elif tagS[:5] == "=====":
            """ format new page """
            pagenoS = str(self.labelD["pageI"])
            uS = self.labelD["headuS"].replace("p##", pagenoS)
            self.labelD["pageI"] = int(pagenoS) + 1
            r2S = rS = (
                "\n"
                + "_" * self.labelD["widthI"]
                + "\n"
                + uS
                + "\n"
                + "_" * self.labelD["widthI"]
                + "\n"
            )

        elif tagS == ":=":
            """ equation evluate and format """

            tbl1L = []
            hdr1L = []
            wI = self.labelD["widthI"]
            lpL = lineS.split("|")
            eqS = lpL[0]
            eqS = eqS.replace(":=", "=").strip()
            parL = lpL[1:]
            unit1S, unit2S, dec1S, dec2S = parL[0].split(",")
            refS = parL[1].strip()
            unit1S, unit2S = unit1S.strip(), unit2S.strip()
            dec1S, dec2S = dec1S.strip(), dec2S.strip()
            fmt1S = "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
            fmt2S = "Unum.set_format(value_format='%." + dec2S + "f', auto_norm=True)"

            # equation as string
            spL = eqS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            eq1S = sp.pretty(sp.sympify(sp.simplify(spS), _clash2, evaluate=False))
            eq1S = textwrap.indent(eq1S, "    ")
            refS = refS.rjust(self.labelD["widthI"])

            uS = refS + "\n" + eq1S + "\n\n"
            r2S = "\n\n..  code:: \n\n\n" + refS + "\n" + eqS + "\n\n"
            rS = ".. raw:: math\n\n   " + eqS + "\n"

            if unit1S != "-":
                exec(eqS, globals(), self.rivtD)
            else:
                cmdS = spL[0] + " = " + spL[1]
                exec(cmdS, globals(), self.rivtD)

            # rivtL and rivtD append
            valU = eval(spL[0], globals(), self.rivtD)
            self.rivtD[spL[0]] = valU
            vxS = str(valU).strip()
            vxL = vxS.split(" ")
            exS = vxL[0] + " * " + vxL[1].upper()
            ex2S = spL[0].strip() + " = " + exS
            exvS = ",".join((ex2S, unit1S, unit2S, dec1S, refS.strip()))
            rivtL.append(exvS)

            # equation and table elements
            symeqO = sp.sympify(spL[1], _clash2, evaluate=False)
            symaO = symeqO.atoms(sp.Symbol)
            hdr1L.append(spL[0])
            hdr1L.append("[" + spL[0] + "]")
            for vS in symaO:
                hdr1L.append(str(vS))
            numvarI = len(symaO) + 2
            # print("header----------", hdr1L)

            # eval value
            eval(fmt1S)
            val1U = valU.cast_unit(eval(unit1S))
            val2U = valU.cast_unit(eval(unit2S))
            tbl1L.append(str(val1U))
            tbl1L.append(str(val2U))
            # print("table--------------", tbl1L)

            # loop over variables
            eval(fmt2S)
            for aO in symaO:
                a1U = eval(str(aO), globals(), self.rivtD)
                tbl1L.append(str(a1U))
                # print("ao", aO, a1U)

            # write table
            # print(tbl1L)
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

        else:
            pass

        return uS, r2S, rS, self.folderD, self.labelD, self.rivtD, rivtL

    def blocktag(self, tagS, blockS, rivtL):
        """

        color _[[B]]   bldindblk
        color _[[C]]   codeblk
        color _[[I]]   italindblk
        color _[[L]]   literalblock
        color _[[N]]   indentblock
        color _[[X]]   latexblk
        title _[[V]]   valuesblk

        Args:
            tagS (_type_): _description_
            lineS (_type_): _description_

        Returns:
            _type_: _description_
        """

        blockL = blockS.split("\n")

        if tagS == "[B]]":
            """ bold indent block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            # utf
            luS = "Table " + str(tnumI) + " - " + blockS
            # rst
            lrS = "\n" + "Table " + fillS + ": " + blockS

        elif tagS == "[I]]":
            """ italic indent block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + blockS
            lrS = "\n" + "Table " + fillS + ": " + blockS

        elif tagS == "[L]]":
            """ literal block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + blockS
            lrS = "\n" + "Table " + fillS + ": " + blockS

        elif tagS == "[O]]":
            """ code block """
            iS = ""
            for s in blockL:
                s = "    " + s + "\n"
                iS += s

            uS = r2S = rS = iS

        elif tagS == "[N]]":
            """ indent block """
            iS = ""
            for s in blockL:
                s = "    " + s + "\n"
                iS += s

            uS = r2S = rS = iS

        elif tagS == "[X]]":
            """ latex block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + blockS
            lrS = "\n" + "**" + "Table " + fillS + ": " + blockS

        elif tagS == "[V]]":
            """ values block """

            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            fillS = str(tnumI).zfill(2)
            tbL = []
            uS = "\nTable " + fillS + " - " + blockL[0] + "\n\n"
            r2S = "\n**Table " + fillS + "**: " + blockL[0] + "\n\n"
            rS = "\n**Table " + fillS + "**: " + blockL[0] + "\n\n"

            # print(f"{blockL=}")
            for vaS in blockL[1:]:
                vaL = vaS.split("|")
                if len(vaL) != 3:
                    continue
                if ":=" not in vaL[0]:
                    continue
                # print(f"{vaS=}")
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
                fmt1S = (
                    "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
                )
                eval(fmt1S)

                # rivtL append
                exvS = ",".join((eqS, unit1S, unit2S, dec1S, descripS))
                rivtL.append(exvS)

                # rivtD append
                if unit1S != "-":
                    try:
                        exec(eqS, globals(), self.rivtD)
                    except ValueError as ve:
                        print(f"A ValueError occurred: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    valU = eval(varS, {}, self.rivtD)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
                    self.rivtD[varS] = val1U
                    # print(f"{self.rivtvD=}")
                else:
                    cmdS = varS + " = " + valS
                    exec(cmdS, globals(), self.rivtD)
                    valU = eval(varS)
                    val1U = str(valU)
                    val2U = str(valU)
                tbL.append([varS, val1U, val2U, descripS])
                self.rivtD[varS] = valU

            # write value table
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
            uS += output.getvalue() + "\n"
            r2S += output.getvalue() + "\n"
            rS += output.getvalue() + "\n"
            sys.stdout = old_stdout
            sys.stdout.flush()

            return uS, r2S, rS, self.folderD, self.labelD, self.rivtD, rivtL

        else:
            pass
