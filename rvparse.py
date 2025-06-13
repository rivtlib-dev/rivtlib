import re
import logging
import warnings

from pathlib import Path
from . import rvtag
from . import rvcmdiv


class Section:
    """converts section string to utf and rest doc strings"""

    def __init__(self, stS, sL, folderD, labelD, rivtD):
        """preprocess section headers and string
        Args:
            stS (str): section type
            sL (list): rivt section lines
        """
        # region
        errlogP = Path(folderD["rivtP"], "temp", "rivt-log.txt")
        modnameS = __name__.split(".")[1]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogP,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
        self.logging = logging

        sutfS = ""  # utf doc
        srs2S = ""  # rst2pdf doc
        srstS = ""  # rest doc
        spL = []  # preprocessed lines
        self.folderD = folderD
        self.labelD = labelD
        self.rivtD = rivtD
        # section heading
        hL = sL[0].split("|")
        if hL[0].strip()[0:2] == "--":
            labelD["docS"] = hL[0].split("--")[1][1]  # section title
            sutfS = "\n"
            srs2S = "\n"
            srstS = "\n"
        else:
            labelD["rvtosB"] = hL[1].strip()  # open-source flag
            labelD["colorS"] = hL[2].strip()  # background color
            labelD["docS"] = hL[0].strip()  # section title
            snumI = labelD["secnumI"] + 1
            labelD["secnumI"] = snumI
            snumS = "[ " + str(snumI) + " ]"
            headS = snumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            sutfS = "\n" + headS + "\n" + bordrS + "\n"
            srs2S = "\n" + headS + "\n" + bordrS + "\n"
            srstS = "\n" + headS + "\n" + bordrS + "\n"
        # print(sutfS, srs2S, srstS)
        self.sutfS = sutfS  # utf doc
        self.srs2S = srs2S  # rst2pdf doc
        self.srstS = srstS  # rest doc
        print(sutfS)  # STDOUT section header

        spL = []  # strip leading spaces and comments from section
        for slS in sL[1:]:
            if len(slS) < 5:
                slS = "\n"
                spL.append(slS)
                continue
            if "#" in slS[:5]:
                continue
            if slS.strip()[:9] == "=-=-=-=-=":
                slS = "    _[P]"
            spL.append(slS[4:])
        self.logging.info(f"rivt function : {stS}")
        self.spL = spL  # preprocessed list
        self.stS = stS  # section type
        # endregion

    def section(self, tagL, cmdL):
        """parse section
        Args:
            self.spL (list): preprocessed section list
        Returns:
            sutfS (str): utf doc
            srs2S (str): rst2pdf doc
            srstS (str): resT doc
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): calculated values
            rivtL (list): values for export
        """
        # region
        rivtL = []
        blockB = False
        blockS = """"""
        tagS = ""
        uS = rS = xS = """"""  # returned doc line

        sutfS = self.sutfS
        srs2S = self.srs2S
        srstS = self.srstS
        folderD = self.folderD
        labelD = self.labelD
        rivtD = self.rivtD

        for slS in self.spL:  # loop over rivt section lines
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
                srs2S += " \n"
                srstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            elif blockB:  # block accumulate
                # print(f"{blockS}")
                if blockB and ("_[[Q]]" in slS):  # end of block
                    blockB = False
                    tC = rvtag.Tag(folderD, labelD, rivtD, rivtL, blockS)
                    uS, rS, xS, folderD, labelD, rivtD, rivtL = tC.tagbx(tagS)
                    print(uS)  # STDOUT - block
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
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
                    cmC = rvcmdiv.Cmdiv(folderD, labelD, rivtD, rivtL, parL)
                    uS, rS, xS, folderD, labelD, rivtD, rivtL = cmC.cmdx(cmdS)
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
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
                    tC = rvtag.Tag(folderD, labelD, rivtD, rivtL, lineS)
                    if len(tagS) < 3:  # line tag
                        uS, rS, xS, folderD, labelD, rivtD, rivtL = tC.taglx(tagS)
                        sutfS += uS + "\n"
                        srs2S += rS + "\n"
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
                    tC = rvtag.Tag(folderD, labelD, rivtD, rivtL, lineS)
                    uS, rS, xS, folderD, labelD, rivtvD, rivtL = tC.tagex()
                    print(uS)  # STDOUT- tagged line
                    continue
            else:  # everything else
                self.sutfS += slS + "\n"
                self.srs2S += slS + "\n"
                self.srstS += slS + "\n"
                print(slS)  # STDOUT - line as is

        return sutfS, srs2S, srstS, folderD, labelD, rivtD, rivtL
        # endregion
