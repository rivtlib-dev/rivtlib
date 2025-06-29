# python #!
import csv
import sys
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import tabulate
from IPython.display import display as _display
from PIL import Image

from rivtlib.rvunits import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """select commands

    Run     WIN - Windows command script
            OSX - OSX command script
            LINUX - Linux command script

    Insert  TEXT - insert text from file
            IMG - insert image from file
            IMG2 - insert side by side images from files
            TABLE - insert table from file


    Values  IMG - insert image from file
            IMG2 - insert side by side images from files
            TABLE - insert table from file
            VALUE - insert values from file

    Tools   PYTHON - python script


    |TEXT| rel. pth |  plain; rivt
    |IMG| rel. pth | scale factor, caption (_[F])       .png, .jpg
    |IMG2| rel. pth, rel. pth | sf1, sf2, c1, c2 (_[F]) .png, .jpg
    |TABLE| rel. pth | col width, l;c;r, title (_[T])   .csv, .xls, .txt
    |VALUE| rel. pth | col width, l;c;r, title (_[T])   .csv
    |WIN| rel. pth | print, noprint
    |OSX| rel. pth | print, noprint
    |LINUX| rel. pth | print, noprint
    |PYTHON| rel. pth | print, noprint

    """

    def __init__(self, folderD, labelD, rivtD, rivtL, parL):
        """an Insert or Value object
        Args:
            folderD (dict): folders
            labelD (dict): labels
            rivtD (dict): values
            rivtL (list): values for export
            parL (list): command parameters
        Vars:
            uS (str): utf string
            rS (str): rst2pdf string
            xS (str): reST string
        """
        # region
        self.folderD = folderD
        self.labelD = labelD
        self.rivtD = rivtD
        self.rivtL = rivtL
        self.pthS = parL[1].strip()
        self.parS = parL[2].strip()
        self.uS = ""
        self.rS = ""
        self.xS = ""
        # endregion

    def cmdx(self, cmdS):
        """parse section

        Args:
            cmdS (str): command
        Returns:
            uS, rS, xS, folderD, labelD, rivtD, rivtL
        """
        # region
        method = getattr(self, cmdS)
        method()

        return (
            self.uS,
            self.rS,
            self.xS,
            self.folderD,
            self.labelD,
            self.rivtD,
            self.rivtL,
        )
        # endregion

    def IMG(self):
        """insert image

        |IMG| rel. pth | scale factor, caption (_[F])
        """
        # region
        if "_[F]" in self.parS:
            numS = str(self.labelD["figI"])
            self.labelD["figI"] = int(numS) + 1
            figuS = "Fig. " + numS + " - "
            figrS = "**Fig. " + numS + " -**"

        else:
            figuS = " "
        # print(f"{parS=}")
        # print(f"{pthS=}")
        parL = self.parS.split(",")
        pthS = parL[0].strip()
        capS = parL[0].strip()
        scS = parL[1].strip()
        insP = Path(self.folderD["projP"] / "source" / pthS)
        insS = str(insP.as_posix())
        if capS == "-":
            capS = " "
        # pthxS = str(Path(*Path(self.folderD["rivP"]).parts[-1:]))
        try:
            img1 = Image.open(self.pthS)
            _display(img1)
        except:  # noqa: E722
            pass
        self.uS = figuS + capS + " [file: " + self.pthS + " ] \n"
        self.rS = self.xS = (
            "\n\n.. image:: "
            + insS
            + "\n"
            + "   :width: "
            + scS
            + "% \n"
            + "   :align: center \n\n\n"
            + ".. class:: center \n\n"
            + figrS
            + capS
            + "\n"
        )
        # endregion

    def IMG2(self):
        """insert side by side images

        |IMG2| rel. pth, rel. pth | sf1, sf2, c1, c2 (_[F])
        """
        # region
        # print(f"{parS=}")
        parL = self.parS.split(",")
        fileL = self.pthS.split(",")
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

        self.uS = "<" + cap1S + " : " + str(file1P) + "> \n"
        self.rS = (
            "\n.. image:: "
            + self.pthS
            + "\n"
            + "   :scale: "
            + scale1S
            + "%"
            + "\n"
            + "   :align: center"
            + "\n\n"
        )
        # endregion

    def TABLE(self):
        """insert table

        |TABLE| rel. pth | col width, l;c;r, title (_[T])
        """
        # region
        # print(f"{pthS=}")
        if "_[T]" in self.parS:
            tnumI = int(self.labelD["tableI"])
            fillS = str(tnumI)
            utitlnS = "\nTable " + fillS + " - "
            rtitlnS = "\n**Table " + fillS + " -** "
            self.labelD["tableI"] = tnumI + 1
            parS = (self.parS.replace("_[T]", " ")).strip()
        else:
            utitlnS = " "
            rtitlnS = " "
        pthP = Path(self.pthS)  # path
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
        insP = Path(self.folderD["srcP"], self.pthS)
        pS = " [file: " + self.pthS + "]" + "\n\n"
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
            pDF1 = pd.read_excel(self.pthS, header=None)
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

        self.uS = utlS + uS + "\n"
        self.rS = rtlS + rS + "\n"
        self.xS = rtlS + rS + "\n"
        # endregion

    def TEXT(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.folderD["srcP"], self.pthS)
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.rS = fileS
        self.xS = fileS
        # endregion

    def VALUE(self):
        """insert values

        |VALUE| rel. pth | title (_[T])
        """
        # region
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        fillS = str(tnumI)
        utitlnS = "\nTable " + fillS + " - " + self.parS.strip("_[T]")
        rtitlnS = "\n**Table " + fillS + " -** " + self.parS.strip("_[T]")
        insP = Path(self.folderD["srcP"], self.pthS)
        pS = " [file: " + self.pthS + "]" + "\n\n"
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
            fmt1S = "Unum.set_format(value_format='%." + dec1S + "f', auto_norm=True)"
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
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()
        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        pS = "[from file: " + self.pthS + "]" + "\n\n"
        self.uS = utitlnS + pS + outS + "\n"
        self.rS = rtitlnS + pS + outS + "\n"
        self.xS = rtitlnS + pS + outS + "\n"
        # endregion

    def WIN(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.rS = fileS
        self.xS = fileS
        # endregion

    def OSX(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.rS = fileS
        self.xS = fileS
        # endregion

    def LINUX(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.rS = fileS
        self.xS = fileS
        # endregion

    def PYTHON(self):
        """insert text

        |TEXT| rel. pth |  plain; rivt
        """
        # region
        # print(f"{pthS=}")
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / "source" / self.pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + self.pthS + "]" + "\n\n"
        parL = self.parS.split(",")
        # extS = pthP.suffix[1:]  # file extension
        # pthxP = Path(*Path(pthS).parts[-3:])
        with open(insP, "r") as fileO:
            fileS = fileO.read()
        self.uS = fileS
        self.rS = fileS
        self.xS = fileS
        # endregion
