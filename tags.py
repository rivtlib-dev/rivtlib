#
import fnmatch
import csv
import logging
import re
import sys
import warnings
from datetime import datetime, time
from io import StringIO
from pathlib import Path

import IPython
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
import tabulate
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib.units import *
from rivtlib import cmds

tabulate.PRESERVE_WHITESPACE = True


class Tag:
    """
       format to utf8 or reSt

        Functions:
             _[1-6]                  headings
             _[#]                    foot
             _[D]                    descrip
             _[C]                    center
             _[S]                    sympy
             _[N]                    number (sympy)
             _[E]                    equation
             _[F]                    figure
             _[T]                    table
             _[H]                    hline
             _[G]                    page
             _[K]                    url, reference
             _[[N]]                  indblk
             _[[O]]                  codeblk (literal)
             _[[B]]                  boldblk (latex pdf)
             _[[L]]                  latexblk (latex pdf)
             _[[I]]                  italblk (latex pdf)
             _[[T]]                  itinblk (latex pdf)
             _[[Q]]                  quit

    """

    def __init__(self,  folderD, labelD):
        """tags that format to utf and reSt

        """
        self.folderD = folderD
        self.labelD = labelD
        # print(folderD)
        errlogP = folderD["errlogP"]
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def tag_parse(self, tagcmdS, lineS):
        """parse a tagged line

        Args:
            tagcmd (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        tC = Tag(self.folderD, self.labelD)
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        uS, rS = functag(lineS)

        # print(f"{tcmdS=}")
        # print(f"{lineS=}")
        return uS, rS, self.folderD, self.labelD

    def equa(self, lineS):
        """ format equation label _[E]

        Args:
            lineS (str): _description_
        Returns:
            str : _description_
        """
        enumI = int(self.labelD["equI"])
        self.labelD["equI"] = enumI + 1
        wI = self.labelD["widthI"]
       # utf
        fillS = "Eq-" + str(enumI).zfill(2)
        uS = rS = lineS + fillS.rjust(wI-len(lineS))
        # rst
        rS = uS

        return uS, rS

    def table(self, lineS):
        """format table title _[T]

        Args:
            lineS (_type_): _description_
        Returns:
            _type_: _description_
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        fillS = str(tnumI).zfill(2)
        # utf
        uS = "Table " + str(tnumI) + " - " + lineS
        # rst
        rS = "\n" + "**" + "Table " + fillS + ": " + lineS

        return uS, rS

    def figure(self, lineS):
        """utf figure caption _[F]

        Args:
            lineS (_type_): _description_

        Returns:
            _type_: _description_
        """
        fnumI = int(self.labelD["figI"])
        self.labelD["figI"] = fnumI + 1
        lineS = "Fig. " + str(fnumI) + " - " + self.lineS

        return lineS + "\n"

    def foot(self):
        """ footnote number _[#]

        Args:
            lineS (str): rivt line
        Returns:
            str, str: formatted utf, reSt 
        """
        ftnumI = self.labelD["footL"].pop(0)
        self.labelD["noteL"].append(ftnumI + 1)
        self.labelD["footL"].append(ftnumI + 1)
        lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")
        print(lineS)
        return lineS

    def description(self, lineS):
        """ footnote description _[D]

        Args:
            lineS (str): rivt line
        Returns:
            str: formatted utf 
            str: formatted reSt 
        """
        ftnumI = self.labelD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS

        return lineS

    def center(self, lineS):
        """ center text _[C]

        Args:
            lineS (str): rivt line
        Returns:
            str, str: formatted utf, reSt 
        """
        # utf
        uS = lineS.center(int(self.labelD["widthI"])) + "\n"
        # rst
        rS = "\n::\n\n" + lineS.center(int(self.labelD['widthI'])) + "\n"

        return uS, rS

    def sympy(self, lineS):
        """ format sympy math _[S]


        Args:
            lineS (str): rivt line
        Returns:
            str, str: formatted utf, reSt 
        """
        spS = lineS.strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            # sps = sp.encode('unicode-escape').decode()
        except:
            pass
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # utf
        uS = lineS
        # rst
        rS = ".. raw:: math\n\n   " + lineS + "\n"

        # print(uS)
        return uS, rS

    def plain(self, lineS, folderD, labelD):
        """format plain literal text _[P]

        :param lineS: _description_
        :type lineS: _type_
        """
        print(self.lineS)
        return self.lineS

    def link(self, lineS, folderD, labelD):
        """format url or internal link _[LINK]

        :return: _description_
        :rtype: _type_
        """
        lineL = self.lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]
        print(lineS)
        return lineS

    def hline(self, lineS, folderD, labelD):
        """horizontal line _[H]

        :return lineS: underline
        :rtype: str
        """
        return self.lineS

    def page(self, lineS, folderD, labelD):
        """insert new page header _[PAGE]

        :return lineS: page header
        :rtype: str
        """
        pagenoS = str(self.labelD["pageI"])
        rvtS = self.labelD["headuS"].replace("p##", pagenoS)
        self.labelD["pageI"] = int(pagenoS)+1
        lineS = "\n"+"_" * self.labelD["widthI"] + "\n" + rvtS +\
                "\n"+"_" * self.labelD["widthI"] + "\n"
        return "\n" + rvtS

    def blkplain(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkcode(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkbold(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkital(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkind(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkitind(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blklatex(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def blkquit(self, lineS, folderD, labelD):
        """format table title _[T]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        # utf
        luS = "Table " + str(tnumI) + " - " + lineS
        # rst
        lrS = "\n" + "**" + "Table " + fillS + ": " + lineS

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS
