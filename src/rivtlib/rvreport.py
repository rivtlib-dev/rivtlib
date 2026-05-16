"""generate a rivt report

This module is called by the rivt-report.py file that contains
report settings.
"""

import configparser
import glob
import logging
import os
import subprocess
import sys
import warnings
from datetime import datetime
from pathlib import Path

import __main__

reptP = os.getcwd()
rivtP = os.path.dirname(reptP)
pypathS = os.path.dirname(sys.executable)
reptPkgP = os.path.join(pypathS, "Lib", "site-packages", "rivt")
publicP = Path(rivtP, "_rivt-public")
storeP = Path(reptP, "_stored")
pubP = Path(reptP, "_published")
pdfpubP = Path(pubP, "pdfdocs")
htmlpubP = Path(pubP, "docs")
rstdocsP = Path(reptP, "_rstdocs")
srcP = Path(reptP, "src")
logsP = Path(storeP, "logs")
rivt_storedP = storeP
rptlogT = Path(storeP, "logs", "reportlog.txt")
timeS = datetime.now().strftime("%Y-%m-%d")

inS = __main__.iniS
repD = {}
configL = configparser.ConfigParser()
configL.read_string(inS)
repD["repname"] = configL["report"]["repname"]
repD["regen"] = configL["report"]["regen"]
repD["exclude"] = configL["report"]["exclude"]
repD["cover"] = configL["report"]["cover"]
repD["coverlogo"] = configL["report"]["coverlogo"]
repD["title"] = configL["report"]["title"]
repD["subtitle"] = configL["report"]["subtitle"]
repD["client"] = configL["report"]["client"]
repD["authors"] = configL["report"]["authors"]
repD["version"] = configL["report"]["version"]
repD["projref"] = configL["report"]["projectref"]
repD["copyright"] = configL["report"]["copyright"]
repD["runlogo"] = configL["report"]["copyright"]
repD["runlabel"] = configL["report"]["running_label"]
repD["pdfpage"] = configL["report"]["pdf_pagesize"]
repD["pdfmargin"] = configL["report"]["pdf_margins"]
repD["pdflink"] = configL["report"]["pdf_link"]

modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-8s  " + modnameS + "   %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=rptlogT,
    filemode="w",
)
warnings.filterwarnings("ignore")


def get_py():
    """list of doc reports"""

    rst_folderP = reptP
    rivtfL = glob.glob("rv???*.py", root_dir=rst_folderP)

    return rivtfL


def get_txt():
    """list of doc reports"""

    txt_folderP = Path(pubP, "_doctext")
    txtfL = glob.glob("rv???*.txt", root_dir=txt_folderP)

    return txtfL


def get_readme():
    """list of doc reports"""

    rme_folderP = Path(pubP, "readme")
    rdfL = glob.glob("rv???*.txt", root_dir=rme_folderP)

    return rdfL


def htmlx(frstT, pubT, rivtP):
    """write readme and html doc

    Returns:
        msgS (str): completion message

    """

    confpy()  # update conf.py
    coverS()  # update cover page
    yamlS()  # update yaml file
    baseP = self.fD["reptP"]
    srcS = f"{baseP}/src/{self.coverlogo}"
    destS = f"{baseP}/_rstdocs/_static/img/{self.coverlogo}"
    shutil.copy(srcS, destS)
    rvbaseS = self.fD["rbaseS"]
    rvfileS = self.fD["rbaseS"] + ".rst"
    rvdocS = self.fD["rbaseS"] + ".html"
    rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
    rvdocT = str(Path(self.fD["reptPubP"], "docs", rvdocS))
    timeS = datetime.now().strftime("%Y-%m-%d")
    rvauthT = str(Path(self.fD["rstdocsP"], "_templates", "rv-author.html"))
    rvdateT = str(Path(self.fD["rstdocsP"], "_templates", "rv-date.html"))
    rvtitleT = str(Path(self.fD["rstdocsP"], "_templates", "rv-title.html"))

    rvdateS = f"""
<!-- _templates/rv-date.html -->
<div class="footer-item">
<p class="rvdate">
    {timeS}
</p>
</div>
"""
    with open(rvdateT, "w", encoding="utf-8") as f2:
        f2.write(rvdateS)

    rvauthS = f"""
<!-- _templates/rv-author.html -->
<div class="footer-item">
<p class="rvauthor">
    {self.authorS}
</p>
</div>
"""
    with open(rvauthT, "w", encoding="utf-8") as f2:
        f2.write(rvauthS)

    rvtitleS = f"""
<!-- _templates/rv-title.html -->
<div class="footer-item">
<p class="rvtitle">
    {self.docnameS}  v.{self.verS} 
</p>
</div>
"""
    with open(rvtitleT, "w", encoding="utf-8") as f2:
        f2.write(rvtitleS)

    self.drstS = f"{self.docnameS}\n" + "=" * 70 + "\n\n" + self.drstS
    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(self.drstS)
    with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
        f5.write(self.dutfS)
    htmlcmdS = f"sphinx-build -E -D root_doc={rvbaseS} {str(self.fD['rstdocsP'])} {self.fD['htmlpubP']} \n"
    try:
        result = subprocess.run(htmlcmdS, shell=True, check=True)
        if not result.returncode:
            print("\nhtml script executed")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print("Stderr:", e.stderr)

    parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    return f"file written: {short_p} \n"


