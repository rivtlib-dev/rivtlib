"""
parse section string
"""

import logging
import os
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

    def __init__(self, tyS, rsL, fD, lD, rivtD, rivtL):
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
        with open(errlogT, "a") as f4:
            f4.write(rsL[0] + "\n")
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
        srstS = ""  # rest doc
        stxtS = ""  # text doc
        slatS = ""  # latex doc

        # preprocess rivt string
        # ----------------------------------------------   section header
        hL = rsL[0].split("|")
        lD["docS"] = hL[0].strip()  # section title
        if hL[0].strip()[0:2] == "--":
            lD["docS"] = hL[0].split("--")[1][1]
            sutfS = "\n"
            srstS = "\n"
            stxtS = "\n"
        else:
            snumI = lD["secnumI"] + 1
            lD["secnumI"] = snumI
            snumS = "[ " + str(snumI) + tyS.lower() + " ]"
            headS = snumS + " " + hL[0].strip()
            headS = snumS + " " + hL[0].strip()
            bordrS = lD["widthI"] * "-" + "\n"
            sutfS = "\n" + headS + "\n" + bordrS
            srstS = "\n" + headS + "\n" + bordrS
            stxtS = "\n" + headS + "\n" + bordrS
            print(sutfS)  # STDOUT section header
        file_path = str(fD["rivtT"])  # insert interactive link
        for linenumI, lineS in enumerate(rivtL):
            if rsL[0] in lineS:
                print(f"[link] {file_path}:{linenumI + 1}\n")
                break
        # parse header
        try:
            paraL = hL[1].strip().split("|")
        except Exception:
            paraL = []
        # set default section parameters
        lD["rvtypeS"] = tyS
        lD["rvpubB"] = False
        if tyS == "R" or tyS == "T" or tyS == "D":
            lD["showB"] = False
        if tyS == "I" or tyS == "V":
            lD["showB"] = True
        # override section defaults
        if len(paraL) > 0:
            if "hide" in paraL:
                fD["showB"] = False
            if "print" in paraL:
                fD["showB"] = True
            if "private" in paraL:
                fD["publicB"] = False
            if "public" in paraL:
                fD["publicB"] = True
        self.sutfS = sutfS  # utf doc
        self.srstS = srstS  # rst2pdf doc
        self.stxtS = stxtS  # rest doc
        self.logging.info("SECTION " + str(lD["secnumI"]) + " - type " + tyS)
        # preprocess  section
        self.spL = []
        for slS in rsL[1:]:
            if len(slS) < 5:  # blank line to new line
                slS = "     \n"
                self.spL.append(slS[4:])
                continue
            elif "##" in slS[:6]:  # skip comment line
                continue
            elif "." * 5 in slS[:6]:  # page break to tag
                slS = "    _[P]"
                self.spL.append(slS[4:])
                continue
            else:
                self.spL.append(slS[4:])  # preprocessed list
        # endregion

    # ----------------------------------------------------   API parsing loop
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
        rivL = []
        tabL = []
        mD = {}
        mD["uS"] = mD["rS"] = mD["tS"] = """"""  # returned doc line
        blockB = False
        blockS = """"""
        tagS = ""
        sutfS = self.sutfS
        srstS = self.srstS
        stxtS = self.stxtS
        fD = self.fD
        lD = self.lD
        rivtD = self.rivtD
        # --------------------------------------- loop over content substring
        for slS in self.spL:
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
                # print(f"{blockS}")
                if blockB and ("_[[END]]" in slS):  # end of block
                    blockB = False
                    tC = rvtag.Tag(fD, lD, rivtD, rivL, blockS)
                    # print("****", tagS, blockS)
                    mD, lD = tC.tagbx(tagS)
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    sutfS += mD["tS"] + "\n"
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
                    tC = rvcmd.Cmd(self.tyS, fD, lD, rivtD, rivL, lineS)
                    tbL, rivtD, rivL = tC.vdefine(lineS)
                    tabL.append(tbL)
                    continue
            elif " <=: " in slS:  # assign
                if " <=: " in cmdL:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(self.tyS, fD, lD, rivtD, rivL, lineS)
                    mD = tC.vassign(lineS)
                    lD, rivL, rivtD = (mD["lD"], mD["rivL"], mD["rivtD"])
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    sutfS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - equation table
                    continue
            elif " :=: " in slS:  # function
                if " :=: " in cmdL:
                    lineS = slS.strip()
                    tC = rvcmd.Cmd(self.tyS, fD, lD, rivtD, rivL, lineS)
                    mD = tC.vfunc(lineS)
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    sutfS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT - equation table
                    continue
            elif tyS == "V" and any(item in slS for item in cmdL[8]):
                for opS in cmdL[8]:
                    if opS in slS:
                        lineS = slS.strip()
                        tC = rvcmd.Cmd(self.tyS, fD, lD, rivtD, rivL, lineS)
                        mD = tC.vcompare(lineS, opS)
                        sutfS += mD["uS"] + "\n"
                        srstS += mD["rS"] + "\n"
                        sutfS += mD["tS"] + "\n"
                        print(mD["uS"])  # STDOUT - compare table
                        break
                continue
            else:
                pass
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
                    slL = slS.split("_[")
                    lineL = slL[1].split("]")
                    lineS = slL[0] + lineL[1]
                    tagS = lineL[0]
                    if tagS in tagL:  # check list
                        # print(f"{tagS=}")
                        self.logging.info(f"tag : _[{tagS}]")
                        tC = rvtag.Tag(fD, lD, rivtD, rivL, lineS)
                        if tagS[0] != "[":  # line tag
                            mD, lD = tC.taglx(tagS)
                            sutfS += mD["uS"] + "\n"
                            srstS += mD["rS"] + "\n"
                            sutfS += mD["tS"] + "\n"
                            print(mD["uS"])  # STDOUT- tagged line
                            continue
            if slS[0:1] == "|":  # ----------------------------- commands
                parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                self.logging.info(f"command : {cmdS}")
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:  # verify scope
                    cmC = rvcmd.Cmd(self.tyS, fD, lD, rivtD, rivL, parL)
                    mD = cmC.cmdx(cmdS)
                    lD, rivL, rivtD = (mD["lD"], mD["rivL"], mD["rivtD"])
                    sutfS += mD["uS"] + "\n"
                    srstS += mD["rS"] + "\n"
                    sutfS += mD["tS"] + "\n"
                    print(mD["uS"])  # STDOUT- command
                    continue
            else:  # everything else
                print(slS, flush=True)  # STDOUT - raw line
                sutfS += slS + "\n"
                srstS += slS + "\n"
                sutfS += slS + "\n"

        # export values file
        if self.tyS == "V" and len(rivL) > 0:
            fileS = lD["valprfx"] + str(lD["secnumI"]) + ".csv"
            fileP = Path(fD["storeP"], fileS)
            with open(fileP, "w") as file1:
                file1.write("\n".join(rivL))

        return sutfS, srstS, stxtS, fD, lD, rivtD
        # endregion

    def prt_tabl(self, tabL):
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

        return outS
