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
        self.r2s = ""
        # endregion

    def taglx(self, tagS):
        """formats a line

         API         Syntax                    Description
        ------- -------------------------- ----------------------------------------
         I, V      text _[#]  text            endnote number (all)
         I, V      text _[C]                  center text (all)
         I, V      text _[R]                  right justify text (all)
         I, V     label _[E]                  equation number and label (all)
         I, V   caption _[I]                  image number and caption (all)[1]
         I, V     title _[T]                  table number and title (all)[1]
         I, V      text _[G] term to link     link term to glossary (all)
         I, V      text _[S] section link     link to section in doc (all)
         I, V      text _[D] report link      link to doc in report (all)
         I, V      text _[U] external url     external url link (all)
         I, V      \-\-\-\-\-                 >4 dashes inserts line (all)[2]
         I, V      \=\=\=\=\=                 >4 underscores inserts page (all)[2]
         I         math _[L]                  format LaTeX math (all)
         I         math _[A]                  format ASCII math (all)

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
            self.r2s,
            self.r2s,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )
        # endregion

    def tagbx(self, tagS):
        """formats a block

         API         Syntax                    Description
        ------- -------------------------- ----------------------------------------
        R        _[[WIN]] label, *wait;nowait*           Windows command script (all)
        R        _[[MACOS]] label, *wait;nowait*         Mac shell script (all)
        R        _[[LINUX]] label, *wait;nowait*         Linux shell script (all)
        I, V     _[[INDENT]] spaces (4 default)          Indent (all)
        I, V     _[[ITALIC]] spaces (4 default)          Italic indent - (all)
        I, V     _[[ENDNOTES]] optional label            Endnote descriptions (all)
        I, V     _[[TEXT]] optional language             *literal*, code (all)
        I, V     _[[TOPIC]] topic                        Topic (all)
        T        _[[PYTHON]] label, *rvspace*;newspace   Python script (all)
        T        _[[LATEX]] label                        LaTeX markup (pdf)[1]
        T        _[[HTML]] label                         HTML markup (html)
        T        _[[RST]] label                          reStructuredText markup (all)
        D        _[[LAYOUT]] label                       Doc format settings (all)
        ALL      _[[END]]                                End block (all)

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
            self.r2s,
            self.r2s,
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
        self.r2s = lineS.center(int(self.lablD["widthI"])) + "\n"
        self.r2s = "\n::\n\n" + lineS.center(int(self.lablD["widthI"])) + "\n"
        # endregion

    def lD(self):
        """footnote description"""
        # region
        lineS = self.strLS
        ftnumI = self.lablD["noteL"].pop(0)
        self.uS = "[" + str(ftnumI) + "] " + lineS
        self.r2s = "[" + str(ftnumI) + "] " + lineS
        self.r2s = "[" + str(ftnumI) + "] " + lineS
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
        self.r2s = lineS + " - " + fillS + "\n"
        self.r2s = lineS + " - " + fillS + "\n"
        # endregion

    def lF(self):
        """number figure"""
        # region
        lineS = self.strLS
        fnumI = int(self.lablD["figI"])
        self.lablD["figI"] = fnumI + 1
        self.uS = "Fig. " + str(fnumI) + " - " + lineS + "\n"
        self.r2s = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        self.r2s = "**Fig. " + str(fnumI) + " -** " + lineS + "\n"
        # endregion

    def lN(self):
        """number footnote"""
        # region
        lineS = self.strLS
        ftnumI = self.lablD["footL"].pop(0)
        self.lablD["noteL"].append(ftnumI + 1)
        self.lablD["footL"].append(ftnumI + 1)
        self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.r2s = lineS.replace("*]", "[" + str(ftnumI) + "]")
        self.r2s = lineS.replace("*]", "[" + str(ftnumI) + "]")
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
        self.r2s = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.r2s = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lT(self):
        """number table"""
        # region
        lineS = self.strLS
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        self.uS = "\nTable " + str(tnumI) + ": " + lineS
        self.r2s = "\n**Table " + fillS + "**: " + lineS
        self.r2s = "\n**Table " + fillS + "**: " + lineS
        # endregion

    def lU(self):
        "format url link"
        # region
        lineS = self.strLS
        lineL = lineS.split(",")
        self.uS = lineL[0] + ": " + lineL[1]
        self.r2s = ".. _" + lineL[0] + ": " + lineL[1]
        self.r2s = ".. _" + lineL[0] + ": " + lineL[1]
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
        self.r2s = "\n\n.. code:: \n\n\n" + self.uS + "\n\n"
        self.r2s = ".. raw:: math\n\n   " + lineS + "\n"
        # endregion

    def lH(self):
        "horizontal line"
        # region
        self.uS = "-" * 80
        self.r2s = "-" * 80
        self.r2s = "-" * 80
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
        self.r2s = (
            "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
            + self.uS
            + "\n"
            + "_" * self.lablD["widthI"]
            + "\n"
        )
        self.r2s = (
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
        self.r2s = "\n" + "Table " + fillS + ": " + blockS
        self.r2s = "\n" + "Table " + fillS + ": " + blockS
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