def pdfx(frepT, pubT):
    """write readme and pdf doc

    Returns:
        msgS (str): completion message
    """
    # region

    with open(frepT, "r", encoding="utf-8") as f1:
        read_rstS = f1.read()

    confpy()  # update conf.py
    coverS()  # update cover page
    yamlS()  # update yaml file

    verS = repD["version"]
    authors = repD["authors"]
    repnameS = repD["repname"]
    rvfileT = frstT
    rvdocT = pubT
    headblkS = (
        f"""**{repnameS}** - v{verS} |s| |s| |s| |s| Sect: **###Section###**"""
    )
    foot1blkS = f"""{timeS} |s| |s| |s| **|** |s| |s| |s| {authors}"""
    foot2blkS = f"""**{repD["runlabel"]}**"""

    imgS = f"""
.. |blklogo| image:: ../src/{repD["runlogo"]}
:height: 100px
:alt: logo


"""
    headS = f"""
.. header::
.. list-table::
    :class: header-box
    :align: left
    :widths: 90 10
    
    * - {headblkS}
        - p. **###Page###**   

        
"""

    footS = f"""
.. footer:: 
.. list-table::
    :class: footer-box
    :align: left
    :widths: 84 22 16
    
    * - {foot1blkS}        
        - {foot2blkS}        
        - |blklogo|

                
"""

    tcontentS = """


.. contents:: Table of Contents 
:depth: 4

|

"""

    drstS = (
        ".. |s| unicode:: 0xA0 \n\n\n"
        + imgS
        + tcontentS
        + headS
        + footS
        + "\n\n"
        + read_rstS
    )

    # print("xxxxxxxxxxxxxx")
    # print("0000000000", drstS)

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(drstS)
    pdfcmdS = f"sphinx-build -a -E -b pdf -D root_doc={repD['repname']} {rstdocsP} {pdfpubP} \n"
    try:
        result = subprocess.run(pdfcmdS, shell=True, check=True)
        if not result.returncode:
            print("\npdf script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")
        print("Stderr:", e.stderr)

    parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)

    return f"file written: {short_p} \n"
    # endregion


