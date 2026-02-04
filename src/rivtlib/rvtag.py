import textwrap

import sympy as sp
import tabulate
from fastcore.utils import store_attr
from numpy import *  # noqa: F403
from sympy.abc import _clash2

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """formats lines and blocks of text

    Methods:
        taglx(tagS): formats line
        tagbx(tagS): formats block
    """

    def __init__(self, foldD, lablD, rivD, rivL, strLS):
        """tags object

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
        store_attr()
        self.uS = ""
        self.r2S = ""
        self.rS = ""
        # endregion

    def taglx(self, tagS):
        """formats a line

         API         Syntax                    Description (output types)
        ------- -------------------------- ----------------------------------------
         I         text _[C]                  center text (all)
         I         text _[R]                  right justify text (all)
         I         math _[M]                  format ASCII math (all)
         I         math _[L]                  format LaTeX math (all)
         I         text _[#] text             endnote number (all)
         I         text _[G] term to link     link term to glossary (all)
         I         text _[S] section link     link to section in doc (all)
         I, V      text _[D] report link      link to doc in report (all)
         I, V      text _[U] external url     external url link (all)
         I, V     label _[E]                  equation number and label (all)
         I, V     label _[I]                  image number and label (all)
         I, V     title _[T]                  table number and title (all)
         all      text  _[P]                  new page (rlabpdf, texpdf)

         Args:
             tagS (str):  last two characers of tag symbol
         Returns:
             uS, r2S, rS, foldD, lablD, rivD, rivL
        """

        # region
        cmdS = "l" + tagS[0]
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.r2S,
            self.rS,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )
        # endregion

    def tagbx(self, tagS):
        """formats a block

         API         Syntax                    Description (output types)
        ------- -------------------------- ----------------------------------------
        R        _[[SHELL]] label, *wait;nowait*         Windows command script (all)
        I, V     _[[INDENT]] spaces (4 default)          Indent (all)
        I, V     _[[ITALIC]] spaces (4 default)          Italic indent  (all)
        I, V     _[[ENDNOTES]] optional label            Endnote descriptions (all)
        I, V     _[[TEXT]] optional language             *literal*, code (all)
        I, V     _[[TOPIC]] topic                        Topic (all)
        T        _[[PYTHON]] label, *rvspace*;newspace   Python script (all)
        T        _[[MARKUP]] label                       LaTeX markup (pdf)[1]
        D        _[[LAYOUT]] label                       Doc format settings (all)
        all      _[[END]]                                End block (all)

        Args:
            tagS (str): characters of tag symbol with leading "_[" stripped
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
            self.r2S,
            self.rS,
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
        self.r2S = "\n.. class:: align-center\n\n   " + lineS + "\n\n"
        self.rS = "\n.. class:: align-center\n\n   " + lineS + "\n\n"
        # endregion

    def lR(self):
        """right justify text"""
        # region
        lineS = self.strLS
        self.uS = lineS.center(int(self.lablD["widthI"])) + "\n"
        self.r2S = lineS.center(int(self.lablD["widthI"])) + "\n"
        self.rS = "\n::\n\n" + lineS.center(int(self.lablD["widthI"])) + "\n"
        # endregion

    def lN(self):
        """number footnote"""
        # region
        lineS = self.strLS
        ftnumI = self.lablD["footL"].pop(0)
        self.lablD["noteL"].append(ftnumI + 1)
        self.lablD["footL"].append(ftnumI + 1)
        self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.r2S = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        # endregion

    def lM(self):
        """format sympy"""
        # region
        lineS = self.strLS
        spS = lineS.strip()
        spL = spS.split("=")
        spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        indlineS = textwrap.indent(lineS, "     ")
        self.uS = lineS + "\n"
        self.r2S = "\n\n.. code:: \n\n\n" + indlineS + "\n\n"
        self.rS = ".. code:: \n\n   " + indlineS + "\n\n"
        # endregion

    def lU(self):
        "format url link"
        # region
        lineS = self.strLS
        lineL = lineS.split(",")
        self.uS = lineL[0] + ": " + lineL[1]
        self.r2S = ".. _" + lineL[0] + ": " + lineL[1]
        self.rS = ".. _" + lineL[0] + ": " + lineL[1]
        # endregion

    def lT(self):
        """number table"""
        # region
        lineS = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
        self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"
        # endregion

    def lI(self):
        """number image"""
        # region
        lineS = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
        self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"
        # endregion

    def lE(self):
        """number equation"""
        # region
        lineS = self.strLS
        enumI = int(self.lablD["equI"])
        self.lablD["equI"] = enumI + 1
        fillS = " **[Eq " + str(enumI) + "]**"
        refS = lineS + fillS
        self.uS = lineS + " [Eq " + str(enumI) + "]".rjust(self.lablD["widthI"])
        self.uS += "\n"
        self.r2S = "\n.. class:: align-right\n\n   " + refS + "\n\n\n"
        self.rS = (
            ".. raw:: html\n\n" + '   <p align="right">' + refS + "</p> \n\n"
        )
        # endregion

    def bB(self):
        """bold-indent block"""
        # region
        blockL = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        self.uS = "Table " + str(tnumI) + " - " + blockS
        self.r2S = "\n" + "Table " + fillS + ": " + blockS
        self.rS = "\n" + "Table " + fillS + ": " + blockS
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

    def bP(self):
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
        self.r2S = (
            "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
        )
        self.rS = (
            "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
        )
        # endregion
