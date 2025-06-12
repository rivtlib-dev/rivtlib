"""generates a report

DOC - write doc
APPEND - append pdf to doc
PREPEND - prepend pdf to doc
REPORT - generate report template file

Args:
    folderD (_type_): _description_
    labelD (_type_): _description_
    dtypeS (_type_): _description_
    styleS (_type_): _description_


parse a write command
Commands:
    |DOC| rel. pth | type, init
    |APPEND| rel. pth | divider; nodivider
    |PREPEND| rel. pth | divider; nodivider
    |REPORT| rel. pth | overwrite; nowrite
Args:
    cmdS (str): command

"""

# region
dtypeS = dtypeS
folderD = folderD
labelD = labelD
yamlP = Path(folderD["projP"], "doc/styles/", styleS.strip() + ".yaml")
iniP = Path(folderD["projP"], "doc/styles/", styleS.strip() + ".ini")
# endregion


def genreport(typeS):
    pass


def rename_div():
    """_summary_"""
    pass


def doc_list():
    """
    list of documents to be included in report

    Each document starts with 'r' followed by a four digit number. List the
    numbers in quotes for each document to be excluded from the report,
    separated by commas.

    Example:
    To exclude documents 02 and 03 from division 01 and document 04
    from division 02 provide the following entry:

        return exclude_docs = ["0102", "0103", "0204"]

    To include all documents leave the list empty.

    """

    return doclistL
