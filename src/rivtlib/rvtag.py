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

    def __init__(self, fD, lD, rivtD, rivL, strL):
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
        self.rivtD = rivtD
        self.rivL = rivL

    def taglx(self, tagS):
        """formats a line

         API         Syntax                         Description (output types)
        ------- ---------------------------------------- --------------------------------
         I          **text text**                        bold words
         I           *text text*                         italic words
         I,V      text  _[C]                             bold center text (all)
         I,V      math  _[M]                             format ASCII math (all)
         I,V      math  _[X]                             format LaTeX math (all)
         I,V      label _[F]                             figure number and label (all)
         I,V      title _[T]                             table number and title (all)
         I,V      text  _[#] text                        number endnote (all)
         I,V      text  _[V] var_name ] text             variable substitution (all)
         I,V      text  _[G] term link ] text            link term to glossary (all)
         I,V      text  _[D] label,filename ] text       variable substitution (all)
         I,V      text  _[S] label, section link ] text  link to section in report (all)
         I,V      text  _[U] label, external link ] text external url link (all)
         all      ## text                                non-printing comment

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

        if cmdS == "lC":
            """center text"""

            uS = tS = lineS.center(wI) + "\n"
            rS = "\n.. rst-class:: align-center\n\n**" + lineS + "**\n"
            lS = "\n.. rst-class:: align-center\n\n**" + lineS + "**\n"

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
            refS = lineL[1]
            try:
                spL = spS.split("=")
                sp1S = spL[0]
            except Exception:
                sp1S = spS
            spS = "Eq(" + sp1S + ",(" + spL[1] + "))"
            eq1S = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
            # text
            eqxS = textwrap.indent(eq1S, chr(9474) + "     ")
            toptS = chr(9484) + "  Eq-" + self.enumS + " | " + lineL[1] + "\n"
            eqtS = toptS + chr(9474) + "\n" + eqxS + "\n" + chr(9492) + "\n"
            # rest
            spaS = "\n|\n"
            eq1S = textwrap.indent(eq1S, "           ")
            erS = "\n**Eq." + self.enumS + ":**" + refS + "\n"
            eqrS = spaS + erS + "\n.. code-block:: text \n\n" + eq1S + "\n\n"
            uS = tS = eqtS + "\n"
            rS = eqrS + "\n\n"
            lS = ""

        elif cmdS == "lT":
            """number table"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            uS = tS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS + "\n\n"
            lS = "\n**Table " + fillS + "**: " + lineS + "\n\n"

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
            # print(lineL)
            txt1 = lineL[0]
            txt2 = lineL[1].split("|")[0].strip()
            txt3 = lineL[1].split("|")[1].strip()
            txt2a = txt2.split(",")[0].strip()
            txt2b = "<" + txt2.split(",")[1].strip() + ">"
            uS = tS = f"{txt1} {txt2a} {txt2b} {txt3}"
            rS = lS = f"{txt1} `{txt2a} {txt2b}`__ {txt3}"

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
            tnumI = int(self.lD["tableI"])
            fileS = "t" + self.lD["docnumS"][2:] + str(tnumI) + ".csv"
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            titleS = blkL[0].strip() + " (stored: " + fileS + ")"
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
            """markup block
            
            literal
            html
            reST
            endnote
            center
            bold
            italic
            mermaid
            latex
            
            """
            # region
            blkL = (self.strL).split("\n", 1)
            marktypS = blkL[0].strip()
            if marktypS == "literal":
                txtS = blkL[1]
                uS = tS = txtS
                rS = (
                    "\n"
                    + "\n.. code-block:: text \n\n"
                    + "\n\n"
                    + textwrap.indent(txtS, "       ")
                )

                lS = ""
            else:
                pass
            # endregion

        elif cmdS == "bARG":
            """argument block"""
            # region
            blkL = (self.strL).split("\n", 1)
            parS = blkL[0].strip()
            varS = parS.split("|")[0].strip()
            untS = parS.split("|")[1].strip()
            self.lD["unit_note"] = untS
            argS = blkL[1].strip()
            argwS = textwrap.indent(argS, "    ")
            borderS = "    " + 75 * "="
            kwargD = {}
            for line in argS.splitlines():
                clean_line = line.split("#")[0].strip()
                if not clean_line:
                    continue
                if "=" in clean_line:
                    key, value = clean_line.split("=", 1)
                    kwargD[key.strip()] = value.strip()
            self.rivtD[varS] = kwargD
            for key, value in kwargD.items():
                self.rivtD[varS][key] = eval(value)
            intS = f"    Function Arguments Dictionary : {varS} ({untS})\n{borderS}\n{argwS}\n{borderS}\n"
            inrS = f".. code-block:: text \n\n    Function Arguments Dictionary : {varS} ({untS})\n{borderS}\n{argwS}\n{borderS}"
            uS = tS = intS + "\n"
            rS = inrS + "\n"
            lS = ""
            # endregion

        elif cmdS == "bPYT":
            """Python block"""
            # region
            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            self.uS = "\nTable " + str(tnumI) + ": " + lineS
            self.r2S = "\n**Table " + fillS + "**: " + lineS + "\n"
            self.rS = "\n**Table " + fillS + "**: " + lineS + "\n"
            # endregion

        else:
            pass

        mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
        }

        return mD, self.lD, self.rivtD

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
