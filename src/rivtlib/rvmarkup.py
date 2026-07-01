"""functions that process inline markup"""

import textwrap


def typex(lD, r1S):
    """call command

    Args:
        cmdS (str): command keyword

    Returns:
        uS, rS, tS, lS, fD, lD, rivtD, rivL
    """
    cmdS = lD["runtypeS"]
    typcmdS = cmdS + "x"
    uS, tS, rS = globals()[typcmdS](lD, r1S)

    return uS, tS, rS


def pythonx():
    pass


def endnotesx(lD, r1S):
    """writes endnotes

    footnote marks are inserted in rvparse loops
    """

    wI = lD["widthI"]
    erS = "\n"
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
        lS = ln.strip() + "\n"
        euS = f"[{str(fnI)}] {lS}\n\n"
        euS = textwrap.fill(euS, width=wI) + "\n\n"
        erS = f".. [{str(fnI)}] {lS}\n\n"
        uS += euS
        rS += erS
    tS = uS
    lS = rS

    print(uS)
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
