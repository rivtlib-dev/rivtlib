import csv
import logging
import re
import sys
import warnings
from datetime import datetime, time
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
from io import StringIO
from pathlib import Path
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex
from tabulate import tabulate
from rivtlib import units
from rivtlib import cmd_utf
from rivtlib import cmd_rst
from rivtlib import tag_utf
from rivtlib import tag_rst

# tabulate.PRESERVE_WHITESPACE = True


class RivtParse:
    """format rivt-strings as utf and rst files"""

    def __init__(self, hS, tS, folderD, labelD,  rivtD):
        """process header string

        Args:
            hS (str)): header string
            tS (str): section type
            folderD (dict): _description_
            labelD (dict): _description_
            rivtD (dict): _description_

        Returns:
            cmdL (list): list of valid commands
            tagsL (list): list of valid tags
            folderD (dict): _description_
            labelD (dict): 
            rivtD (dict): local dictionary

        """

        self.rivtD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        self.errlogP = folderD["errlogP"]
        self.tS = tS

        hdrstS = """"""
        hdreadS = """"""
        hdutfS = """"""""
        xrstS = xutfS = ""
        rivtS = """"""                              # rivt input string
        utfS = """"""                               # utf-8 output string
        rmeS = """"""                               # readme output string
        xremS = """"""                              # redacted readme string
        rstS = """"""                               # reST output string
        declareS = """"""                           # declares output string
        assignS = """"""                            # assigns output string

        # section headings
        # initialize return strings
        hL = hS.split("|")               # section string as list
        titleS = hL[0].strip()           # sectiobn title
        labelD["xch"] = hL[1].strip()    # set xchange
        labelD["color"] = hL[2].strip()  # set background color
        if hS.strip()[0:2] == "--":      # omit section heading
            return "\n", "\n", "\n"

        headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"
        labelD["docS"] = titleS
        bordrS = labelD["widthI"] * "="
        hdutfS = (headS + "\n" + bordrS + "\n" + titleS + "\n" + bordrS + "\n")
        hdmdS = (headS + "\n## " + titleS + "\n")

        snumI = labelD["secnumI"] + 1
        labelD["secnumI"] = snumI
        docnumS = labelD["docnumS"]
        dnumS = docnumS + "-[" + str(snumI) + "]"
        headS = dnumS + " " + titleS
        bordrS = labelD["widthI"] * "-"

        hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
        hdmdS = "### " + headS + "\n"
        hdrstS += (
            ".. raw:: latex"
            + "   \n\n ?x?vspace{.2in} "
            + "   ?x?begin{tcolorbox} "
            + "   ?x?textbf{ " + titleS + "}"
            + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
            + "   ?x?end{tcolorbox}"
            + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
            + "\n\n")

        # print(hdutfS)
        # return hdutfS, hdmdS, hdrstS

        if tS == "I":
            self.cmdL = ["append", "image", "table", "text"]
            self.tagsD = {"u]": "underline", "c]": "center", "r]": "right",
                          "e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description", "s]": "sympy",
                          "link]": "link", "line]": "line", "page]": "page",
                          "[c]]": "centerblk",  "[p]]": "plainblk",
                          "[l]]": "latexblk", "[o]]": "codeblk", "[q]]": "quitblk"}

        elif tS == "V":
            self.cmdL = ["image", "table", "assign", "eval"]
            self.tagsD = {"e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description",
                          "s]": "sympy", "=": "eval"}

        elif tS == "R":
            self.cmdL = ["run", "process"]
            self.tagsD = {}

        elif tS == "T":
            self.cmdL = ["python"]
            self.tagsD = {}

        elif tS == "W":
            self.cmdL = ["write"]
            self.tagsD = {}
        else:
            pass

    def str_parse(self, strL):
        """str_parse _summary_

        Args:
            strL (_type_): _description_

        Returns:
            _type_: _description_
        """

        xutfS = """"""      # cumulative utf local string
        xrstS = """"""      # cumulative rst local string
        uS = """"""         # local line
        blockB = False

        # value table alignment
        hdraL = ["variable", "value", "[value]", "description"]
        alignaL = ["left", "right", "right", "left"]
        hdreL = ["variable", "value", "[value]", "description [eq. number]"]
        aligneL = ["left", "right", "right", "left"]

        blockevalL = []     # current value table
        blockevalB = False  # stop accumulation of values
        vtableL = []        # value table for export
        eqL = []            # equation result table
        lineS = ""
        for uS in strL:
            # print(f"{blockassignB=}")
            # print(f"{uS=}")
            if blockB:                                 # accumulate block
                lineS += uS
                continue
            if blockB and uS.strip() == "[q]]":        # end of block
                tagS = self.tagsD["[q]"]
                rvtS = tag_utf.TagsUTF(lineS, tagS,
                                       self.labelD, self.folderD,  self.rivtD)
                xutfS += rvtS + "\n"
                rvtS = tag_md.TagsMD(lineS, tagS,
                                     self.labelD, self.folderD,  self.rivtD)
                xmdS += rvtS + "\n"
                rvtS = tag_rst.TagsRST(lineS, tagS,
                                       self.labelD, self.folderD,  self.rivtD)
                xrstS += rvtS + "\n"
                blockB = False
            if blockevalB and len(uS.strip()) < 2:    # value tables
                vtableL += blockevalL
                if tfS == "declare":
                    vutfS = self.dtable(blockevalL, hdrdL,
                                        "rst", aligndL) + "\n\n"
                    vmdS = self.dtable(blockevalL, hdrdL,
                                       "html", aligndL) + "\n\n"
                    xutfS += vutfS
                    xmdS += vmdS
                    xrstS += vutfS
                if tfS == "assign":
                    vutfS = self.dtable(blockevalL, hdrdL,
                                        "rst", aligndL) + "\n\n"
                    vmdS = self.atable(blockevalL, hdraL,
                                       "html", alignaL) + "\n\n"
                    xutfS += vutfS
                    xmdS += vmdS
                    xrstS += vutfS
                blockevalL = []
                blockevalB = False
            elif uS[0:2] == "||":                      # commands
                usL = uS[2:].split("|")
                parL = usL[1:]
                cmdS = usL[0].strip()
                if cmdS in self.cmdL:
                    rvtC = cmd_utf.CmdUTF(
                        parL, self.labelD, self.folderD, self.rivtD)
                    utfS = rvtC.cmd_parse(cmdS)
                    # print(f"{utfS=}")
                    xutfS += utfS
                    rvtC = cmd_md.CmdMD(
                        parL, self.labelD, self.folderD, self.rivtD)
                    mdS = rvtC.cmd_parse(cmdS)
                    # print(f"{mdS=}")
                    xmdS += mdS
                    rvtC = cmd_rst.CmdRST(
                        parL, self.labelD, self.folderD, self.rivtD)
                    reS = rvtC.cmd_parse(cmdS)
                    xrstS += reS
            elif "_[" in uS:                           # line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                     # block tag
                    blockB = True
                if tagS in self.tagsD:
                    rvtC = tag_utf.TagsUTF(lineS, self.labelD, self.folderD,
                                           self.tagsD, self.rivtD)
                    utfxS = rvtC.tag_parse(tagS)
                    xutfS += utfxS + "\n"
                    rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,
                                         self.tagsD, self.rivtD)
                    mdS = rvtC.tag_parse(tagS)
                    xmdS += mdS + "\n"
                    rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,
                                           self.tagsD, self.rivtD)
                    reS = rvtC.tag_parse(tagS)
                    xrstS += reS + "\n"
            elif "=" in uS and self.methS == "V":       # equation tag
                # print(f"{uS=}")
                usL = uS.split("|")
                lineS = usL[0]
                self.labelD["unitS"] = usL[1].strip()
                self.labelD["descS"] = usL[2].strip()
                rvtC = tag_md.TagsMD(lineS, self.labelD, self.folderD,
                                     self.localD)
                if ":=" in uS:                         # declare tag
                    tfS = "declare"
                    blockevalL.append(rvtC.tag_parse(":="))

                    rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,
                                           self.localD)
                    eqL = rvtC.tag_parse(":=")
                    blockevalB = True
                    continue
                else:
                    tfS = "assign"                     # assign tag
                    eqL = rvtC.tag_parse("=")
                    mdS += eqL[1]
                    blockevalL.append(eqL[0])

                    rvtC = tag_rst.TagsRST(lineS, self.labelD, self.folderD,
                                           self.localD)
                    eqL = rvtC.tag_parse("=")
                    rstS += eqL[1]
                    blockevalB = True
                    continue
            else:
                print(uS)       # pass unformatted string

        # export values
        valP = Path(self.folderD["dataP"], self.folderD["valfileS"])
        with open(valP, "w", newline="") as f:
            writecsv = csv.writer(f)
            writecsv.writerow(hdraL)
            writecsv.writerows(vtableL)

        return (xutfS, xrstS,  self.labelD, self.folderD, self.rivtD)

    def atable(self, tblL, hdreL, tblfmt, alignaL):
        """write assign values table"""

        locals().update(self.rivtD)

        valL = []
        for vaL in tblL:

            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            valL.append([varS, val1U, val2U, descripS])

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdreL,
                showindex=False,  colalign=alignaL))
        mdS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.localD.update(locals())
        print("\n" + mdS+"\n")
        return mdS

    def dtable(self, tblL, hdrvL, tblfmt, alignvL):
        """write declare values table"""

        locals().update(self.rivtD)

        valL = []
        for vaL in tblL:
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2], vaL[3]
            descripS = vaL[4].strip()
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + " * " + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            valL.append([varS, val1U, val2U, descripS])

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                valL, tablefmt=tblfmt, headers=hdrvL,
                showindex=False,  colalign=alignvL))
        mdS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        self.rivtD.update(locals())

        print("\n" + mdS+"\n")
        return mdS
