import re
from pathlib import Path
from datetime import datetime, time
from rivtlib import cmds, tags

from . import rvals, rwrite


class RivtParse:
    """format rivt-strings to utf and rst docs"""

    def __init__(self, tS):
        """

        Args:
            tS (str): section type
        """
        self.tS = tS
        # print(f"{tS=}")
        if tS == "R":
            self.cmdL = ["run", "process"]
            self.tagsD = {}
        elif tS == "I":
            self.cmdL = ["IMG", "IMG2", "TABLE", "TEXT"]
            self.tagsD = {
                "B]": "centerbold",
                "C]": "center",
                "D]": "descrip",
                "E]": "equa",
                "F]": "figure",
                "H]": "hline",
                "P]": "page",
                "S]": "sympy",
                "T]": "table",
                "U]": "url",
                "#]": "foot",
                "[B]]": "blkindbld",
                "[I]]": "blkindit",
                "[L]]": "blklatex",
                "[O]]": "blkcode",
                "[Q]]": "blkquit",
            }
        elif tS == "V":
            self.cmdL = ["IMG", "IMG2", "VALUES"]
            self.tagsD = {
                "E]": "equa",
                "F]": "figure",
                "V]": "value",
                "S]": "sympy",
                "P]": "page",
                "[V]]": "blkval",
                "[Q]]": "blkquit",
            }
        elif tS == "T":
            self.cmdL = ["python"]
            self.tagsD = {}
        elif tS == "W":
            self.cmdL = ["publish", "pend"]
            self.tagsD = {}
        else:
            pass

    def symstrip(self, txtS):
        """strip leading spaces,  strip * from utf doc string

        Args:
            txtS (str): line of rivt text

        Returns:
            str: stripped line - utf output
        """
        # bold markup
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

        return txtrS

    def parse_sec(self, strL, folderD, labelD, rivtpD, rivtvD):
        """parse section

        Args:
            strL (list): section string

        Returns:
            xutfS (str): utf formatted section string
            xrstS (str): rest formatted section string
            folderD (dict): folder paths
            labelD (dict): labels
            rivtD (dict): rivt objects
        """

        # ulS = current line
        blockB = False  # block flag
        blockS = """"""  # accum block
        uS = """"""  # formatted utf line
        rS = """"""  # formmated reSt line
        xutfS = """"""  # accum utf section string
        xrstS = """"""  # accum rst section string
        hS = strL[0]  # section header
        hL = hS.split("|")
        if self.tS == "W":  # omit header for Write
            hdutfS = ""
            hdrstS = ""
        elif hS.strip()[0:2] == "--":
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
        xutfS += hdutfS
        xrstS += hdrstS
        print(hdutfS)  # stdout header
        try:
            valN = folderD["valN"]  # value export file
            valN = valN.replace("qqqqqq", str(snumI))
            valsP = folderD["valsP"]
            valP = Path(valsP, valN)
            folderD["valP"] = valP
        except:
            pass
        # print(strL)
        # print(f"{self.tS=}")
        blockS = """"""
        for ulS in strL[1:]:  # section contents
            # print(f"{ulS=}")
            if len(ulS.strip()) < 1 and not blockB:
                xutfS += "\n"
                xrstS += " \n"
                print(" ")  # stdout blank
                continue
            try:
                if ulS[0] == "#":  # skip comments
                    continue
            except:
                pass
            if blockB:  # block accumulate
                blockS += ulS + "\n"
                if blockB and ulS.strip() == "_[[Q]]":  # block end
                    blockB = False
                    if self.tS == "V":  # valform block
                        blockL = blockS.split("\n")
                        tvC = rvals.TagV(folderD, labelD, rivtpD, rivtvD)
                        uS, rS, folderD, labelD, rivtpD, rivtvD = tvC.tag_parse(
                            tagcmd, blockL
                        )
                        print(uS)  # stdout valread
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                        blockL = []
                        continue
                    uS, rS = tC.tag_parse(tagcmd, blockS)
                    print(uS)  # stdout block
                    xutfS += uS + "\n"
                    xrstS += rS + "\n"
                    blockS = """"""
                    continue
            elif ulS[0:1] == "|":  # read/write commands
                if ulS[0:2] == "||":
                    parL = ulS[2:].split("|")
                else:
                    parL = ulS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                # print(cmdS, pthS, parS)
                if cmdS in self.cmdL:
                    if self.tS == "R":  # run commands
                        pass
                    elif self.tS == "I":  # insert commands
                        rviC = cmds.Cmd(folderD, labelD)
                        uS, rS, folderD, labelD = rviC.cmd_parse(cmdS, pthS, parS)
                        print(uS)  # stdout command
                        xutfS += uS
                        xrstS += rS
                        continue
                    elif self.tS == "V":  # values command
                        valsP = folderD["valsP"]
                        rvvC = rvals.CmdV(folderD, labelD, rivtpD, rivtvD)
                        uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                            cmdS, pthS, parS
                        )
                        print(uS)  # stdout valread
                        xutfS += uS
                        xrstS += rS
                        continue
                    elif self.tS == "T":  # tools command
                        continue
                    else:
                        pass
            elif "_[" in ulS:  # tags
                ulL = ulS.split("_[")  # split tag
                lineS = ulL[0].strip()
                tagS = ulL[1].strip()
                tagcmd = self.tagsD[tagS]  # get tag name
                if tagS in self.tagsD:  # filter tags
                    # print(f"{tagS=}")
                    tC = tags.Tag(folderD, labelD)
                    if len(tagS) < 3:  # line tag
                        uS, rS, folderD, labelD = tC.tag_parse(tagcmd, lineS)
                        print(uS)  # stdout tag
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                        continue
                    else:
                        blockS = ""  # block start
                        blockB = True
                        try:
                            xutfS += lineS + "\n"
                            xrstS += lineS + "\n"
                        except:
                            continue
                else:
                    pass
            elif self.tS == "V" and ":=" in ulS:  # ':=' command
                eqL = ulS.split("|", 1)
                eqS = eqL[0].strip()
                parS = eqL[1].strip()
                rvvC = rvals.CmdV(folderD, labelD, rivtpD, rivtvD)
                uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                    "equate", eqS, parS
                )
                xutfS += uS
                xrstS += rS
                print(uS)  # stdout equation
                uS, rS, folderD, labelD, rivtpD, rivtvD = rvvC.cmd_parse(
                    "equtable", eqS, parS
                )
                print(uS)  # stdout equ table
                xutfS += uS
                xrstS += rS
            else:
                xrstS += ulS + "\n"
                ulS = self.asterstrip(ulS)  # strip asterik format
                print(ulS)  # stdout - no format
                xutfS += ulS + "\n"

        if self.tS == "V":
            with open(folderD["valP"], "w") as file:  # export value file
                file.write(labelD["valexpS"])

        if self.tS == "T":
            pass

        if self.tS == "W":
            rwrite()

        return (xutfS, xrstS, folderD, labelD, rivtpD, rivtvD)
