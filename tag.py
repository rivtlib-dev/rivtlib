#
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
from rivtlib import cmd


tabulate.PRESERVE_WHITESPACE = True


class Tag():
    """subclass - convert rivt tags to MD or reST

            ============================ =======================================
            tags                                   description 
            ============================ =======================================

            I,V line format:
            text _[h1-h6]                     heading type        
            text _[b]                       bold 
            text _[i]                       italic
            text _[c]                       center
            text _[bic]                     combined formatting
            text _[u]                       underline   
            text _[r]                       right justify
            text _[l]                       LaTeX math
            text _[s]                       sympy math
            text _[l,s;bic]                 combined formatting
            text _[e]                       equation label and autonumber
            text _[f]                       figure caption and autonumber
            text _[t]                       table title and autonumber
            text _[#]                       footnote and autonumber
            text _[d]                       footnote description 
            _[line]                         horizontal line
            _[page]                         new page
            _[address, label]               url, internal reference
            I,V  block format:          
            _[[b]]                          bold
            _[[c]]                          center
            _[[i]]                          italic
            _[[p]]                          plain  
            _[[bcip]]                       combined formatting
            _[[l]]                          LaTeX
            _[[h]]                          HTML 
            _[[q]]                          quit block

        """

    def tag_parse(self, tagS):
        """convert rivt tags to md

        """

        if tagS in self.tagsD:
            return eval("self." + self.tagsD[tagS] + "()")
        if "b" in tagS and "c" in tagS:
            return self.boldcenter()
        if "b" in tagS and "i" in tagS:
            return self.bolditalic()
        if "b" in tagS and "i" in tagS and "c" in tagS:
            return self.bolditaliccenter()
        if "i" in tagS and "c" in tagS:
            return self.italiccenter()

    def declare(self):
        """declare variable values

        :return: _description_
        :rtype: _type_
        """
        locals().update(self.localD)
        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descripS = str(self.labelD["descS"])
        if unit1S.strip() != "-":
            cmdS = varS + "= " + valS + "*" + unit1S
        else:
            cmdS = varS + "= as_unum(" + valS + ")"

        exec(cmdS, globals(), locals())
        self.localD.update(locals())
        return [varS, valS, unit1S, unit2S, descripS]

    def assign(self):
        """assign value to equation

        :return: _description_
        :rtype: _type_
        """
        locals().update(self.localD)
        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descS = str(self.labelD["eqlabelS"])
        precI = int(self.labelD["descS"])  # trim result
        fmtS = "%." + str(precI) + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())

                val1U = eval(varS).cast_unit(eval(unit1S))
                val1U.set_format(value_format=fmtS, auto_norm=True)
                val2U = val1U.cast_unit(eval(unit2S))
                # print(f"{val1U=}")
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)

        spS = "Eq(" + varS + ",(" + valS + "))"
        mdS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        mdS = "\n" + mdS + "\n"
        eqL = [varS, valS, unit1S, unit2S, descS]

        print(mdS)                      # print equation

        subS = " "
        if self.labelD["subB"]:
            subS = self.vsub(eqL, precI, varS, val1U)
            print(subS)                  # print with substition

        self.localD.update(locals())
        return [eqL, mdS + "\n" + subS + "\n\n"]

    def vsub(self, eqL, precI, varS, val1U):
        """substitute variables with values

        :param eqL: _description_
        :type eqL: _type_
        :param precI: _description_
        :type precI: _type_
        :param varS: _description_
        :type varS: _type_
        :param val1U: _description_
        :type val1U: _type_
        :return: _description_
        :rtype: _type_
        """

        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        # print(f"{symeq=}")
        symat = symeq.atoms(sp.Symbol)
        # print(f"{symat=}")
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            # print(f"{n1O=}")
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            # print(f"{n1U=}")
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            # print(f"{new_var=}")
            with sp.evaluate(False):
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
            # print(f"{symeq=}")
        out2 = sp.pretty(symeq, wrap_line=False)
        # print('out2a\n', out2)
        # symat1 = symeq.atoms(sp.Symbol)  # adjust character length
        # for n2 in symat1:
        #     orig_var = str(n2).replace("~", "")
        #     orig_var = orig_var.replace("|", "_")
        #     expr = eval(varL[1])
        #     if type(expr) == float:
        #         form = "{%." + str(precI) + "f}"
        #         symeval1 = form.format(eval(str(expr)))
        #     else:
        #         try:
        #             symeval1 = eval(
        #                 orig_var.__str__()).__str__()
        #         except:
        #             symeval1 = eval(orig_var.__str__()).__str__()
        #     out2 = out2.replace(n2.__str__(), symeval1)   # substitute
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        self.localD.update(locals())
        mdS = out3 + "\n\n"

        return mdS

    def declare(self):
        """ := declare variable value

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
        """
        locals().update(self.localD)
        varS = str(self.lineS).split(":=")[0].strip()
        valS = str(self.lineS).split(":=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descripS = str(self.labelD["descS"])
        if unit1S.strip() != "-":
            cmdS = varS + "= " + valS + "*" + unit1S
        else:
            cmdS = varS + "= as_unum(" + valS + ")"

        exec(cmdS, globals(), locals())

        self.localD.update(locals())

        return [varS, valS, unit1S, unit2S, descripS]

    def assign(self):
        """ = assign result to equation

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
        """
        locals().update(self.localD)
        varS = str(self.lineS).split("=")[0].strip()
        valS = str(self.lineS).split("=")[1].strip()
        unit1S = str(self.labelD["unitS"]).split(",")[0]
        unit2S = str(self.labelD["unitS"]).split(",")[1]
        descS = str(self.labelD["eqlabelS"])
        precI = int(self.labelD["descS"])  # trim result
        fmtS = "%." + str(precI) + "f"
        if unit1S.strip() != "-":
            if type(eval(valS)) == list:
                val1U = array(eval(valS)) * eval(unit1S)
                val2U = [q.cast_unit(eval(unit2S)) for q in val1U]
            else:
                cmdS = varS + "= " + valS
                exec(cmdS, globals(), locals())

                val1U = eval(varS).cast_unit(eval(unit1S))
                val1U.set_format(value_format=fmtS, auto_norm=True)
                val2U = val1U.cast_unit(eval(unit2S))
        else:
            cmdS = varS + "= as_unum(" + valS + ")"
            exec(cmdS, globals(), locals())

            valU = eval(varS)
            valdec = round(valU.number(), precI)
            val1U = val2U = str(valdec)
        spS = "Eq(" + varS + ",(" + valS + "))"
        # symeq = sp.sympify(spS, _clash2, evaluate=False)
        # eqltxS = sp.latex(symeq, mul_symbol="dot")
        eqS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        indeqS = eqS.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"
        eqL = [varS, valS, unit1S, unit2S, descS]
        self.localD.update(locals())

        subS = "\n\n"
        if self.labelD["subB"]:              # replace variables with numbers
            subS = self.vsub(eqL, precI, varS, val1U) + "\n\n"

        assignL = [varS, str(val1U), unit1S, unit2S, descS]
        return [assignL, rstS + subS]

    def vsub(self, eqL, precI, varS, val1U):
        """substitute numbers for variables in printed output

        :return assignL: assign results
        :rtype: list
        :return rstS: restruct string 
        :rtype: string
        """
        locals().update(self.localD)
        fmtS = "%." + str(precI) + "f"
        varL = [str(eqL[0]), str(eqL[1])]
        # resultS = vars[0].strip() + " = " + str(eval(vars[1]))
        # sps = sps.encode('unicode-escape').decode()
        eqS = "Eq(" + eqL[0] + ",(" + eqL[1] + "))"
        with sp.evaluate(False):
            symeq = sp.sympify(eqS.strip())
        symat = symeq.atoms(sp.Symbol)
        for n1O in symat:
            if str(n1O) == varS:
                symeq = symeq.subs(n1O, sp.Symbol(str(val1U)))
                continue
            n1U = eval(str(n1O))
            n1U.set_format(value_format=fmtS, auto_norm=True)
            evlen = len(str(n1U))  # get var length
            new_var = str(n1U).rjust(evlen, "~")
            new_var = new_var.replace("_", "|")
            with sp.evaluate(False):                # sub values
                symeq = symeq.subs(n1O, sp.Symbol(new_var))
        out2 = sp.pretty(symeq, wrap_line=False)
        # symat1 = symeq.atoms(sp.Symbol)
        # for n2 in symat1:
        #     orig_var = str(n2).replace("~", "")
        #     orig_var = orig_var.replace("|", "_")
        #     expr = eval(varL[1])
        #     if type(expr) == float:
        #         form = "{%." + str(precI) + "f}"
        #         symeval1 = form.format(eval(str(expr)))
        #     else:
        #         try:
        #             symeval1 = eval(
        #                 orig_var.__str__()).__str__()
        #         except:
        #             symeval1 = eval(orig_var.__str__()).__str__()
        #     out2 = out2.replace(n2.__str__(), symeval1)   # substitute
        # print('out2b\n', out2)
        out3 = out2  # clean up unicode
        out3 = out3.replace("*", "\\u22C5")
        _cnt = 0
        for _m in out3:
            if _m == "-":
                _cnt += 1
                continue
            else:
                if _cnt > 1:
                    out3 = out3.replace("-" * _cnt, "\u2014" * _cnt)
                _cnt = 0
        self.localD.update(locals())
        indeqS = out3.replace("\n", "\n   ")
        rstS = "\n::\n\n   " + indeqS + "\n\n"

        return rstS


class TagUTF(Tag):
    """TagsUTF _summary_

    Args:
        Tags (_type_): _description_
    """

    def __init__(self, lineS, tagsD, folderD, labelD, rivtD):
        """convert rivt tags to md or reST

        """

        self.lineS = lineS
        self.tagsD = tagsD
        self.localD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        self.lineS = lineS
        self.widthI = labelD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

        modnameS = self.labelD["rivN"]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")

    def bold(self):
        """bold text _[b]

        :return lineS: bold line
        :rtype: str
        """
        print(self.lineS)
        return self.lineS

    def center(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = self.lineS.center(int(self.widthI))
        print(lineS)
        return lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """
        print(self.lineS)
        return self.lineS

    def boldcenter(self):
        """center text _[bc]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)

    def bolditalic(self):
        """center text _[bc]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.center(int(self.widthI))

        print(lineS)
        return lineS

    def bolditaliccenter(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = self.lineS.rjust(int(self.widthI))

        print(lineS)
        return lineS

    def italiccenter(self):
        """center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = self.lineS.center(int(self.widthI))
        print(lineS)
        return lineS

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """

        lineS = self.lineS.rjust(int(self.widthI))

        return lineS

    def label(self, labelS, numS):
        """format labels for equations, tables and figures

            :return labelS: formatted label
            :rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        labelS = secS + " - " + labelS + numS
        # store for equation table
        self.labelD["eqlabelS"] = self.lineS + " [" + numS.zfill(2) + "]"
        return labelS

    def description(self):
        """footnote description _[d]

        :return lineS: footnote
        :rtype: str
        """
        ftnumI = self.labelD["noteL"].pop(0)
        lineS = "[" + str(ftnumI) + "] " + self.lineS
        print(lineS)
        return lineS

    def equation(self):
        """md equation label _[e]

        :return lineS: md equation label
        :rtype: str
        """

        enumI = int(self.labelD["equI"]) + 1
        fillS = str(enumI).zfill(2)
        wI = self.labelD["widthI"]
        refS = self.label("E", fillS)
        spcI = len("Equ. " + fillS + " - " + self.lineS.strip())
        lineS = "Equ. " + fillS + " - " + self.lineS.strip() \
            + refS.rjust(wI-spcI)
        self.labelD["equI"] = enumI

        print(lineS)
        return lineS

    def figure(self):
        """md figure caption _[f]

        :return lineS: figure label
        :rtype: str
        """

        fnumI = int(self.labelD["figI"])
        self.labelD["figI"] = fnumI + 1
        lineS = "Fig. " + str(fnumI) + " - " + self.lineS

        print(lineS + "\n")
        return lineS + "\n"

    def foot(self):
        """footnote number _[#]


        """
        ftnumI = self.labelD["footL"].pop(0)
        self.labelD["noteL"].append(ftnumI + 1)
        self.labelD["footL"].append(ftnumI + 1)
        lineS = self.lineS.replace("*]", "[" + str(ftnumI) + "]")
        print(lineS)
        return lineS

    def latex(self):
        """format latex

        :return lineS: formatted latex
        :rtype: str
        """
        txS = self.lineS
        # txS = txs.encode('unicode-escape').decode()
        ptxS = sp.parse_latex(txS)
        lineS = sp.pretty(sp.sympify(ptxS, _clash2, evaluate=False))
        print(lineS)
        return lineS

    def plain(self):
        """format plain literal text _[p]

        :param lineS: _description_
        :type lineS: _type_
        """
        print(self.lineS)
        return self.lineS

    def sympy(self):
        """format line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """

        spS = self.lineS.strip()
        # try:
        #     spL = spS.split("=")
        #     spS = "Eq(" + spL[0] + ",(" + spL[1] + "))"
        #     # sps = sp.encode('unicode-escape').decode()
        # except:
        lineS = sp.pretty(sp.sympify(spS, _clash2, evaluate=False))
        print(lineS)
        return lineS

    def table(self):
        """format table title  _[t]

        :return lineS: md table title
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        self.labelD["tableI"] = tnumI + 1
        lineS = "Table " + str(tnumI) + " - " + self.lineS
        print(lineS)
        return lineS

    def link(self):
        """format url or internal link _[link]

        :return: _description_
        :rtype: _type_
        """
        lineL = self.lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]
        print(lineS)
        return lineS

    def page(self):
        """insert new page header _[page]

        :return lineS: page header
        :rtype: str
        """
        pagenoS = str(self.labelD["pageI"])
        rvtS = self.labelD["headuS"].replace("p##", pagenoS)
        self.labelD["pageI"] = int(pagenoS)+1
        lineS = "\n"+"_" * self.labelD["widthI"] + "\n" + rvtS +\
                "\n"+"_" * self.labelD["widthI"] + "\n"
        return "\n" + rvtS

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """
        return self.lineS

    def centerblk(self):
        """

        """
        lineS = ""
        for i in self.lineS:
            lineS += i.center(int(self.widthI))

        return lineS

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def codeblk(self):
        pass

    def rightblk(self):
        pass

    def shadeblk(self):
        """ start shade block _[[s]]

        :param lineS: _description_
        :type lineS: _type_
        """
        pass

    def quitblock(self):
        """ quit shade block _[[q]]

        :param lineS: _description_
        :type lineS: _type_
        """
        pass

    def tagblk(self):
        pass


class TagRST(Tag):
    """convert rivt tags to reST

    """

    def __init__(self, lineS, tagsD, folderD, labelD, rivtD):
        """convert rivt tags to md or reST

        """

        self.tagsD = tagsD
        self.localD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        self.lineS = lineS
        self.vgap = "2"
        self.widthI = labelD["widthI"]
        self.errlogP = folderD["errlogP"]
        self.valL = []                         # accumulate values in list

        modnameS = self.labelD["rivN"]
        # print(f"{modnameS=}")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS +
            "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=self.errlogP,
            filemode="w",
        )
    warnings.filterwarnings("ignore")

    def bold(self):
        """bold text _[b]

        :return lineS: bold line
        :rtype: str
        """
        return "**" + self.lineS.strip() + "**"

    def center(self):
        """center text _[c]

        : return lineS: centered line
        : rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} " + self.lineS + " ?x?end{center}" \
            + "\n"

        return lineS

    def italic(self):
        """italicize text _[i]

        :return lineS: centered line
        :rtype: str
        """
        return "*" + self.lineS.strip() + "*"

    def right(self):
        """right justify text _[r]

        :return lineS: right justified text
        :rtype: str
        """
        return "?x?hfill " + self.lineS

    def boldcenter(self):
        """bold center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textbf{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
        return lineS

    def boldright(self):
        """bold right text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textbf{" + self.lineS + "}" \
            + "\n"
        return lineS

    def italiccenter(self):
        """italic center text _[c]

        :return lineS: centered line
        :rtype: str
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} ?x?textit{" + self.lineS +  \
            "} ?x?end{center}" + "\n"
        return lineS

    def italicright(self):
        """italic right text _[c]

        :return lineS: centered line
        :rtype: str
        """

        lineS = ".. raw:: latex \n\n" \
            + "?x?hfill ?x?textit{" + self.lineS + "}" \
            + "\n"
        return lineS

    def label(self, labelS, numS):
        """format labels for equations, tables and figures

            : return labelS: formatted label
            : rtype: str
        """
        secS = str(self.labelD["secnumI"]).zfill(2)
        return secS + " - " + labelS + numS

    def description(self):
        """footnote description _[d]

        : return lineS: footnote
        : rtype: str
        """
        return ".. [*] " + self.lineS

    def equation(self):
        """reST equation label _[e]

        : return lineS: reST equation label
        : rtype: str
        """
        enumI = int(self.labelD["equI"])
        fillS = str(enumI).zfill(2)
        refS = self.label("E", fillS)
        lineS = "\n\n" + "**" + "Eq. " + str(enumI) + ": "  \
                + self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n\n"
        return lineS

    def figure(self):
        """figure label _[f]

        : return lineS: figure label
        : rtype: str
        """
        fnumI = int(self.labelD["figI"])
        fillS = str(fnumI).zfill(2)
        refS = self.label("F", fillS)
        lineS = "\n \n" + "**" + "Figure " + str(fnumI) + ": " + \
                self.lineS.strip() + "** " + " ?x?hfill " + refS + "\n \n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def footnumber(self):
        """insert footnote number _[#]

        :return: _description_
        :rtype: _type_
        """
        lineS = "".join(self.lineS)
        return lineS.replace("*]", "[*]_ ")

    def latex(self):
        """format latex _[l]

        :return lineS: reST formatted latex
        :rtype: str
        """
        return ".. raw:: math\n\n   " + self.lineS + "\n"

    def link(self):
        """url or internal link

        :return: _description_
        :rtype: _type_
        """
        lineL = lineS.split(",")
        lineS = ".. _" + lineL[0] + ": " + lineL[1]

        return lineS

    def line(self):
        """insert line _[line]:

        param lineS: _description_
        :type lineS: _type_
        """
        return self.widthI * "-"

    def plain(self):
        """format plain literal _[p]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def sympy(self):
        """reST line of sympy _[s]

        :return lineS: formatted sympy
        :rtype: str
        """
        spS = self.lineS
        txS = sp.latex(S(spS))
        return ".. raw:: math\n\n   " + txS + "\n"

    def underline(self):
        """underline _[u]

        :return lineS: underline
        :rtype: str
        """
        return ":math: `?x?text?x?underline{" + self.lineS.strip() + "}"

    def page(self):
        """insert page break _[page]

        :return lineS: page break line
        :rtype: str
        """
        return ".. raw:: latex \n\n ?x?newpage \n"

    def table(self):
        """table label _[t]

        :return lineS: figure label
        :rtype: str
        """
        tnumI = int(self.labelD["tableI"])
        fillS = str(tnumI).zfill(2)
        refS = self.label("T", fillS)
        lineS = "\n" + "**" + "Table " + fillS + ": " + self.lineS.strip() + \
                "** " + " ?x?hfill " + refS + "\n"
        return self.vgap + lineS + self.vgap + " ?x?nopagebreak \n"

    def centerblk(self):
        """_summary_
        """
        lineS = ".. raw:: latex \n\n" \
            + "   ?x?begin{center} + ?x?parbox{5cm}" \
            + self.lineS + " ?x?end{center}" \
            + "\n\n"
        return lineS

    def latexblk(self):
        pass

    def mathblk(self):
        pass

    def codeblk(self):
        pass

    def rightblk(self):
        pass

    def tagblk(self):
        pass
