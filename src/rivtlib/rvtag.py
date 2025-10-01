#
"""_summary_

Returns:
    _type_: _description_
"""

import textwrap

import sympy as sp
import tabulate
from numpy import *  # noqa: F403
from sympy.abc import _clash2

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """formats a line or block

    Methods:
        taglx(tagS): formats line
        tagbx(tagS): formats block
    """

    def __init__(self, foldD, lablD, rivD, rivL, strLS):
        """tag object
        Args:
            foldD (dict): folder dictionary
            lablD (dict): label dictionary
            rivD (dict): values dictionary
            rivL (list): values list for export
            strLS (str): string to format
        Vars:
            uS (str): utf string
            rS (str): rst2pdf string
            xS (str): reST string
        """
        # region
        self.foldD = foldD
        self.lablD = lablD
        self.rivD = rivD
        self.rivL = rivL
        self.strLS = strLS
        self.uS = ""
        self.rS = ""
        self.xS = ""
        # endregion

    def taglx(self, tagS):
        """format line
        text        _[C]    center
        text        _[B]    bold center
        text        _[D]    footnote description
        label       _[E]    equation label and number
        caption     _[F]    figure caption and number
        text        _[N]    number footnote
        text        _[R]    right justify
        equation    _[S]    sympy
        title       _[T]    table title and number
        url, label  _[U]    url
        equation    _[Y]    sympy with equation number
        ------  =>  _[H]    horizontal line (6 -- min.)
        ======  =>  _[P]    new page (6 == min.)
        Args:
            tagS (str): tag symbol
        Returns:
            uS, r2S, rS, foldD, lablD, rivD, rivL
        """
        # region
        cmdS = "l" + tagS[0]
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )
        # endregion

    def tagbx(self, tagS):
        """formats a block
        _[[B]]              bold indent
        _[[I]]              italic indent
        _[[C]] language     literal
        _[[L]]              LaTeX
        _[[N]]              indent
        _[[T]] label        topic
        _[[Q]]              quit
        Args:
            tagS (str): tag symbol
        Returns:
            uS, r2S, rS, foldD, lablD, rivD, rivL
        """
        # region
        self.blockL = self.strLS.split("\n")
        cmdS = "b" + tagS[1]
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )
        # endregion

    def lC(self):
        """center text"""
        # region
        lineS = self.strLS
        self.uS = lineS.center(int(self.lablD["widthI"])) + "\n"
        self.rS = lineS.center(int(self.lablD["widthI"])) + "\n"
        self.xS = "\n::\n\n" + lineS.center(int(self.lablD["widthI"])) + "\n"
        # endregion

    def lD(self):
        """footnote description"""
        # region
        lineS = self.strLS
        ftnumI = self.lablD["noteL"].pop(0)
        self.uS = "[" + str(ftnumI) + "] " + lineS
        self.rS = "[" + str(ftnumI) + "] " + lineS
        self.xS = "[" + str(ftnumI) + "] " + lineS
        # endregion

    def lE(self):
        """number equation"""
        # region
        lineS = self.strLS
        enumI = int(self.lablD["equI"])
        self.lablD["equI"] = enumI + 1
        fillS = "\n" + "Eq. " + str(enumI)
        self.uS = fillS + " - " + lineS
        fillS = "**Eq " + str(enumI) + "**"
        self.rS = lineS + " - " + fillS + "\n"
        self.xS = lineS + " - " + fillS + "\n"
        # endregion

    def lF(self):
        """number figure"""
        # region
        lineS = self.strLS
        fnumI = int(self.lablD["figI"])
        self.lablD["figI"] = fnumI + 1
        self.uS = "Fig. " + str(fnumI) + " - " + lineS + "\n"
        self.rS = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        self.xS = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        # endregion

    def lN(self):
        """number footnote"""
        # region
        lineS = self.strLS
        ftnumI = self.lablD["footL"].pop(0)
        self.lablD["noteL"].append(ftnumI + 1)
        self.lablD["footL"].append(ftnumI + 1)
        self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.xS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        # endregion

    def lS(self):
        """format sympy"""
        # region
        lineS = self.strLS
        spS = lineS.strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        self.uS = textwrap.indent(lineS, "     ")
        self.rS = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.xS = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lT(self):
        """number table"""
        # region
        lineS = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.rS = "\n**Table " + fillS + "**: " + lineS
        self.xS = "\n**Table " + fillS + "**: " + lineS
        # endregion

    def lU(self):
        "format url link"
        # region
        lineS = self.strLS
        lineL = lineS.split(",")
        self.uS = lineL[0] + ": " + lineL[1]
        self.rS = ".. _" + lineL[0] + ": " + lineL[1]
        self.xS = ".. _" + lineL[0] + ": " + lineL[1]
        # endregion

    def lY(self):
        "format and number sympy"
        # region
        lineS = self.strLS
        spS = lineS.strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        self.uS = textwrap.indent(lineS, "     ")
        self.rS = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.xS = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lH(self):
        "horizontal line"
        # region
        self.uS = "-" * 80
        self.rS = "-" * 80
        self.xS = "-" * 80
        # endregion

    def lP(self):
        "new page"
        # region
        pgnS = str(self.lablD["pageI"])
        self.uS = (
            "\n"
            + "=" * (int(self.lablD["widthI"]) - 10)
            + " Page "
            + pgnS
            + "\n"
        )
        # self.uS = self.lablD["headuS"].replace("p##", pagenoS)
        self.lablD["pageI"] = int(pgnS) + 1
        self.rS = (
            "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
        )
        self.xS = (
            "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
        )
        # endregion

    def bB(self):
        """bold-indent block"""
        # region
        blockL = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        self.uS = "Table " + str(tnumI) + " - " + blockS
        self.rS = "\n" + "Table " + fillS + ": " + blockS
        self.xS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bC(self):
        """code-literal block"""
        # region
        blockL = self.strLS
        iS = ""
        for s in blockL:
            s = "    " + s + "\n"
            iS += s

        uS = r2S = rS = iS
        # endregion

    def bI(self):
        """italic-indent block"""
        # region
        print("IIII")
        # endregion

    def bL(self):
        """literal block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bS(self):
        """indent block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bX(self):
        """latex block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "**" + "Table " + fillS + ": " + blockS
        # endregion
