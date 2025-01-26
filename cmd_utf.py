#
import sys
import csv
import textwrap
import logging
from pathlib import Path
import tabulate
import csv
import logging
import warnings
import fnmatch
import numpy.linalg as la
import pandas as pd
import sympy as sp
import matplotlib.pyplot as plt
import configparser
from io import StringIO
from numpy import *
from sympy.parsing.latex import parse_latex
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from tabulate import tabulate
from pathlib import Path
from datetime import datetime
from rivtlib import parse
from rivtlib.units import *


class CmdUTF():

    def __init__(self, paramL, labelD, folderD,  localD):
        """commands to format utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.localD = localD
        self.folderD = folderD
        self.labelD = labelD
        self.widthII = labelD["widthI"] - 1
        self.paramL = paramL
        self.errlogP = folderD["errlogP"]

        baseS = self.labelD["baseS"]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + baseS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def cmd_parse(cmdL, apiS, insertB):
        """_summary_
        """

        label1 = cmdL[0]
        path1 = cmdL[1]
        param1 = cmdL[2]

        if filetype == "pdf":
            cmd_append(x)
        elif filetype == "jpg" or filetype == "png" or filetype == "svg":
            cmd_image(x)
        elif filetype == "csv" and apiS == "I":
            cmd_table(x)
        elif filetype == "csv" and apiS == "V":
            cmd_data(x)
        elif filetype == "csv" and apiS == "I":
            cmd_append(x)
        elif filetype == "csv" and apiS == "V":
            cmd_append(x)
        elif filetype == "csv" and apiS == "I":
            cmd_append(x)
        elif filetype == "csv" and apiS == "V":
            cmd_append(x)
        elif filetype == "csv" and apiS == "I":
            cmd_append(x)
        elif filetype == "csv" and apiS == "V":
            cmd_append(x)

    def append(self):
        """_summary_
        """
        pass

    def assign(self):
        """import values from files

        """

        hdrL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        plenI = 2                       # number of parameters
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return
        if self.paramL[0] == "data":
            folderP = Path(self.folderD["dataP"])
        else:
            folderP = Path(self.folderD["dataP"])
        fileP = Path(self.paramL[1].strip())
        pathP = Path(folderP / fileP)
        valL = []
        fltfmtS = ""
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        for vaL in readL[1:]:
            if len(vaL) < 5:
                vL = len(vaL)
                vaL += [""] * (5 - len(vL))  # pad values
            varS = vaL[0].strip()
            valS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            descripS = vaL[4].strip()
            if not len(varS):
                valL.append(["_ _", "_ _", "_ _", "Total"])  # totals
                continue
            val1U = val2U = array(eval(valS))
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = varS + "= " + valS + "*" + unit1S
                    exec(cmdS, globals(), locals())
                    valU = eval(varS)
                    val1U = str(valU.number()) + " " + str(valU.unit())
                    val2U = valU.cast_unit(eval(unit2S))
            valL.append([varS, val1U, val2U, descripS])

        rstS = self.vtable(valL, hdrL, "rst", alignL)

        # print(mdS + "\n")
        return rstS

    def github(self):
        """_summary_
        """
        pass

    def txthtml(self, txtfileL):
        """9a _summary_

        :return: _description_
        :rtype: _type_
        """
        txtS = ""
        flg = 0
        for iS in txtfileL:
            if "src=" in iS:
                flg = 1
                continue
            if flg == 1 and '"' in iS:
                flg = 0
                continue
            if flg == 1:
                continue
            txtS += " "*4 + iS
            txtS = htm.html2text(txtS)
            mdS = txtS.replace("\n    \n", "")

            return mdS

    def txttex(self, txtfileS, txttypeS):
        """9b _summary_

        :return: _description_
        :rtype: _type_
        """

        soup = TexSoup(txtfileS)
        soupL = list(soup.text)
        soupS = "".join(soupL)
        soup1L = []
        soupS = soupS.replace("\\\\", "\n")
        soupL = soupS.split("\n")
        for s in soupL:
            sL = s.split("&")
            sL = s.split(">")
            try:
                soup1L.append(sL[0].ljust(10) + sL[1])
            except:
                soup1L.append(s)
        soupS = [s.replace("\\", " ") for s in soup1L]
        soupS = "\n".join(soup1L)

        return soupS

    def project(self):
        """insert project information from txt

            :return lineS: utf text
            :rtype: str
        """

        print("< for project data see PDF output >")
        return "(... for project data - see PDF report output ...)"

    def image(self):
        """insert image(s) from files

        """
        utfS = ""
        iL = self.paramL
        if len(iL[0].split(",")) == 1:
            file1S = iL[0].strip()
            #  file1S = file1S.replace("/", "|")
            utfS = "< Figure path: " + file1S + "> \n"
        elif len(iL[0].split(",")) == 2:
            iL = iL[0].split(",")
            file1S = iL[0].strip()
            file2S = iL[1].strip()
            utfS = "Figure path: " + file1S + "\n" + "Figure path: " + file2S + "\n"
        print(utfS)
        return utfS

    def table(self):
        """insert table from csv or xlsx file

            :return lineS: md table
            :rtype: str
        """

        tableS = ""
        alignD = {"s": "", "d": "decimal",
                  "c": "center", "r": "right", "l": "left"}
        plenI = 2
        if len(self.paramL) != plenI:
            logging.info(
                f"{self.cmdS} command not evaluated: {plenI} parameters required")
            return

        fileP = Path(self.paramL[0].strip())
        prfxP = self.folderD["docpathP"]
        if str(fileP)[0:4] == "data":
            pathP = Path(prfxP, fileP)                       # file path
        elif str(fileP)[0:4] == "data":
            pass
        else:
            pass
        maxwI = int(self.paramL[1].split(",")[0])        # max column width
        keyS = self.paramL[1].split(",")[1].strip()
        alignS = alignD[keyS]
        extS = pathP.suffix[1:]
        # print(f"{extS=}")
        if extS == "csv":                               # read csv file
            with open(pathP, "r") as csvfile:
                readL = list(csv.reader(csvfile))
        elif extS == "xlsx":                            # read xls file
            pDF1 = pd.read_excel(pathP, header=None)
            readL = pDF1.values.tolist()
        else:
            logging.info(
                f"{self.cmdS} not evaluated: {extS} file not processed")
            return

        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate(
            readL,
            tablefmt="rst",
            headers="firstrow",
            numalign="decimal",
            maxcolwidths=maxwI,
            stralign=alignS))

        tableS = output.getvalue()
        sys.stdout = old_stdout

        print(tableS)
        return tableS

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

    def vals(self):
        """import data from files


            :return lineS: md table
            :rtype: str
        """

        locals().update(self.rivtD)
        valL = []
        if len(vL) < 5:
            vL += [""] * (5 - len(vL))  # pad command
        valL.append(["variable", "values"])
        vfileS = Path(self.folderD["cpath"] / vL[2].strip())
        vecL = eval(vL[3].strip())
        with open(vfileS, "r") as csvF:
            reader = csv.reader(csvF)
        vL = list(reader)
        for i in vL:
            varS = i[0]
            varL = array(i[1:])
            cmdS = varS + "=" + str(varL)
            exec(cmdS, globals(), locals())
            if len(varL) > 4:
                varL = str((varL[:2]).append(["..."]))
            valL.append([varS, varL])
        hdrL = ["variable", "values"]
        alignL = ["left", "right"]
        self.vtable(valL, hdrL, "rst", alignL)
        self.rivtD.update(locals())

        return

    def vtable(self, tbL, hdrL, tblfmt, alignL):
        """write value table"""

        # locals().update(self.rivtD)
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate(
                tbL, headers=hdrL, tablefmt=tblfmt,
                showindex=False, colalign=alignL
            )
        )
        mdS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return mdS

        # self.calcS += mdS + "\n"
        # self.rivtD.update(locals())
