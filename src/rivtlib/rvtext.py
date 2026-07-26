"""functions that process block text"""

import ast
import io
import sys
import textwrap
from pathlib import Path

from docutils.core import publish_parts


def build_transcript(txtS, rivtD):
    """
    Returns (transcript, source_lines)

    transcript   -- list of strings representing the full annotated
                    output: every source line (comments/blank lines
                    included) plus any print() output inserted right
                    after the statement that generated it.
    source_lines -- list of every raw line of the input file, as strings,
                    in original order (this is the plain "capture every
                    line as a string" list, with no output mixed in).
    """
    lines = txtS.splitlines()

    tree = ast.parse(txtS)

    globals_ns = globals().copy()
    transcript = []
    source_lines = []

    prev_end = 0
    real_stdout = sys.stdout

    def emit_raw(ln_start, ln_end):
        for ln in range(ln_start, ln_end + 1):
            text = lines[ln - 1]
            source_lines.append(text)
            transcript.append(text)

    for node in tree.body:
        start = node.lineno
        end = getattr(node, "end_lineno", start)

        # Comment-only / blank lines sitting between statements: just
        # display them, nothing to execute.
        if start - 1 >= prev_end + 1:
            emit_raw(prev_end + 1, start - 1)

        # The statement's own source lines.
        emit_raw(start, end)

        # Execute just this one statement, capturing whatever it prints.
        module = ast.Module(body=[node], type_ignores=[])
        ast.fix_missing_locations(module)
        code_obj = compile(module, txtS, "exec")

        buf = io.StringIO()
        sys.stdout = buf
        try:
            exec(code_obj, globals_ns)
            rivtD.update(globals_ns)
        finally:
            sys.stdout = real_stdout

        output = buf.getvalue()
        if output:
            transcript.extend(output.rstrip("\n").split("\n"))

        prev_end = end

    # Any trailing comment/blank lines after the final statement.
    if prev_end + 1 <= len(lines):
        emit_raw(prev_end + 1, len(lines))

    globals().update(globals_ns)
    result = "\n".join(transcript)
    return result, rivtD


def format_text(texttypS, blkS, fcontS, fnaS, lD, fD, rivtD):
    """formats text blocks called by rv.T

     Args:
         texttypS (string): type of text block
         blkS (string): block of text
         iS (string): file text

    type parameters:
         engineering and analysis
         ------------------------
         PYTHON - execute python code block
         python - format code block
         opensees - requires opensees installation
         subpython - substitute into python code block

         document formatting
         -------------------
         boldn - bold text with indent
         italicn - italic text with indent
         indentn - format literal with indent
         wrapn - wrap with indent
         rstn - format restructured text
         html - insert in html
         note - note in box
         text - format literal text block
         subtext -  substitute into literal text block
         subrst - substitute into restructured text block

         diagrams and math
         -----------------
         latex - requires texlive cli, pdf only
         mermaid - requires mermaid cli
         dot - requires graphviz cli


     Returns:
         uS, tS, rS, lS: utf, text, rst, raw html or latex
    """
    txtS = blkS

    if "rst" in texttypS.strip():
        """restructured text block"""
        n = int(texttypS.split("rst")[1].strip())
        txtS = textwrap.dedent(txtS)
        uS = tS = textwrap.indent(txtS, " " * n)
        riS = textwrap.indent(txtS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""

    elif "bold" in texttypS.strip():
        """bold text block"""
        n = int(texttypS.split("bold")[1].strip())
        uS = tS = txtS
        riS = "**" + txtS.strip() + "**"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""

    elif "italic" in texttypS.strip():
        """italic text block"""
        n = int(texttypS.split("italic")[1].strip())
        uS = tS = txtS
        riS = "*" + txtS.strip() + "*"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""

    elif "indent" in texttypS.strip():
        """indent text block"""
        n = int(texttypS.split("indent")[1].strip())
        paraL = txtS.split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(ln, prefix=n * " ") + "\n\n"

    elif texttypS == "wrap":
        """wrap text block"""
        paraL = txtS.split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.fill(ln, 80) + "\n\n"

    elif texttypS == "note":
        """note text block"""
        txtS = textwrap.dedent(txtS)
        utxtS = "Notes:\n" + txtS
        uS = tS = textwrap.indent(utxtS, " " * 4)
        riS = textwrap.indent(txtS, " " * 4)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
        rS = (
            "\n"
            + "\n.. note::  "
            + "\n\n"
            + textwrap.indent(txtS, prefix="    ")
            + "\n"
        )
        lS = ""

    elif texttypS == "text":
        """literal text block"""
        uS = tS = txtS
        rS = (
            "\n\n.. code-block:: text \n\n"
            + textwrap.indent(txtS, "        ")
            + "\n\n"
        )
        lS = ""

    elif texttypS == "html":
        """format html block"""
        uS = tS = "\n" + txtS + "\n"
        partS = publish_parts(source=txtS, writer_name="html")
        rS = "\n" + partS["body"] + "\n\n"
        lS = ""

    elif texttypS == "PYTHON":
        """execute python code block"""
        # txtS = txtS[1:]
        txtdS = textwrap.dedent(txtS)
        pytxtS, rivtD = build_transcript(txtdS, rivtD)
        uS = tS = pytxtS
        lS = ""
        rS = (
            "\n.. code-block:: python\n\n"
            + textwrap.indent(pytxtS, "   ")
            + "\n\n"
        )

    elif texttypS == "subpython":
        fstrS = '''f"""''' + fcontS.strip() + '''"""'''
        subS = eval(fstrS, globals(), rivtD)
        fnS = Path(fD["storeP"], "scripts", "rv-" + fnaS)
        with open(fnS, "w") as f1:
            f1.write(subS)
        subrS = (
            "\n\n.. code-block:: python\n\n"
            + textwrap.indent(subS, "   ")
            + "\n\n"
        )
        subuS = textwrap.indent(subS, "   ")

        uS = tS = blkS + "\n\n" + subuS + "\n\n"
        rS = blkS + "\n\n" + subrS + "\n\n"
        lS = ""

    elif texttypS == "python":  # python code
        """ format python code block"""
        uS = tS = txtS
        rS = (
            "\n"
            + "\n.. code-block:: python"
            + "\n\n"
            + textwrap.indent(txtS, prefix="    ")
            + "\n"
        )
        lS = ""
    else:
        pass

    return uS, tS, rS, lS, rivtD


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
