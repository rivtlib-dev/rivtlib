"""functions that process inline markup"""


def typex(cmdS, r1S):
    """call command

    Args:
        cmdS (str): command keyword

    Returns:
        uS, rS, tS, lS, fD, lD, rivtD, rivL
    """
    typcmdS = cmdS + "x"
    uS, tS, rS = globals()[typcmdS](r1S)

    return uS, tS, rS


def pythonx():
    pass


def endnotesx(r1S):
    endL = r1S.split("\n")
    endrS = "\n" + "-" * 80 + "\n\n"
    enduS = "\n" + "-" * 80 + "\n\n"
    fnI = 0
    for ln in endL:
        lS = " ".join(ln.strip())
        fnI += 1
        enduS += f"[{str(fnI)}] {lS}\n\n"
        endrS += f".. [{str(fnI)}] {lS}\n\n"

    uS = tS = enduS
    rS = lS = endrS

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
