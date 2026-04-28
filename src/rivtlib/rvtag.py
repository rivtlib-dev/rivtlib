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

    def __init__(self, fD, lD, rivD, rivL, strLS):
        """tags object

        Args:
            fD (dict): fDer dictionary
            lD (dict): label dictionary
            rivD (dict): values dictionary
            rivL (list): values list for export
            strLS (str): line or block string to format
        Vars:
            uS (str): utf string
            rS (str): rst string

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
         I, V, T  label _[E]                      equation number and label (all)
         I, V, T  label _[I]                      image number and label (all)
         I, V, T  title _[T]                      table number and title (all)
         all      text  _[P]                      new page (rlabpdf, texpdf)

         Args:
             tagS (str):  last two characers of tag symbol
         Returns:
             uS, r2S, rS, fD, lD, rivD, rivL
        """
        cmdS = "l" + tagS[0]
        wI = int(self.lD["widthI"])
        lineS = self.strLS
        # region
        if cmdS == "lP":
            """insert new page"""
            pass

        elif cmdS == "lT":
            """number table"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lI":
            """number image"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lE":
            """number equation"""

            enumI = int(self.lD["equI"])
            self.lD["equI"] = enumI + 1
            fillS = " [Eq " + str(enumI) + "]"
            refS = lineS + fillS
            self.uS = (lineS + " [Eq " + str(enumI) + "]").rjust(
                self.lD["widthI"]
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
            ftnumI = self.lD["footL"].pop(0)
            self.lD["noteL"].append(ftnumI + 1)
            self.lD["footL"].append(ftnumI + 1)
            self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.r2S = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")

        elif cmdS == "lP":
            "new page"
            # region
            pgnS = str(self.lD["pageI"])
            self.uS = (
                "\n"
                + "=" * (int(self.lD["widthI"]) - 10)
                + " Page "
                + pgnS
                + "\n"
            )
            # self.uS = self.lD["headuS"].replace("p##", pagenoS)
            self.lD["pageI"] = int(pgnS) + 1
            self.r2S = (
                "\n"
                + "_" * self.lD["widthI"]
                + "\n"
                + self.uS
                + "\n"
                + "_" * self.lD["widthI"]
                + "\n"
            )
            self.rS = (
                "\n"
                + "_" * self.lD["widthI"]
                + "\n"
                + self.uS
                + "\n"
                + "_" * self.lD["widthI"]
                + "\n"
            )
            # endregion

        else:
            pass

        return (
            self.uS,
            self.r2S,
            self.rS,
            self.fD,
            self.lD,
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
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        blockS = self.strLS
        blockL = (self.strLS).split("\n")
        cmdS = "b" + tagS[0:3]
        wI = int(self.lD["widthI"])

        if cmdS == "bSHE":
            """shell command"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "bTEX":
            """code-literal block"""
            # region
            blockL = self.strLS
            iS = ""
            for s in blockL:
                s = "    " + s + "\n"
                iS += s

            uS = r2S = rS = iS
            # endregion

        elif cmdS == "bITA":
            """italic-indent block"""
            # region
            print("IIII")
            # endregion

        elif cmdS == "bIND":
            """indent block"""
            # region
            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + blockS
            lrS = "\n" + "Table " + fillS + ": " + blockS
            # endregion

        elif cmdS == "bTAB":
            """table block"""
            # region
            blkL = (self.strLS).split("\n", 1)
            titleS = blkL[0].strip()
            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "Table " + str(tnumI) + ": " + titleS + "\n" + blkL[1]
            self.r2S = (
                "**Table " + str(tnumI) + "**: " + titleS + "\n\n" + blkL[1]
            )
            self.rS = (
                "**Table " + str(tnumI) + "**: " + titleS + "\n\n" + blkL[1]
            )
            # endregion

        elif cmdS == "bLAT":
            """latex block"""
            # region
            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            luS = "Table " + str(tnumI) + " - " + blockS
            lrS = "\n" + "**" + "Table " + fillS + ": " + blockS
            # endregion

        return (
            self.uS,
            self.r2S,
            self.rS,
            self.fD,
            self.lD,
            self.rivD,
            self.rivL,
        )
        # endregion
