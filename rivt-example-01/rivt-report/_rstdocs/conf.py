
import sys
import os
from pathlib import Path

font_folder_path = os.path.join(os.path.dirname(__file__), '_static',  'fonts')
# sys.path.append(str(Path(".").resolve()))

project = "Example 1 - rivt doc"
copyright = "--"
author = "self.R Holland"
release = "1.0.0a17"

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
pygments_style = "borland"
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
html_context = {"default_mode": "dark"}
html_sidebars = {"**": ["sidebar-nav-bs.html"]}
html_theme_options = {
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
    "logo": {
            "text": "rivt",
        "image_dark": "logo2.png",
        "image_light": "logo2.png",
    },
}
favicons = [
    {
        "rel": "icon",
        "sizes": "16x16",
        "href": "favicon-16x16.png",
    },
    {
        "rel": "icon",
        "sizes": "32x32",
        "href": "favicon-32x32.png",
    },
]
# -- Options for PDF output -------------------------------------------------
# source start file, target name, title, author, options
# options: ('index', 'MyProject', 'My Project', 'Author Name', {"pdf_compressed": True})
# More than one author : \r'Guido van Rossum\Fred L. Drake, Jr., editor'
pdf_documents = [("rv001-doc-example01", "rv001-doc-example01", "Example 1 - rivt doc", 
            "R Holland")]
# A colon-separated list of folders to search for fonts.
pdf_font_path = ["_rstdocs/_static/fonts","../_rstdocs/_static/fonts/" ]
# A list of folders to search for stylesheets.
pdf_style_path = ["_rstdocs","../_rstdocs"]
# A comma-separated list of custom stylesheets.
pdf_stylesheets = ["rivtstyle.yaml"]
# If false, no coverpage is generated.
pdf_use_coverpage = False
# Name of the cover page template to use
pdf_cover_template = ""
# Label to use as a prefix for the subtitle on the cover page
# subtitle_prefix = "User Manual"
# Show Table Of Contents at the beginning?
pdf_use_toc = False
# How many levels deep should the table of contents be?
pdf_toc_depth = 2
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
# Insert footnotes where they are defined 
pdf_inline_footnotes = True
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
    