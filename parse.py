

from rivtlib import cmds, tags
from rivtlib.units import *


class RivtParse:
    """format rivt-strings to utf and rst docs"""

    def __init__(self, hS, tS, folderD, labelD,  rivtD):
        """format header string

        Args:
            hS (str)): header string
            tS (str): section type
            folderD (dict): _description_
            labelD (dict): _description_
            rivtD (dict): _description_

        Returns:
            cmdL (list): list of valid commands
            tagsL (list): list of valid tags
            folderD (dict): _description_
            labelD (dict):
            rivtD (dict): local dictionary

        """

        self.rivtD = rivtD
        self.folderD = folderD
        self.labelD = labelD
        self.errlogP = folderD["errlogP"]
        self.tS = tS

        hdrstS = """"""
        hdreadS = """"""
        hdutfS = """"""""
        xrstS = xutfS = ""
        rivtS = """"""                              # rivt input string
        utfS = """"""                               # utf-8 output string
        rmeS = """"""                               # readme output string
        xremS = """"""                              # redacted readme string
        rstS = """"""                               # reST output string
        declareS = """"""                           # declares output string
        assignS = """"""                            # assigns output string

        # section headings
        # initialize return strings
        hL = hS.split("|")               # section string as list
        titleS = hL[0].strip()           # sectiobn title
        labelD["xch"] = hL[1].strip()    # set xchange
        labelD["color"] = hL[2].strip()  # set background color
        if hS.strip()[0:2] == "--":      # omit section heading
            return "\n", "\n", "\n"

        headS = datetime.now().strftime("%Y-%m-%d | %I:%M%p") + "\n"
        labelD["docS"] = titleS
        bordrS = labelD["widthI"] * "="
        hdutfS = (headS + "\n" + bordrS + "\n" + titleS + "\n" + bordrS + "\n")
        hdmdS = (headS + "\n## " + titleS + "\n")

        snumI = labelD["secnumI"] + 1
        labelD["secnumI"] = snumI
        docnumS = labelD["docnumS"]
        dnumS = docnumS + "-[" + str(snumI) + "]"
        headS = dnumS + " " + titleS
        bordrS = labelD["widthI"] * "-"

        hdutfS = bordrS + "\n" + headS + "\n" + bordrS + "\n"
        hdmdS = "### " + headS + "\n"
        hdrstS += (
            ".. raw:: latex"
            + "   \n\n ?x?vspace{.2in} "
            + "   ?x?begin{tcolorbox} "
            + "   ?x?textbf{ " + titleS + "}"
            + "   ?x?hfill?x?textbf{SECTION " + dnumS + " }"
            + "   ?x?end{tcolorbox}"
            + "   \n" + "   ?x?newline" + "   ?x?vspace{.05in}"
            + "\n\n")

        # print(hdutfS)
        # return hdutfS, hdmdS, hdrstS

        if tS == "I":
            self.cmdL = ["append", "image", "table", "text"]
            self.tagsD = {"u]": "underline", "c]": "center", "r]": "right",
                          "e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description", "s]": "sympy",
                          "link]": "link", "line]": "line", "page]": "page",
                          "[c]]": "centerblk",  "[p]]": "plainblk",
                          "[l]]": "latexblk", "[o]]": "codeblk", "[q]]": "quitblk"}

        elif tS == "V":
            self.cmdL = ["image", "table", "assign", "eval"]
            self.tagsD = {"e]": "equation", "f]": "figure", "t]": "table",
                          "#]": "foot", "d]": "description",
                          "s]": "sympy", "=": "eval"}

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
            rvtS = tag_utf.TagsUTF(lineS, tagS, labelD, folderD, rivtD)
            xutfS += rvtS + "\n"
            rvtS = tag_rst.TagsRST(lineS, tagS, labelD, folderD, rivtD)
            xrstS += rvtS + "\n"

    def str_parse(self, strL):
        """str_parse _summary_

        Args:
            strL (_type_): _description_

        Returns:
            _type_: _description_
        """

        uS = """"""         # local line
        xutfS = """"""      # accum utf local string
        xrstS = """"""      # accum rst local string
        blockS = ""         # accum block
        blockB = False      # block flag
        blckevalL = []      # current value table
        eqL = []            # equation result table
        vtableL = []        # value table for export
        hdraL = ["variable", "value", "[value]", "description"]   # value align
        alignaL = ["left", "right", "right", "left"]
        hdreL = ["variable", "value", "[value]", "description [eq. number]"]
        aligneL = ["left", "right", "right", "left"]

        for uS in strL:
            # print(f"{uS=}")
            if blockB:                                 # accum block
                blockS += uS
                if blockB and uS.strip() == "_[[q]]":
                    parse_block(blockS)
                    blockB = False
                    continue
            elif uS[0:2] == "||":                      # commands
                parL = uS[2:].split("|")[1:]
                cmdS = parL[0].strip()
                if cmdS in self.cmdL:
                    rvtC = cmd_utf.CmdUTF(parL, labelD, folderD, rivtD)
                    utfS = rvtC.cmd_parse(cmdS)
                    xutfS += utfS
                    rvtC = cmd_rst.CmdRST(parL, labelD, folderD, rivtD)
                    reS = rvtC.cmd_parse(cmdS)
                    xrstS += reS
                    # print(f"{utfS=}")
            elif "_[" in uS:                           # line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                     # block tag
                    blockB = True
                    continue
                if tagS in self.tagsD:
                    rvtC = tag_utf.TagsUTF(
                        lineS, labelD, folderD, tagsD, rivtD)
                    utfxS = rvtC.tag_parse(tagS)
                    xutfS += utfxS + "\n"
                    rvtC = tag_rst.TagsRST(
                        lineS, labelD, folderD, tagsD, rivtD)
                    reS = rvtC.tag_parse(tagS)
                    xrstS += reS + "\n"
            elif "=" in uS and self.methS == "V":      # equation tag
                # print(f"{uS=}")
                usL = uS.split("|")
                lineS = usL[0]
                self.labelD["unitS"] = usL[1].strip()
                self.labelD["descS"] = usL[2].strip()
                if "=" in uS:                          # declare tag
                    tfS = "assign"
                    blockevalL.append(rvtC.tag_parse("="))
                    rvtC = tag_rst.TagsRST(lineS, labelD, folderD, localD)
                    eqL = rvtC.tag_parse(":=")
                    blockB = True
                    continue
                else:
                    tfS = "eval"                       # assign tag
                    eqL = rvtC.tag_parse("=")
                    rvtC = tag_rst.TagsRST(lineS, labelD, folderD, localD)
                    eqL = rvtC.tag_parse("=")
                    rstS += eqL[1]
                    blockB = True
                    continue
                    # export values

                valP = Path(self.folderD["valsP"], self.folderD["valfileS"])
                with open(valP, "w", newline="") as f:
                    writecsv = csv.writer(f)
                    writecsv.writerow(hdraL)
                    writecsv.writerows(vtableL)
            else:
                print(uS)                              # print string

        return (xutfS, xrstS,  self.labelD, self.folderD, self.rivtD)
