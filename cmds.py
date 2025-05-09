# python #!
import csv
import logging
import sys
import warnings
import textwrap
from io import StringIO
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy.linalg as la
import pandas as pd
import sympy as sp
import tabulate
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *  # noqa: F403
from PIL import Image
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import tags
from rivtlib.units import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """commands

    |IMG| rel. pth | caption, scale, (**[_F]**)        .png, .jpg
    |IMG2| rel. pth | c1, c2, s1, s2, (**[_F]**)       .png, .jpg
    |TEXT| rel. pth |  plain; rivt                      .txt
    |TABLE| rel. pth | col width, l;c;r                 .csv, .txt, .xls
    |VALUE| rel. pth | col width, l;c;r                .csv, .txt, .xls

        cC = globals()["CmdV"](self.folderD, self.labelD, self.rivtD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

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

    def comm(self, cmdS, pthS, parS):
        """command parsing"""

        if cmdS == "IMG":
            """ image insert """

            print(f"{parS=}")
            print(f"{pthS=}")
            parL = parS.split(",")
            capS = parL[0].strip()
            scS = parL[1].strip()
            insP = Path(self.folderD["projP"] / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            # pthxS = str(Path(*Path(self.folderD["rivP"]).parts[-1:]))
            if capS == "-":
                capS = " "
            if parL[2].strip() == "_[F]":
                numS = str(self.labelD["figI"])
                self.labelD["figI"] = int(numS) + 1
                figS = "**Fig. " + numS + " -** "
            else:
                figS = " "
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

            return uS, rS, xS

        if cmdS == "IMG2":
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

            return uS, rS, xS

        if cmdS == "TABLE":
            """table insert"""

            # print(f"{pthS=}")
            uS = rS = ""
            pthP = Path(pthS)  # path
            extS = pthP.suffix[1:]  # file extension
            parL = parS.split(",")
            titleS = parL[0].strip()  # title
            if titleS == "-":
                titleS = " "
            maxwI = int(parL[1].strip())  # max col. width
            alnS = parL[2].strip()  # col. alignment
            rowS = parL[3].strip()  # read rows
            alignD = {"s": "", "d": "decimal", "c": "center", "r": "right", "l": "left"}
            if parL[4].strip() == "_[T]":  # table number
                tnumI = int(self.labelD["tableI"])
                fillS = str(tnumI).zfill(2)
                utitlnS = "\nTable " + fillS + " - "
                rtitlnS = "\n**Table " + fillS + " -** "
                self.labelD["tableI"] = tnumI + 1
            else:
                utitlnS = " "
                rtitlnS = " "

            # pthxP = Path(*Path(pthS).parts[-3:])
            # pthxS = str(pthxP.as_posix())
            insP = Path(self.folderD["projP"])
            insP = Path(Path(insP) / pthS)
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
                return

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

            return uS, rS, xS

        if cmdS == "TEXT":
            """text file insert"""

            # print(f"{pthS=}")
            uS = rS = xS = ""
            pthP = Path(pthS)  # path
            extS = pthP.suffix[1:]  # file extension
            parL = parS.split(",")
            insP = Path(self.folderD["projP"])
            insP = Path(Path(insP) / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            # pthxP = Path(*Path(pthS).parts[-3:])

            with open(insP, "r") as fileO:
                fileL = fileO.readlines()

            uS = pS.rjust(self.labelD["widthI"]) + ubS
            rS = pS + rb2S
            xS = pS + rb2S

            return uS, rS, xS

        if cmdS == "VALUE":
            """values file insert"""

            vnumI = int(self.labelD["valueI"])
            fillS = str(vnumI).zfill(2)
            utitlnS = "\nValue Table " + fillS + " - " + parS.strip("_[V]")
            rtitlnS = "\n**Value Table " + fillS + " -** " + parS.strip("_[V]")
            self.labelD["valueI"] = vnumI + 1

            insP = Path(self.folderD["projP"])
            insP = Path(Path(insP) / pthS)
            insS = str(insP.as_posix())
            pS = " [file: " + pthS + "]" + "\n\n"
            with open(insP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
            # print(f"{readL=}")
            for iL in readL:  # add to valexp
                iS = ",".join(iL)
                self.labelD["valexpS"] += iS + "\n"
            tbL = []
            for vaL in readL:
                # print(f"{vaL=}")
                if len(vaL) < 4:
                    continue
                eqS = vaL[0].strip()
                varS = vaL[0].split(":=")[0].strip()
                valS = vaL[0].split(":=")[1].strip()
                descripS = vaL[1].strip()
                unit1S, unit2S = vaL[2], vaL[3]
                dec1S, dec2S = vaL[4], vaL[5]
                self.rivtpD[varS] = valS, unit1S, unit2S, dec1S, dec2S
                if unit1S != "-":
                    if type(eval(valS)) == list:
                        val1U = array(eval(valS)) * eval(unit1S)
                        val2U = [varS.cast_unit(eval(unit2S)) for varS in val1U]
                    else:
                        eqS = varS + " = " + valS
                        try:
                            exec(eqS, globals(), self.rivtvD)
                        except ValueError as ve:
                            print(f"A ValueError occurred: {ve}")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")
                        valU = eval(varS, globals(), self.rivtvD)
                        val1U = str(valU.cast_unit(eval(unit1S)))
                        val2U = str(valU.cast_unit(eval(unit2S)))
                else:
                    eqS = varS + " = " + valS
                    exec(eqS, globals(), self.rivtD)
                    valU = eval(varS)
                    val1U = str(valU)
                    val2U = str(valU)
                tbL.append([varS, val1U, val2U, descripS])

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
            rS = rtitlnS + pS + r2S + "\n"
            xS = rtitlnS + pS + rS + "\n"

            return uS, rS, xS
