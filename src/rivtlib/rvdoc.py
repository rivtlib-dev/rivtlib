import configparser
import logging
import os
import subprocess
import sys
import warnings
from datetime import datetime
from pathlib import Path

from fastcore.utils import store_attr

import __main__


class Cmdp:
    """doc publish object

    Args:
        Args:
            fD (dict): fDers
            lD (dict): labels
            rivD (dict): values
            rivL (list): values for export

        Vars:
            sS (str): rv.D API content substring
            uS (str): utf doc string
            r2S (str): rlabpdf doc string
            rS (str): reST doc string
    """

    def __init__(self, sS, fD, lD, rivtD, dutfS, drstS, dtxtS):
        # region
        store_attr()
        self.pthS = ""
        self.parS = ""
        self.sL = sS.split("\n")
        self.rivtP = fD["rivtP"]
        errlogT = fD["errlogT"]
        self.confg = []

        modnameS = os.path.splitext(os.path.basename(__main__.__file__))[0]
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)-8s  "
            + modnameS
            + "   %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M",
            filename=errlogT,
            filemode="w",
        )
        warnings.filterwarnings("ignore")
        self.logging = logging
        # strip leading spaces and comments from section
        sL = sS.split("\n")  # unprocessed lines
        spL = []
        for slS in sL[1:]:
            if len(slS) < 5:
                continue
            if len(slS.strip()) > 0:
                spL.append(slS[4:])
        self.spL = spL  # preprocessed list
        with open(errlogT, "a") as f4:
            f4.write(self.sL[0] + "\n")
        self.logging.info("SECTION : " + self.sL[0])
        # endregion

    def cmdx(self):
        """parse commands and blocks in Doc API
        Commands:
            | PUBLISH | doc name; - | text; html; pdf; texpdf
            | ATTACHPDF | rel. path | prepend;append

        Blocks:
            _[[METADATA]]
            _[[END]]

        Returns:
            msgS (str): completion message
        """
        # region
        msgS = ""
        ptempS = ""
        blockB = False
        self.blockS = """"""
        self.docnameS = " "
        uS = rS = tS = lS = ""
        for pS in self.spL:
            if len(pS) > 0:
                if pS[0:11] == "| PUBLISH |":
                    pL = pS[5:].split("|")
                    typeS = str(pL[2].strip())
                    self.docnameS = str(pL[1].strip()).strip()
                    if self.docnameS == "-":
                        self.docnameS = self.fD["docnameS"]
                    dtypeS = typeS + ("x")
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                    continue
                elif pS[0:13] == "| ATTACHPDF |":
                    dtypeS = "attachpdfx"
                    self.pthS = pL[1].strip()
                    self.parS = pL[2].strip()
                    obj = getattr(Cmdp, dtypeS)
                    msgS = obj(self)
                    continue
                elif "_[[" in pS and ("_[[END]]" not in pS):  # block start
                    bsL = pS.split("]]")
                    tagS = bsL[0][3:].strip()
                    if tagS == "METADATA":
                        # print(f"{tagS=}")
                        self.logging.info(f"block tag : {tagS}]]")
                        self.blockS = """"""
                        blockB = True
                        continue
                elif blockB and ("_[[END]]" in pS):  # block terminate
                    if tagS == "METADATA":
                        obj = getattr(Cmdp, "metadatax")
                        msgS = obj(self)
                        self.blockS = """"""
                        continue
                elif blockB:
                    self.blockS += pS + "\n"
                    continue
                else:  # everything else
                    pass
            uS += pS
            rS += pS
            tS += pS
            lS += pS

        mD = {
            "uS": uS,
            "rS": rS,
            "tS": tS,
            "lS": lS,
        }

        return msgS
        # endregion

    def htmlx(self):
        """write readme and sphinx-html files

        Returns:
            msgS (str): completion message

        """
        self.confpy()  # update conf.py
        rvbaseS = self.fD["rbaseS"]
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".html"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        rvdocT = str(Path(self.fD["rivtpubP"], "docs", rvdocS))
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        htmlcmdS = f"sphinx-build -E -D root_doc={rvbaseS} {str(self.fD['rstdocsP'])} {self.fD['htmlpubP']} \n"
        try:
            result = subprocess.run(htmlcmdS, shell=True, check=True)
            if not result.returncode:
                print("\nhtml script executed")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        return (
            f"html doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )

    def pdfx(self):
        """write readme and sphinx-pdf files

        Returns:
            msgS (str): completion message
        """
        # region
        self.confpy()  # update conf.py
        self.coverS()  # update cover page
        rvbaseS = self.fD["rbaseS"]
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".pdf"
        rvfileT = str(Path(self.fD["rstdocsP"], rvfileS))
        rvdocT = str(Path(self.fD["rivtpubP"], "pdfdocs", rvdocS))
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(self.drstS)
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)
        pdfcmdS = f"sphinx-build -E -b pdf -D root_doc={rvbaseS} {str(self.fD['rstdocsP'])} {self.fD['pdfpubP']} \n"
        try:
            result = subprocess.run(pdfcmdS, shell=True, check=True)
            if not result.returncode:
                print("\npdf script executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
            print("Stderr:", e.stderr)
        return (
            f"pdf doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )
        # endregion

    def textx(self):
        """write readme and text files

        Returns:
            msgS (str): completion message
        """
        self.confpy()  # update conf.py
        rvdocS = self.fD["rbaseS"] + ".txt"
        rvdocT = str(Path(self.fD["rivtpubP"], "txtdocs", rvdocS))
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
        with open("README.txt", "w", encoding="utf-8") as f5:
            f5.write(self.dutfS)

        return (
            f"text doc written: {str(rvdocT)} \n"
            + "readme file written: README.txt"
        )

    def metadatax(self):
        """read meta block as config file

        Returns:
            msgS (str): metadata read
        """

        self.configL = configparser.ConfigParser()
        self.configL.read_string(self.blockS)
        self.authorS = self.configL["doc"]["authors"]
        self.verS = self.configL["doc"]["version"]
        self.copyS = self.configL["doc"]["copyright"]
        self.repoS = self.configL["doc"]["repo"]
        self.liceS = self.configL["doc"]["license"]
        self.f1_authorS = self.configL["doc"]["fork1_authors"]
        self.f1_verS = self.configL["doc"]["fork1_version"]
        self.f1_repoS = self.configL["doc"]["fork1_repo"]
        self.f1_liceS = self.configL["doc"]["fork1_license"]
        self.coverlogo = self.configL["layout"]["coverlogo"]
        self.footlogo = self.configL["layout"]["footlogo"]
        self.rlabfooterS = self.configL["layout"]["pdf_footer"]
        self.rlabpageS = self.configL["layout"]["pdf_pagesize"]
        self.rlabmarginS = self.configL["layout"]["pdf_margins"]
        self.rlabheaderS = self.configL["layout"]["pdf_header"]
        self.rlabcoverS = self.configL["layout"]["pdf_cover"]
        self.rlabwidth = self.configL["layout"]["text_width"]

    def attachpdfx(self):
        """attach pdf or insert pdf as download file"""

        msgS = "attachment"
        return msgS

    def confpy(self):
        """write config.py"""

        rvbaseS = self.fD["rbaseS"]
        rvfileT = str(Path(self.fD["rstdocsP"], "conf.py"))

        confpyS = f"""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(".").resolve()))

project = "{self.docnameS}"
copyright = "{self.copyS}"
author = "{self.authorS}"
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
templates_path = ["_templates"]
locale_dirs = ["_locale"]
html_title = "rivt"
html_theme = "pydata_sphinx_theme"
html_context = {{"default_mode": "dark"}}
html_sidebars = {{"**": ["sidebar-nav-bs.html"]}}
html_static_path = ["_static", "_static/img"]
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
    "footer_start": ["copyright"],
    "footer_end": [],
    "logo": {{
            "text": "rivt",
        "image_dark": "rivhome11c.png",
        "image_light": "rivhome11c.png",
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
pdf_documents = [("{rvbaseS}", "{rvbaseS}", "{self.docnameS}", 
            "{self.authorS}")]
# Label to use as a prefix for the subtitle on the cover page
subtitle_prefix = "User Manual"
# A list of folders to search for stylesheets. Example:
pdf_style_path = ["./rstdocs_/_static/pdfstyle"]
# A colon-separated list of folders to search for fonts. Example:
pdf_font_path = ["./rstdocs_/_staticfonts"]
# A comma-separated list of custom stylesheets. Example:
pdf_stylesheets = ["./rstdocs_/_static/pdfstyle/stylepdf1.yaml"]
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
pdf_use_toc = True
# How many levels deep should the table of contents be?
pdf_toc_depth = 9999
# Insert footnotes where they are defined instead of
# at the end.
pdf_inline_footnotes = True
# If false, no index is generated.
pdf_use_index = True
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
# Page template name for "regular" pages
# pdf_page_template = 'cutePage'
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
        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(confpyS)

    def coverS(self):
        """
        cover page

        """

        timeS = datetime.now().strftime("%Y-%m-%d - %I:%M%p")
        rvfileT = str(Path(self.fD["rstdocsP"], "_templates", "pdfcover.rst"))
        coverpgS = f"""
.. role:: big-text

|
|
        
.. image:: ../_src/{self.coverlogo}
   :width: 600px
   :align: center

|
|
|


.. class:: center

    :big-text:`{self.docnameS}`

|
|
|
|
|
|

.. class:: center

    **{self.authorS}**

|

.. class:: center

    {timeS}

    
.. raw:: pdf

   PageBreak

"""

        with open(rvfileT, "w", encoding="utf-8") as f5:
            f5.write(coverpgS)

    def latexx(self):
        """Modify TeX file to avoid problems with escapes:

        -  Replace marker "aaxbb " inserted by rivt with
            \\hfill because it is not handled by reST).
        - Delete inputenc package
        - Modify section title and add table of contents

         write calc rSt file to d00_docs fDer

        Args:
            cmdS (str): [description]
            doctypeS ([type]): [description]
            stylefileS ([type]): [description]
            calctitleS ([type]): [description]
            startpageS ([type]): [description]

        convert reST to tex file

        0. insert [i] data into model (see _genxmodel())
        1. read the expanded model
        2. build the operations ordered dictionary
        3. execute the dictionary and write the md-8 calc and Python file
        4. if the pdf flag is set re-execute xmodel and write the PDF calc
        5. write variable summary to stdout

        :param pdffileS: _description_
        :type pdffileS: _type_

        """
        pypathS = os.path.dirname(sys.executable)
        rvstyleP = os.path.join(
            pypathS,
            "Lib",
            "site-packages",
            "rivtlib",
            "styles",
        )
        rvfileS = self.fD["rbaseS"] + ".rst"
        rvdocS = self.fD["rbaseS"] + ".html"

        return (
            "tex pdf doc written: "
            + rvdocS
            + "\n"
            + "readme written: README.txt"
        )
