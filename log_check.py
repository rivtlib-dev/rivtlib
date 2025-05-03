import logging
import warnings
from pathlib import Path


def log_bak(rivtFP, modnameS, folderD):
    """
    start logging and write doc bak file
    """

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        filename=folderD["errlogP"],
        filemode="w",
    )
    warnings.filterwarnings("ignore")
    # warnings.simplefilter(action="ignore", category=FutureWarning)

    docshortP = Path(folderD["docP"].parts[-2:])
    bakshortP = Path(folderD["bakP"].parts[-2:])

    if folderD["docP"].exists():
        logging.info(f"""rivt file : [{folderD["docS"]}]""")
        logging.info(f"""rivt path : [{folderD["docP"]}]""")
        print(f"""rivt short path : [{docshortP}]""")
    else:
        logging.info(f"""rivt file path not found: {folderD["docP"]}""")

    # write backup doc file
    with open(rivtFP, "r") as f2:
        rivtS = f2.read()
    with open(folderD["bakP"], "w") as f3:
        f3.write(rivtS)
    logging.info(f"""rivt backup: [{bakshortP}]""")
    print(" ")


class UnumError(Exception):
    """
    A Unum error occurred that was unrelated to dimensional errors.
    """

    pass


class ShouldBeUnitlessError(TypeError):
    """
    An operation on a Unum failed because it had units unexpectedly.
    """

    def __init__(self, u):
        TypeError.__init__(self, "expected unitless, got %s" % u)


class IncompatibleUnitsError(TypeError):
    """
    An operation on two Unums failed because the units were incompatible.
    """

    def __init__(self, unit1, unit2):
        TypeError.__init__(
            self, "%s can't be converted to %s" % (unit1.unit(), unit2.unit())
        )


class ConversionError(UnumError):
    """
    Failed to convert a unit to the desired type.
    """

    def __init__(self, u):
        UnumError.__init__(self, "%s has no conversion" % u)


class NameConflictError(UnumError):
    """
    Tried to define a symbol that was already defined.
    """

    def __init__(self, unit_key):
        UnumError.__init__(self, "%s is already defined." % unit_key)


class NonBasicUnitError(UnumError):
    """
    Expected a basic unit but got a non-basic unit.
    """

    def __init__(self, u):
        UnumError.__init__(self, "%s not a basic unit" % u)
