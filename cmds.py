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
from rivtlib.unit import *

tabulate.PRESERVE_WHITESPACE = True


class CmdW:
    """
        write commands

        || WRITE | rel. pth |  dec1                      .csv
        || REPORT | rel. pth | rel. pth | dec1, dec2     .csv

    """
    pass


class Cmd:
    """
        insert commands that format to utf8 or reSt

        || APPEND | rel. pth | num; nonum                      .pdf
        || TEXT | rel. pth |  plain; rivt                      .txt
        || TABLE | rel. pth | col width, l;c;r                 .csv, .txt, .xls
        || IMG  | rel. pth | caption, scale, (**[_F]**)        .png, .jpg
        || IMG2  | rel. pth | c1, c2, s1, s2, (**[_F]**)       .png, .jpg

    """

    def __init__(self,  folderD, labelD):
        """commands that format to utf and reSt

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

        return uS, rS

    def deflabel(self, labelS, numS):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        self.labelD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

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
        parL = parS.split(",")
        fileP = Path(pthS)
        capS = parL[0]
        scS = parL[1].strip()
        scF = float(scS)
        figS = ""
        if len(parL) == 3:
            if parL[2] == "_[F]":
                numS = self.labelD["fnum"]
                figS = self.deflabel(capS, numS)
        try:
            img1 = Image.open(pthS)
            img1 = img1.resize((int(img1.size[0]*scF), int(img1.size[1]*scF)))
            _display(img1)
        except:
            pass
        uS = "< " + capS + " : " + str(fileP) + " > \n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :scale: "
              + scS + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )
        print(uS)
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
        figS = ""
        if len(parL) == 5:
            if parL[2] == "_[F]":
                numS = self.labelD["fnum"]
                figS = self.deflabel(capS, numS)
        try:
            img1 = Image.open(pthS)
            _display(img1)
        except:
            pass
        uS = "<" + capS + " : " + str(fileP) + "> \n"
        rS = ("\n.. image:: "
              + pthS + "\n"
              + "   :scale: "
              + scale1S + "%" + "\n"
              + "   :align: center"
              + "\n\n"
              )
        print(uS)
        return uS, rS

    # def combine_images_side_by_side(image_path1, image_path2, output_path):
    #     """Combines two images horizontally side by side.

    # Args:
    #     image_path1: Path to the first image.
    #     image_path2: Path to the second image.
    #     output_path: Path to save the combined image.
    # """
    # try:
    #     img1 = Image.open(image_path1)
    #     img2 = Image.open(image_path2)

    #     new_width = img1.width + img2.width
    #     new_height = max(img1.height, img2.height)

    #     new_img = Image.new('RGB', (new_width, new_height), 'white')

    #     new_img.paste(img1, (0, 0))
    #     new_img.paste(img2, (img1.width, 0))

    #     new_img.save(output_path)
    #     print(f"Combined image saved to: {output_path}")

    # except FileNotFoundError:
    #     print("Error: One or both image files not found.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    # if __name__ == '__main__':
    #     combine_images_side_by_side('image1.jpg', 'image2.jpg', 'combined_image.jpg')

    def table(self, pthS, parS):
        """insert table from csv, xlsx or reSt file

        """

        uS = rS = """"""
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}
        pthS = pthS.split(":")                            # strip rows
        pthP = Path(pthS[0])
        parL = parS.split(",")
        maxwI = int(parL[0])
        keyS = parL[1].strip()
        alignS = alignD[keyS]
        extS = pthP.suffix[1:]
        readL = []
        # print(f"{extS=}")
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
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
            return

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate.tabulate(
            readL,
            tablefmt="rst",
            headers="firstrow",
            numalign="decimal",
            maxcolwidths=maxwI,
            stralign=alignS))

        uS = rS = output.getvalue()
        sys.stdout = old_stdout

        print(uS)
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
