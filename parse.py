from rivtlib import tag, cmd
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
            self.cmdL = ["append", "image", "table", "text"]
            self.tagsD = {"u]": "underline", "c]": "center", "r]": "right",
                          "e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description", "s]": "sympy",
                          "link]": "link", "line]": "line", "page]": "page",
                          "[b]]": "bold", "[i]]": "italic", "[c]]": "centerblk",
                          "[p]]": "plainblk", "[l]]": "latexblk",
                          "[o]]": "codeblk", "[bi]]": "boldindent",
                          "[ii]]": "italicindent", ",": "url", "[q]]": "quitblk"}

        elif tS == "V":
            self.cmdL = ["image", "table", "assign", "eval"]
            self.tagsD = {"e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description", "v]": "value",
                          "s]": "sympy", "=": "eval", "[V]]": "values"}

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

    def str_parse(self, strL, folderD, labelD, rivtD):
        """str_parse _summary_

        Args:
            strL (_type_): _description_

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
        if hS.strip()[0:2] == "--":
            labelD["docS"] = hL[0].strip()             # set section title
            labelD["xch"] = hL[1].strip()              # set xchange flag
            labelD["color"] = hL[2].strip()            # set background color
            hdutfS = hdrstS = "\n"
        else:
            labelD["docS"] = hL[0].strip()             # set section title
            labelD["xch"] = hL[1].strip()              # set xchange flag
            labelD["color"] = hL[2].strip()            # set background color
            labelD["secnumI"] = labelD["secnumI"] + 1  # increment section
            dnumS = labelD["docnumS"] + "-[" + str(snumI) + "]"
            headS = dnumS + " " + hL[0].strip()
            bordrS = labelD["widthI"] * "-"
            hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
            hdrstS = (
                ".. raw:: latex"
                + "   \n\n ?x?vspace{.2in} "
                + "   ?x?begin{tcolorbox} "
                + "   ?x?textbf{ " + titleS + "}"
                + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
                + "   ?x?end{tcolorbox}"
                + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
                + "\n\n")
        xutfS += hdutfS                                # add to local rivt str
        xrstS += hdrstS

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
                if blockB and uS.strip() == "_[[q]]":
                    blockB = False
                    parse_block(blockS)
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
                if cmdS in self.cmdL:
                    rvtC = cmd.CmdUTF(labelD, folderD, rivtD)
                    utS = rvtC.cmd_parse(cmdS, pthP, parL)
                    rvtC = cmd.CmdRST(parL, labelD, folderD, rivtD)
                    reS = rvtC.cmd_parse(cmdS)
                    xutfS += utS
                    xrstS += reS
                    continue
            elif "_[" in uS:                              # tags
                usL = uS.split("_[")                      # line, tag list
                lineS = usL[0]
                tagS = usL[1].strip()
                tagcmd = self.tagsD[tagS]                 # get tag name
                if tagS in self.tagsD:
                    if len(lineS) > 0:                    # line empty in block
                        rvtuC = tag.TagUTF(tagcmd, folderD, labelD, rivtD)
                        utS = rvtuC.tag_parse(lineS)      # format lines
                        xutfS += utS + "\n"
                    else:                                 # flag for block
                        blockB = True
                        rvtrC = tag.TagRST(tagcmd, folderD, labelD, rivtD)
                        reS = rvtrC.tag_parse(lineS)
                        xrstS += reS + "\n"
            else:
                xutfS += uS + "\n"                        # return other
                xrstS += uS + "\n"

        return (xutfS, xrstS, folderD, labelD, rivtD)

    def block_parse(self, blockS):
        """block_parse

        Args:
            self (_type_): _description_
        """
        if blevalB and len(uS.strip()) < 2:    # value tables
            vtableL += blevalL
            if tfS == "declare":
                vutfS = self.dtable(blevalL, hdrdL, "rst", aligndL) + "\n\n"
                xutfS += vutfS
                xrstS += vutfS
            if tfS == "assign":
                vutfS = self.dtable(blevalL, hdrdL, "rst", aligndL) + "\n\n"
                xutfS += vutfS
                xmdS += vmdS
                xrstS += vutfS
            blevalL = []

            # export values
            valP = Path(self.folderD["valsP"], self.folderD["valfileS"])
            with open(valP, "w", newline="") as f:
                writecsv = csv.writer(f)
                writecsv.writerow(hdraL)
                writecsv.writerows(vtableL)

            tagS = self.tagsD["[q]"]
            rvtS = tag.TagUTF(lineS, tagS, labelD, folderD, rivtD)
            xutfS += rvtS + "\n"
            rvtS = tag.TagRST(lineS, tagS, labelD, folderD, rivtD)
            xrstS += rvtS + "\n"
