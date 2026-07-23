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
        """bold text block"""
        n = int(iS)
        uS = tS = txtS
        riS = "**" + txtS.strip() + "**"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "italic":
        """italic text block"""
        n = int(iS)
        uS = tS = txtS
        riS = "*" + txtS.strip() + "*"
        riS = textwrap.indent(riS, " " * n)
        rS = "\n\n" + riS + "\n\n"
        lS = ""
    elif texttypS == "indent":
        """indent text block"""
        n = int(iS)
        paraL = txtS.split("\n\n")
        blkS = ""
        for ln in paraL:
            ln = ln.lstrip("\n")
            ln = ln.replace("\n", " ")
            blkS += textwrap.indent(blkS, prefix=n * " ") + "\n\n"
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
        """format html block"""
        uS = tS = "\n" + txtS + "\n"
        partS = publish_parts(source=txtS, writer_name="html")
        rS = lS = "\n" + partS["body"] + "\n\n"
    elif texttypS == "text":
        """literal text block"""
        uS = tS = txtS
        rS = (
            "\n\n.. code-block:: text \n\n"
            + textwrap.indent(txtS, "        ")
            + "\n\n"
        )
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
    elif texttypS == "PYTHON":  # execute python
        """execute python code block

        """
        blkL = (self.strL).split("\n", 1)
        txtS = blkL[1]
        self.build_transcript(txtS)
        pytxtS = self.build_transcript(txtS)
        uS = tS = pytxtS
        lS = ""
        rS = (
            "\n.. code-block:: python\n\n"
            + textwrap.indent(pytxtS, "   ")
            + "\n\n"
        )
    else:
        pass

    return uS, tS, rS, lS

    def build_transcript(self, txtS):
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
                self.rivtD.update(globals_ns)
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
        return result


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
