"""
rivtlib
=======

**rivtlib** is a Python library that produces rivt docs and reports. **rivt**
is a lightweight markup language used by **rivtlib** for writing engineering
documents. It wraps parts of the restructuredtext markup language. **rivt** is
designed to make it easy to share and reuse engineering document templates.

A rivt file is a Python file (*.py) that imports **rivtlib**::

    **import rivtlib.rivtapi as rv**


and exposes 6 functions::


    rv.R(rS) - (Run) Run shell scripts
    rv.I(rS) - (Insert) Insert text, images, tables and math equations
    rv.V(rS) - (Values) Evaluate tables, values and equations
    rv.T(rS) - (Tools) Execute Python functions
    rv.D(rS) - (Docs) Write formatted document files
    rv.S(rS) - (Skip) Skip rivt-string processing
    rv.Q(rS) - (Quit) Exit processing of rivt file


where **rS** is a triple quoted string.

"""
