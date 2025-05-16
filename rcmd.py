# python #!
import csv
import logging
import sys
import textwrap
import warnings
from io import StringIO
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import pandas as pd
import sympy as sp
import tabulate
from IPython.display import Image as _Image
from IPython.display import display as _display
from PIL import Image
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib.runits import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """commands

    |IMG| rel. pth | caption, scale, (_[F])        .png, .jpg
    |IMG2| rel. pth | c1, c2, s1, s2, (_[F])       .png, .jpg
    |TABLE| rel. pth | col width, l;c;r (_[T])     .csv, .txt, .xls
    |TEXT| rel. pth |  plain; rivt                 .txt
    |VALUE| rel. pth | col width, l;c;r (_[T])     .csv

    """

    def __init__(self, folderD, labelD, rivtD):
        """command dictionaries"""
        self.folderD = folderD
        self.labelD = labelD
        self.rivtD = rivtD

        errlogP = folderD["errlogP"]
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def cmds(self, cmdS, pthS, parS, rivtL):
        """command parsing"""

        folderD = self.folderD
        labelD = self.labelD
        rivtD = self.rivtD

        if cmdS == "IMG":
            """ image insert """
            if "_[F]" in parS:
                numS = str(self.labelD["figI"])
                self.labelD["figI"] = int(numS) + 1
                figS = "**Fig. " + numS + " -** "
            else:
                figS = " "
            # print(f"{parS=}")
            # print(f"{pthS=}")
            parL = parS.split(",")
            capS = parL[0].strip()
            scS = parL[1].strip()
            insP = Path(folderD["projP"] / "src" / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            # pthxS = str(Path(*Path(self.folderD["rivP"]).parts[-1:]))
            if capS == "-":
                capS = " "
            try:
                img1 = Image.open(pthS)
                _display(img1)
            except:
                pass
            uS = figS + capS + " [file: " + pthS + " ] \n"
            rS = xS = (
                "\n\n.. image:: "
                + insS
                + "\n"
                + "   :width: "
                + scS
                + "% \n"
                + "   :align: center \n\n\n"
                + ".. class:: center \n\n"
                + figS
                + capS
                + "\n"
            )

        elif cmdS == "IMG2":
            """image insert side by side """

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

            uS = "<" + cap1S + " : " + str(file1P) + "> \n"
            rS = (
                "\n.. image:: "
                + pthS
                + "\n"
                + "   :scale: "
                + scale1S
                + "%"
                + "\n"
                + "   :align: center"
                + "\n\n"
            )

        elif cmdS == "TABLE":
            """table insert"""

            # print(f"{pthS=}")
            if "_[T]" in parS:
                tnumI = int(self.labelD["tableI"])
                fillS = str(tnumI).zfill(2)
                utitlnS = "\nTable " + fillS + " - "
                rtitlnS = "\n**Table " + fillS + " -** "
                self.labelD["tableI"] = tnumI + 1
                parS = (parS.replace("_[T]", " ")).strip()
            else:
                utitlnS = " "
                rtitlnS = " "
            uS = rS = ""
            pthP = Path(pthS)  # path
            extS = pthP.suffix[1:]  # file extension
            parL = parS.split(",")
            titleS = parL[0].strip()  # title
            if titleS == "-":
                titleS = " "
            maxwI = int(parL[1].strip())  # max col. width
            alnS = parL[2].strip()  # col. alignment
            rowL = eval(parL[3].strip())  # rows
            if len(rowL) == 0:
                pass
            alignD = {"s": "", "d": "decimal", "c": "center", "r": "right", "l": "left"}
            # pthxP = Path(*Path(pthS).parts[-3:])
            # pthxS = str(pthxP.as_posix())
            insP = Path(self.folderD["projP"])
            insP = Path(Path(insP) / "src" / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            utlS = utitlnS + titleS + pS  # file path text
            rtlS = rtitlnS + titleS + pS
            readL = []
            if extS == "csv":  # read csv file
                with open(insP, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        # print(f"{row=}")
                        if row and row[0].startswith("#"):
                            continue
                        else:
                            readL.append(row)
            elif extS == "xlsx":  # read xls file
                pDF1 = pd.read_excel(pthS, header=None)
                readL = pDF1.values.tolist()
            else:
                pass

            sys.stdout.flush()
            old_stdout = sys.stdout
            output = StringIO()
            alignS = alignD[alnS]
            output.write(
                tabulate.tabulate(
                    readL,
                    tablefmt="rst",
                    headers="firstrow",
                    numalign="decimal",
                    maxcolwidths=maxwI,
                    stralign=alignS,
                )
            )
            uS = rS = output.getvalue()
            sys.stdout = old_stdout

            uS = utlS + uS + "\n"
            rS = rtlS + rS + "\n"
            xS = rtlS + rS + "\n"

        elif cmdS == "TEXT":
            """text file insert"""

            # print(f"{pthS=}")
            uS = rS = xS = ""
            pthP = Path(pthS)  # path
            extS = pthP.suffix[1:]  # file extension
            parL = parS.split(",")
            insP = Path(self.folderD["projP"])
            insP = Path(Path(insP) / "src" / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            # pthxP = Path(*Path(pthS).parts[-3:])

            with open(insP, "r") as fileO:
                fileS = fileO.read()

            uS = fileS
            rS = fileS
            xS = fileS

        elif cmdS == "VALUE":
            """insert values file"""

            tnumI = int(labelD["tableI"])
            labelD["tableI"] = tnumI + 1
            fillS = str(tnumI).zfill(2)
            utitlnS = "\nTable " + fillS + " - " + parS.strip("_[T]")
            rtitlnS = "\n**Table " + fillS + " -** " + parS.strip("_[T]")

            insP = Path(folderD["projP"])
            insP = Path(Path(insP) / "src" / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            with open(insP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
            # print(f"{readL=}")
            tbL = []
            for vaL in readL:
                # print(f"{vaL=}")
                if len(vaL) != 5:
                    continue
                eqS = vaL[0].strip()
                varS = vaL[0].split("=")[0].strip()
                valS = vaL[0].split("=")[1].strip()
                unit1S, unit2S = vaL[1], vaL[2]
                dec1S, descripS = vaL[3].strip(), vaL[4].strip()
                fmt1S = (
                    "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
                )
                eval(fmt1S)

                if unit1S != "-":
                    if isinstance(eval(valS), list):
                        val1U = np.array(eval(valS)) * eval(unit1S)
                        val2U = [varS.cast_unit(eval(unit2S)) for varS in val1U]
                    else:
                        eqS = varS + " = " + valS
                        try:
                            exec(eqS, globals(), self.rivtD)
                        except ValueError as ve:
                            print(f"A ValueError occurred: {ve}")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                        valU = eval(varS, globals(), self.rivtD)
                        val1U = str(valU.cast_unit(eval(unit1S)))
                        val2U = str(valU.cast_unit(eval(unit2S)))
                else:
                    eqS = varS + " = " + valS
                    exec(eqS, globals(), self.rivtD)
                    valU = eval(varS)
                    val1U = str(valU)
                    val2U = str(valU)
                tbL.append([varS, val1U, val2U, descripS])

            # print("tbl", tbL)
            tblfmt = "rst"
            hdrvL = ["variable", "value", "[value]", "description"]
            alignL = ["left", "right", "right", "left"]
            sys.stdout.flush()
            old_stdout = sys.stdout
            output = StringIO()
            output.write(
                tabulate.tabulate(
                    tbL,
                    tablefmt=tblfmt,
                    headers=hdrvL,
                    showindex=False,
                    colalign=alignL,
                )
            )
            uS = rS = xS = output.getvalue()
            sys.stdout = old_stdout
            sys.stdout.flush()

            # pthxS = str(Path(*Path(pthS).parts[-3:]))
            pS = "[from file: " + pthS + "]" + "\n\n"
            uS = utitlnS + pS + uS + "\n"
            rS = rtitlnS + pS + rS + "\n"
            xS = rtitlnS + pS + rS + "\n"

        return uS, rS, xS, folderD, labelD, rivtD, rivtL
