#
import logging
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

    Function Name list:

    _[C]     center
    _[D]     descrip
    _[E]     equation
    _[#]     foot
    _[F]     figure
    _[S]     sympy
    _[L]     sympy label
    _[T]     table
    _[H]     hline
    _[P]     page
    _[U]     url
     :=      equals
    color _[[B]]   bldindblk
    color _[[C]]   codeblk
    color _[[I]]   italindblk
    color _[[L]]   literalblock
    color _[[X]]   latexblk
    title _[[V]]   valuesblk
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

        if self.tS == "V":
        with open(folderD["valP"], "w") as file:  # export value file
            file.write(labelD["valexpS"])


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

    def linetags(self, tagS, lineS):
        """ """

        if tagS == "C]":
            """ center line """

            uS = lineS.center(int(self.labelD["widthI"])) + "\n"
            rS = lineS.center(int(self.labelD["widthI"])) + "\n"
            tS = "\n::\n\n" + lineS.center(int(self.labelD["widthI"])) + "\n"

            return uS, rS, tS

        elif tagS == "D]":
            """ footnote description"""
            ftnumI = self.labelD["noteL"].pop(0)

            uS, rS, tS = "[" + str(ftnumI) + "] " + lineS

            return uS, rS, tS

        elif tagS == "E]":
            """ equation label """
            enumI = int(self.labelD["equI"])
            self.labelD["equI"] = enumI + 1
            wI = self.labelD["widthI"]
            fillS = "\nE" + str(enumI).zfill(2)

            uS = fillS + " - " + lineS + "\n"
            fillS = "\n**E" + str(enumI).zfill(2) + "** - "
            rS = fillS + "   " + lineS + "\n"
            tS = uS

            return uS, rS, tS

        elif tagS == "F]":
            """ figure caption"""
            fnumI = int(self.labelD["figI"])
            self.labelD["figI"] = fnumI + 1

            uS = rS = tS = "Fig. " + str(fnumI) + " - " + lineS + "\n"

            return uS, rS, tS

        elif tagS == "#]":
            """ footnote number """
            ftnumI = self.labelD["footL"].pop(0)
            self.labelD["noteL"].append(ftnumI + 1)
            self.labelD["footL"].append(ftnumI + 1)

            uS = rS = tS = lineS.replace("*]", "[" + str(ftnumI) + "]")

            return uS, rS, tS

        elif tagS == "S]":
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

            return uS, rS, tS

        elif tagS == "T]":
            tnumI = int(self.labelD["tableI"])
            self.labelD["tableI"] = tnumI + 1
            fillS = str(tnumI).zfill(2)
            uS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS
            tS = "\n**Table " + fillS + "**: " + lineS

            return uS, rS, tS

        elif tagS == "U]":
            lineL = self.lineS.split(",")
            lineS = ".. _" + lineL[0] + ": " + lineL[1]

            return lineS

        elif tagS == "H]":
            uS = "-" * 80
            rS = "-" * 80
            tS = "-" * 80

            return uS, rS, tS

        elif tagS == "P]":
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

    def blocktags(self, tagS, lineS):
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
            self.labelD["tableI"] = vnumI + 1
            fillS = str(vnumI).zfill(2)
            uS = "\nValue Table " + str(vnumI) + ": " + lineS
            r2S = "\n**Value Table " + fillS + "**: " + lineS
            rS = "\n**Value Table " + fillS + "**: " + lineS

            return uS, r2S

        else:
            pass
