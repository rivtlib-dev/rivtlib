''' 
rivtlib
=======

**rivtlib** is a Python library that produces rivt docs and reports. **rivt**
is a lightweight markup language used by **rivtlib** for writing engineering
documents. It wraps parts of the restructuredtext markup language. **rivt** is
designed to make it easy to share and reuse engineering document templates.


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

    
where **rS** is a triple quoted string that follows rivt markup syntax. The
syntax wraps and extends reStructuredText. A **rivt** document (doc) is a text,
HTML or PDF ouput file from a processed rivt file. Each doc is also a
subdivision in a **rivt report** - a collated collection of rivt docs.


rivt directory
--------------

rivt-Report-Label/               
    ├── d01-div-label/                  (division 1 files)
        ├── r0101-label1.py             (rivt subdivsion file)
        └── r0102-label2.py             (rivt subdivsion file)
    ├── d02-div-label/                  (division 2 files)
        └── r0201-label3.py             (rivt subdivision file)
    ├── rivt-docs/                      (document output)
        ├── rivt-pdf_/                      
            ├── rivt0101-label1.pdf      
            ├── rivt0102-label2.pdf
            ├── rivt201-label3.pdf
            └── Report-Label.pdf 
        ├── rivt-text_/                    
            ├── rivt0101-label1.txt      
            ├── rivt0102-label2.txt
            └── rivt0201-label3.txt          
        ├── rivt-html_/                    
            ├── rivt0101-label1.html
            ├── rivt0102-label2.html
            └── rivt0201-label3.html        
        ├── rivt-temp_/
            └── d0201-label3.tex
    ├── r01/                            (source files)         
        ├── ins
            ├── fig1.png            
            └── attach1.pdf
        ├── run
            └── sap.cmd
        ├── tool
            ├── func1.py                   
            └── func2.py
        └── val
            └── val0101.csv
    ├── r02/                    
        ├── data1.csv                   
        └── standards.txt
    ├── config.ini                      (report config file)
    ├── cover-page.pdf                  (report cover page)
    └── README.txt                      (GitHub searchable report) 



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


rivtzip files
-------------

**rivt** is part of the open source **rivtzip** framework and is distributed
under the MIT license. **rivtzip** is an open source framework for publishing
rivt documents. The framework can be downloaded as a portable Windows zip file,
or installed through OS specific shell scripts (https://rivt.zip). It includes::

    **VSCode** - document editing and processing

    **Python** - analysis and formatting
        
    **Latex** - typesetting
        
    **GitHub** - version control

    **QCAD** - diagramming


'''
