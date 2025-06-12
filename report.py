"""report functions

variables defined in an importing file that generates a report

# ===========================
# process
# ===========================
rerun = False                   # flag that reruns rivt files
rtype = "rst2pdf"               # report type
yamlP = "doc/styles/"
iniP = "doc/styles"

# ===========================
# layout
# ===========================
toc = True                      # insert table of contents
append_count = False            # include append/prepend in page count
charwidth = "80"                # width for text docs
pagesize = "letter"             # page size
header = "<datetime > | Solar Canopy - Larkspur, Ca. | page < page >"
footer = "<datetime > | Solar Canopy - Larkspur, Ca. | page < page >"

# ===========================
# cover and toc
# ===========================
cover_pdf = ""                  # insert cover (overrides other cover settings)
cover_title1 = "Solar Canopy"   # first line of default cover
cover_title2 = "Larkspur, Ca."  # second line of default cover
cover_author = "rhh"            # third line of default cover
cover_image = "img.png"         # image
cover_title3 = "<datetime>"     # last line of default cover

# ===========================
# files
# ===========================
report_include = "all"          # rivt files to include e.g. "r0101, r0201"
report_exclude = ""             # rivt files to exclude e.g. "r0101, r0201"
report_title = "Solar Canopy Calculations"
d01 = "Codes and Loads"         # rename a division
r0101 = "Codes"                 # rename a subdivision (rivt file)
r0102 = "Loads"
d02 = "Frame"
r0201 = "Steel Frame"
r0202 = "Solar Panels"
d03 = "Foundation"
r0301 = "Slab"
r0302 = "Walls"

"""


def genreport():
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

    pass


def runall():
    pass


def rename_div():
    """_summary_"""
    pass
