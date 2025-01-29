from rivtlib import tag, cmd
from pathlib import Path


class RivtParse:
    """format rivt-strings to utf and rst docs"""

    def __init__(self, tS):
        """format header string

        Args:
            tS (str): section type

        """

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

    def str_parse(self, tS, strL, folderD, labelD, rivtD):
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
        if hS.strip()[0:2] == "--":
            hdutfS = hdrstS = "\n", "\n", "\n"
        else:
            hL = hS.split("|")                    # section string as list
            titleS = hL[0].strip()                # section title
            labelD["xch"] = hL[1].strip()         # set xchange
            labelD["color"] = hL[2].strip()       # set background color
            labelD["docS"] = titleS
            snumI = labelD["secnumI"] + 1         # increment section number
            labelD["secnumI"] = snumI
            docnumS = labelD["docnumS"]
            dnumS = docnumS + "-[" + str(snumI) + "]"
            headS = dnumS + " " + titleS
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
        xutfS += hdutfS
        xrstS += hdrstS

        # section body
        for uS in strL[1:]:
            try:
                if uS[0] == "#":                      # skip comment lines
                    continue
                elif len(uS) < 1:
                    continue
            except:
                pass
            # print(f"{uS=}")
            if blockB:                                 # accum block
                blockS += uS
                if blockB and uS.strip() == "_[[q]]":
                    parse_block(blockS)
                    blockB = False
                    continue
            elif uS[0:2] == "||":                      # commands
                parL = uS[2:].split("|")
                cmdS = parL[0].strip()
                pthP = Path(parL[1].strip())
                pars = parL[2].strip()
                parL = pars.split(",")
                if cmdS in self.cmdL:
                    rvtC = cmd.CmdUTF(labelD, folderD, rivtD)
                    utfS = rvtC.cmd_parse(cmdS, pthP, parL)
                    rvtC = cmd.CmdRST(parL, labelD, folderD, rivtD)
                    reS = rvtC.cmd_parse(cmdS)
                    xutfS += utfS
                    xrstS += reS
            elif "_[" in uS:                           # line tag
                usL = uS.split("_[")
                lineS = usL[0]
                tagS = usL[1].strip()
                if tagS[0] == "[":                     # block tag
                    blockB = True
                    continue
                if tagS in self.tagsD:
                    rvtC = tag.TagUTF(lineS, self.tagsD,
                                      folderD, labelD, rivtD)
                    utfxS = rvtC.tag_parse(tagS)
                    xutfS += utfxS + "\n"
                    rvtC = tag.TagRST(lineS, self.tagsD,
                                      folderD, labelD, rivtD)
                    reS = rvtC.tag_parse(tagS)
                    xrstS += reS + "\n"
            elif "=" in uS and self.tS == "V":      # equation tag
                # print(f"{uS=}")
                usL = uS.split("|")
                lineS = usL[0]
                labelD["unitS"] = usL[1].strip()
                labelD["descS"] = usL[2].strip()
                if "=" in uS:                          # declare tag
                    tfS = "assign"
                    blockevalL.append(rvtC.tag_parse("="))
                    rvtC = tag.TagsRST(lineS, labelD, folderD, localD)
                    eqL = rvtC.tag_parse(":=")
                    blockB = True
                    continue
                else:
                    tfS = "eval"                       # assign tag
                    eqL = rvtC.tag_parse("=")
                    rvtC = tag.TagsRST(lineS, labelD, folderD, localD)
                    eqL = rvtC.tag_parse("=")
                    rstS += eqL[1]
                    blockB = True
                    continue
                    # export values

                valP = Path(folderD["valsP"], folderD["valfileS"])
                with open(valP, "w", newline="") as f:
                    writecsv = csv.writer(f)
                    writecsv.writerow(hdraL)
                    writecsv.writerows(vtableL)
            else:
                xutfS += uS + "\n"

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
