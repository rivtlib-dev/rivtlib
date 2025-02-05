from rivtlib import tags, cmds
from pathlib import Path


class RivtParse:
    """format rivt-strings to utf and rst docs"""

    def __init__(self, tS):
        """format header string

        Args:
            tS (str): section type

        """

        self.tS = tS

        if tS == "I":
            self.cmdL = ["append", "img", "img2", "table", "text"]
            self.tagsD = {"H]": "hline", "C]": "center", "B]": "centerbold",
                          "E]": "equation", "F]": "figure", "T]": "table",
                          "#]": "foot", "D]": "descrip", "S]": "sympy",
                          "K]": "link", "PAGE]": "page", "URL]": "url",
                          "[P]]": "plainblk","[N]]": "indblk", "[O]]": "codeblk",
                          "[L]]": "latexblk",  "[I]]": "italblk", "[B]]": "boldblk",
                          "[T]]": "itinblk", "[Q]]": "quitblk", }

        elif tS == "V":
            self.cmdL = ["img", "img2", "table", "equation",
                         "eval", "vals", "vcfg", "="]
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
        """str_parse _summary_

        Args:
            strL (str): rivt string list

        Returns:
            xutfS (str): utf formatted rivt section string
            xrstS (str): rest formatted rivt section string
            folderD (dict): folder path dictionary
            labelD (dict): label dictionary
            rivtD (dict): rivt dictionary
        """

        uS = """"""         # local line
        xutfS = """"""      # accum utf section string
        xrstS = """"""      # accum rst section string
        blockS = ""         # accum block
        blockB = False      # block flag
        blckevalL = []      # current value table
        eqL = []            # equation result table
        vtableL = []        # value table for export
        hdrstS = """"""
        hdreadS = """"""
        hdutfS = """"""""
        rivtS = """"""      # rivt input string
        rmeS = """"""       # readme output string
        xremS = """"""      # redacted readme string
        evalS = """"""      # eval output string
        assignS = """"""    # assign output string
        parL = []

        # value table
        hdraL = ["variable", "value", "[value]", "description"]
        alignaL = ["left", "right", "right", "left"]
        hdreL = ["variable", "value", "[value]", "description [eq. number]"]
        aligneL = ["left", "right", "right", "left"]

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
            labelD["xch"] = hL[1].strip()              # set xchange flag
            labelD["color"] = hL[2].strip()            # set background color
            snumI = labelD["secnumI"] = labelD["secnumI"] + 1
            dnumS = labelD["docnumS"] + "-[" + str(snumI) + "]"
            headS = dnumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
            hdrstS = "**" + headS + "**" + "\n\n" + bordrS + "\n"

        xutfS += hdutfS       # add section header to local rivt str
        xrstS += hdrstS

        # print(strL)
        for uS in strL[1:]:                            # section body
            # print(f"{uS=}")
            try:
                if uS[0] == "#":                       # skip comment lines
                    continue
                elif len(uS) < 1:
                    continue
            except:
                pass
            if blockB:                                 # accumulate block
                blockS += uS
                if blockB and uS.strip() == "_[[Q]]":
                    blockB = False
                    self.parse_block(blockS)
                    taguS = rvtuC.tag_parse(tagS, lineS)  # format blocks
                    tagrS = rvtrC.tag_parse(tagS, lineS)
                    xutfS += taguS + "\n"
                    xrstS += tagrS + "\n"
                    continue
            elif uS[0:2] == "||":                       # commands
                parL = uS[2:].split("|")
                cmdS = parL[0].strip()
                pthP = Path(parL[1].strip())
                pars = parL[2].strip()
                parL = pars.split(",")
                if cmdS in self.cmdL:                   # filter commands
                    rviC = cmds.Cmd(labelD, folderD, rivtD)
                    reS, utS = rvtC.cmd_parse(cmdS, pthP, parL)
                    rvvC = cmds.CmdV(parL, labelD, folderD, rivtD)
                    reS, utS = rvvC.cmd_parse(cmdS)
                    xutfS += utS
                    xrstS += reS
            elif "_[" in uS:                            # tags
                usL = uS.split("_[")                    # split off tags
                lineS = usL[0]
                tagS = usL[1].strip()
                tagcmd = self.tagsD[tagS]                # get tag name
                if tagS in self.tagsD:                   # filter tags
                    if len(tagS) < 3:                    # line tags
                        rvlC = tags.Tag(folderD, labelD)
                        utS = rvlC.tag_parse(tagcmd, lineS)
                        xutfS += utS + "\n"
                    else:                                # block tags
                        blockB = True
                        rvbC = tags.Tag(folderD, labelD)
                        reS = rvbC.tag_parse(tagcmd, lineS)
                        xrstS += reS + "\n"
            else:
                xutfS += uS + "\n"                       # return other
                xrstS += uS + "\n"

        return (xutfS, xrstS, folderD, labelD, rivtD)
