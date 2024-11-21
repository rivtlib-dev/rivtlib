''' 
rivt API
--------

**rivt** is a lightweight markup language for writing, organizing and
sharing engineering documents and reports. It is designed to be legible,
flexible and efficient. **rivt** is also the name of an open source framework
used for producing rivt documents.

**rivtlib** is a Python library that processes rivt files and is distributed
under the open source MIT license. It runs on platforms that support Python
3.11 or later and works within a framework of five established, open souce
technologies:

- Language: Python with open source libraries including **rivtlib**
- IDE: VSCode and extensions
- Typesetting: Latex TexLive Distribution
- Diagrams: QCAD
- Version control: GitHub

The **rivt** framework can be downloaded as a portable Windows zip file or
installed through OS specific shell scripts (https://rivtcode.net). It is also
available as an online service at https://rivtonline.net.

A rivt document (doc) is a text, HTML or PDF ouput file from a processed rivt
file. A rivt report (report) is an organized collection of rivt docs.
**rivtlib** organizes and generates both large reports and single file docs.

A rivt file is a Python file that imports **rivtlib** 

**import rivtlib.rivtapi as rv**

which exposes 6 API functions and **rS** is a triple quoted rivt-string

::

rv.R(rS) - (Run) Run shell scripts 
rv.I(rS) - (Insert) Insert static text, images, tables and math equations 
rv.V(rS) - (Values) Evaluate tables, values and equations 
rv.T(rS) - (Tools) Execute Python functions
rv.X(rS) - (eXclude) Skip rivt-string processing 
rv.W(rS) - (Write) Write formatted rivt documents 


'''
