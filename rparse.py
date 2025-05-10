import re
from pathlib import Path

from . import rcmd, rtag

from . import rparam


class Section:
    """converts section string to utf and rest doc strings"""

    def __init__(self, stS, sL, labelD):
        """
        preprocess section headers and strings

        Args:
            stS (str): section type
            sL (list): rivt section lines

        """
        sutfS = ""  # utf doc
        srs2S = ""  # rst2pdf doc
        srstS = ""  # rest doc
        spL = []  # preprocessed lines

        # section header
        hL = sL[0].split("|")
        labelD["docS"] = hL[0].strip()  # section title
        labelD["xch"] = hL[1].strip()  # xchange flag
        labelD["color"] = hL[2].strip()  # background color
        if hL[0].strip()[0:2] == "--":
            labelD["docS"] = hL[2:].strip()  # section title
        else:
            snumI = labelD["secnumI"] = labelD["secnumI"] + 1
            snumS = "[ " + str(snumI) + " ]"
            headS = snumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            sutfS = "\n" + headS + "\n" + bordrS + "\n"
            srs2S = "\n" + headS + "\n" + bordrS + "\n"
            srstS = "\n" + headS + "\n" + bordrS + "\n"
            # print(sutfS, srstS, xrstS)

        # strip leading spaces, # comments, * markup for utf doc
        for slS in sL[1:]:
            try:
                slS = slS[4:]
            except:
                slS = slS
            print("----", slS)
            try:
                if slS[0] == "#":  # comments
                    continue
            except:
                print("\n s")
                continue
            txt1L = re.findall(r"\*\*(.*?)\*\*", slS)  # bold
            if len(txt1L) > 0:
                for tS in txt1L:
                    t1S = "**" + tS + "**"
                    txtaS = slS.replace(t1S, tS)
                    spL.append(txtaS)
            else:
                spL.append(slS)

            txt2L = re.findall(r"\*(.*?)\*", slS)  # italic
            if len(txt2L) > 0:
                for tS in txt2L:
                    t2S = "*" + tS + "*"
                    txtrS = slS.replace(t2S, tS)
                    spL.append(txtrS)
            else:
                spL.append(slS)
            # print(f"{txt1L=}")

        self.spL = spL  # preprocessed list
        self.stS = stS  # section type
        self.sutfS = sutfS  # utf doc
        self.srs2S = srs2S  # rst2pdf doc
        self.srstS = srstS  # rest doc

    def section(self, tagL, cmdL, folderD, labelD, rivtD):
        """parse section

        Args:
            self.spL (list): preprocessed section list

        Returns:
            sutfS (str): utf doc section
            srstS (str): rest doc section
            xrstS (str): tex doc section
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): calculated values

        """
        blockB = False
        blockS = """"""
        tagS = ""
        uS = rS = xS = """"""  # doc line
        sutfS = self.sutfS
        srs2S = self.srs2S
        srstS = self.srstS

        for slS in self.spL:  # loop over section lines
            # print(f"{slS=}")
            if len(slS.strip()) < 1 and not blockB:
                sutfS += "\n"
                srs2S += " \n"
                srstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            if blockB:  # block accumulate
                blockS += slS + "\n"
                if blockB and ("_[[Q]]" in slS):  # block end
                    blockB = False
                    tC = rtag.Tag(folderD, labelD, rivtD)
                    uS, rS, xS = tC.blocktag(tagS, blockS)
                    print(uS)  # STDOUT - block
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
                    srstS += xS + "\n"
                    tagS = ""
                    blockS = """"""
                    continue
            if slS[0:1] == "|":  # commands
                if slS[0:2] == "||":
                    parL = slS[2:].split("|")
                else:
                    parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:  # check list
                    comC = rcmd.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.comm(cmdS, pthS, parS)
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
                    srstS += xS + "\n"
                    print(uS)  # STDOUT- command
                    continue

            elif "_[" in slS:  # tags
                slL = slS.split("_[")
                lineS = slL[0].strip()
                tagS = slL[1].strip()
                if tagS in tagL:  # check list
                    # print(f"{tagS=}")
                    tC = rtag.Tag(folderD, labelD, rivtD)
                    if len(tagS) < 3:  # line tag
                        uS, rS, xS, folderD, labelD, rivtD = tC.linetag(tagS, lineS)
                        sutfS += uS + "\n"
                        srs2S += rS + "\n"
                        srstS += xS + "\n"
                        print(uS)  # STDOUT- tagged line
                        continue
                    else:  # block tag - start
                        blockS = ""
                        blockB = True
                        blockS += lineS + "\n"
                        continue
            elif ":=" in slS:  # equals tag
                if ":=" in tagS:
                    eqL = slS.split("|", 1)
                    eqS = eqL[0].strip()
                    parS = eqL[1].strip()
                    comC = rcmd.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.valtag(cmdS, eqS, parS)
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
                    srstS += xS + "\n"
                    print(uS)  # STDOUT equation
                    uS, rS, xS, folderD, labelD, rivtD = comC.valtag(
                        "equtable", eqS, parS
                    )
                    sutfS += uS + "\n"
                    srs2S += rS + "\n"
                    srstS += xS + "\n"
                    print(uS)  # STDOUT equation table
            else:  # everything else
                sutfS += slS + "\n"
                srs2S += slS + "\n"
                srstS += slS + "\n"
                print(slS)  # STDOUT - line as is

        return sutfS, srs2S, srstS, folderD, labelD, rivtD
