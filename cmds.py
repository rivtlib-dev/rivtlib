# python #!
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
from PIL import Image
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import tags
from rivtlib.units import *

tabulate.PRESERVE_WHITESPACE = True


def rivtdict(self, rivS):
    """_summary_

    var, unit1, unit2, dec1, dec2

    from valread:  equ, desc, unit1, unit2, dec1, dec2
    from valtable: equ | desc | unit | dec
    from equtable: equ | desc | unit | dec

    """

    return self.rivtD


class Cmd:
    """
        insert commands that format to utf8 or reSt

        || APPEND | rel. pth | num; nonum                      .pdf
        || IMG  | rel. pth | caption, scale, (**[_F]**)        .png, .jpg
        || IMG2  | rel. pth | c1, c2, s1, s2, (**[_F]**)       .png, .jpg
        || TEXT | rel. pth |  plain; rivt                      .txt
        || TABLE | rel. pth | col width, l;c;r                 .csv, .txt, .xls
    """

    def __init__(self,  folderD, labelD):
        """commands that format to utf and reSt

        """
        self.folderD = folderD
        self.labelD = labelD
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

    def cmd_parse(self, cmdS, pthS, parS):
        """parse a tagged line

        Args:
            cmdS (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        cC = globals()['Cmd'](self.folderD, self.labelD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(f"{cmdS=}")
        # print(f"{pthS=}")
        # print(f"{parS=}")

        return uS, rS, self.folderD, self.labelD

    def append(self):
        """_summary_
        """
        pass

    def img(self, pthS, parS):
        """ insert image from file

        Args:
            pthS (str): relative file path
            parS (str): parameters

        Returns:
            uS (str): formatted utf string
            rS (str): formatted reSt string
        """
        # print(f"{parS=}")
        projP = self.folderD["rivP"]
        parL = parS.split(",")
        fileP = Path(pthS)
        capS = parL[0]
        scS = parL[1].strip()
        scF = float(scS)
        figS = "Fig. "
        if len(parL) == 3:
            if parL[2] == "_[F]":
                numS = str(self.labelD["fnum"])
                self.labelD["fnum"] = int(numS) + 1
                figS = figS + numS + capS
        img1 = Image.open(pthS)
        img1 = img1.resize((int(img1.size[0]*scF), int(img1.size[1]*scF)))
        try:
            _display(img1)
        except:
            pass
        uS = figS + capS + " : " + str(fileP) + "\n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :width: "
              + scS + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )

        return uS, rS

    def img2(self, pthS, parS):
        """ insert side by side images from files

        Args:
            pthS (str): relative file path
            parS (str): parameters

        Returns:
            uS (str): formatted utf string
            rS (str): formatted reSt string
        """
        # print(f"{parS=}")
        parL = parS.split(",")
        fileL = pthS.split(",")
        file1P = Path(fileL[0])
        file2P = Path(fileL[1])
        cap1S = parL[0].strip()
        cap2S = parL[1].strip()
        scale1S = parL[2].strip()
        scale2S = parL[3].strip()
        figS = "Fig. "
        if parL[2] == "_[F]":
            numS = str(self.labelD["fnum"])
            self.labelD["fnum"] = int(numS) + 1
            figS = figS + numS + cap1S
        try:
            img1 = Image.open(pthS)
            _display(img1)
        except:
            pass
        uS = "<" + cap1S + " : " + str(file1P) + "> \n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :scale: "
              + scale1S + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )

        return uS, rS

    def table(self, pthS, parS):
        """insert table from csv, xlsx or reSt file

        """
        # print(f"{pthS=}")
        uS = rS = """"""
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}
        pthP = Path(pthS)
        parL = parS.split(",")
        maxwI = int(parL[0])
        keyS = parL[1].strip()
        alignS = alignD[keyS]
        extS = pthP.suffix[1:]
        readL = []
        if extS == "csv":                                  # read csv file
            with open(pthP, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    # print(f"{row=}")
                    if row and row[0].startswith('#'):
                        # print(f"{row=}")
                        continue
                    else:
                        readL.append(row)
        elif extS == "xlsx":                               # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            return
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate.tabulate(
            readL, tablefmt="rst", headers="firstrow",
            numalign="decimal", maxcolwidths=maxwI, stralign=alignS))

        uS = rS = output.getvalue()
        sys.stdout = old_stdout

        pS = "\n" + "[values read from file: " + pthS + "]"
        uS += pS
        rS += pS

        return uS, rS

    def text(self):
        """insert text from file

        || text | folder | file | type

        :param lineS: string block

        """
        plenI = 3
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated:  \
                                    {plenI} parameters required")
            return
            if self.paramL[0] == "data":
                folderP = Path(self.folderD["dataP"])
            else:
                folderP = Path(self.folderD["dataP"])
                fileP = Path(self.paramL[1].strip())
                pathP = Path(folderP / fileP)
                txttypeS = self.paramL[2].strip()
                extS = pathP.suffix
                with open(pathP, "r", encoding="md-8") as f1:
                    txtfileS = f1.read()
                with open(pathP, "r", encoding="md-8") as f2:
                    txtfileL = f2.readlines()
                j = ""
            if extS == ".txt":
                # print(f"{txttypeS=}")
                if txttypeS == "plain":
                    print(txtfileS)
                    return txtfileS
                elif txttypeS == "code":
                    pass
                elif txttypeS == "rivttags":
                    xtagC = parse.RivtParseTag(
                        self.folderD, self.labelD,  self.localD)
                    xmdS, self.labelD, self.folderD, self.localD = xtagC.md_parse(
                        txtfileL)
                    return xmdS
                elif extS == ".html":
                    mdS = self.txthtml(txtfileL)
                    print(mdS)
                    return mdS
            elif extS == ".tex":
                soupS = self.txttex(txtfileS, txttypeS)
                print(soupS)
                return soupS
            elif extS == ".py":
                pass
