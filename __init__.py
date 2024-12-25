''' 
rivtlib
=======

**rivtlib** is a Python library that generates rivt docs and reports. **rivt**
is a lightweight markup language for writing engineering documents based on
restructured text Python libraries. **rivt** is designed to make it easy to
share and reuse engineering document templates.


rivt API
--------

A rivt file is a Python file (*.py) that imports **rivtlib**:: 

    **import rivtlib.rivtapi as rv**


and exposes 6 API functions ::


    rv.R(rS) - (Run) Run shell scripts 
    rv.I(rS) - (Insert) Insert text, images, tables and math equations 
    rv.V(rS) - (Values) Evaluate tables, values and equations 
    rv.T(rS) - (Tools) Execute Python functions 
    rv.X(rS) - (eXclude) Skip rivt-string processing 
    rv.W(rS) - (Write) Write formatted rivt documents 

    
where **rS** is a triple quoted string that follows rivt markup syntax. A
**rivt** doc (document) is a text, HTML or PDF ouput file from a processed rivt
file. A **rivt report** (report) is a collated collection of rivt docs.


rivt directory
--------------

rivt_Report-Label/
    ├── div01_div-label/            
        ├── dat01_source/          
            ├── data.csv
            ├── attachment1.pdf
            ├── fig.png
            └── functions.py
        ├── riv01_label1.py        
        └── riv02_label2.py
    ├── [div02_div-label/          
        ├── dat02_source/          
            ├── data.csv
            └── fig.png
        └── riv01_label3.py      
    ├── rivtdocs_/                 
        ├── pdf_/
            ├── doc0101_label1.pdf
            ├── doc0102_label2.pdf
            ├── doc0201_label3.pdf
            └── Report-Label.pdf
        ├── text_/
            ├── doc0101_label1.txt
            ├── doc0102_label2.txt
            └── doc0201_label3.txt
        ├── md_/
            ├── doc0101_label1.md
            ├── doc0102_label2.md
            └── doc0201_label3.md
        ├── html_/
            ├── doc0101_label1.html
            ├── doc0102_label2.html
            └── doc0201_label3.html
        ├── temp_/
            └── doc0201_label3.tex
    ├── config.ini                  
    ├── cover-page.pdf              
    └── README.txt                  


rivtpub directory
-----------------

rivtpub_Report-Label/
    ├── div01_div-label/           
        ├── dat01_source/          
            ├── data.csv
            ├── attachment1.pdf
            ├── fig.png
            └── functions.py
        ├── riv01_label1.py        
        └── riv02_label2.py
    ├── [div02_div-label/          
        ├── dat02_source/           
            ├── data.csv
            └── fig.png
        └── riv01_label3.py        
    └── README.txt                 


rivtzip
-------

**rivt** is part of the open source **rivtzip** framework and is distributed
under the MIT license. **rivtzip** is an open source framework for publishing
rivt documents. The framework can be downloaded as a portable Windows zip file,
or installed through OS specific shell scripts (https://rivt.zip). It includes
five established technologies::

    VSCode - document editing and processing

    Python - analysis and formatting
        
    Latex - typesetting
        
    GitHub - version control

    QCAD - diagramming


'''
