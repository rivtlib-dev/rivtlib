import re
from pathlib import Path

from rivtlib import cmds, params, tags


class Section:
    """section string to utf, rst and xrst doc string"""

    def __init__(self, stS, sL, labelD):
        """
        preprocess section headers and strings

        Args:
            stS (str): section type
            sL (list): rivt section lines

        """
        sutfS = ""
        srstS = ""
        xrstS = ""
        ssL = []

        # section header
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
            # print(sutfS, srstS, xrstS)

        # strip leading spaces, # comments, * markup for utf doc
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
            self.ssL (list): preprocessed section list

        Returns:
            sutfS (str): utf doc section
            srstS (str): rest doc section
            xrstS (str): tex doc section
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): calculated values

        """
        blockB = False  # block flag
        blockS = """"""  # block accumulator
        uS = rS = xS = """"""  # doc line
        sutfS = srstS = xrstS = """"""  # utf doc

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
                    tC = tags.Tag(folderD, labelD, rivtD)
                    uS, rS, xS = tC.blocktags(tagS, blockS)
                    print(uS)  # STDOUT - block
                    sutfS += uS + "\n"
                    srstS += rS + "\n"
                    xrstS += xS + "\n"
                    tagS = ""
                    blockS = """"""
                    continue
            if self.stS == "R":
                tagD, cmdL = params.rtag_cmd()
            elif self.stS == "I":
                tagD, cmdL = params.itag_cmd()
            elif self.stS == "V":
                tagD, cmdL = params.vtag_cmd()
            elif self.stS == "T":
                tagD, cmdL = params.ttag_cmd()
            else:
                pass

            if slS[0:1] == "|":  # commands
                if slS[0:2] == "||":
                    parL = slS[2:].split("|")
                else:
                    parL = slS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                # print(cmdS, pthS, parS)
                if cmdS in cmdL:
                    comC = cmds.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.cmd_parse(
                        cmdS, pthS, parS
                    )
                    sutfS += uS + "\n"
                    srstS += rS + "\n"
                    xrstS += xS + "\n"
                    print(uS)  # STDOUT- command
                    continue
            elif "_[" in slS:  # tags
                slL = slS.split("_[")
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
                    else:  # block tag - start
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
                    comC = cmds.Cmd(folderD, labelD, rivtD)
                    uS, rS, xS, folderD, labelD, rivtvD = comC.cmd_parse(
                        cmdS, eqS, parS
                    )
                    sutfS += uS + "\n"
                    srstS += rS + "\n"
                    xrstS += xS + "\n"
                    print(uS)  # STDOUT equation
                    uS, rS, xS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                        "equtable", eqS, parS
                    )
                    print(uS)  # STDOUT equation table
                    xutfS += uS
                    xrstS += rS
            else:
                xrstS += slS + "\n"
                print(slS)  # STDOUT - line as is
                xutfS += slS + "\n"

        return sutfS, srstS, xrstS, folderD, labelD, rivtD
