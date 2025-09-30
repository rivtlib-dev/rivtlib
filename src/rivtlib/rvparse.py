"""
parse section string
"""

import logging
import os
import re
import warnings

import __main__

from . import rvcmd, rvtag


class Section:
    """convert rivt string to utf and reST doc strings"""

    def __init__(self, stS, sL, foldD, lablD, rivD):
        """process section headers and preprocess string
        Args:
            stS (str): section type
            sL (list): rivt section lines
        """
        # region
        errlogP = foldD["errlogT"]
        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format=(
                "%(asctime)-8s  " + modnameS + " %(levelname)-8s  %(message)-8s"
            ),
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
        self.logging = logging

        sutfS = ""  # utf doc
        srsrS = ""  # rst2pdf doc
        srstS = ""  # rest doc
        spL = []  # preprocessed lines
        self.foldD = foldD
        self.lablD = lablD
        self.rivD = rivD
        self.stS = stS

        # section header
        hL = sL[0].split("|")
        lablD["docS"] = hL[0].strip()  # section title
        if hL[0].strip()[0:2] == "--":
            lablD["docS"] = hL[0].split("--")[1][1]  # section title
            sutfS = "\n"
            srsrS = "\n"
            srstS = "\n"
        else:
            snumI = lablD["secnumI"] + 1
            lablD["secnumI"] = snumI
            snumS = "[ " + str(snumI) + " ]"
            headS = snumS + " " + hL[0].strip()
            bordrS = lablD["widthI"] * "-"
            sutfS = "\n" + headS + "\n" + bordrS + "\n"
            srsrS = "\n" + headS + "\n" + bordrS + "\n"
            srstS = "\n" + headS + "\n" + bordrS + "\n"
        try:
            paraL = hL[1].strip().split("|")
        except Exception:
            paraL = []

        # set default section parameters
        lablD["rvtypeS"] = stS  # section type
        lablD["publicB"] = False
        if stS == "R":
            lablD["printB"] = False
            lablD["publicB"] = False
        elif stS == "I":
            lablD["printB"] = True
            lablD["publicB"] = False
        elif stS == "V":
            lablD["printB"] = True
            lablD["publicB"] = False
            foldD["alias"] = "rvsource"
        elif stS == "T":
            lablD["printB"] = False
            lablD["publicB"] = False
        elif stS == "D":
            lablD["printB"] = False
            lablD["publicB"] = False
        elif stS == "M":
            lablD["printB"] = False
            lablD["publicB"] = False
        else:
            pass

        # override section defaults
        if len(paraL) > 0:
            if "rvlocal" in paraL:
                foldD["alias"] = "rvlocal"
            if "rvsource" in paraL:
                foldD["alias"] = "rvsource"
            if "hide" in paraL:
                foldD["printB"] = False
            if "print" in paraL:
                foldD["printB"] = True
            if "private" in paraL:
                foldD["publicB"] = False
            if "public" in paraL:
                foldD["publicB"] = True

        # print(sutfS, srsrS, srstS)
        self.sutfS = sutfS  # utf doc
        self.srsrS = srsrS  # rst2pdf doc
        self.srstS = srstS  # rest doc
        print(sutfS)  # STDOUT section header
        self.logging.info("SECTION " + str(lablD["secnumI"]) + " - type " + stS)

        spL = []  # strip leading spaces and comments from section content
        for slS in sL[1:]:
            if len(slS) < 5:  # blank line to new line
                slS = "\n"
                spL.append(slS)
                continue
            if "#" in slS[:5]:  # skip comment line
                continue
            if "." * 10 in slS:  # page break to tag
                slS = "    _[P]"
            spL.append(slS[4:])

        self.spL = spL  # preprocessed list
        self.stS = stS  # section type
        # endregion

    def content(self, tagL, cmdL):
        """parse section content
        Args:
            tagL (list): list of valid tags
            cmdL (list): list of valid commands
        Returns:
            sutfS (str): utf doc string
            srsrS (str): rst2pdf doc string
            srstS (str): resT doc string
            foldD (dict): folder paths
            lablD (dict): labels
            rivD (dict): calculated values
            rivL (list): values for export
        """
        # region
        rivL = []
        blockB = False
        blockS = """"""
        tagS = ""
        uS = rS = xS = """"""  # returned doc line

        sutfS = self.sutfS
        srsrS = self.srsrS
        srstS = self.srstS
        foldD = self.foldD
        lablD = self.lablD
        rivD = self.rivD

        for slS in self.spL:  # loop over section lines
            # print(slS)
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
            if len(slS.strip()) < 1 and not blockB:
                sutfS += "\n"
                srsrS += " \n"
                srstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            elif blockB:  # block accumulate
                # print(f"{blockS}")
                if blockB and ("_[[Q]]" in slS):  # end of block
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
            elif slS[0:1] == "|":  # commands
                parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                self.logging.info(f"command : {cmdS}")
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:  # check list
                    cmC = rvcmd.Cmd(foldD, lablD, rivD, rivL, parL)
                    uS, rS, xS, foldD, lablD, rivD, rivL = cmC.cmdx(cmdS)
                    sutfS += uS + "\n"
                    srsrS += rS + "\n"
                    srstS += xS + "\n"
                    print(uS)  # STDOUT- command
                    continue
            elif "_[" in slS:  # tags
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
            elif ":=" in slS:
                if ":=" in tagL:
                    lineS = slS.strip()
                    tC = rvcmd.Tag(foldD, lablD, rivD, rivL, lineS)
                    uS, rS, xS, foldD, lablD, rivtvD, rivL = tC.define()
                    print(uS)  # STDOUT- tagged line
                    continue
            elif "<=" in slS:
                if "<=" in tagL:
                    lineS = slS.strip()
                    tC = rvcmd.Tag(foldD, lablD, rivD, rivL, lineS)
                    uS, rS, xS, foldD, lablD, rivtvD, rivL = tC.assign()
                    print(uS)  # STDOUT- tagged line
                    continue
            else:  # everything else
                self.sutfS += slS + "\n"
                self.srsrS += slS + "\n"
                self.srstS += slS + "\n"
                print(slS)  # STDOUT - line as is

        # write values file
        if self.stS == "V"
            fileS = folderD["valN"] + "-" + str(labelD["secnumI"]) + ".csv"
            fileP = Path(folderD["valP"], fileS)
            with open(fileP, "w") as file1:
                file1.write("\n".join(rivtL))

        return sutfS, srsrS, srstS, foldD, lablD, rivD, rivL
        # endregion
