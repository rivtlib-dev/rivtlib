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

from rivtlib.unit import *
from rivtlib import cmds

tabulate.PRESERVE_WHITESPACE = True
class Tag:
    """convert tags to formatted text or reSt
    Args:
        tags (str): 
            ====================== =======================================
            tags                                   description 
            ====================== =======================================
             _[h1-h6]                heading type        
             _[C]                    center
             _[S]                    sympy math
             _[E]                    equation label and autonumber
             _[F]                    figure caption and autonumber
             _[T]                    table title and autonumber
             _[#]                    footnote and autonumber
             _[D]                    footnote description 
             _[HLINE]                horizontal line
             _[PAGE]                 new page
             _[address, label]       url, internal reference        
             _[[Q]]                  end block              
             _[[P]]                  start plain text block  
             _[[N]]                  start indent text block
             _[[B]]                  start bold text block (latex pdf)
             _[[I]]                  start italic text block (latex pdf)
             _[[O]]                  start indent bold block (latex pdf)
             _[[T]]                  start indent italic block (latex pdf)
             _[[L]]                  start LaTeX block (latex pdf)
    
    
    # \*[a-zA-Z0-9_]*\*
    
    """

    def __init__(self,  folderD, labelD,  rivtD):
        """tag formatting to utf and reSt

        """
        self.rivtD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        errlogP = self.folderD["errlogP"]
        modnameS = self.labelD["rivN"]
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
        tC = globals()['Tag']("folderD, labelD,  rivtD")
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        utS, reS = functag(lineS, self.folderD, self.labelD)
        
        print(f"{tcmdS=}")
        print(f"{lineS=}")
        return utS, reS
    def center(self, lineS, labelD, folderD):
        """center text _[C]

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_

        Returns:
            _type_: _description_
        """        
        # utf
        luS = lineS.center(int(labelD["widthI"])) + "\n"
        # rst
        lrS = "\n::\n\n" +  lineS.center(int(labelD['widthI'])) + "\n"

        print("***center***", f"{luS=}", f"{lrS=}")
        return luS, lrS
        
    def sympy(self, lineS, folderD, labelD):
        """format sympy math _[S]

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_

        Returns:
            _type_: _description_
        """        
        spS = self.lineS.strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
            # sps = sp.encode('unicode-escape').decode()
        except:
            pass
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # utf
        luS = lineS.center(int(labelD["widthI"])) + "\n"
        # rst
        lrS = ".. raw:: math\n\n   " + lineS + "\n"

        print("***sympy***", f"{luS=}", f"{lrS=}")
        return luS, lrS

    def table(self, lineS, folderD, labelD):
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

    def figure(self, lineS, folderD, labelD):
        """utf figure caption _[F]

        :return lineS: figure label
        :rtype: str
        """
        fnumI = int(self.labelD["figI"])
        self.labelD["figI"] = fnumI + 1
        lineS = "Fig. " + str(fnumI) + " - " + self.lineS

        return lineS + "\n"

    def labels(self, labelS, numS):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        self.labelD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

    def plain(self, lineS, folderD, labelD):
        """format plain literal text _[P]

        :param lineS: _description_
        :type lineS: _type_
        """
        print(self.lineS)
        return self.lineS

    def foot(self, lineS, folderD, labelD):
        """footnote number _[#]


        """
        ftnumI = self.labelD["footL"].pop(0)
        self.labelD["noteL"].append(ftnumI + 1)
        self.labelD["footL"].append(ftnumI + 1)
        lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")
        print(lineS)
        return lineS

    def description(self, lineS, folderD, labelD):
        """footnote description _[D]

        :return lineS: footnote
        :rtype: str
        """
        ftnumI = self.labelD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS
        print(lineS)
        return lineS

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

