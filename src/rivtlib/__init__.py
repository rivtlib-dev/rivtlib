"""
rivtlib
=======

*rivtlib* is a Python library for writing and sharing engineering documents. It
outputs *rivt docs* and *reports* from a *rivt file*.  A rivt file is a Python
file (*.py) that imports *rivtlib*::

rivt API

usage:
    import rivtlib.rvapi as rv

API functions:
    rv.R(rS) - (Run) Execute shell scripts
    rv.I(rS) - (Insert) Insert static text, math, images and tables
    rv.V(rS) - (Values) Evaluate values and equations
    rv.T(rS) - (Tools) Execute Python scripts
    rv.D(rS) - (Docs) Publish formatted doc file
    rv.S(rS) - (Skip) Skip processing of section
    rv.X(rS) - (Exit) Exit processing of rivt file

where the argument rS is a triple quoted utf-8 string (rivt string)

where **rS** is a triple quoted rivt string that uses *rivt markup* - a
lightweight markup language that wraps *restructuredtext*. *rivt docs* and
*reports* may be output as text, PDF or HTML files from the same *rivt file*.

A *rivt file* may be run from the command line as::

    python rvddss-filename.py

where *rvddss-* is the doc number and *dd* and *ss* are integers identifying the
report division and subdivision respectively.
See the `rivt User Manual <https://rivt.info>`_ for details.

"""
