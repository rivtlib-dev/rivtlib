"""functions that process block text"""

import textwrap

from docutils.core import publish_parts

from rivtlib.rvreport import htmlx


def format_text(texttypS, blkL, iS, lD, rivtD):
    """formats various types of text blocks

    called by rv.T and | TEXT |

    Args:
        texttypS (string): type of text block
        blkL (list): block list of strings
        iS (string): indent

    Options:
        bold:n - bold text with indent
        endnote - list of endnotes in order
        html - include in html
        indent:n - format literal with indent
        italic:n - italic text with indent
        latex - include in pdf, attach to pdf
        note - note in box
        rst - format restructured text
        text - format literal
        wrap:n - wrap with indent

        latex - requires texlive cli
        mermaid - requires mermaid cli
        dot - requires graphviz cli

    Returns:
        uS, tS, rS, lS: utf formatted, text, rst, html or latex formatted strings
    """

    if texttypS == "bold":
        n = int(iS)
        txtS = blkL[1]
        uS = tS = txtS
        riS = "**" + txtS.strip() + "**"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "italic":
        n = int(iS)
        txtS = blkL[1]
        uS = tS = txtS
        riS = "*" + txtS.strip() + "*"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "indent":
        n = int(iS)
        paraL = blkL[1].split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(blkS, prefix=n * " ") + "\n\n"
    elif texttypS == "wrap":  # note block
        paraL = blkL[1].split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(ln, 80) + "\n\n"
    elif texttypS == "note":  # note block
        paraL = blkL[1].split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.fill(ln, 80) + "\n\n"
        uS = tS = blkS
        rS = (
            "\n"
            + "\n.. note::  "
            + "\n\n"
            + textwrap.indent(blkS, prefix=n * " ")
            + "\n"
        )
        lS = ""
    elif texttypS == "text":
        txtS = blkL[1]
        uS = tS = txtS
        rS = (
            "\n"
            + "\n.. code-block:: text \n\n"
            + "\n\n"
            + textwrap.indent(txtS, "       ")
        )
        lS = ""
    elif texttypS == "rst-html":
        uS = tS = "\n" + blkL[1] + "\n"
        partS = publish_parts(source=blkL[1], writer_name="html")
        rS = lS = "\n" + partS["body"] + "\n\n"

    elif texttypS == "endnotes":
        endL = blkL[1].split("\n")
        endrS = "\n" + "-" * 80 + "\n\n"
        enduS = "-" * 80 + "\n\n"
        endtS = "\n" + "-" * 80 + "\n\n"
        fnI = 0
        for ln in endL:
            lS = " ".join(ln.strip())
            fnI += 1
            enduS += f"[{str(fnI)}] {lS}\n\n"
            endrS += f".. [{str(fnI)}] {lS}\n\n"
        uS = enduS
        tS = endtS
        rS = lS = endrS

        """writes endnotes
        endnotesx(lD, r1S):
        footnote marks are inserted in rvparse loops
        """

        wI = lD["widthI"]
        erS = "\n" + "-" * 20 + "\n"
        euS = "\n" + "-" * 80 + "\n\n"
        fnI = 0
        r1L = r1S.split("\n")
        r2L = []
        for ln in r1L:
            ln = ln.strip()
            if len(ln) == 0:
                ln = "\n\n"
            else:
                pass
            r2L.append(ln)
        r2S = "".join(r2L)
        groups = r2S.split("\n\n")
        result = [group.replace("\n", " ") for group in groups]
        fnI = 0
        uS = euS
        rS = erS
        for ln in result:
            if len(ln.strip()) == 0:
                continue
            fnI += 1
            ftnoteS = lD["divS"] + "." + str(lD["sdivI"]) + "." + str(fnI)
            lS = ln.strip() + "\n"
            euS = f"[{ftnoteS}] {lS}\n\n"
            euS = textwrap.fill(euS, width=wI) + "\n\n"
            lS = textwrap.indent(lS, " " * 4)
            erS = "\n\n" + f".. _[{ftnoteS}]:\n\n**[{ftnoteS}]** \n{lS}\n\n\n"
            uS += euS
            rS += erS
        tS = uS
        lS = rS

    print(uS)
    return uS, tS, rS, lS


def typex(lD, r1S):
    """call command

    Args:
        cmdS (str): command keyword

    Returns:
        uS, rS, tS, lS, fD, lD, rivtD, rivL
    """

    return uS, tS, rS


def mermaidx():
    pass


def dotx():
    pass


def latexx():
    pass


def htmlx():
    pass


def rstx():
    pass
