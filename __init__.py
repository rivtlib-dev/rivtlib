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


and exposes 6 functions::


    rv.R(rS) - (Run) Run shell scripts 
    rv.I(rS) - (Insert) Insert text, images, tables and math equations 
    rv.V(rS) - (Values) Evaluate tables, values and equations 
    rv.T(rS) - (Tools) Execute Python functions 
    rv.X(rS) - (eXclude) Skip rivt-string processing 
    rv.W(rS) - (Write) Write formatted documents and reports

    
where **rS** is a triple quoted string that follows rivt markup syntax. The
syntax wraps and extends reStructuredText. A **rivt** document (doc) is a text,
HTML or PDF ouput file from a processed rivt file. Each doc can also be a
subdivision in a collated collection of rivt docs -  a **rivt report**.


rivt directory
--------------

rivt-Report-Label/               
    ├── d01-div-label/                  (division 1 files)
        ├── ins01/                      (insert files)
            ├── fig1.png            
            └── attach1.pdf
        └── val01/                      (values files)
            └── val0101.csv
        ├── r0101-label1.py             (rivt file)
        └── r0102-label2.py             (rivt file)
    ├── d02-div-label/                  (division 2 files)
        ├── ins01/      
            ├── data1.csv                   
            └── standards.txt
        └── r0201-label3.py             (rivt file)
    ├── rivt-docs/                      (document output)
        ├── rivt-pdf/                      
            ├── rivt0101-label1.pdf      
            ├── rivt0102-label2.pdf
            ├── rivt201-label3.pdf
            └── Report-Label.pdf 
        ├── rivt-xpdf/                      
            ├── rivt0101-label1.pdf      
            ├── rivt0102-label2.pdf
            ├── rivt201-label3.pdf
            └── Report-Label.pdf 
        ├── rivt-text/                    
            ├── rivt0101-label1.txt      
            ├── rivt0102-label2.txt
            └── rivt0201-label3.txt          
        ├── rivt-html/                    
            ├── rivt0101-label1.html
            ├── rivt0102-label2.html
            └── rivt0201-label3.html        
        ├── rivt-temp/
            └── d0201-label3.tex             
    ├── tools/                           (functions and terminal files)
        ├── func1.py                   
        └── sap.cmd
        └── func2.py                  
    ├── rivt-config.ini                 (report config file)
    ├── cover-page.pdf                  (report cover page)
    └── README.txt                      (report - GitHub searchable) 
               


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
