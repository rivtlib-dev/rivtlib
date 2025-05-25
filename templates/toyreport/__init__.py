#! python
''' This script generates an example folder and file structure for a
toy rivt report.

**rivt** is an open source engineering document markdown language for writing,
organizing and sharing engineering documents. **rivtlib** is a Python library
for processing rivt. It runs on any platform that supports Python 3.10 or
later. rivtlib works with both single file documents and extensive reports with
hundreds of files. 

A rivt file is a Python file that begins with the import statement:

*import rivtlib.rivtapi as rv*
 
which provides four API functions. Each function takes a single, triple quoted
string as an argument.

rv.R(rS) - report and document configuration (Rivtinit)
rv.I(rS) - static text, images, tables and math (Insert)
rv.V(rS) - equations (Values)
rv.T(rS) - Python functions and scripts (Tools)
rv.write() - formatted rivt document output

rv.R may be followed by arbitrary sequences of rv.I, rv.V and rv.T. When
running in an IDE (e.g. VSCode), each function may be run interactively using
the standard cell decorator *# %%*. Interactive output and output to stdout
(terminal) is formatted as utf-8 text. The rv.write() function exports
calculated values to a file for later use, and generates formatted documents
and reports in GitHub Markdown (ghmd) and PDF.

rivt syntax includes arbitrary unicode and rivt commands and tags. It wraps and
extends reStructuredText (reST).  See https://rivt-doc.net  for user manual

========
commands
========

A rivt command reads or writes external files and is triggered by starting a
line with ||. Commands are implemented per API function. Either-or parameter
choices below are designated with semi-colons. List parameters are separated
with commas.

=============== ===============================================================
 name                      Commands (VSCode snippet prefix)
=============== ===============================================================

Rivtinit (ri)       rv.R("""label | toc;notoc,start page

                        ||text (te)
                        ||append (ap)

                        """)

Insert (in)         rv.I("""label | nocolor;hexvalue  
                        
                        ||image (im)
                        ||text (te)
                        ||table (ta)

                    """)

Values (va)         rv.V("""label | sub;nosub 
                
                        ||declare (de)

                        """)

Tools (to)          rv.T("""label | summary;inline
                
                        Python code

                        """)

Exclude             rv.X("""any API function

                        A method changed to X is not evaluated (used for
                        comments and debugging).

                    """)

Write (pu)          rv.write_public(text,md,pdf,report)
      (pr)          rv.write_private(text,md,pdf,report)


================================================ ============== 
       command syntax                                API      
================================================ ============== 

|| text | rel file path | rivt;plain;default        R I V      

|| append | rel file path | num;nonum                 R        

|| image  | rel file path, .. | .50, ..               I        
 
|| table  | rel file path | 30,r;l;c                  I        

|| declare | rel file path | print;noprint            V        

====
tags
====

rivt tags are typically entered at the end of line and are processed per API
function. Line tags apply to a single line. Block tags appy to blocks of text.

===================== ================================== ==========
   line tags                 description                   API
===================== ================================= ===========
text _[b]                bold                            R I V 
text _[c]                center                          R I V  
text _[i]                italic                          R I V  
text _[bc]               bold center                     R I V  
text _[bi]               bold italic                     R I V
text _[r]                right justify                   R I V
text _[u]                underline                       R I V   
text _[p]                plain                           R I V   
text _[l]                LaTeX math                        I V
text _[s]                sympy math                        I V
text _[bs]               bold sympy math                   I V
text _[e]                equation label, autonumber        I V
text _[f]                figure caption, autonumber        I V
text _[t]                table title, autonumber           I V
text _[#]                footnote, autonumber              I V
text _[d]                footnote description              I V
_[page]                  new page                          I V
_[address, label]        url or internal reference         I V
= (declare)              a = 1.2 | unit, alt | descrip       V
:= (assign)              a := b + c | unit, alt | n,n        V


==================== ========================== ==========
   block tags                description            API
==================== ========================== ==========
_[[b]]                  start bold                 R I
_[[c]]                  start center               R I
_[[i]]                  start italic               R I
_[[p]]                  start plain                R I
_[[l]]                  start LaTeX                  I
_[[e]]                  end block                  R I


=================
rivt file example
=================

File formatting conventions follow Python pep8 and ruff conventions. API
function declarations start in column one. All other lines are indented 4
spaces to facilitate section folding, bookmarks and legibility. The first line
of each function defines the heading for a new document section, followed by
section parameters. New sections may be suppressed by prepending the heading
label with a double hyphen (--).

--------------------------------------

import rivtlib.rivtapi as rv

rv.R("""Introduction | notoc, 1

    The Rivtinit method is the first method of a rivt file and specifies
    repository, report and document settings.

    The first line of any method is the heading line, which starts a new
    document section. If the section heading is preceded by two dashes (--) it
    becomes a section reference and a new section is not started. The toc
    parameter specifies whether a document table of contents is generated and
    inserted at the top of the document (not to be confused with a report table
    of contents). The page number is the starting page number for the doc, when
    processed as a stand alone document.

    The init command specifies the name of the configuration file which is read
    from the rivt-doc folder. Report formatting can be easily modified by
    specifying a different init file.

    ||init | rivt01.ini

    The text command inserts text from an external file. Text files may be
    plain text or include rivt tags.

    ||text | private/data/proj.txt | plain
    
    The append command attaches PDF files to the end of the doc.

    || append | append/report1.pdf
    || append | append/report2.pdf

    
    """)

rv.I("""The Insert method | nocolor 

    The Insert method formats static information e.g. images and text. The
    color command specifies a background color for the section.

    ||text | data01/describe.txt | rivt     

    The table command inserts and formats tabular data from csv or xls files.
    The _[t] tag formats and autonumbers table titles.

    A table title  _[t]
    || table | data/file.csv | 60,r

    The image command inserts and formats image data from png or jpg files. The
    _[f] tag formats and autonumbers figures.
        
    A figure caption _[f]
    || image | data/f1.png | 50

    Two images may be placed side by side as follows:

    The first figure caption  _[f]
    The second figure caption  _[f]
    || image | private/image/f2.png, private/image/f3.png | 45,35
    
    The tags _[x] and _[s] format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    """)

rv.V("""The Values method |  nosub 

    The Values method assigns values to variables and evaluates equations. The
    sub or nosub setting specifies whether equations are also printed with
    substituted numerical values.
    
    The equal tag declares a value. A sequence of declared values terminated
    with a blank line is formatted as a table.
    
    Example of assignment list _[t]
    f1 = 10.1 * LBF |LBF, N| a force value
    d1 = 12.1 * IN  |IN, CM| a length value

    An equation tag provides an equation description and number. A colon-equal
    tag assigns a value and specifies the result units and the output decimal
    places printed in the result and equation.

    Example equation - Area of circle  _[e]
    a1 := 3.14(d1/2)^2 | IN^2, CM^2 | 1,2

    || declare | data01/values02.csv
    
    The declare command imports values from the csv file written by rivt when
    processing values in other documents. 

""")

rv.T("""The Tools method | summary

    # The Tools method processes Python code in the rivt namespace and prints
    # the code and the result of any print statement in the doc. 
    # Functions may be written explicitly or imported from other
    # files. Line comments (#) are printed. Triple quotes cannot be used. Use
    # raw strings instead.
    
    # Four Python libraries are imported by rivt and available as: 
    # pyplot -> plt
    # numpy -> np
    # pandas -> pd
    # sympy -> sy
    
    # Python code example:
    
    def f1(x,y): z = x + y
        print(z)
        return Z

    with open('file.csv', 'r') as f: 
        input = f.readlines()
    
    var = range(10)
    with open('fileout.csv', 'w') as f: 
        f.write(var)
        
    """)

rv.X("""any text

    Changing a function to X skips evaluation of that function. Its uses
    include review comments and debugging.

    """) 

-----------------------------------------------

=======
folders
=======

rivtlib can process single rivt files, but typically it is used to generate
reports. A rivt report is generated from the folder structure illustrated
below. rivt documents are organized into divisions. Document inputs and outputs
may be stored in or directed to publically shareable or private foldrers.
Reports is formatted with divisions, subdivisions and sections.

Fixed folder and file prefixes are shown in [ ]. Report and document headings
are taken from the folder and file labels. Tools are available to generate
starter folder templates.

[rivt]_Report-Label/               
    ├── [div01]-div-label/            (division folder)
        ├── [data01]/                 (resource data)
            ├── data.csv                   
            ├── attachment.pdf
            └── fig.png            
             functions.py                   
        ├── [riv01]-label1.py         (rivt file)
        └── [riv02]-label2.py         (rivt file)   
    ├── [div02]-div-label/            (division folder)
        ├── [data02]/                 (resource data)
            ├── data.csv
            └── fig.png
        └── [riv01]_label3.py         (rivt file)
    ├── [data-private]/                 
        ├── [data]/                   (private data)                   
            ├── data.csv
            ├── attachment.pdf
            └── fig.png        
        ├── [functions]/              (private functions)                   
            ├── [data]/
            ├── [output]/
            └── function.py                
        ├── [rivt-docs]/              (private output documents)
            ├── [pdf]/                      
                ├── doc0101-label1.pdf      
                ├── doc0102-label2.pdf
                ├── doc0201-label3.pdf
                └── Report-Label.pdf 
            ├── [text]/                    
                ├── doc0101-label1.txt      
                └── doc0201-label3.txt       
            ├── doc0101-label1.md            
            └── doc0201-label3.md
        ├── [temp]/
            └── doc0201-label3.tex 
    ├── [functions]/                  (public functions)                   
        ├── [data]/
        ├── [output]/
        ├── function1.py
        └── function2.py                
    ├── [rivt-docs]/                  (public output documents)
        ├── [pdf]/                      
            ├── doc0101-label1.pdf      
            ├── doc0102-label2.pdf
            ├── doc0201-label3.pdf
            └── Report-Label.pdf 
        ├── [text]/                    
            ├── doc0101-label1.txt      
            ├── doc0102-label2.txt
            └── doc0201-label3.txt           
    ├── .gitignore
    ├── config.ini                    (config file)
    ├── doc0101-label1.md             (public output documents) 
    ├── doc0102-label2.md
    ├── doc0201-label3.md
    └── README.txt                    (cumulative documents - searchable) 
'''
