import csv
import logging
import re
import sys
import warnings
from io import StringIO
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
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

    def __init__(self, methS, folderD, labelD,  rivtD):
        """ rivt-strings as utf and reST line by line

            :param dict folderD: folder paths
            :param dict labelD: numbers that increment
            :param dict outputS: output type
            :param dict outputS: output type
        """

        self.rivtD = rivtD
        self.folderD = folderD  # folder paths
        self.labelD = labelD      # incrementing formats
        self.errlogP = folderD["errlogP"]
        self.methS = methS

        hdrstS = """"""
        hdreadS = """"""
        hdutfS = """"""""

        # section headings
        xmdS = xrstS = xutfS = ""
        rL = rS.split("\n")

        rsL = rS.split("|")              # function string as list
        titleS = rsL[0].strip()          #
        labelD["tocS"] = rsL[1].strip()  # set redaction
        labelD["pageI"] = int(rsL[2])    # set background color
        if rS.strip()[0:2] == "--":         # omit section heading
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

#        print(hdutfS)
#        return hdutfS, hdmdS, hdrstS

        utfS += hutfS
        rstS += hrstS

        # valid commands and tags
        if methS == "R":
            self.cmdL = ["run", "process"]

            self.tagsD = {"link]": "link", "line]": "line", "page]": "page"}

        elif methS == "I":
            self.cmdL = ["image", "table", "text"]

            self.tagsD = {"b]": "bold", "i]": "italic", "u]": "underline",
                          "c]": "center", "r]": "right",
                          "e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description",
                          "l]": "latex", "s]": "sympy",
                          "link]": "link", "line]": "line", "page]": "page",
                          "[c]]": "centerblk",  "[p]]": "plainblk",
                          "[l]]": "latexblk", "[m]]": "mathblk",
                          "[o]]": "codeblk", "[q]]": "quitblk"}

        elif methS == "V":
            self.cmdL = ["image", "table", "text", "assign", "declare"]

            self.tagsD = {"e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description",
                          "l]": "latex", "s]": "sympy",
                          ":=": "declare",  "=": "assign"}

        elif methS == "T":
            self.cmdL = []

            self.tagsD = {}

        elif methS == "W":
            self.cmdL = []

            self.tagsD = {}
        else:
            pass

        modnameS = __name__.split(".")[1]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
        # self.rivtD.update(locals())

    def str_parse(self, strL):
        """parse method string line by line starting with second line

            :param list strL: split method string
            :return mdS: md formatted string
            :return rstS: reST formatted string
            :return labelD: increment references
            :return folderD: folder paths
            :rtype mdS: string
            :rtype rstS: string
            :rtype folderD: dictionary
            :rtype labelD: dictionary
        """

        xutfS = """"""      # utfS local string
        xmdS = """"""       # mdS local string
        xrstS = """"""      # rstS local string
        uS = """"""         # raw local line
        blockB = False

        # table alignment
        hdrdL = ["variable", "value", "[value]", "description"]
        aligndL = ["left", "right", "right", "left"]
        hdraL = ["variable", "value", "[value]", "description [eq. number]"]
        alignaL = ["left", "right", "right", "left"]

        blockevalL = []     # current value table
        blockevalB = False  # stop accumulation of values
        vtableL = []        # value table for export
        eqL = []            # equation result table
        lineS = ""
        for uS in strL:
            # print(f"{blockassignB=}")
            # print(f"{uS=}")
            uS = uS[4:]                                # remove indent
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

        return (xutfS, xmdS, xrstS,  self.labelD, self.folderD, self.rivtD)

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