def textx():
    """write readme and text doc

    Returns:
        msgS (str): completion message
    """
    self.confpy()  # update conf.py
    rvdocS = self.fD["rbaseS"] + ".txt"
    rvdocT = str(Path(self.fD["reptPubP"], "txtdocs", rvdocS))
    timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
    doctitleS = self.docnameS
    versionS = "v-" + self.verS.strip()
    authorS = self.authorS.strip()

    borderS = "=" * 80
    hdlS = doctitleS + " | " + authorS + " | " + timeS + " | " + versionS
    headS = "\n" + hdlS + "\n" + borderS + "\n"
    self.dutfS = headS + "\n" + self.dutfS

    with open(rvdocT, "w", encoding="utf-8") as f5:
        f5.write(self.dutfS)
    with open(self.fD["readmeT"], "w", encoding="utf-8") as f5:
        f5.write(self.dutfS)

    parts = Path(rvdocT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    return f"file written: {short_p} \n"


# -------------------------------------------------------------------


def coverS():
    """
    cover page

    """

    # timeS = datetime.now().strftime("%Y-%m-%d")
    rvfileT = str(Path(rstdocsP, "_templates", "pdfcover.rst"))
    coverpgS = f"""
.. role:: big-text

|
|
        
.. image:: ../src/{repD["coverlogo"]}
   :width: 600px
   :align: center

|
|
|


.. class:: center

    :big-text:`{repD["repname"]}`

|
|
|
|
|
|

.. class:: center

   Attn: **{repD["client"]}**

|

.. class:: center

   project: **{repD["projref"]}**

   

.. raw:: pdf

   PageBreak mainPage
   SetPageCounter 1

   
"""

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(coverpgS)


def confpy():
    """write config.py"""

    rvbaseS = repD["repname"]
    rvfileT = str(Path(rstdocsP, "conf.py"))

    confpyS = f"""
import sys
from pathlib import Path

sys.path.append(str(Path(".").resolve()))

project = "{rvbaseS}"
copyright = "{repD["copyright"]}
author = "{repD["authors"]}"
release = "{repD["version"]}"

extensions = [
    "sphinx.ext.githubpages",
    "sphinx_togglebutton",
    "sphinxcontrib.jquery",
    "sphinx_copybutton",
    "sphinx_favicon",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx_design",
    "sphinx_new_tab_link",
    "rst2pdf.pdfbuilder",
]
root_doc = "index"
duration_write_json = ""
html_show_sourcelink = False
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".rst", ".md"]
templates_path = ["_templates"]
locale_dirs = ["_locale"]
html_title = " "
html_theme = "pydata_sphinx_theme"
html_context = {{"default_mode": "dark"}}
html_sidebars = {{"**": ["sidebar-nav-bs.html"]}}
html_static_path = ["_static", "_static/img", "../src"]
html_css_files = ["css/custom.css"]
html_theme_options = {{
    "pygments_light_style": "tango",
    "pygments_dark_style": "github-dark",
    "navbar_start": ["navbar-logo"],
    "collapse_navigation": True,
    "header_links_before_dropdown": 6,
    "navbar_align": "left",
    "show_toc_level": 1,
    "navigation_depth": 1,
    "footer_start": ["rv-author"],
    "footer_center": ["rv-title"],
    "footer_end": ["rv-date"],
    "logo": {{
            "text": "{repD["runlabel"]}",
        "image_dark": "{repD["runlogo"]}",
        "image_light": "{repD["runlogo"]}",
    }},
}}
favicons = [
    {{
        "rel": "icon",
        "sizes": "16x16",
        "href": "favicon-16x16.png",
    }},
    {{
        "rel": "icon",
        "sizes": "32x32",
        "href": "favicon-32x32.png",
    }},
]
# -- Options for PDF output -------------------------------------------------
# source start file, target name, title, author, options
# options: ('index', 'MyProject', 'My Project', 'Author Name', {{"pdf_compressed": True}})
# More than one author : \\r'Guido van Rossum\\Fred L. Drake, Jr., editor'
pdf_documents = [("{rvbaseS}", "{rvbaseS}", "{repD["repname"]}", 
            "{repD["authors"]}")]
# Label to use as a prefix for the subtitle on the cover page
subtitle_prefix = "User Manual"
# A list of folders to search for stylesheets.
pdf_style_path = ["./_rstdocs/_static/pdfstyle"]
# A colon-separated list of folders to search for fonts.
pdf_font_path = ["./_rstdocs/_static/fonts"]
# Example: compressed=True
pdf_compressed = False
# Language to be used for hyphenation support
pdf_language = "en_US"
# literal blocks wider than the frame overflow, shrink or truncate
pdf_fit_mode = "shrink"
# 1 means top-level sections start in a new page 0 disabled
pdf_break_level = 0
# When a section starts in a new page, force it to be 'even', 'odd', 'any
pdf_breakside = "any"
# If false, no coverpage is generated.
pdf_use_coverpage = True
# Name of the cover page template to use
pdf_cover_template = "_templates/pdfcover.rst"
# Show Table Of Contents at the beginning?
pdf_use_toc = False
# Page template name for "regular" pages
pdf_page_template = 'mainPage'
# How many levels deep should the table of contents be?
pdf_toc_depth = 9999
# Insert footnotes where they are defined 
pdf_inline_footnotes = False
# If false, no index is generated.
pdf_use_index = False
# If false, no modindex is generated.
pdf_use_modindex = False
# Add section number to section references
pdf_use_numbered_links = False
# Background images fitting mode
pdf_fit_background_mode = "scale"
# Repeat table header on tables that cross a page boundary?
pdf_repeat_table_rows = True
# Enable smart quotes (1, 2 or 3) or disable by setting to 0
pdf_smartquotes = 0
# verbosity level. 0 1 or 2
# pdf_verbosity = 0
# Documents to append as an appendix to all manuals.
# pdf_appendices = []
# Enable experimental feature to split table cells. Use it
# if you get "DelayedTable too big" errors
# pdf_splittables = False
# Set the default DPI for images
# pdf_default_dpi = 72
# Enable rst2pdf extension modules
# pdf_extensions = []
# A comma-separated list of custom stylesheets.
pdf_stylesheets = ["./_rstdocs/_static/pdfstyle/rivtstyle.yaml"]
    """

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(confpyS)


def yamlS():
    """write rivt yaml file for pdf"""

    rvfileT = str(Path(rstdocsP, "_static", "pdfstyle", "rivtstyle.yaml"))

    rivstyS = f"""
fontsAlias:
  fontSerif: DejaVuSans
  fontSerifBold: DejaVuSans-Bold
  fontSerifBoldItalic: DejaVuSans-BoldOblique
  fontSerifItalic: DejaVuSans-Oblique
  fontMono: DejaVuSansMono
  fontMonoBold: DejaVuSansMono-Bold
  fontMonoBoldItalic: DejaVuSansMono-BoldOblique
  fontMonoItalic: DejaVuSansMono-Oblique
  fontSans: DejaVuSans
  fontSansBold: DejaVuSans-Bold
  fontSansBoldItalic: DejaVuSans-BoldOblique
  fontSansItalic: DejaVuSans-Oblique
pageSetup:
  firstTemplate: coverPage
  height: null
  margin-bottom: 4mm
  margin-gutter: 1mm
  margin-left: 1.5cm
  margin-right: 1.5cm
  margin-top: 4mm
  size: letter
  spacing-footer: 10mm
  spacing-header: 10mm
  width: null
pageTemplates:
  coverPage:
    showFooter: true
    showHeader: false
    underline: false
  noHead:
    frames: [[0%,0%,100%,100%]]
    showFooter: true
    showHeader: false
    underline: false
  mainPage:
    frames: [[0%,0%,100%,110%]]
    showFooter: True
    showHeader: True
styles:
  base:
    allowWidows: 1
    allowOrphans: 1 
    alignment: TA_LEFT
    allowOrphans: false
    allowWidows: false
    backColor: null
    borderColor: null
    borderPadding: 5
    borderRadius: null
    borderWidth: 0
    bulletFontName: fontMono
    bulletFontSize: 10
    bulletIndent: 0
    commands: []
    firstLineIndent: 0
    fontName: fontSans
    fontSize: 9
    hyphenation: false
    leading: 12
    leftIndent: 0
    parent: null
    rightIndent: 0
    spaceAfter: 1
    spaceBefore: 1
    strike: false
    textColor: black
    wordWrap: null
    linkUnderline: {repD["pdflink"]}
    linkColor: blue
  tableofcontents:
    parent: normal
  big-text:
    fontSize: 150%
    parent: base
    fontName: fontSansBold
  blockquote:
    leftIndent: 20
    parent: bodytext
  bodytext:
    alignment: TA_JUSTIFY
    hyphenation: true
    parent: normal
    spaceBefore: 6
  align-center:
    alignment: TA_CENTER
    parent: bodytext
  align-right:
    alignment: TA_RIGHT
    parent: bodytext
  code:
    spaceBefore: 6
    spaceAfter: 6
    backColor: "#d1dede"
    borderColor: darkgray
    borderPadding: 6
    borderWidth: 0.5
    leftIndent: 0
    parent: literal
    fontName: fontMonoBold
  compgreen:
    textColor: green
    alignment: TA_RIGHT
    fontName: fontSansBold
  compred:
    textColor: red
    alignment: TA_RIGHT
    fontName: fontSansBold
  contents:
    parent: normal
  figure:
    spaceBefore: 18
    spaceAfter: 12
    alignment: TA_CENTER
    colWidths:
      - 100%
    commands:
      - - VALIGN
        - - 0
          - 0
        - - -1
          - -1
        - TOP
      - - ALIGN
        - - 0
          - 0
        - - -1
          - -1
        - CENTER
    parent: bodytext
  figure-caption:
    alignment: TA_CENTER
    fontName: fontSans
    parent: bodytext
  figure-legend:
    parent: bodytext
  footer-box:
    alignment: TA_CENTER
    fontName: fontSans
    commands:
      - - BOX
        - - 0
          - 0
        - - -1
          - -1
        - 0.25
        - white
  header-box:
    alignment: TA_RIGHT
    fontName: fontSans
    commands:
      - - BOX
        - - 0
          - 0
        - - -1
          - -1
        - 0.25
        - white
  heading:
    keepWithNext: true
    parent: normal
    spaceAfter: 1
    spaceBefore: 10
    fontName: fontSerif
    textColor: "#222222"
  heading1:
    fontSize: 120%
    parent: heading
    fontName: fontSansBold
    underlineColor: black
    underlineWidth: 1
    underlineOffset: 5
  heading2:
    fontSize: 110%
    parent: heading
    fontName: fontSansBold
    underlineColor: black
    underlineWidth: 1
    underlineOffset: 5
  heading3:
    fontSize: 100%
    parent: heading
  heading4:
    parent: heading
  heading5:
    parent: heading
  heading6:
    parent: heading
  hint:
    parent: admonition
  hint-heading:
    parent: admonition-heading
  image:
    spaceBefore: 5
    spaceAfter: 5
    alignment: TA_CENTER
    parent: bodytext
  important:
    parent: admonition
  important-heading:
    parent: admonition-heading
  italic:
    fontName: fontSansItalic
    parent: bodytext
  line:
    parent: lineblock
    spaceBefore: 0
  lineblock:
    parent: bodytext
  linenumber:
    parent: code
  literal:
    firstLineIndent: 0
    fontName: fontMono
    hyphenation: false
    parent: normal
    wordWrap: null
  normal:
    parent: base
  note:
    parent: admonition
  note-heading:
    parent: admonition-heading
  option-list:
    colWidths:
      - null
      - null
    commands:
      - - VALIGN
        - - 0
          - 0
        - - -1
          - -1
        - TOP
      - - TOPPADDING
        - - 0
          - 0
        - - -1
          - -1
        - 0
  rubric:
    alignment: TA_CENTER
    parent: bodytext
    textColor: darkred
  separation:
    parent: normal
  sidebar:
    backColor: cornsilk
    borderColor: darkgray
    borderPadding: 8
    borderWidth: 0.5
    float: none
    parent: normal
    width: 100%
  sidebar-subtitle:
    parent: heading4
  sidebar-title:
    parent: heading3
  subtitle:
    fontSize: 85%
    parent: title
    spaceBefore: 12
  table:
    alignment: TA_LEFT
    spaceBefore: 1
    spaceAfter: 1
    borderPadding: 5
    leftPadding: 6
    rightPadding: 6
    topPadding: 5
    bottomPadding: 5
    background-color: white
    alternate-row-background-color: lightgray
    commands:
      - - ROWBACKGROUNDS
        - - 0
          - 0
        - - -1
          - -1
        - - white
          - "#E0E0E0"
      - - BOX
        - - 0
          - 0
        - - -1
          - -1
        - 0.25
        - black        
  admonition:
    borderWidth: 0
    borderPadding: 0
  table-heading:
    alignment: TA_LEFT
    borderWidth: 0
    borderPadding: 0
    backColor: "#c5d1c5"
    borderColor: darkgray
    fontName: fontMonoBold
  tip-heading:
    parent: admonition-heading
  title:
    alignment: TA_CENTER
    fontSize: 120%
    keepWithNext: false
    parent: heading
    fontName: fontSansBold
    spaceAfter: 36
  title-reference:
    fontName: fontSansItalic
    parent: normal
  toc:
    parent: normal
    fontSize: 100%
  toc1:
    fontName: fontSansBold
    parent: toc
  toc10:
    leftIndent: 100
    parent: toc
  toc11:
    leftIndent: 100
    parent: toc
  toc12:
    leftIndent: 100
    parent: toc
  toc13:
    leftIndent: 100
    parent: toc
  toc14:
    leftIndent: 100
    parent: toc
  toc15:
    leftIndent: 100
    parent: toc
  toc2:
    leftIndent: 20
    parent: toc
  toc3:
    leftIndent: 40
    parent: toc
  toc4:
    leftIndent: 60
    parent: toc
  toc5:
    leftIndent: 80
    parent: toc
  toc6:
    leftIndent: 100
    parent: toc
  toc7:
    leftIndent: 100
    parent: toc
  toc8:
    leftIndent: 100
    parent: toc
  toc9:
    leftIndent: 100
    parent: toc
  topic-title:
    parent: heading3
  warning:
    parent: admonition
  warning-heading:
    parent: admonition-heading

"""

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(rivstyS)


# write rst for each rivt file in list
rivtfL = get_py()
print("\n\nrivt files included in report\n---------------------------")
for s in rivtfL:
    print("rivt file:", s)
print("---------------------------\n\n")
for frstS in rivtfL:
    frstT = Path(reptP, frstS)
    parts = Path(frstT).parts[-3:]  # Take last 3 segments
    short_p = ".../" + "/".join(parts)
    print("\nrun file: ", short_p, "\n")
    subprocess.run(["python", frstT, "-t none"])
    # log
    rbaseS = frstS.split(".")[0]
    docnumS = rbaseS[0:6]
    errlogN = docnumS + "log.txt"
    errlogT = Path(logsP, errlogN)
    with open(errlogT, "a") as f1:
        f1.write("write report: " + repD["title"] + "\n")
    logging.info("Report : " + repD["title"])

# aggregate rst into report rst file
rstfL = []
for fS in rivtfL:
    rstfL.append(fS.replace(".py", ".rst"))
reprst = (repD["repname"].replace(".pdf", ".rst")).strip()
freptT = Path(rstdocsP, reprst)
reportS = """\n"""
for fpubS in rstfL:
    frsT = Path(rstdocsP, fpubS)
    with open(frsT, "r") as f2:
        rstS = f2.read()
    reportS += rstS
with open(freptT, "w") as f3:
    f3.write(reportS)
# log
rbaseS = fpubS.split(".")[0]
docnumS = rbaseS[0:6]
errlogN = docnumS + "log.txt"
errlogT = Path(logsP, errlogN)
with open(errlogT, "a") as f4:
    f4.write("write report: " + repD["title"] + "\n")
logging.info("Report : " + repD["title"])

# write readme report
reptitleS = repD["repname"]
versionS = repD["version"]
authorS = repD["authors"]
borderS = "=" * 80
hdlS = reptitleS + " | " + authorS + " | " + timeS + " | " + versionS
headS = "\n" + hdlS + "\n" + borderS + "\n\n"
readmeT = Path(rivtP, "README.txt")
rtxtS = headS
rtxtL = get_readme()
with open(readmeT, "w") as outfile:
    for fname in rtxtL:
        readT = Path(pubP, "readme", fname)
        with open(readT) as infile:
            outfile.write(infile.read())
            outfile.write("\n")
            outfile.flush()
# with open(, "w", encoding="utf-8") as f3:
parts = Path(readmeT).parts[-3:]  # Take last 3 segments
short_p = ".../" + "/".join(parts)
print("\nreport written: ", short_p, "\n")
logging.info("README report : " + repD["title"])

# set report path
get_typeS = repD["repname"].split(".")[-1].strip()
if get_typeS == "pdf":
    pubT = Path(pubP, "pdfdocs", repD["repname"].strip())
elif get_typeS == "txt":
    pubT = Path(pubP, "txtdocs", repD["repname"].strip())
elif get_typeS == "html":
    pubT = Path(pubP, "docs", repD["repname"].strip())
else:
    print("File type not recognizedxxxx")
    print("Type must be '.pdf', '.html' or '.txt' ")
    sys.exit()
# log
rbaseS = frstS.split(".")[0]
docnumS = rbaseS[0:6]
errlogN = docnumS + "log.txt"
errlogT = Path(logsP, errlogN)
with open(errlogT, "a") as f1:
    f1.write("write report: " + repD["title"] + "\n")
logging.info("Report : " + repD["title"])

# write report
if get_typeS == "text":
    """write text report"""

    msgS = textx()
    print(msgS)
elif get_typeS == "pdf":
    """write pdf report"""

    print("write pdf report")
    msgS = pdfx(freptT, pubT)
    print(msgS)
elif get_typeS == "html":
    """write html report"""

    msgS = htmlx()
    print(msgS)
else:
    pass
