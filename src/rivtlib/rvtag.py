import csv
import textwrap
from pathlib import Path

import docutils.parsers.rst.tableparser
import docutils.statemachine
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

    def __init__(self, fD, lD, rivD, rivL, strL):
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
        sp.init_printing(use_unicode=True)
        # sp.init_printing()
        self.strL = strL
        self.fD = fD
        self.lD = lD
        self.rivD = rivD
        self.rivL = rivL

    def taglx(self, tagS):
        """formats a line

         API         Syntax                         Description (output types)
        ------- --------------------------------- -----------------------------------
         I          **text text**                   bold words
         I           *text text*                    italic words
         I,V      text  _[C]                        bold center text (all)
         I,V      text  _[R]                        right justify text (all)
         I,V      text  _[B]                        bold text (all)
         I,V      math  _[M]                        format ASCII math (all)
         I,V      math  _[X]                        format LaTeX math (all)
         I,V      label _[F]                        figure number and label (all)
         I,V      title _[T]                        table number and title (all)
         I,V      text  _[P]                        new page (pdf)
         I,V      text  _[#] text                   number endnote (all)
         I,V      text  _[V] var_name ] text        variable substitution (all)
         I,V      text  _[G] term link ] text       link term to glossary (all)
         I,V      text  _[S] section link ] text    link to section in report (all)
         I,V      text  _[U] external link ] text   external url link (all)
         all      ## text                           non-printing comment

         Args:
             tagS (str):  last two characers of tag symbol
         Returns:
             uS, r2S, rS, fD, lD, rivD, rivL
        """
        cmdS = "l" + tagS[0]
        wI = int(self.lD["widthI"])
        lineS = self.strL[0].strip()
        lineL = self.strL
        # region

        if cmdS == "lP":
            """new page"""

            uS = tS = lineS + "\n"
            rS = "\n.. raw:: pdf\n\n   " + "PageBreak" + "\n\n"
            lS = "\n.. raw:: pdf\n\n   " + "PageBreak" + "\n\n"

        elif cmdS == "lC":
            """center text"""

            uS = tS = lineS.center(wI) + "\n"
            rS = "\n.. rst-class:: align-center\n\n**" + lineS + "**\n\n"
            lS = "\n.. rst-class:: align-center\n\n**" + lineS + "**\n\n"

        elif cmdS == "lR":
            """right justify text"""

            uS = tS = lineS.rjust(wI) + "\n"
            rS += "\n.. rst-class:: align-right\n\n   " + lineS + "\n"
            lS = ""

        if cmdS == "lB":
            """bold text"""

            uS = tS = lineS + "\n"
            rS = lS = "**" + lineS + "**" + "\n"

        if cmdS == "lI":
            """italic text"""

            uS = tS = lineS + "\n"
            rS = lS = "*" + lineS + "*" + "\n"

        elif cmdS == "lM":
            """format sympy"""

            self.enumI = int(self.lD["equI"])
            self.enumI += 1
            self.lD["equI"] = self.enumI
            self.enumS = str(self.enumI)
            spS = lineL[0].strip()
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            # text
            eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
            toptS = chr(9484) + "  Eq-" + self.enumS + " | " + lineL[1] + "\n"
            eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
            # rest
            spS = "\n|\n\n"
            eq1S = textwrap.indent(eq1S, "           ")
            erS = "\n**Eq." + self.enumS + "**\n"
            eqrS = spS + erS + "\n.. code-block:: text \n\n" + eq1S + "\n\n"
            uS = tS = eqtS + "\n"
            rS = eqrS + "\n\n"
            lS = ""

        elif cmdS == "lT":
            """number table"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            uS = tS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS + "\n"
            lS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lF":
            """number figure"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            uS = tS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS + "\n"
            lS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "lL":
            """format latex"""

            spS = lineS.strip()
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            indlineS = textwrap.indent(lineS, "     ")
            uS = tS = indlineS + "\n"
            rS = "\n.. code:: \n\n" + indlineS + "\n\n"
            lS = "\n.. code:: \n\n" + indlineS + "\n\n"

        elif cmdS == "lG":
            """format glossary term link"""

            lineL = lineS.split(",")
            uS = tS = lineL[0] + ": " + lineL[1]
            rS = ".. _" + lineL[0] + ": " + lineL[1]
            lS = ".. _" + lineL[0] + ": " + lineL[1]

        elif cmdS == "lS":
            """format section link"""

            lineL = lineS.split(",")
            uS = tS = lineL[0] + ": " + lineL[1]
            rS = ".. _" + lineL[0] + ": " + lineL[1]
            lS = ".. _" + lineL[0] + ": " + lineL[1]

        elif cmdS == "lU":
            """format url link"""

            uS = tS = " ".join(lineL[1:]).strip()
            txL = lineL[1].split(",")
            rS = "`" + txL[0].strip() + " <" + txL[1].strip() + ">`_" + lineL[2]
            lS = "`" + txL[0].strip() + " <" + txL[1].strip() + ">`_" + lineL[2]

        elif cmdS == "l#":
            """number footnote"""
            ftnumI = self.lD["footL"].pop(0)
            self.lD["noteL"].append(ftnumI + 1)
            self.lD["footL"].append(ftnumI + 1)
            self.uS = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.r2S = lineS.replace("*]", "[" + str(ftnumI) + "]")
            self.rS = lineS.replace("*]", "[" + str(ftnumI) + "]")

        else:
            pass

        # endregion

        mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
        }

        return mD, self.lD

    def tagbx(self, tagS):
        """formats a block

         API         Syntax                               Description (output types)
        --------- -------------------------------------- -------------------------------------
        R          _[[SHELL]] type, *wait;nowait*          command script (all)
        I          _[[TOPIC]] topic label                  topic box (all)
        I          _[[BOX]] optional label                 box (all)
        V          _[[TABLE]] title                        format table, store csv (all)
        T          _[[MARKUP]] type                        markup (all)
        D          _[[METADATA]] label                     meta and layout data (all)
        all        _[[END]]                                end block (all)

        Args:
            tagS (str): characters of tag symbol with leading "_[" stripped
        Returns:
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        cmdS = "b" + tagS[0:3]
        wI = int(self.lD["widthI"])

        if cmdS == "bSHE":
            """shell blocki"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "bTAB":
            """table block"""
            # region
            blkL = (self.strL).split("\n", 1)
            titleS = blkL[0].strip()
            tnumI = int(self.lD["tableI"])
            fileS = "t" + self.lD["docnumS"][2:] + str(tnumI) + ".csv"
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            spS = "\n|\n\n"
            uS = tS = "Table " + str(tnumI) + ": " + titleS + "\n" + blkL[1]
            rS = f"""{spS}**Table {str(tnumI)}**: {titleS} \n\n{blkL[1]}"""
            lS = "**Table " + str(tnumI) + "**: " + titleS + "\n\n" + blkL[1]

            hdatS, bdatS = self.parse_simple_rst_table(blkL[1])
            rstL = hdatS + bdatS
            pathP = Path(self.fD["storeP"], fileS)
            with open(str(pathP), mode="w", newline="") as f1:
                wfile = csv.writer(f1)
                wfile.writerows(rstL)

        elif cmdS == "bMAR":
            """markup block"""
            # region
            blkL = (self.strL).split("\n", 1)
            titleS = blkL[0].strip()
            tnumI = int(self.mD["lD"]["tableI"])
            self.mD["lD"]["tableI"] = tnumI + 1
            fillS = str(tnumI)
            uS = "Table " + str(tnumI) + ": " + titleS + "\n" + blkL[1]
            rS = "**Table " + str(tnumI) + "**: " + titleS + "\n\n" + blkL[1]
            tS = "**Table " + str(tnumI) + "**: " + titleS + "\n\n" + blkL[1]
            lS = ""
            # endregion

        elif cmdS == "bPYT":
            """Python block"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "bTOP":
            """topics block"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        elif cmdS == "bBOX":
            """box block"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"

        else:
            pass

        mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
        }

        return mD, self.lD

    def parse_simple_rst_table(self, table_text):
        # Prepare the input for docutils
        lines = docutils.statemachine.StringList(
            table_text.strip().splitlines()
        )

        # Initialize the parser
        parser = docutils.parsers.rst.tableparser.SimpleTableParser()

        # Parse into a tuple: (column_widths, header_rows, body_rows)
        # The header and body rows are lists of cells (each cell is a list of lines)
        col_widths, headers, body = parser.parse(lines)

        # helper to clean up cell content
        clean = lambda cell: " ".join(line.strip() for line in cell[3]).strip()

        # Process headers
        header_data = [[clean(cell) for cell in row] for row in headers]

        # Process body
        body_data = [[clean(cell) for cell in row] for row in body]

        return header_data, body_data
