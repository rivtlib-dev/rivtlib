"""
parses a section string
"""

import logging
import os
import re
import sys
import textwrap
import warnings
from io import StringIO
from pathlib import Path

import tabulate
from fastcore.utils import store_attr

import __main__

from . import rvcmd, rvtag


class Rs:
    """convert rivt string to formatted text and reST strings"""

    def __init__(self, tyS, rsL, fD, lD, rivtD, rivtL, vdescD):
        """setup logs, header and preprocess content substring

        Args:
            tyS (str): rivt string type
            rsL (list): rivt string list
            fD (dict): _description_
            lD (dict): _description_
            rivtD (dict): _description_
            rivtL (list): _description_
        """

        store_attr()
        # region - write header to errlog
        errlogT = fD["errlogT"]
        warnings.filterwarnings("ignore")
        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format=(
                "%(asctime)-8s  " + modnameS + " %(levelname)-8s  %(message)-8s"
            ),
            datefmt="%m-%d %H:%M",
            filename=errlogT,
            filemode="a",
        )
        self.logging = logging
        logging.info(rsL[0])  # log header
        stxtS = ""  # text doc
        sutfS = ""  # utf doc
        srstS = ""  # rest doc
        sltxS = ""  # latex doc
        newpageS = ""
        self.vardescD = vdescD
        # ----------------------------------------------   section header
        if lD["cntflgI"] == 0:  # add transition and API type
            transS = "\n"
            lD["cntflgI"] += 1
        else:  # add tags and transition
            transS = "\n\n--------------\n\n"
        if lD["notagB"] == "False":
            addtgS = tyS.lower()
        else:
            addtgS = ""
        hL = rsL[0].split("|")
        # -----  get section title
        lD["docS"] = hL[0].strip()
        if hL[0].strip()[0:2] == "--":
            lD["docS"] = hL[0].split("--")[1][1]
            sutfS = "\n"
            srstS = "\n"
            stxtS = "\n"
        else:
            snumI = lD["secnumI"] + 1
            lD["secnumI"] = snumI
            sdivS = str(lD["sdivI"])
            divS = str(lD["divS"])
            snumS = f"{divS}.{sdivS}.{str(snumI)}{addtgS}"
            snum1S = f"**{divS}.{sdivS}.{str(snumI)}{addtgS}**"
            headS = snumS + " | " + hL[0].strip()
            head1S = snum1S + " | " + hL[0].strip()
            bordrS = lD["widthI"] * "-" + "\n"
            sutfS = "\n" + headS + "\n" + bordrS
            stxtS = "\n" + headS + "\n" + bordrS
            srstS = "\n" + head1S + "\n" + bordrS
            print(sutfS)  # STDOUT section header
        file_path = str(fD["rivtT"])  # insert interactive link
        for linenumI, lineS in enumerate(rivtL):
            if rsL[0] in lineS:
                print(f"[link] {file_path}:{linenumI + 1}\n")
                break
        # ----------  parse header params
        try:
            paraL = hL[1].strip().split("|")
        except Exception:
            paraL = []
        # set default header parameters
        lD["rvtypeS"] = tyS
        lD["mergeB"] = "False"
        lD["privB"] = "True"
        if lD["privateB"] == "True" or lD["privateB"] == "False":
            lD["privB"] = lD["privateB"]
        if tyS == "D":
            lD["privB"] = "False"
        lD["docB"] = "False"
        if tyS == "I" or tyS == "V":
            lD["docB"] = "True"
        # override header defaults
        if len(paraL) > 0:
            if "doc" in paraL:
                lD["docB"] = "True"
            elif "nodoc" in paraL:
                lD["docB"] = "True"
            if "private" in paraL:
                lD["privB"] = "True"
            elif "public" in paraL:
                lD["privB"] = "False"
            if "section" in paraL:
                lD["mergeB"] = "False"
            elif "merge" in paraL:
                lD["mergeB"] = "True"
            newpageS = ""  # for rst2pdf doc
            if "pdfpage" in paraL:
                newpageS = "\n\n.. raw:: pdf\n\n   " + "PageBreak" + "\n\n"
            else:
                pass

        # initialize content substring
        srstS = transS + newpageS + srstS  # add transition and new page
        self.sutfS = sutfS  # utf doc
        self.stxtS = stxtS  # text doc
        self.srstS = srstS  # rst2pdf doc
        self.logging.info("SECTION " + snumS + " - type " + tyS)
        # preprocess  section
        self.spL = []
        for slS in rsL[1:]:
            if len(slS) < 5:  # blank line to new line
                slS = " \n"
                self.spL.append(slS)
                continue
            elif "##" in slS[:8]:  # skip comment line
                continue
            else:
                self.spL.append(slS[4:])  # preprocessed list
        # endregion

    def prt_tabl(self, tabL):
        tblfmt = "rst"
        hdrvL = ["variable", "value", "[value]", "description"]
        alignL = ["left", "left", "left", "left"]
        sys.stdout.flush()
        old_stdout = sys.stdout
        output = StringIO()
        output.write(
            tabulate.tabulate(
                tabL,
                tablefmt=tblfmt,
                headers=hdrvL,
                showindex=False,
                colglobalalign=alignL,
                headersalign=alignL,
            )
        )
        outS = output.getvalue()
        sys.stdout = old_stdout
        sys.stdout.flush()

        return outS + "\n"

    def remove_aster(self, text):
        # remove italic and bold * from rv.I content
        # (?<!\*)    - Negative lookbehind: ensure the asterisk isn't preceded by another *
        # \*{1,2}    - Match 1 or 2 asterisks
        # (?!\*)     - Negative lookahead: ensure the asterisk isn't followed by another *
        # (?!\s)     - Negative lookahead: ensure the asterisk isn't followed by a space
        pattern = r"(?<!\*)(?:\*{1,2})(?!\*)(?!\s)"

        return re.sub(pattern, "", text)

    # ------------------------------------------------- section content
    def content(self, tyS, tagL, cmdL):
        """parse content substring
        Args:
            tyS (str): api type
            tagL (list): tag list
            cmdL (list): command list
        Returns:
            sutfS (str): utf doc string
            srstS (str): rest doc string
            stxtS (str): text doc string
            fD (dict): folder paths
            lD (dict): labels
            rivtD (dict): calculated values
            rivL (list): export values
        """
        # region
        # print(f"{cmdL=}")
        # print(f"{tagL=}")
        # ---- doc level vars
        sutfS = self.sutfS  # accumulated utf doc
        stxtS = self.stxtS  # accumulated text doc
        srstS = self.srstS  # accumulated reST doc
        fD = self.fD  # folder dict
        lD = self.lD  # label dict
        rivtD = self.rivtD
        # --- sectiion level vars
        vardescD = self.vardescD  # var description for formatting
        blockB = False  # block accumulator
        blockS = """"""  # block string
        tagS = ""  # line tags
        rivL = []  # vars for export
        tabL = []  # inline tables
        mD = {}  # returns as dict
        mD["uS"] = mD["tS"] = mD["rS"] = """"""  # returned doc string
        # ---------------------------------- loop over content substring
        for slS in self.spL:
            if tyS == "I":
                slS = self.remove_aster(slS)
            # print("**", f"{slS=}")
            if len(slS.strip()) == 0 and len(tabL) > 0:  # print inline valtable
                outS = self.prt_tabl(tabL)
                sutfS += outS + " \n"
                srstS += outS + " \n"
                stxtS += outS + " \n"
                print(outS, "\n")  # STDOUT - values block
                tabL = []
                continue
            elif len(slS.strip()) == 0 and not blockB:  # print blank line
                sutfS += " \n"
                srstS += " \n"
                stxtS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            else:
                pass
            if blockB:  # ----------------------------------- block accumulate
                # print(f"**{blockS}")
                if blockB and ("_[[END]]" in slS):  # end of block
                    blockB = False
                    tC = rvtag.Tag(fD, lD, rivtD, rivL, blockS)
                    # print("*******", tagS, blockS)
                    mD, lD, rivtD = tC.tagbx(tagS)
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    stxtS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - block
                    tagS = ""
                    blockS = """"""
                    continue
                else:
                    blockS += slS + " \n"
                    continue
            if " ==: " in slS:  # define ------------------- operators
                if " ==: " in cmdL:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(
                        self.tyS, fD, lD, rivtD, rivL, lineS, vardescD
                    )
                    tbL, rivtD, rivL, vardescD = tC.vdefine(lineS)
                    tabL.append(tbL)
                    continue
            elif " <=: " in slS:  # assign
                if " <=: " in cmdL:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(
                        self.tyS, fD, lD, rivtD, rivL, lineS, vardescD
                    )
                    mD, vardescD = tC.vassign(lineS)
                    lD, rivL, rivtD = (mD["lD"], mD["rivL"], mD["rivtD"])
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    stxtS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - equation table
                    continue
            elif " :=: " in slS:  # function
                if " :=: " in cmdL:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(
                        self.tyS, fD, lD, rivtD, rivL, lineS, vardescD
                    )
                    mD, vardescD = tC.vfunc(lineS)
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    stxtS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - equation table
                    continue
            elif tyS == "V" and "|" in slS and (x in slS for x in cmdL[0]):
                opS = [item for item in cmdL[0] if item in slS]
                if opS == []:
                    pass
                else:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(
                        self.tyS, fD, lD, rivtD, rivL, lineS, vardescD
                    )
                    mD = tC.vcompare(lineS, opS[0])  # return first in list
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    stxtS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - compare table
                    continue
            if "_[" in slS:  # ------------------------------ tags / blocks
                if "_[[" in slS:
                    slL = slS.split("_[[")
                    lineL = slL[1].split("]]")
                    lineS = lineL[1]
                    tagS = lineL[0]
                    if tagS in tagL:
                        # print(f"{tagS=}")
                        self.logging.info(f"tag : _[[{tagS}]]")
                        blockS = ""
                        blockB = True
                        blockS += lineS + "\n"
                    continue
                else:
                    s1L = slS.split("_[")
                    s2L = s1L[1].split("]")
                    lineL = [s1L[0]] + s2L[1:]
                    tagS = s2L[0]
                    if tagS in tagL:  # check tag list
                        # print(f"{tagS=}")
                        self.logging.info(f"tag : _[{tagS}]")
                        tC = rvtag.Tag(fD, lD, rivtD, rivL, lineL)
                        if tagS[0] != "[":  # line tag
                            mD, lD = tC.taglx(tagS)
                            sutfS += mD["uS"] + "\n"
                            srstS += mD["rS"] + "\n"
                            stxtS += mD["tS"] + "\n"
                            print(mD["uS"])  # STDOUT- tagged line
                            continue
            if slS.strip()[0:1] == "|":  # ---------------------- commands
                parL = slS.strip()[1:].split("|")
                cmdS = parL[0].strip()
                self.logging.info(f"command : {cmdS}")
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:  # verify scope
                    cmC = rvcmd.Cmd(
                        self.tyS, fD, lD, rivtD, rivL, parL, vardescD
                    )
                    mD = cmC.cmdx(cmdS)
                    lD, rivL, rivtD = (mD["lD"], mD["rivL"], mD["rivtD"])
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    stxtS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - command
                    continue
            else:  # everything else - STDOUT - raw line
                print(textwrap.fill(slS, width=lD["widthI"]), flush=True)
                sutfS += textwrap.fill(slS, width=lD["widthI"]) + "\n"
                srstS += slS + "\n"
                stxtS += textwrap.fill(slS, width=lD["widthI"]) + "\n"

        # export values file
        if self.tyS == "V" and len(rivL) > 0:
            fileS = lD["valprfx"] + str(lD["secnumI"]) + ".csv"
            fileP = Path(fD["storeP"], fileS)
            with open(fileP, "w") as file1:
                file1.write("\n".join(rivL))

        return sutfS, stxtS, srstS, fD, lD, rivtD
        # endregion
