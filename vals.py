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

import tabulate
from PIL import Image
from IPython.display import Image as _Image
from IPython.display import display as _display
from numpy import *
import sympy as sp
from sympy.abc import _clash2
from sympy.core.alphabets import greeks
from sympy.parsing.latex import parse_latex

from rivtlib import tags, cmds
from rivtlib.units import *

tabulate.PRESERVE_WHITESPACE = True


class CmdV:
    """ value commands format to utf8 or reSt

    Commands:
        a = 1+1 | unit | reference
        | VREAD | rel. pth |  dec1
    """

    def __init__(self, folderD, labelD, rivtD):
        """commands that format a utf doc

        Args:
            paramL (list): _description_
            labelD (dict): _description_
            folderD (dict): _description_
            localD (dict): _description_
        """

        self.rivtD = rivtD
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

        cC = globals()['CmdV'](self.folderD, self.labelD, self.rivtD)
        ccmdS = cmdS.lower()
        functag = getattr(cC, ccmdS)
        uS, rS = functag(pthS, parS)

        # print(self.rivtD)
        return uS, rS, self.folderD, self.labelD, self.rivtD

    def rivttype(self):
        pass

    def valread(self, pthS, parS):
        """ import values from csv files, update rivtD

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        locals().update(self.rivtD)
        pathP = Path(self.folderD["projP"] / "vals" / pthS)
        with open(pathP, "r") as csvfile:
            readL = list(csv.reader(csvfile))
        # print(f"{readL=}")
        # add to valexp
        for iL in readL:
            iS = ",".join(iL)
            self.labelD["valexpS"] += iS+"\n"
        tbL = []
        for vaL in readL:
            # print(f"{vL=}")
            if len(vaL[0].strip()) < 1:
                continue
            if "=" not in vaL[0]:
                continue
            cmdS = vaL[0].strip()
            varS = vaL[0].split("=")[0].strip()
            valS = vaL[0].split("=")[1].strip()
            descripS = vaL[1].strip()
            unit1S, unit2S = vaL[2].strip(), vaL[3].strip()
            dec1I, dec2I = int(vaL[4]), int(vaL[5])
            loc = {"x": 1}
            loc[varS] = loc.pop('x')
            if unit1S != "-":
                if type(eval(valS)) == list:
                    val1U = array(eval(valS)) * eval(unit1S)
                    val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
                else:
                    cmdS = vaL[0].strip()
                    # print(f"{cmdS=}")
                    try:
                        exec(cmdS, globals(), loc)
                    except ValueError as ve:
                        print(f"A ValueError occurred: {ve}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                    exec(cmdS)
                    valU = eval(varS, globals(), loc)
                    val1U = str(valU.cast_unit(eval(unit1S)))
                    val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + " = " + valS
                exec(cmdS, globals(), locals())
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            self.rivtD.update(loc)
            tbL.append([varS, val1U, val2U, descripS])

        tblfmt = 'rst'
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]
        vC = CmdV(self.folderD, self.labelD, self.rivtD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)
        pS = "\n" + "[values read from file: " + pthS + "]"
        uS += pS
        rS += pS

        return uS, rS

    def valtable(self, tbL, hdrL, alignL, tblfmt):
        """ format table

        """
        # print(f"{tbL=}")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tbL, tablefmt=tblfmt, headers=hdrL,
                showindex=False,  colalign=alignL))
        uS = rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return uS, rS

    def valwrite(self, pthS, parS):
        pass

    def eqform(self, eqS, parS):
        """format equation ' = '

        Args:
            lineS (_type_): _description_
            labelD (_type_): _description_
            folderD (_type_): _description_
        Returns:
            _type_: _description_
        """

        alignaL = ["left", "right", "right", "left"]
        hdreL = ["variable", "value", "[value]", "description [eq. number]"]
        aligneL = ["left", "right", "right", "left"]
        wI = self.labelD["widthI"]

        spS = eqS.strip()
        refS = parS.split("|")[0].strip()
        try:
            spL = spS.split("=")
            spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"

        except:
            pass
        refS = refS.rjust(wI)
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        # utf
        uS = refS + "\n" + lineS + "\n\n"
        # rst
        rS = ".. raw:: math\n\n   " + lineS + "\n"

        return uS, rS

    def eqtable(self, eqS, parS):
        """format equation table, update rivtD

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string
        :rtype: string
        """
        vaL = []
        wI = self.labelD["widthI"]
        eqS = eqS.strip()
        refS = parS.split("|")
        varS = eqS.split("=")[0].strip()
        valS = eqS.split("=")[1].strip()
        descripS = refS[0].strip()
        unitL = refS[1].split(",")
        unit1S, unit2S = unitL[0], unitL[1]
        decL = refS[2].split(",")
        dec1I, dec2I = int(decL[0]), int(decL[1])
        if unit1S != "-":
            try:
                # print("----", eqS)
                exec(eqS, globals(), self.rivtD)
            except ValueError as ve:
                print(f"A ValueError occurred: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            cmdS = varS + " = " + valS
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
        fmtS = "%." + str(dec1I) + "f"
        n1U = eval(varS, globals(), self.rivtD)
        n1U.set_format(value_format=fmtS, auto_norm=True)
        val1U = str(n1U.cast_unit(eval(unit1S)))
        val2U = str(n1U.cast_unit(eval(unit2S)))
        tbl1L.append(val1U)
        tbl2L.append(val2U)
        fmtS = "%." + str(dec2I) + "f"
        for aO in symaO:
            n1U = eval(str(aO), globals(), self.rivtD)
            n1U.set_format(value_format=fmtS, auto_norm=True)
            tbl1L.append(n1U)
            tbl2L.append(n1U)
        tblL = [tbl1L]
        tblL.append(tbl2L)
        tblfmt = 'rst'
        alignL = []
        for nI in range(numvarI):
            alignL.append("center")
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(tabulate.tabulate(tblL, tablefmt=tblfmt, headers=hdr1L,
                                       showindex=False,  colalign=alignL))
        uS = rS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        refS = parS.split("|")
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

    def __init__(self,  folderD, labelD, rivtD):
        """tags that format to utf and reSt

        """
        self.rivtD = rivtD
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

    def tag_parse(self, tagcmdS, blockL):
        """parse a tagged line

        Args:
            tagcmd (_type_): _description_
            lineS (_type_): _description_

        Returns:
            utS: formatted utf string
        """

        tC = TagV(self.folderD, self.labelD, self.rivtD)
        tcmdS = str(tagcmdS)
        functag = getattr(tC, tcmdS)
        uS, rS = functag(blockL)
        # print(f"{tcmdS=}")
        # print(self.rivtD)

        return uS, rS, self.folderD, self.labelD, self.rivtD

    def values(self, blockL):
        """return value table, update rivtD

        """

        locals().update(self.rivtD)
        vaL = []
        tbL = []
        # print(f"{blockL=}")
        for vaS in blockL:
            # print(f"{vaS=}")
            vaL = vaS.split("|")
            # print(f"{vaL=}")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if "=" not in vaL[0]:
                continue
            cmdS = vaL[0].strip()
            varS = vaL[0].split("=")[0].strip()
            valS = vaL[0].split("=")[1].strip()
            descripS = vaL[1].strip()
            unitL = vaL[2].split(",")
            unit1S, unit2S = unitL[0], unitL[1]
            decL = vaL[3].split(",")
            dec1I, dec2I = decL[0], decL[1]
            if unit1S != "-":
                try:
                    exec(cmdS, globals(), self.rivtD)
                except ValueError as ve:
                    print(f"A ValueError occurred: {ve}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                # print(globals())
                valU = eval(varS, {}, self.rivtD)
                val1U = str(valU.cast_unit(eval(unit1S)))
                val2U = str(valU.cast_unit(eval(unit2S)))
            else:
                cmdS = varS + " = " + valS
                exec(cmdS, globals(), self.rivtD)
                valU = eval(varS)
                val1U = str(valU)
                val2U = str(valU)
            tbL.append([varS, val1U, val2U, descripS])

        for vaS in blockL:
            vaL = vaS.split("|")
            if len(vaL) != 4 or len(vaL[0]) < 1:
                continue
            if "=" not in vaL[0]:
                continue
            iS = ",".join(vaL)
            self.labelD["valexpS"] += iS + "\n"

        tblfmt = 'rst'
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "right", "right", "left"]

        vC = CmdV(self.folderD, self.labelD, self.rivtD)
        uS, rS = vC.valtable(tbL, hdrvL, alignL, tblfmt)
        return uS, rS
