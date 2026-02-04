"""
parse section string
"""

import logging
import os
import re
import sys
import warnings
from io import StringIO
from pathlib import Path

import tabulate
from fastcore.utils import store_attr

import __main__

from . import rvcmd, rvtag


class Rs:
    """convert rivt string to formatted text and reST strings"""

    def __init__(self, stS, rsL, foldD, lablD, rivtD, prflagB, rivtL):
        """process logs, header and preprocess content

        Args:
            stS (str): section type
            rsL (list): rivt string list
        """
        store_attr()
        # region - write header to apilog
        apilogT = foldD["apilogT"]
        with open(apilogT, "a") as f4:
            f4.write(rsL[0] + "\n")
        errlogT = foldD["errlogT"]
        warnings.filterwarnings("ignore")
        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format=(
                "%(asctime)-8s  " + modnameS + " %(levelname)-8s  %(message)-8s"
            ),
            datefmt="%m-%d %H:%M",
            filename=errlogT,
            filemode="w",
        )
        self.logging = logging
        sutfS = ""  # utf doc
        srsrS = ""  # rst2pdf doc
        srstS = ""  # rest doc
        spL = []  # preprocessed lines
        # section header
        hL = rsL[0].split("|")
        lablD["docS"] = hL[0].strip()  # section title
        if hL[0].strip()[0:2] == "--":
            lablD["docS"] = hL[0].split("--")[1][1]
            srsrS = "\n"
            srstS = "\n"
        else:
            snumI = lablD["secnumI"] + 1
            lablD["secnumI"] = snumI
            snumS = "[ " + str(snumI) + stS.lower() + " ]"
            headS = snumS + " " + hL[0].strip()
            headS = snumS + " " + hL[0].strip()
            bordrS = lablD["widthI"] * "-" + "\n"
            sutfS = "\n" + headS + "\n" + bordrS
            srsrS = "\n" + headS + "\n" + bordrS
            srstS = "\n" + headS + "\n" + bordrS
            print(sutfS)  # STDOUT section header
        # insert interactive link
        if not prflagB:
            file_path = str(foldD["rivtT"])
            for linenumI, lineS in enumerate(rivtL):
                if rsL[0] in lineS:
                    print(f"{file_path}:{linenumI + 1}\n")
                    break
        try:
            paraL = hL[1].strip().split("|")
        except Exception:
            paraL = []
        # set default section parameters
        lablD["rvtypeS"] = stS  # section type
        lablD["publicB"] = False
        if stS == "R" or stS == "T" or stS == "M":
            lablD["showB"] = False
        if stS == "I" or stS == "V":
            lablD["showB"] = True
        # override section defaults
        if len(paraL) > 0:
            if "hide" in paraL:
                foldD["showB"] = False
            if "print" in paraL:
                foldD["showB"] = True
            if "private" in paraL:
                foldD["publicB"] = False
            if "public" in paraL:
                foldD["publicB"] = True
        self.sutfS = sutfS  # utf doc
        self.srsrS = srsrS  # rst2pdf doc
        self.srstS = srstS  # rest doc
        self.logging.info("SECTION " + str(lablD["secnumI"]) + " - type " + stS)
        spL = []  # strip leading spaces and comments from section content
        for slS in rsL[1:]:
            if len(slS) < 5:  # blank line to new line
                slS = "\n"
                spL.append(slS)
                continue
            if "##" in slS[:6]:  # skip comment line
                continue
            if "." * 5 in slS:  # page break to tag
                slS = "    _[P]"
            spL.append(slS[4:])
        self.spL = spL  # preprocessed list
        # endregion

    def content(self, tS, tagL, cmdL):
        """parse content substring
        Args:
            tagL (list): tag list
            cmdL (list): command list
        Returns:
            sutfS (str): utf doc string
            srsrS (str): rst2pdf doc string
            srstS (str): resT doc string
            foldD (dict): folder paths
            lablD (dict): labels
            rivD (dict): calculated values
            rivL (list): export values
        """
        # region
        # print(f"{cmdL=}")
        # print(f"{tagL=}")
        rivL = []
        tabL = []
        blockB = False
        blockS = """"""
        tagS = ""
        uS = rS = xS = """"""  # returned doc line

        sutfS = self.sutfS
        srsrS = self.srsrS
        srstS = self.srstS
        foldD = self.foldD
        lablD = self.lablD
        rivD = self.rivtD

        for slS in self.spL:  # loop over content substring
            # print(f"{slS=}")
            if self.stS == "I":
                txt2L = []
                # print(f"{slS=}")
                txt1L = re.findall(r"\*\*(.*?)\*\*", slS)  # strip bold
                if len(txt1L) > 0:
                    for tS in txt1L:
                        t1S = "**" + tS + "**"
                        slS = slS.replace(t1S, tS)
                txt2L = re.findall(r"\*(.*?)\*", slS)  # strip italic
                if len(txt2L) > 0:
                    for tS in txt2L:
                        t2S = "*" + tS + "*"
                        slS = slS.replace(t2S, tS)
                # print(f"{txt1L=}")
            if len(tabL) > 0 and len(slS.strip()) == 0:  # values block
                tblfmt = "rst"
                hdrvL = ["variable", "value", "[value]", "description"]
                alignL = ["left", "right", "right", "left"]
                sys.stdout.flush()
                old_stdout = sys.stdout
                output = StringIO()
                output.write(
                    tabulate.tabulate(
                        tabL,
                        tablefmt=tblfmt,
                        headers=hdrvL,
                        showindex=False,
                        colalign=alignL,
                    )
                )
                outS = output.getvalue()
                sys.stdout = old_stdout
                sys.stdout.flush()
                sutfS += outS
                srsrS += outS
                srstS += outS
                print(outS)  # STDOUT - values block
                tabL = []
                sutfS += "\n"
                srsrS += " \n"
                srstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            if len(slS.strip()) == 0 and not blockB:
                sutfS += "\n"
                srsrS += " \n"
                srstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            if blockB:  # block accumulate
                # print(f"{blockS}")
                if blockB and ("_[[END]]" in slS):  # end of block
                    blockB = False
                    tC = rvtag.Tag(foldD, lablD, rivD, rivL, blockS)
                    uS, rS, xS, foldD, lablD, rivD, rivL = tC.tagbx(tagS)
                    print(uS)  # STDOUT - block
                    sutfS += uS + "\n"
                    srsrS += rS + "\n"
                    srstS += xS + "\n"
                    tagS = ""
                    blockS = """"""
                    continue
                blockS += slS + "\n"
                continue
            if slS[0:1] == "|":  # commands
                parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                self.logging.info(f"command : {cmdS}")
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:  # verify scope
                    cmC = rvcmd.Cmd(self.stS, foldD, lablD, rivD, rivL, parL)
                    uS, rS, xS, foldD, lablD, rivD, rivL = cmC.cmdx(cmdS)
                    sutfS += uS + "\n"
                    srsrS += rS + "\n"
                    srstS += xS + "\n"
                    print(uS)  # STDOUT- command
                    continue
            if tS == "V":  # compare
                if " ==: " in slS:
                    if " ==: " in cmdL:
                        lineS = slS.strip()
                        tC = rvcmd.Cmd(
                            self.stS, foldD, lablD, rivD, rivL, lineS
                        )
                        uS, rS, xS, foldD, lablD, rivD, rivL, tbL = tC.vdefine(
                            lineS
                        )
                        tabL.append(tbL)
                        continue
                if " <=: " in slS:
                    if " <=: " in cmdL:
                        lineS = slS.strip()
                        tC = rvcmd.Cmd(
                            self.stS, foldD, lablD, rivD, rivL, lineS
                        )
                        uS, rS, xS, foldD, lablD, rivD, rivL = tC.vassign(lineS)
                        sutfS += uS + "\n"
                        srsrS += rS + "\n"
                        srstS += xS + "\n"
                        print(uS)  # STDOUT - equation table
                        continue
                if " :=: " in slS:
                    if " :=: " in cmdL:
                        lineS = slS.strip()
                        tC = rvcmd.Cmd(
                            self.stS, foldD, lablD, rivD, rivL, lineS
                        )
                        uS, rS, xS, foldD, lablD, rivD, rivL = tC.vfunc(lineS)
                        sutfS += uS + "\n"
                        srsrS += rS + "\n"
                        srstS += xS + "\n"
                        print(uS)  # STDOUT - equation table
                        continue
                for subS in cmdL[8]:
                    if subS in slS:
                        matchS = subS
                        lineS = slS.strip()
                        tC = rvcmd.Cmd(
                            self.stS, foldD, lablD, rivD, rivL, lineS
                        )
                        stdS, uS, rS, xS, foldD, lablD, rivD, rivL = (
                            tC.vcompare(lineS, matchS)
                        )
                        sutfS += uS + "\n"
                        srsrS += rS + "\n"
                        srstS += xS + "\n"
                        print(stdS)  # STDOUT - compare table
                        continue
                continue
            if "_[" in slS:  # tags
                slL = slS.split("_[")
                lineS = slL[0].strip()
                tagS = slL[1].strip()
                self.logging.info(f"tag : _[{tagS}")
                if tagS in tagL:  # check list
                    # print(f"{tagS=}")
                    tC = rvtag.Tag(foldD, lablD, rivD, rivL, lineS)
                    if len(tagS) < 3:  # line tag
                        uS, rS, xS, foldD, lablD, rivD, rivL = tC.taglx(tagS)
                        sutfS += uS + "\n"
                        srsrS += rS + "\n"
                        srstS += xS + "\n"
                        print(uS)  # STDOUT- tagged line
                        continue
                    else:  # block tag - start
                        blockS = ""
                        blockB = True
                        blockS += lineS + "\n"
            else:  # everything else
                print(slS)  # STDOUT - raw line
                sutfS += slS + "\n"
                srsrS += slS + "\n"
                srstS += slS + "\n"

        # export values file
        if self.stS == "V" and len(rivL) > 0:
            fileS = lablD["valprfx"] + str(lablD["secnumI"]) + ".csv"
            if foldD["rvsingleB"]:
                fileP = Path(foldD["val_P"], fileS)
            else:
                fileP = Path(foldD["val_P"], fileS)
            with open(fileP, "w") as file1:
                file1.write("\n".join(rivL))

        return sutfS, srsrS, srstS, foldD, lablD, rivD
        # endregion
