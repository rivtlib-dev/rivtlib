''' 
rivtlib
=======

A **rivt doc** (document) is a text, HTML or PDF ouput file from a processed
rivt file. A **rivt report** (report) is a collated collection of rivt docs.
**rivtlib** is a Python library that generates rivt docs and reports. It is part
of the open source **rivtzip** framework and is distributed under the MIT
license.

**rivtzip** is an open source framework for publishing rivt documents. The
framework can be downloaded as a portable Windows zip file, or installed through
OS specific shell scripts (https://rivt.zip). It includes five established
technologies::

    VSCode and extensions - document editing and processing

    Python and libraries - analysis and formatting
        
    Latex - typesetting
        
    Git, GitHub - version control

    QCAD - diagramming


rivt API
--------

**rivt** is a lightweight markup language for writing engineering documents
based on restructured text Python libraries. **rivt** is designed to make it
easy to share and reuse engineering document templates.  

A rivt file is a Python file (*.py) that imports **rivtlib**:: 

    **import rivtlib.rivtapi as rv**


and exposes 6 API functions ::

    rv.R(rS) - (Run) Run shell scripts 
    rv.I(rS) - (Insert) Insert text, images, tables and math equations 
    rv.V(rS) - (Values) Evaluate tables, values and equations 
    rv.T(rS) - (Tools) Execute Python functions 
    rv.X(rS) - (eXclude) Skip rivt-string processing 
    rv.W(rS) - (Write) Write formatted rivt documents 

    
where **rS** is a triple quoted string that follows rivt markup syntax.

'''
