"""generates report

DOC - write doc
APPEND - append pdf to doc
PREPEND - prepend pdf to doc
REPORT - generate report template file
"""

def __init__(self, folderD, labelD, dtypeS, styleS):
    """command object (type is write)
    Args:
        folderD (_type_): _description_
        labelD (_type_): _description_
        dtypeS (_type_): _description_
        styleS (_type_): _description_
    """
    # region
    self.dtypeS = dtypeS
    self.folderD = folderD
    self.labelD = labelD
    self.yamlP = Path(folderD["projP"], "doc/styles/", styleS.strip() + ".yaml")
    self.iniP = Path(folderD["projP"], "doc/styles/", styleS.strip() + ".ini")
    # endregion

def repx(self, cmdS):
    """parse a write command
    Commands:
        |DOC| rel. pth | type, init
        |APPEND| rel. pth | divider; nodivider
        |PREPEND| rel. pth | divider; nodivider
        |REPORT| rel. pth | overwrite; nowrite
    Args:
        cmdS (str): command
    """
    # region
    getattr(self, cmdS)

    return
    # endregion


def exclude_divisions():
    """
    list of divisions to be excluded from the report

    Each division folder starts with a two digit number. List the numbers in
    quotes for each division to be excluded from the report, separated by
    commas.

    Example:
    To exclude divisions 02 and 05 provide the following entry:

        return exclude_div := ["02", "05"]

    To include all divisions leave the list empty.
    """

    return exclude_divs := []

def exclude_documents():
    """
    list of documents to be excluded from the report

    Each document starts with a four digit number. List the numbers in quotes
    for each document to be excluded from the report, separated by commas.

    Example:
    To exclude documents 02 and 03 from division 01 and document 04
    from division 02 provide the following entry:

        return exclude_docs = ["0102", "0103", "0204"]

    To include all documents leave the list empty.

    """

    return exclude_docs := []


def rename_divisions():
    """_summary_

    [report]
    title = Solar Canopy Calculations
    d01 = Codes and Loads
    r0101 = Codes
    r0102 = Loads
    d02 = Frame
    r0201 = Steel Frame
    r0202 = Solar Panels
    d03 = Foundation
    r0301 = Slab
    r0302 = Walls
    """

def genreport():
    pass