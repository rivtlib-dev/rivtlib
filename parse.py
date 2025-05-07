import re
from configparser import ConfigParser
from datetime import datetime
from pathlib import Path

from rivtlib import cmds, rinsert, rrun, rtool, rvalue, rwrite, tags


class Section:
    """section string to utf, rest and xrst doc string"""

    def __init__(self, stS, sL):
        """

        Args:
            stS (str): section type
            sL (list): section lines
        """

    def stitle(self, shS):
        hL = shS.split("|")

        if hS.strip()[0:2] == "--":
            labelD["docS"] = hL[0].strip()  # section title
            labelD["xch"] = hL[1].strip()  # xchange flag
            labelD["color"] = hL[2].strip()  # background color
            hdutfS = hdrstS = "  "  # empty header
        else:
            titleS = labelD["docS"] = hL[0].strip()  # section title
            labelD["xch"] = hL[1].strip()  # xchange flag
            labelD["color"] = hL[2].strip()  # background color
            snumI = labelD["secnumI"] + 1
            labelD["secnumI"] = snumI
            dnumS = "[ " + str(snumI) + " ]"
            headS = dnumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            hdutfS = "\n" + headS + "\n" + bordrS + "\n"
            hdrstS = "\n" + headS + "\n" + bordrS + "\n"
            hdrxtS = "\n" + headS + "\n" + bordrS + "\n"

            return hdutfS, hdrstS, hdrstS

            # print(hdutfS, hdrstS, hdrstS)
        return hdutfS, hdrstS, hdxstS

    def sstrip(self, sL):
        """strip -> leading spaces, # comment, * from utf string

        Args:
            txtS (str): line of rivt text

        Returns:
           sustfS (str) : stripped line - utf output
           sustfS (str) : stripped line - utf output
           sustfS (str) : stripped line - utf output
        """
        # bold markup
        for slS in sL:
            txtaS = txtS
            txt1L = re.findall(r"\*\*(.*?)\*\*", txtS)
            if len(txt1L) > 0:
                for tS in txt1L:
                    t1S = "**" + tS + "**"
                    txtaS = txtS.replace(t1S, tS)
            else:
                pass
            # italic markup
            txt2L = re.findall(r"\*(.*?)\*", txtaS)
            if len(txt2L) > 0:
                for tS in txt2L:
                    t2S = "*" + tS + "*"
                    txtrS = txtaS.replace(t2S, tS)
            else:
                txtrS = txtrS
            # print(f"{txt1L=}")

            if slS[0] == "#":  # skip comments
                pass

        return sutfS, srstS, xrstS

    def section(self, strL, folderD, labelD, rivtD):
        """parse section

        Args:
            strL (list): section string

        Returns:
            sutfS (str): utf formatted section string
            srstS (str): rest formatted section string
            xrstS (str): rest formatted section string
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): rivt objects
        """

        blockB = False  # block flag
        blockS = """"""  # accum block
        uS = """"""  # utf doc line
        rS = """"""  # rest doc line
        xS = """"""  # tex doc line
        sutfS = """"""  # utf doc section
        srstS = """"""  # rst doc section
        xrstS = """"""  # tex doc section

        sutfS, srstS, xrstS = self.stitle(self, self.sL[0])  # section title
        ssL = self.sstrip(self, self.sL[1:])  # preprocess section

        for slS in ssL[1:]:  # loop over section lines
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
            elif ulS[0:1] == "|":  # commands
                if ulS[0:2] == "||":
                    parL = ulS[2:].split("|")
                else:
                    parL = ulS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                # print(cmdS, pthS, parS)
                if cmdS in self.cmdL:
                    comC = cmds.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.cmd_parse(
                        cmdS, pthS, parS
                    )
            elif "_[" in ulS:  # tags
                ulL = ulS.split("_[")  # split tag
                lineS = ulL[0].strip()
                tagS = ulL[1].strip()
                tnameS = self.tagsD[tagS]  # get tag name
                if tagS in self.tagsD:  # filter tags
                    # print(f"{tagS=}")
                    tC = tags.Tag(folderD, labelD)
                    if len(tagS) < 3:  # line tag
                        uS, rS, folderD, labelD = tC.tag_parse(tnameS, lineS)
                        print(uS)  # STDOUT- tagged line
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                        continue
                    else:  # block start
                        blockS = ""
                        blockB = True
                        try:
                            xutfS += lineS + "\n"
                            xrstS += lineS + "\n"
                        except:
                            continue
                else:
                    pass
            elif ":=" in ulS:  # equals tag
                tagS = ulL[1].strip()
                tnameS = self.tagsD[":="]  # get tag name
                if ":=" in self.tagsD[tagS]:
                    eqL = ulS.split("|", 1)
                    eqS = eqL[0].strip()
                    parS = eqL[1].strip()
                    rvvC = rvals.CmdV(folderD, labelD, rivtpD, rivtvD)
                    uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
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
                xrstS += ulS + "\n"
                ulS = self.asterstrip(ulS)  # strip asterik format
                print(ulS)  # STDOUT - line as is
                xutfS += ulS + "\n"

        if self.tS == "T":
            rtool()

        return (sutfS, srstS, xrstS, folderD, labelD, rivtD)
