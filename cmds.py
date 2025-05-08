# python #!
import csv
import fnmatch
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
from numpy import *  # noqa: F403
from PIL import Image
from reportlab.lib.utils import ImageReader
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import tags
from rivtlib.units import *  # noqa: F403

tabulate.PRESERVE_WHITESPACE = True


class Cmd:
    """
    commands

    | IMG  | rel. pth | caption, scale, (**[_F]**)        .png, .jpg
    | IMG2  | rel. pth | c1, c2, s1, s2, (**[_F]**)       .png, .jpg
    | TEXT | rel. pth |  plain; rivt                      .txt
    | TABLE | rel. pth | col width, l;c;r                 .csv, .txt, .xls
    | VALUES | rel. pth | col width, l;c;r                .csv, .txt, .xls
    || PUBLISH | rel. pth | col width, l;c;r              .csv, .txt, .xls
    || PREPEND | rel. pth | num; nonum                    .pdf
    || APPEND | rel. pth | num; nonum                     .pdf

                    if self.tS == "R":  # run commands
                        pass
                    elif self.tS == "I":  # insert commands
                        rviC = cmds.Cmd(folderD, labelD)
                        uS, rS, folderD, labelD = rviC.cmd_parse(cmdS, pthS, parS)
                        print(uS)  # stdout command
                        xutfS += uS
                        xrstS += rS
                        continue
                    elif self.tS == "V":  # values command
                        valsP = folderD["valsP"]
                        rvvC = rvals.CmdV(folderD, labelD, rivtpD, rivtvD)
                        uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                            cmdS, pthS, parS
                        )
                        print(uS)  # stdout valread
                        xutfS += uS
                        xrstS += rS
                        continue
                    elif self.tS == "T":  # tools command
                        continue
                    else:
                        pass



    """

    def __init__(self, folderD, labelD, rivtD):
        """commands that format to utf and reSt"""
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

    def cmd_parse(self, cmdS, pthS, parS):
        """parse a tagged line

        Args:
            cmdS (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        cC = globals()["Cmd"](self.folderD, self.labelD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(f"{cmdS=}")
        # print(f"{pthS=}")
        # print(f"{parS=}")

        return uS, rS, self.folderD, self.labelD self.rivtD

    def img(self, pthS, parS):
        """insert image from file

        Args:
            pthS (str): relative file path
            parS (str): parameters

        Returns:
            uS (str): formatted utf string
            r2S (str): formatted rst2 string
            rS (str): formatted reSt string
        """
        print(f"{parS=}")
        print(f"{pthS=}")
        parL = parS.split(",")
        capS = parL[0].strip()
        scS = parL[1].strip()
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / pthS)
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
        # utf
        uS = figS + capS + " [file: " + pthS + " ] \n"
        # rst2
        r2S = (
            "\n\n.. image:: "
            + insS
            + "\n"
            + "   :width: "
            + scS
            + "% \n"
            + "   :align: center \n"
            + "\n\n"
            + ".. class:: center \n\n"
            + figS
            + capS
            + "\n"
        )
        # rSt
        r2S = (
            "\n\n.. image:: "
            + insS
            + "\n"
            + "   :width: "
            + scS
            + "% \n"
            + "   :align: center \n"
            + "\n\n"
            + ".. class:: center \n\n"
            + figS
            + capS
            + "\n"
        )
        return uS, r2S

    def img2(self, pthS, parS):
        """insert side by side images from files

        Args:
            pthS(str): relative file path
            parS(str): parameters

        Returns:
            uS(str): formatted utf string
            rS(str): formatted reSt string
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

        return uS, rS

    def table(self, pthS, parS):
        """insert table from csv, xlsx or reSt file"""
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

        # utf
        uS = utlS + uS + "\n"
        # rst2
        r2S = rtlS + rS + "\n"
        # rst
        rS = rtlS + rS + "\n"

        return uS, r2S

    def text(self, pthS, parS):
        """insert text from file using block formats

        | text | file | type

        """

        # print(f"{pthS=}")
        uS = rS = ""
        pthP = Path(pthS)  # path
        extS = pthP.suffix[1:]  # file extension
        parL = parS.split(",")
        typeS = parL[0].strip()  # title
        insP = Path(self.folderD["projP"])
        insP = Path(Path(insP) / pthS)
        insS = str(insP.as_posix())
        pS = " [file: " + pthS + "]" + "\n\n"
        # pthxP = Path(*Path(pthS).parts[-3:])

        with open(insP, "r") as fileO:
            fileL = fileO.readlines()

        blkC = tags.Tag()
        match typeS:
            case "[[]]":
                ubS, rb2S = blkC.blkplain(fileL, self.folderD, self.labelD)
            case "[[S]]":
                ubS, rb2S = blkC.blkspace(fileL, self.folderD, self.labelD)
            case "[[C]]":
                ubS, rb2S = blkC.blkcode(fileL, self.folderD, self.labelD)
            case "[[L]]":
                ubS, rb2S = blkC.blklatex(fileL, self.folderD, self.labelD)
            case "[[O]]":
                ubS, rb2S = blkC.blkital(fileL, self.folderD, self.labelD)
            case "[[B]]":
                ubS, rb2S = blkC.blkbold(fileL, self.folderD, self.labelD)
            case "[[I]]":
                ubS, rb2S = blkC.blkitind(fileL, self.folderD, self.labelD)

        # utf
        uS = pS.rjust(self.labelD["widthI"]) + ubS
        # rst2
        r2S = pS + rb2S
        # rst
        rS = pS + rb2S

        return uS, r2S


