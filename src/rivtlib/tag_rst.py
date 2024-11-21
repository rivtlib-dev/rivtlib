import csv
import logging
import warnings
from datetime import datetime
from io import StringIO
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex
from tabulate import tabulate
from rivtlib.units import *


class TagsRST():
    """convert rivt tags to reST

    """

    def __init__(self, lineS, labelD, folderD,  tagsD, localD):
        """convert rivt tags to md or reST

        """

        self.tagsD = tagsD
        self.localD = localD
        self.folderD = folderD
        self.labelD = labelD
        self.lineS = lineS
        self.vgap = "2"
        self.widthI = labelD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

        modnameS = self.labelD["modnameS"]
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

    def bold(self):
        """bold text _[b]

        :return lineS: bold line
        :rtype: str
        """
        return "**" + self.lineS.strip() + "**"

    def center(self):
        """center text _[c]

        : return lineS: centered line
        : rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} " + self.lineS + " ?x?end{center}" \
            + "\n"

        return lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """
        return "*" + self.lineS.strip() + "*"

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """
        return "?x?hfill " + self.lineS

    def boldcenter(self):
        """bold center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textbf{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
        return lineS

    def boldright(self):
        """bold right text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textbf{" + self.lineS + "}" \
            + "\n"
        return lineS

    def italiccenter(self):
        """italic center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textit{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
        return lineS

    def italicright(self):
        """italic right text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textit{" + self.lineS + "}" \
            + "\n"
        return lineS

    def label(self, labelS, numS):
        """format labels for equations, tables and figures

            : return labelS: formatted label
            : rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        return secS + " - " + labelS + numS

    def description(self):
        """footnote description _[d]

        : return lineS: footnote
        : rtype: str
        """
        return ".. [*] " + self.lineS

    def equation(self):
        """reST equation label _[e]

        : return lineS: reST equation label
        : rtype: str
        """
        enumI = int(self.labelD["equI"])
        fillS = str(enumI).zfill(2)
        refS = self.label("E", fillS)
        lineS = "\n\n" + "**" + "Eq. " + str(enumI) + ": "  \
                + self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n\n"
        return lineS

    def figure(self):
        """figure label _[f]

        : return lineS: figure label
        : rtype: str
        """
        fnumI = int(self.labelD["figI"])
        fillS = str(fnumI).zfill(2)
        refS = self.label("F", fillS)
        lineS = "\n \n" + "**" + "Figure " + str(fnumI) + ": " + \
                self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n \n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def footnumber(self):
        """insert footnote number _[#]

        :return: _description_
        :rtype: _type_
        """
        lineS = "".join(self.lineS)
        return lineS.replace("*]", "[*]_ ")

    def latex(self):
        """format latex _[l]

        :return lineS: reST formatted latex
        :rtype: str
        """
        return ".. raw:: math\n\n   " + self.lineS + "\n"

    def link(self):
        """url or internal link

        :return: _description_
        :rtype: _type_
        """
        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def line(self):
        """insert line _[line]:

        param lineS: _description_
        :type lineS: _type_
        """
        return self.widthI * "-"

    def plain(self):
        """format plain literal _[p]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def sympy(self):
        """reST line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """
        spS = self.lineS
        txS = sp.latex(S(spS))
        return ".. raw:: math\n\n   " + txS + "\n"

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """
        return ":math: `?x?text?x?underline{" + self.lineS.strip() + "}"

    def page(self):
        """insert page break _[page]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def table(self):
        """table label _[t]

        :return lineS: figure label
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        fillS = str(tnumI).zfill(2)
        refS = self.label("T", fillS)
        lineS = "\n" + "**" + "Table " + fillS + ": " + self.lineS.strip() + \
                "** " + " ?x?hfill " + refS + "\n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def centerblk(self):
        """_summary_
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} + ?x?parbox{5cm}" \
            + self.lineS + " ?x?end{center}" \
            + "\n\n"
        return lineS

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def codeblk(self):
        pass

    def rightblk(self):
        pass

    def tagblk(self):
        pass
