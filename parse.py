from rivtlib import tags, cmds
from pathlib import Path


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
                          "K]": "link", "PAGE]": "page", "URL]": "url",
                          "[P]]": "blkplain",  "[O]]": "blkcode", "[B]]": "blkbold",
                          "[I]]": "blkital",  "[N]]": "blkind", "[T]]": "blkitind",
                          "[L]]": "blklatex",  "[Q]]": "blkquit", }

        elif tS == "V":
            self.cmdL = ["IMG", "IMG2", "TABLE", "EVAL", "VALS", "VCFG", "="]
            self.tagsD = {"E]": "equation", "F]": "figure", "T]": "table",
                          "C]": "center"}

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
        """ add header to rivt strings and parse

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

        # section header
        hS = strL[0]
        hL = hS.split("|")
        # skip printing section title
        if hS.strip()[0:2] == "--":
            labelD["docS"] = hL[0].strip()    # section title
            labelD["xch"] = hL[1].strip()     # xchange flag
            labelD["color"] = hL[2].strip()   # background color
            hdutfS = hdrstS = "\n"
        else:
            # section title
            titleS = labelD["docS"] = hL[0].strip()
            labelD["xch"] = hL[1].strip()               # set xchange flag
            labelD["color"] = hL[2].strip()             # set background color
            snumI = labelD["secnumI"] = labelD["secnumI"] + 1
            dnumS = labelD["docnumS"] + "-[" + str(snumI) + "]"
            headS = dnumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
            hdrstS = "**" + headS + "**" + "\n\n" + bordrS + "\n"

        xutfS += hdutfS                                  # add section header
        xrstS += hdrstS
        print(hdutfS)

        # print(strL)
        for ulS in strL[1:]:                             # section body
            # print(f"{uS=}")
            try:
                if ulS[0] == "#":                        # skip comment lines
                    continue
                elif len(ulS) < 1:
                    continue
            except:
                pass
            if blockB:                                   # accumulate block
                blockS += ulS
                if blockB and ulS.strip() == "_[[Q]]":
                    blockB = False
                    uS, rS = tC.tag_parse(tagcmd, blockS)
                    xutfS += uS + "\n"
                    xrstS += rS + "\n"
                    print(blockS)
                    continue
            elif ulS[0:1] == "|":                        # commands
                if ulS[0:1] == "||":
                    parL = ulS[2:].split("|")
                else:
                    parL = ulS[1:].split("|")
                cmdS = parL[0].strip()                  # command
                pthS = parL[1].strip()                  # file path
                parS = parL[2].strip()
                if cmdS in self.cmdL:                   # filter commands
                    rviC = cmds.Cmd(folderD, labelD)
                    utS, reS = rviC.cmd_parse(cmdS, pthS, parS)
                    if self.tS == "V":
                        rvvC = cmds.CmdV(labelD, folderD, rivtD)
                        utS, reS = rvvC.cmd_parse(cmdS, pthS, parS)
                    xutfS += utS
                    xrstS += reS
            elif "_[" in ulS or "__[" in ulS:            # tags
                ulL = ulS.split("_[")                    # split off tags
                lineS = ulL[0].strip()
                tagS = ulL[1].strip()
                tagcmd = self.tagsD[tagS]                # get tag name
                if tagS in self.tagsD:                   # filter tags
                    tC = tags.Tag(folderD, labelD)
                    if len(tagS) < 3:                    # line tags
                        uS, rS = tC.tag_parse(tagcmd, lineS)
                        xutfS += uS + "\n"
                        xrstS += rS + "\n"
                    else:
                        blockS = ""                      # block tags - init
                        blockB = True
                        try:
                            xutfS += lineS + "\n"
                            xrstS += lineS + "\n"
                        except:
                            pass
            else:
                print(ulS)
                xutfS += uS + "\n"                       # return other
                xrstS += rS + "\n"

        return (xutfS, xrstS, folderD, labelD, rivtD)