class CmdV:
    """value commands format to utf8 or reSt

    Commands:
        a = 1+1 | unit | reference
        | VALREAD | rel. pth |  dec1
    """

    def __init__(self, folderD, labelD, rivtpD, rivtvD):
        """commands that format a utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.rivtvD = rivtvD
        self.rivtpD = rivtpD
        self.folderD = folderD
        self.labelD = labelD

    def cmd_parse(self, cmdS, pthS, parS):
        """parse tagged line

        Args:
            cmdS (str): command
            pthS (str): path or equation string
            parS (str): command parameters

        Returns:
            utS: formatted utf string
        """

        # print(f"{cmdS=}")
        # print(f"{pthS=}")
        # print(f"{parS=}")

        cC = globals()["CmdV"](self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(self.rivtvD)
        return uS, rS, self.folderD, self.labelD, self.rivtpD, self.rivtvD

    def values(self, pthS, parS):
        """import values from csv files, update rivtD

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        if "_[V]" in parS.strip():  # table number
            vnumI = int(self.labelD["valueI"])
            fillS = str(vnumI).zfill(2)
            utitlnS = "\nValue Table " + fillS + " - " + parS.strip("_[V]")
            rtitlnS = "\n**Value Table " + fillS + " -** " + parS.strip("_[V]")
            self.labelD["valueI"] = vnumI + 1
        else:
            utitlnS = "\nValue Table  - " + parS.strip()
            rtitlnS = "\n**Value Table -** " + parS.strip()

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
        vC = CmdV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)  # format table
        r2S = rS

        # pthxS = str(Path(*Path(pthS).parts[-3:]))
        pS = "[from file: " + pthS + "]" + "\n\n"
        uS = utitlnS + pS + uS + "\n"
        r2S = rtitlnS + pS + r2S + "\n"
        rS = rtitlnS + pS + rS + "\n"

        return uS, r2S

    def valtable(self, tbL, hdrL, alignL, tblfmt):
        """format table"""
        # print(f"{tbL=}")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL, tablefmt=tblfmt, headers=hdrL, showindex=False, colalign=alignL
            )
        )
        uS = r2S = rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return uS, r2S

    def equate(self, eqS, parS):
        """format equation ' = '

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        wI = self.labelD["widthI"]

        spS = eqS.strip()
        spS = spS.replace(":=", "=")
        refS = parS.split("|")[0].strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

        except:
            pass
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # utf
        lineS = textwrap.indent(lineS, "    ")
        refS = refS.rjust(self.labelD["widthI"])
        uS = refS + "\n" + lineS + "\n\n"
        # rst2
        r2S = "\n\n..  code:: \n\n\n" + refS + "\n" + lineS + "\n\n"
        # rst
        rS = ".. raw:: math\n\n   " + lineS + "\n"

        return uS, r2S

    def equtable(self, eqS, parS):
        """format equation table, update rivtD

        Args:
            eqS (_type_): _description_
            parS (_type_): _description_

        Returns:
            _type_: _description_
        """
        vaL = []
        wI = self.labelD["widthI"]
        eqS = eqS.strip()
        eqS = eqS.replace(":=", "=")
        refS = parS.split("|")
        varS = eqS.split("=")[0].strip()
        valS = eqS.split("=")[1].strip()
        descripS = refS[0].strip()
        unitL = refS[1].split(",")
        unit1S, unit2S = unitL[0].strip(), unitL[1].strip()
        decL = refS[2].split(",")
        dec1S, dec2S = decL[0].strip(), decL[1].strip()
        if unit1S != "-":
            try:
                exec(eqS, globals(), self.rivtvD)
                # print(f"{self.rivtvD=}")
            except ValueError as ve:
                print(f"A ValueError occurred: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            try:
                exec(eqS, globals(), self.rivtD)
            except ValueError as ve:
                print(f"A ValueError occurred: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            valU = eval(varS, globals(), self.rivtD)
            val1U = str(valU)
            val2U = str(valU)
        eqxS = eqS.split("=")[1]
        symeqO = sp.sympify(eqxS, _clash2, evaluate=False)
        symaO = symeqO.atoms(sp.Symbol)
        numvarI = len(symaO) + 1
        tbl1L = []
        tbl2L = []
        hdr1L = []
        hdr1L.append(varS)
        for vS in symaO:
            hdr1L.append(str(vS))
        fmt1S = "%." + dec1S + "f"
        fmt2S = "%." + dec2S + "f"
        varU = eval(varS, globals(), self.rivtvD)
        varU.set_format(value_format=fmt1S, auto_norm=True)
        val1U = str(varU.cast_unit(eval(unit1S)))
        val2U = str(varU.cast_unit(eval(unit2S)))
        tbl1L.append(val1U)
        tbl2L.append(val2U)
        self.rivtpD[varS] = (val1U, unit1S, unit2S, dec1S, dec2S)
        for aO in symaO:
            # print(self.rivtpD)
            unit1S = self.rivtpD[str(aO)][1]
            unit2S = self.rivtpD[str(aO)][2]
            a1U = eval(str(aO), globals(), self.rivtvD)
            a1U.set_format(value_format=fmt2S, auto_norm=True)
            val1U = str(a1U.cast_unit(eval(unit1S)))
            a2U = eval(str(aO), globals(), self.rivtvD)
            a2U.set_format(value_format=fmt2S, auto_norm=True)
            val2U = str(a2U.cast_unit(eval(unit2S)))
            tbl1L.append(val1U)
            tbl2L.append(val2U)
        tblL = [tbl1L]
        tblL.append(tbl2L)
        alignL = []
        tblfmt = "rst"
        for nI in range(numvarI):
            alignL.append("center")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tblL, tablefmt=tblfmt, headers=hdr1L, showindex=False, colalign=alignL
            )
        )
        uS = output.getvalue()
        rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        refS = parS.split("|")
        eqS = eqS.replace("=", ":=")
        iS = eqS + "," + ",".join(refS)
        self.labelD["valexpS"] += iS + "\n"

        return uS, rS


class TagV:
    """format to utf8 or reSt

    Functions:
            _[E]                    equation
            _[F]                    figure
            _[T]                    table
            _[A]                    page
            _[[V]]                  values
            _[[Q]]                  quit
    """

    def __init__(self, folderD, labelD, rivtpD, rivtvD):
        """tags that format to utf and reSt"""
        self.rivtpD = rivtpD
        self.rivtvD = rivtvD
        self.folderD = folderD
        self.labelD = labelD
        # print(folderD)
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

    def tag_parse(self, tagcmdS, blockL):
        """parse a tagged line

        Args:
            tagcmd (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        tC = TagV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        uS, rS = functag(blockL)
        # print(f"{tcmdS=}")
        # print(self.rivtpD)
        # print(self.rivtvD)

        return uS, rS, self.folderD, self.labelD, self.rivtpD, self.rivtvD

    def valblock(self, blockL):
        """format values
        Args:
            blockL (list): _description_
        Returns:
            : _description_
        """
        vaL = []
        tbL = []
        # print(f"{blockL=}")
        for vaS in blockL:
            # print(f"{vaS=}")
            vaL = vaS.split("|")
            # print(f"{vaL=}")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if ":=" not in vaL[0]:
                continue
            eqS = vaL[0].strip()
            eqS = eqS.replace(":=", "=")
            varS = eqS.split("=")[0].strip()
            valS = eqS.split("=")[1].strip()
            descripS = vaL[1].strip()
            unitL = vaL[2].split(",")
            unit1S, unit2S = unitL[0], unitL[1]
            decL = vaL[3].split(",")
            dec1S, dec2S = decL[0], decL[1]
            if unit1S != "-":
                try:
                    exec(eqS, globals(), self.rivtvD)
                except ValueError as ve:
                    print(f"A ValueError occurred: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                valU = eval(varS, {}, self.rivtvD)
                val1U = str(valU.cast_unit(eval(unit1S)))
                val2U = str(valU.cast_unit(eval(unit2S)))
                # print(f"{self.rivtvD=}")
            else:
                cmdS = varS + " = " + valS
                exec(cmdS, globals(), self.rivtvD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])
            self.rivtpD[varS] = valS, unit1S, unit2S, dec1S, dec2S

        for vaS in blockL:
            vaL = vaS.split("|")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if "=" not in vaL[0]:
                continue
            iS = ",".join(vaL)
            self.labelD["valexpS"] += iS + "\n"

        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]

        vC = CmdV(self.folderD, self.labelD, self.rivtpD, self.rivtvD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)

        return uS + "\n", rS + "\n"
