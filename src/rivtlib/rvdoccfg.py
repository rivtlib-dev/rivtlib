"""
this module includes doc configuration strings

"""

import glob
import os
import shutil
from datetime import datetime
from pathlib import Path


def copy_docs():
    """copy to _rstdocs

    copy page and download folders to _rstdocs
    """
    # Source pattern and destination directory
    rptS = os.getcwd()
    src_P = str(Path(rptS, "rvsrc", "page", "*.*"))
    destP = str(Path(rptS, "_rstdocs", "_static"))

    for fileP in glob.glob(src_P):
        shutil.copy2(fileP, destP)


def pdf_confpy(self, fD):
    """write config.py

    Return:

    """

    # region - pdf confpy
    copy_docs()
    confpyS = f"""
import sys
from pathlib import Path

sys.path.append(str(Path(".").resolve()))

project = "{self.titleS}"
copyright = "{self.copyS}"
author = "self.{self.authorS}"
release = "{self.verS}"

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
    "sphinxcontrib.mermaid"
]
root_doc = "index"
duration_write_json = ""
html_show_sourcelink = False
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".rst"]
templates_path = ["_static"]
html_static_path = ["_static"]
html_css_files = ["_custom.css"]
locale_dirs = ["./_static/_locale"]
html_title = " "
html_theme = "pydata_sphinx_theme"
html_context = {{"default_mode": "dark"}}
html_sidebars = {{"**": ["sidebar-nav-bs.html"]}}
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
            "text": "{self.runlabelS}",
        "image_dark": "{self.runlogo}",
        "image_light": "{self.runlogo}",
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
pdf_documents = [("{self.rvbaseS}", "{self.rvbaseS}", "{self.titleS}", 
            "{self.authorS}")]
# Label to use as a prefix for the subtitle on the cover page
subtitle_prefix = "User Manual"
# A list of folders to search for stylesheets.
pdf_style_path = ["./_rstdocs/"]
# A colon-separated list of folders to search for fonts.
pdf_font_path = ["./_rstdocs/_static/fonts"]
# A comma-separated list of custom stylesheets.
pdf_stylesheets = ["./_rstdocs/rivtstyle.yaml"]
# If false, no coverpage is generated.
pdf_use_coverpage = False
# Name of the cover page template to use
pdf_cover_template = ""
# Show Table Of Contents at the beginning?
pdf_use_toc = False
# Page template name for "regular" pages
pdf_page_template = 'mainPage'
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
    """
    # endregion

    rvfileT = str(Path(fD["rstdocsP"], "conf.py"))
    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(confpyS)


def pdf_yamlS(self, fD):
    """write rivt yaml file for pdf"""

    rvfileT = str(Path(fD["rstdocsP"], "rivtstyle.yaml"))

    # region - pdf yaml
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
  firstTemplate: noHead
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
    linkUnderline: {self.linkB}
    linkColor: blue
  tableofcontents:
    parent: normal
  big-text:
    fontSize: 175%
    parent: base
    fontName: fontSans
  medium-text:
    fontSize: 125%
    parent: base
    fontName: fontSans
  small-text:
    fontSize: 125%
    parent: base
    fontName: fontSans 
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
    # endregion

    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(rivstyS)


def html_templ(self, fD):
    """write html templates

    Return:

    """

    # region - html template
    srcS = Path(fD["reptP"], self.coverlogo)
    destS = Path(fD["rstdocsP"], "_static")
    shutil.copy(srcS, destS)
    srcS = Path(fD["reptP"], self.runlogo)
    shutil.copy(srcS, destS)
    timeS = datetime.now().strftime("%Y-%m-%d")

    rvdateS = f"""
<!-- _templates/rv-date.html -->
<div class="footer-item">
    <p class="rvdate">
        {timeS}
    </p>
</div>
"""
    rvdateT = str(Path(fD["rstdocsP"], "_templates", "rv-date.html"))
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
    rvauthT = str(Path(fD["rstdocsP"], "_templates", "rv-author.html"))
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
    rvtitleT = str(Path(fD["rstdocsP"], "_templates", "rv-title.html"))
    with open(rvtitleT, "w", encoding="utf-8") as f2:
        f2.write(rvtitleS)
    # endregion


def html_confpy(self, fD):
    """write config.py

    Return:

    """

    # region - html confpy
    copy_docs()
    confpyS = f"""
import sys
from pathlib import Path

sys.path.append(str(Path(".").resolve()))

project = "{self.titleS}"
copyright = "{self.copyS}"
author = "self.{self.authorS}"
release = "{self.verS}"

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
templates_path = ["_static"]
html_static_path = ["_static"]
html_css_files = ["custom.css"]
locale_dirs = ["_locale"]
html_title = " "
html_theme = "pydata_sphinx_theme"
html_context = {{"default_mode": "dark"}}
html_sidebars = {{"**": ["sidebar-nav-bs.html"]}}
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
            "text": "{self.runlabelS}",
        "image_dark": "{self.runlogo}",
        "image_light": "{self.runlogo}",
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
"""

    rvfileT = str(Path(fD["rstdocsP"], "conf.py"))
    with open(rvfileT, "w", encoding="utf-8") as f5:
        f5.write(confpyS)


# endregion
