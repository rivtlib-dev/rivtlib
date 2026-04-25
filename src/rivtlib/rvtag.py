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
        store_attr()
        sp.init_printing()
        self.uS = ""
        self.r2S = ""
        self.rS = ""

    def taglx(self, tagS):
        """formats a line

         API         Syntax                    Description (output types)
        ------- -------------------------------- -----------------------------------
         I         text _[C]                      center text (all)
         I         text _[R]                      right justify text (all)
         I         math _[M]                      format ASCII math (all)
         I         math _[L]                      format LaTeX math (all)
         I         text _[#] text                 insert and format endnote (all)
         I, V      text _[G] term link    | text  link term to glossary (all)
         I, V      text _[S] section link | text  link to section in report (all)
         I, V      text _[U] external url | text  external url link (all)
         I, V     label _[E]                      equation number and label (all)
         I, V     label _[I]                      image number and label (all)
         I, V     title _[T]                      table number and title (all)
         all      text  _[P]                      new page (rlabpdf, texpdf)

         Args:
             tagS (str):  last two characers of tag symbol
         Returns:
             uS, r2S, rS, foldD, lablD, rivD, rivL
        """
        cmdS = "l" + tagS[0]
        wI = int(self.lablD["widthI"])
        lineS = self.strLS
        # region
        if cmdS == "lP":
            """insert new page"""
            pass

        elif cmdS == "lT":
            """number table"""

            tnumI = int(self.lablD["tableI"])
            self.lablD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lI":
            """number image"""

            tnumI = int(self.lablD["tableI"])
            self.lablD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lE":
            """number equation"""

            enumI = int(self.lablD["equI"])
            self.lablD["equI"] = enumI + 1
            fillS = " [Eq " + str(enumI) + "]"
            refS = lineS + fillS
            self.uS = (lineS + " [Eq " + str(enumI) + "]").rjust(
                self.lablD["widthI"]
            )
            fillS = " **[Eq " + str(enumI) + "]**"
            refS = lineS + fillS
            self.uS += "\n"
            self.r2S = "\n.. rst-class:: align-right\n\n" + refS + "\n\n"
            self.rS = "\n.. rst-class:: align-right\n\n" + refS + "\n\n"
            # self.rS = (".. raw:: html\n\n" + '   <p align="right">' + refS + "</p> \n\n")

        elif cmdS == "lC":
            """center text"""

            self.uS = lineS.center(wI) + "\n"
            self.r2S = "\n.. class:: align-center\n\n   " + lineS + "\n\n"
            self.rS = "\n.. class:: align-center\n\n   " + lineS + "\n\n"

        elif cmdS == "lR":
            """right justify text"""

            self.uS = lineS.center(wI) + "\n"
            self.r2S = lineS.center(wI) + "\n"
            self.rS = "\n::\n\n" + lineS.center(wI) + "\n"

        elif cmdS == "lM":
            """format sympy"""

            spS = lineS.strip()
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            indlineS = textwrap.indent(lineS, "     ")
            self.uS = indlineS + "\n"
            self.r2S = "\n.. code:: \n\n" + indlineS + "\n\n"
            self.rS = "\n.. code:: \n\n" + indlineS + "\n\n"

        elif cmdS == "lU":
            """format url link"""

            lineL = lineS.split(",")
            self.uS = lineL[0] + ": " + lineL[1]
            self.r2S = ".. _" + lineL[0] + ": " + lineL[1]
            self.rS = ".. _" + lineL[0] + ": " + lineL[1]

        elif cmdS == "l#":
            """number footnoate"""
            ftnumI = self.lablD["footL"].pop(0)
            self.lablD["noteL"].append(ftnumI + 1)
            self.lablD["footL"].append(ftnumI + 1)
            self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.r2S = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")

        else:
            pass

        return (
            self.uS,
            self.r2S,
            self.rS,
            self.foldD,
            self.lablD,
            self.rivD,
            self.rivL,
        )

    def tagbx(self, tagS):
        """formats a block

         API         Syntax                               Description (output types)
        ------- -------------------------------------- -------------------------------------
        R        _[[SHELL]] label, [wait;nowait]         Windows command script (all)
        I        _[[INDENT]] spaces (4 default)          Indent (all)
        I        _[[ITALIC]] spaces (4 default)          Italic indent  (all)
        I        _[[ENDNOTES]] optional label            Endnote descriptions (all)
        I        _[[TABLE]] optional label               Format table and store csv (all)             *literal*, code (all)
        I        _[[TEXT]] optional language             literal; code type (all)
        I        _[[TOPIC]] topic label                  Topic box (all)
        V,T      _[[PYTHON]] label, [rv];my_space        Python script (all)
        T        _[[MARKUP]] type                        Markup snippet (pdf)
        D        _[[METADATA]] label                     Meta and layout data (all)
        all      _[[END]]                                End block (all)

        Args:
            tagS (str): characters of tag symbol with leading "_[" stripped
        Returns:
            uS, r2S, rS, foldD, lablD, rivD, rivL
        """
        # region
        lineS = self.strLS
        self.blockL = (self.strLS).split("\n")
        cmdS = "b" + tagS[1:4]
        wI = int(self.lablD["widthI"])

        if cmdS == "END":
            """end block"""
            pass

        elif cmdS == "lT":
            """number table"""

            tnumI = int(self.lablD["tableI"])
            self.lablD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

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

    def bL(self):
        """literal block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bI(self):
        """italic-indent block"""
        # region
        print("IIII")
        # endregion

    def bS(self):
        """indent block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
        # endregion

    def bT(self):
        """table block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "Table " + fillS + ": " + blockS
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

    def bX(self):
        """latex block"""
        # region
        tnumI = int(self.lablD["tableI"])
        self.lablD["tableI"] = tnumI + 1
        luS = "Table " + str(tnumI) + " - " + blockS
        lrS = "\n" + "**" + "Table " + fillS + ": " + blockS
        # endregion

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
