from pathlib import Path
from rivtlib import tags, cmds, vals


class RivtParse:
    """ format rivt-strings to utf and rst docs"""

    def __init__(self, tS):
        """format header string

        Args:
            tS (str): section type
        """
        self.tS = tS
        if tS == "I":
            self.cmdL = ["APPEND", "IMG", "IMG2", "TABLE", "TEXT"]
            self.tagsD = {"H]": "hline", "C]": "center", "B]": "centerbold",
                          "E]": "equation", "F]": "figure", "T]": "table",
                          "#]": "foot", "D]": "descrip", "S]": "sympy",
                          "K]": "link", "A]": "page", "URL]": "url",
                          "[P]]": "blkplain",  "[O]]": "blkcode", "[B]]": "blkbold",
                          "[I]]": "blkital",  "[N]]": "blkind", "[T]]": "blkitind",
                          "[L]]": "blklatex",  "[Q]]": "blkquit", }
        elif tS == "V":
            self.cmdL = ["IMG", "IMG2", "TABLE", "VREAD"]
            self.tagsD = {"E]": "equation", "F]": "figure", "T]": "table",
                          "PAGE]": "page", "[V]]": "values", "[Q]]": "quit"}
        elif tS == "R":
            self.cmdL = ["run", "process"]
            self.tagsD = {}
        elif tS == "T":
            self.cmdL = ["python"]
            self.tagsD = {}
        elif tS == "W":
            self.cmdL = ["write"]
            self.tagsD = {}
        else:
            pass

    def parse_str(self, strL, folderD, labelD, rivtD):
        """ add header and parse section contents

        Args:
            strL (str): rivt string list

        Returns:
            xutfS (str): utf formatted rivt section string
            xrstS (str): rest formatted rivt section string
            folderD (dict): folder path dictionary
            labelD (dict): label dictionary
            rivtD (dict): rivt dictionary
        """

        ulS = """"""        # current line
        uS = """"""         # formatted utf line
        rS = """"""         # formmated reSt line
        blockS = ""         # accum block
        blockB = False      # block flag
        xutfS = """"""      # accum utf section string
        xrstS = """"""      # accum rst section string
        rivtS = """"""      # rivt input string
        rmeS = """"""       # readme output string
        xremS = """"""      # redacted readme string
        evalS = """"""      # eval output string
        assignS = """"""    # assign output string
        hdrstS = """"""
        hdreadS = """"""
        hdutfS = """"""""
        parL = []

        hS = strL[0]                                    # section header
        hL = hS.split("|")
        if hS.strip()[0:2] == "--":
            labelD["docS"] = hL[0].strip()              # section title
            labelD["xch"] = hL[1].strip()               # xchange flag
            labelD["color"] = hL[2].strip()             # background color
            hdutfS = hdrstS = "\n"                      # empty header
        else:
            # section title
            titleS = labelD["docS"] = hL[0].strip()     # section title
            labelD["xch"] = hL[1].strip()               # xchange flag
            labelD["color"] = hL[2].strip()             # background color
            snumI = labelD["secnumI"] = labelD["secnumI"] + 1
            dnumS = labelD["docnumS"] + "-[" + str(snumI) + "]"
            headS = dnumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
            hdrstS = "**" + headS + "**" + "\n\n" + bordrS + "\n"

        print(hdutfS)                                    # stdout header
        xutfS += hdutfS
        xrstS += hdrstS

        # print(strL)
        blockS = """"""
        for ulS in strL[1:]:                            # section contents
            # print(f"{ulS=}")
            try:
                if ulS[0] == "#":                       # skip comment lines
                    continue
                elif len(ulS) < 1:
                    continue
            except:
                pass
            if blockB:                                  # accumulate block
                blockS += ulS + "\n"
                if blockB and ulS.strip() == "_[[Q]]":
                    blockB = False
                    if self.tS == "V":                  # vread block
                        blockL = blockS.split("\n")
                        tC = vals.TagV(folderD, labelD)
                        uS, rS = tC.tag_parse(tagcmd, blockL)
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                        blockL = []
                        print(uS)                       # stdout vread
                        continue
                    uS, rS = tC.tag_parse(tagcmd, blockS)
                    print(uS)                           # stdout block
                    xutfS += uS + "\n"
                    xrstS += rS + "\n"
                    blockS = """"""
                    continue
            elif self.tS == "R":                        # run function
                continue
            elif self.tS == "T":                        # tools function
                continue
            elif self.tS == "W":                        # write function
                continue
            elif ulS[0:1] == "|":                         # read/write commands
                if ulS[0:2] == "||":
                    parL = ulS[2:].split("|")
                else:
                    parL = ulS[1:].split("|")
                cmdS = parL[0].strip()
                pthS = parL[1].strip()
                parS = parL[2].strip()
                if cmdS in self.cmdL:
                    if self.tS == "V":                   # vread command
                        rvvC = vals.CmdV(folderD, labelD)
                        utS, reS = rvvC.cmd_parse(cmdS, pthS, parS)
                    else:                                # insert commands
                        rviC = cmds.Cmd(folderD, labelD)
                        utS, reS = rviC.cmd_parse(cmdS, pthS, parS)
                        print(utS)                       # stdout command
                        xutfS += utS
                        xrstS += reS
            elif self.tS == "V":
                if "=" in ulS:                           # command =
                    eqL = ulS.split("|", 1)
                    eqS = eqL[0].strip()
                    parS = eqL[1].strip()
                    rvvC = vals.CmdV(folderD, labelD)
                    utS, reS = rvvC.cmd_parse("valeq", eqS, parS)
                    print(utS)                           # stdout =
                    xutfS += utS
                    xrstS += reS
            elif "_[" in ulS or "__[" in ulS:            # tags
                ulL = ulS.split("_[")                    # split off tag
                lineS = ulL[0].strip()
                tagS = ulL[1].strip()
                tagcmd = self.tagsD[tagS]                # get tag name
                if tagS in self.tagsD:                   # filter tags
                    tC = tags.Tag(folderD, labelD)
                    if len(tagS) < 3:                    # line tag
                        uS, rS = tC.tag_parse(tagcmd, lineS)
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                    else:
                        blockS = ""                      # block - init
                        blockB = True
                        try:
                            xutfS += lineS + "\n"
                            xrstS += lineS + "\n"
                        except:
                            pass
            else:
                print(ulS)                               # stdout - no format
                xutfS += uS + "\n"                       # return other
                xrstS += rS + "\n"

        return (xutfS, xrstS, folderD, labelD, rivtD)
