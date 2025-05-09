#
import logging
import sys
import textwrap
import warnings
from datetime import datetime, time
from io import StringIO
from pathlib import Path

import tabulate
from numpy import *  # noqa: F403
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib.units import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """
    formatting tags


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

    def linetag(self, tagS, lineS):
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
        ----                horizontal line
        _[P]                new page

        Args:
            tagS (str): tag symbol
            lineS (str): line from rivt section

        Returns:
            tuple : formatted doc strings
        """

        if tagS == "C]":
            """ center a line """
            uS = lineS.center(int(self.labelD["widthI"])) + "\n"
            rS = lineS.center(int(self.labelD["widthI"])) + "\n"
            xS = "\n::\n\n" + lineS.center(int(self.labelD["widthI"])) + "\n"

            return uS, rS, xS

        elif tagS == "D]":
            """ footnote description """
            ftnumI = self.labelD["noteL"].pop(0)

            uS, rS, xS = "[" + str(ftnumI) + "] " + lineS

            return uS, rS, xS

        elif tagS == "E]":
            """ equation label """
            enumI = int(self.labelD["equI"])
            self.labelD["equI"] = enumI + 1
            fillS = "\nE" + str(enumI).zfill(2)

            uS = fillS + " - " + lineS + "\n"
            fillS = "\n**E" + str(enumI).zfill(2) + "** - "
            rS = fillS + "   " + lineS + "\n"
            xS = uS

            return uS, rS, xS

        elif tagS == "F]":
            """ figure caption"""
            fnumI = int(self.labelD["figI"])
            self.labelD["figI"] = fnumI + 1

            uS = rS = xS = "Fig. " + str(fnumI) + " - " + lineS + "\n"

            return uS, rS, xS

        elif tagS == "#]":
            """ footnote number """
            ftnumI = self.labelD["footL"].pop(0)
            self.labelD["noteL"].append(ftnumI + 1)
            self.labelD["footL"].append(ftnumI + 1)

            uS = rS = tS = lineS.replace("*]", "[" + str(ftnumI) + "]")

            return uS, rS, xS

        elif tagS == "S]":
            """ format equation with sympy """
            spS = lineS.strip()
            try:
                spL = spS.split("=")
                spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            except:
                pass
            lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))

            uS = textwrap.indent(lineS, "     ")
            rS = "\n\n.. code:: \n\n\n" + uS + "\n\n"
            tS = ".. raw:: math\n\n   " + lineS + "\n"

            return uS, rS, xS

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
            rS = "\n\n.. code:: \n\n\n" + uS + "\n\n"
            tS = ".. raw:: math\n\n   " + lineS + "\n"

            return uS, rS, xS

        elif tagS == "T]":
            """ format table title """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            fillS = str(tnumI).zfill(2)
            uS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS
            xS = "\n**Table " + fillS + "**: " + lineS

            return uS, rS, xS

        elif tagS == "U]":
            """ format url """
            lineL = self.lineS.split(",")
            lineS = ".. _" + lineL[0] + ": " + lineL[1]

            return lineS

        elif tagS == "----":
            """ format horizontal line """
            uS = "-" * 80
            rS = "-" * 80
            xS = "-" * 80

            return uS, rS, xS

        elif tagS == "P]":
            """ format new page """
            pagenoS = str(self.labelD["pageI"])
            rvtS = self.labelD["headuS"].replace("p##", pagenoS)
            self.labelD["pageI"] = int(pagenoS) + 1
            lineS = (
                "\n"
                + "_" * self.labelD["widthI"]
                + "\n"
                + rvtS
                + "\n"
                + "_" * self.labelD["widthI"]
                + "\n"
            )

            return "\n" + rvtS

        else:
            pass

        if tagS == ":=":
            """ equation evluate and format """
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

            # write equation table
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
                    tblL,
                    tablefmt=tblfmt,
                    headers=hdr1L,
                    showindex=False,
                    colalign=alignL,
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

    def blocktag(self, tagS, blockS):
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
            luS = "Table " + str(tnumI) + " - " + lineS
            # rst
            lrS = "\n" + "Table " + fillS + ": " + lineS

            # print("***sympy***", f"{luS=}", f"{lrS=}")
            return luS, lrS

        elif tagS == "[I]]":
            """ italic indent block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + lineS
            lrS = "\n" + "Table " + fillS + ": " + lineS

            # print("***sympy***", f"{luS=}", f"{lrS=}")
            return luS, lrS

        elif tagS == "[L]]":
            """ literal block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + lineS
            lrS = "\n" + "Table " + fillS + ": " + lineS

            # print("***sympy***", f"{luS=}", f"{lrS=}")
            return luS, lrS

        elif tagS == "[O]]":
            """ code block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + lineS
            lrS = "\n" + "Table " + fillS + ": " + lineS

            # print("***sympy***", f"{luS=}", f"{lrS=}")
            return luS, lrS

        elif tagS == "[N]]":
            """ indent block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + lineS
            lrS = "\n" + "Table " + fillS + ": " + lineS

            # print("***sympy***", f"{luS=}", f"{lrS=}")
            return luS, lrS

        elif tagS == "[X]]":
            """ latex block """
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            # utf
            luS = "Table " + str(tnumI) + " - " + lineS
            # rst
            lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

            return luS, lrS

        elif tagS == "[V]]":
            """ values block """
            vnumI = int(self.labelD["valueI"])
            self.labelD["valueI"] = vnumI + 1
            fillS = str(vnumI).zfill(2)
            uS = "\nValue Table " + str(vnumI) + ": " + blockL[0]
            rS = "\n**Value Table " + fillS + "**: " + blockL[0]
            xS = "\n**Value Table " + fillS + "**: " + blockL[0]
            tbL = []

            # print(f"{blockL=}")
            for vaS in blockL[1:]:
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
                        exec(eqS, globals(), self.rivtD)
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
                    exec(cmdS, globals(), self.rivtD)
                    valU = eval(varS)
                    val1U = str(valU)
                    val2U = str(valU)
                tbL.append([varS, val1U, val2U, descripS])
                self.rivtD[varS] = valS, unit1S, unit2S, dec1S, dec2S

            for vaS in blockL:
                vaL = vaS.split("|")
                if len(vaL) != 4 or len(vaL[0]) < 1:
                    continue
                if "=" not in vaL[0]:
                    continue
                iS = ",".join(vaL)
                self.labelD["valexpS"] += iS + "\n"

            # export value file
            with open(self.folderD["valP"], "w") as file:
                file.write(self.labelD["valexpS"])

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
            uS = rS = xS = output.getvalue()
            sys.stdout = old_stdout
            sys.stdout.flush()

            return uS + "\n", rS + "\n", xS + "\n"

        else:
            pass
