import re
from pathlib import Path

from rivtlib import cmds, rinsert, rrun, rtool, rvalue, tags


class Section:
    """section string to utf, rst and xrst doc string"""

    def __init__(self, stS, sL, labelD):
        """
        preprocess section strings

        Args:
            stS (str): section type
            sL (list): rivt section lines

        """
        sutfS = ""
        srstS = ""
        xrstS = ""
        ssL = []
        # write section header
        hL = sL[0].split("|")
        labelD["docS"] = hL[0].strip()  # section title
        labelD["xch"] = hL[1].strip()  # xchange flag
        labelD["color"] = hL[2].strip()  # background color
        if hL.strip()[0:2] == "--":
            labelD["docS"] = hL[2:].strip()  # section title
        else:
            snumI = labelD["secnumI"] = labelD["secnumI"] + 1
            snumS = "[ " + str(snumI) + " ]"
            headS = snumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            sutfS = "\n" + headS + "\n" + bordrS + "\n"
            srstS = "\n" + headS + "\n" + bordrS + "\n"
            xrstS = "\n" + headS + "\n" + bordrS + "\n"
            # print(hdutfS, hdrstS, hdrstS)

        # strip leading spaces, # comments, * markup for utf doc string
        for slS in sL[1:]:
            if slS[0] == "#":  # comments
                continue
            txt1L = re.findall(r"\*\*(.*?)\*\*", slS)  # bold
            if len(txt1L) > 0:
                for tS in txt1L:
                    t1S = "**" + tS + "**"
                    txtaS = slS.replace(t1S, tS)
                    ssL.append(txtaS)
            else:
                ssL.append(slS)

            txt2L = re.findall(r"\*(.*?)\*", slS)  # italic
            if len(txt2L) > 0:
                for tS in txt2L:
                    t2S = "*" + tS + "*"
                    txtrS = slS.replace(t2S, tS)
                    ssL.append(txtrS)
            else:
                ssL.append(slS)
            # print(f"{txt1L=}")

        self.ssL = ssL  # stripped list
        self.stS = stS  # section type
        self.sutfS = sutfS  # utf doc
        self.srstS = srstS  # rst doc
        self.xrstS = xrstS  # tex doc

    def section(self, folderD, labelD, rivtD):
        """parse section

        Args:
            strL (list): section string

        Returns:
            sutfS (str): utf doc string
            srstS (str): rest doc string
            xrstS (str): tex doc string
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): calculated values

        """
        blockB = False  # block flag
        blockS = """"""  # block accumulator
        uS = """"""  # utf doc line
        rS = """"""  # rest doc line
        xS = """"""  # tex doc line
        sutfS = """"""  # utf doc
        srstS = """"""  # rst doc
        xrstS = """"""  # tex doc

        for slS in self.ssL:  # loop over section lines
            # print(f"{slS=}")
            if len(slS.strip()) < 1 and not blockB:
                sutfS += "\n"
                srstS += " \n"
                xrstS += " \n"
                print(" ")  # STDOUT- blank line
                continue
            if blockB:  # block accumulate
                blockS += slS + "\n"
                if blockB and ("_[[Q]]" in slS):  # block end
                    blockB = False
                    tC = tags.Tag()
                    uS, rS, xS = tags.blocks(self.tS, blockS)
                    print(uS)  # STDOUT - block
                    sutfS += uS + "\n"
                    srstS += rS + "\n"
                    xrstS += xS + "\n"
                    blockS = """"""
                    continue
            elif slS[0:1] == "|":  # commands
                if slS[0:2] == "||":
                    parL = slS[2:].split("|")
                else:
                    parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                # print(cmdS, pthS, parS)
                if cmdS in self.cmdL:
                    comC = cmds.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.cmd_parse(
                        cmdS, pthS, parS
                    )
            elif "_[" in slS:  # tags
                slL = slS.split("_[")  # split tag
                lineS = slL[0].strip()
                tagS = slL[1].strip()
                tnameS = self.tagsD[tagS]  # get tag name
                if tagS in self.tagsD:  # filter tags
                    # print(f"{tagS=}")
                    tC = tags.Tag(folderD, labelD)
                    if len(tagS) < 3:  # line tag
                        uS, rS, xS, folderD, labelD = tC.tag_parse(tnameS, lineS)
                        sutfS += uS + "\n"
                        srstS += rS + "\n"
                        xrstS += xS + "\n"
                        print(uS)  # STDOUT- tagged line
                        continue
                    else:  # block start
                        blockS = ""
                        blockB = True
                        blockS += lineS + "\n"
                else:
                    pass
            elif ":=" in slS:  # equals tag
                tagS = slL[1].strip()
                tnameS = self.tagsD[":="]  # get tag name
                if ":=" in self.tagsD[tagS]:
                    eqL = slS.split("|", 1)
                    eqS = eqL[0].strip()
                    parS = eqL[1].strip()
                    rvvC = rvals.CmdV(folderD, labelD, rivtD)
                    uS, rS, folderD, labelD, rivtvD = rvvC.cmd_parse(
                        "equate", eqS, parS
                    )
                xutfS += uS
                xrstS += rS
                print(uS)  # STDOUT equation
                uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                    "equtable", eqS, parS
                )
                print(uS)  # STDOUT equals table
                xutfS += uS
                xrstS += rS
            else:
                xrstS += slS + "\n"
                print(ulS)  # STDOUT - line as is
                xutfS += ulS + "\n"

        return (sutfS, srstS, xrstS, folderD, labelD, rivtD)
