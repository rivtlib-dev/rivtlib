"""functions that process block text"""

import textwrap

from docutils.core import publish_parts


def format_text(texttypS, blkS, iS, lD, rivtD):
    """formats various types of text blocks

    called by rv.T and | TEXT |

    Args:
        texttypS (string): type of text block
        blkL (list): block list of strings
        iS (string): indent

    Options:
        bold-n : bold text with indent
        endnote : list of endnotes in order
        html : include in html
        indent-n : format literal with indent
        italic-n : italic text with indent
        latex : include in pdf, attach to pdf
        note : note with border
        rst : format restructured text
        text : format literal
        wrap-n : wrap with indent

        latex - requires texlive cli
        mermaid - requires mermaid cli
        dot - requires graphviz cli

    Returns:
        uS, tS, rS, lS: utf formatted, text, rst, html or latex formatted strings
    """
    txtS = blkS
    n = int(iS.strip())

    if texttypS == "bold":
        n = int(iS)
        uS = tS = txtS
        riS = "**" + txtS.strip() + "**"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "italic":
        n = int(iS)
        uS = tS = txtS
        riS = "*" + txtS.strip() + "*"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "indent":
        n = int(iS)
        paraL = txtS.split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(blkS, prefix=n * " ") + "\n\n"
    elif texttypS == "wrap":  # note block
        paraL = txtS.split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(ln, 80) + "\n\n"
    elif texttypS == "note":  # note block
        paraL = txtS.split("\n\n")
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
    elif texttypS == "html":
        uS = tS = "\n" + txtS + "\n"
        partS = publish_parts(source=txtS, writer_name="html")
        rS = lS = "\n" + partS["body"] + "\n\n"
    elif texttypS == "endnotes":
        r1L = txtS.split("\n")
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
        wI = lD["widthI"]
        fnI = 0
        erS = "\n" + "-" * 20 + "\n"
        euS = "\n" + "-" * 80 + "\n\n"
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
        lS = ""
    elif texttypS == "python":  # note block
        uS = tS = txtS
        rS = (
            "\n"
            + "\n.. code-block:: python"
            + "\n\n"
            + textwrap.indent(txtS, prefix="    ")
            + "\n"
        )
        lS = ""
    elif texttypS == "text":
        uS = tS = txtS
        rS = (
            "\n\n.. code-block:: text \n\n"
            + textwrap.indent(txtS, "        ")
            + "\n\n"
        )
        lS = ""
    return uS, tS, rS, lS


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
