import ast
import csv
import io
import sys
import textwrap
from pathlib import Path

import docutils.parsers.rst.tableparser
import docutils.statemachine
import sympy as sp
import tabulate
from fastcore.utils import store_attr
from numpy import *  # noqa: F403
from sympy.abc import _clash2

from rivtlib import rvtext

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
        self.wI = int(self.lD["widthI"])

    def taglx(self, tagS):
        """formats a line

         API         Syntax                         Description (output types)
        ------- ---------------------------------------- --------------------------------
         I          **text text**                        bold words
         I           *text text*                         italic words
         I,V      text  _[C]                             bold center text (all)
         I,V      text  _[R]                             bold center text (all)
         I,V      text  _[B]                             bold text (pdf, html)
         I,V      math  _[L]                             format LaTeX math (pdf, html)
         I,V      math  _[M]                             format ASCII math (all)
         I,V      title _[T]                             table number and title (all)
         I,V      text  _[#] text                        number endnote (all)
         I,V      text  _[V] var_name | text             variable substitution (all)
         I,V      text  _[G] term link | text            link term to glossary (all)
         I,V      text  _[D] label,filename | text       variable substitution (all)
         I,V      text  _[S] label, section link | text  link to section in report (all)
         I,V      text  _[U] label, external link | text external url link (all)
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
            """bold center text"""

            uS = tS = lineS.center(wI) + "\n"
            rS = lS = "\n.. rst-class:: align-center\n\n**" + lineS + "**\n"

        elif cmdS == "lR":
            """right justify line"""

            uS = tS = lineS.rjust(wI) + "\n"
            rS = lS = "\n.. rst-class:: align-right\n\n   " + lineS + "\n"

        elif cmdS == "lB":
            """bold text"""

            uS = tS = lineS + "\n\n"
            rS = lS = "**" + lineS.strip() + "**" + "\n\n"

        elif cmdS == "lS":
            """format section link"""

            txt1 = lineL[0]
            txt2 = lineL[1].split("|")[0].strip()
            txt3 = lineL[1].split("|")[1].strip()
            txt2a = txt2.split(",")[0].strip()
            txt2b = "<" + txt2.split(",")[1].strip() + ">"
            uS = tS = f"{txt1} {txt2a} [ref: {txt2b}] {txt3}"
            rS = lS = f"{txt1} **<** :ref:`{txt2a} {txt2b}` **>** {txt3}"

        elif cmdS == "lG":
            """format glossary term link"""

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
            txt2b = txt2.split(",")[1].strip()
            uS = tS = f"{txt1} {txt2a} {txt2b} {txt3}".strip()
            rS = lS = f"{txt1} `{txt2a} <{txt2b}>`_ {txt3}".strip()

        elif cmdS == "lD":
            """download link"""

            lineL = lineS.split(",")
            uS = tS = lineL[0] + ": " + lineL[1]
            rS = ".. _" + lineL[0] + ": " + lineL[1]
            lS = ".. _" + lineL[0] + ": " + lineL[1]

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

        elif cmdS == "lL":
            """format latex math"""

            self.enumI = int(self.lD["equI"])
            self.enumI += 1
            self.lD["equI"] = self.enumI
            self.enumS = str(self.enumI)
            eS = "\nEq." + self.enumS + "\n"
            ebS = "\n**Eq." + self.enumS + "**\n\n"
            labellnS = eS + r"[LaTeX] " + lineS.strip()
            indlineS = textwrap.indent(lineS.strip(), "     ")
            uS = tS = labellnS + "\n"
            rS = (
                ebS
                + "\n.. container:: math-block \n\n"
                + "    .. math:: \n\n"
                + "    "
                + indlineS
                + "\n\n"
            )
            lS = ""

        elif cmdS == "lT":
            """label and number table"""

            tnumI = int(self.lD["tableI"])
            self.lD["tableI"] = tnumI + 1
            fillS = str(tnumI)
            uS = tS = "\nTable " + str(tnumI) + ": " + lineS
            rS = "\n**Table " + fillS + "**: " + lineS + "\n\n"
            lS = "\n**Table " + fillS + "**: " + lineS + "\n\n"

        # endregion
        mD = {
            "uS": uS,
            "tS": tS,
            "rS": rS,
            "lS": lS,
        }
        return mD, self.lD

    def tagbx(self, tagS):
        """formats a block

         API         Syntax                               Description (output types)
        --------- -------------------------------------- -------------------------------------
        R          _[[SHELL]] type, *wait;nowait*          command script (all)
        V          _[[PYTHON] topic label                  topic box (all)
        I          _[[BOX]] optional label                 box (all)
        V          _[[TABLE]] title                        format table, store csv (all)
        V,I        _[[TEXT]] type                          markup (all)
        D          _[[METADATA]] label                     meta and layout data (all)
        all        _[[END]]                                end block (all)

        Args:
            tagS (str): characters of tag symbol with leading "_[" stripped
        Returns:
            uS, r2S, rS, fD, lD, rivD, rivL
        """
        # region
        cmdS = "b" + tagS[0:3]
        lineS = self.strL[0].strip()

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
            self.lD["argsname"] = varS
            intS = f"    Function Arguments Dictionary : {varS} ({untS})\n{borderS}\n{argwS}\n{borderS}\n"
            inrS = f".. code-block:: text \n\n    Function Arguments Dictionary : {varS} ({untS})\n{borderS}\n{argwS}\n{borderS}"
            uS = tS = intS + "\n"
            rS = inrS + "\n"
            lS = ""
            # endregion

        elif cmdS == "bTEX":
            """format text
            
            types:  
                bold n - bold text with indent
                endnote - list of endnotes in order
                html - include in html 
                indent n - format literal with indent
                italic n - italic text with indent
                latex - include in pdf, attach to pdf
                note - note in bolx
                rst - format restructured text  
                text - format literal
                wrap n - wrap with indent  

                latex - requires texlive cli
                mermaid - requires mermaid cli
                dot - requires graphviz cli            
            """
            # region
            blkL = (self.strL).split("\n", 1)
            texttypS = blkL[0].strip()
            blkS = blkL[1]
            iS = "0"
            uS, tS, rS, lS = rvtext.format_text(
                texttypS, blkS, iS, self.lD, self.rivtD
            )
            lS = ""

            # endregion
        elif cmdS == "bPYT":
            """execute python code block

            options: 
                compile
                code
            
            """
            blkL = (self.strL).split("\n", 1)
            txtS = blkL[1]
            self.build_transcript(txtS)
            pytxtS = self.build_transcript(txtS)
            uS = tS = pytxtS
            lS = ""
            rS = (
                "\n.. code-block:: python\n\n"
                + textwrap.indent(pytxtS, "   ")
                + "\n\n"
            )

        else:
            pass

        mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
        }

        return mD, self.lD, self.rivtD

    def build_transcript(self, txtS):
        """
        Returns (transcript, source_lines)

        transcript   -- list of strings representing the full annotated
                        output: every source line (comments/blank lines
                        included) plus any print() output inserted right
                        after the statement that generated it.
        source_lines -- list of every raw line of the input file, as strings,
                        in original order (this is the plain "capture every
                        line as a string" list, with no output mixed in).
        """
        lines = txtS.splitlines()

        tree = ast.parse(txtS)

        globals_ns = globals().copy()
        transcript = []
        source_lines = []

        prev_end = 0
        real_stdout = sys.stdout

        def emit_raw(ln_start, ln_end):
            for ln in range(ln_start, ln_end + 1):
                text = lines[ln - 1]
                source_lines.append(text)
                transcript.append(text)

        for node in tree.body:
            start = node.lineno
            end = getattr(node, "end_lineno", start)

            # Comment-only / blank lines sitting between statements: just
            # display them, nothing to execute.
            if start - 1 >= prev_end + 1:
                emit_raw(prev_end + 1, start - 1)

            # The statement's own source lines.
            emit_raw(start, end)

            # Execute just this one statement, capturing whatever it prints.
            module = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(module)
            code_obj = compile(module, txtS, "exec")

            buf = io.StringIO()
            sys.stdout = buf
            try:
                exec(code_obj, globals_ns)
                self.rivtD.update(globals_ns)
            finally:
                sys.stdout = real_stdout

            output = buf.getvalue()
            if output:
                transcript.extend(output.rstrip("\n").split("\n"))

            prev_end = end

        # Any trailing comment/blank lines after the final statement.
        if prev_end + 1 <= len(lines):
            emit_raw(prev_end + 1, len(lines))

        globals().update(globals_ns)
        result = "\n".join(transcript)
        return result

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
        def clean(cell):
            return " ".join(line.strip() for line in cell[3]).strip()

        # Process headers
        header_data = [[clean(cell) for cell in row] for row in headers]

        # Process body
        body_data = [[clean(cell) for cell in row] for row in body]

        return header_data, body_data
