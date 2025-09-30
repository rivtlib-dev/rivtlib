"""
rivLib
=======

*rivLib* is a Python library for writing and sharing engineering documents. It
outputs *rivt docs* and *reports* from a *rivt file*.  A rivt file is a Python
file (*.py) that imports *rivLib*::

    import rivLib.rivtapi as rv

and exposes 8 API functions::

    rv.R(rS) - (Run) Run shell scripts
    rv.I(rS) - (Insert) Insert text, images, tables and math equations
    rv.V(rS) - (Values) Evaluate tables, values and equations
    rv.T(rS) - (Tools) Execute Python functions
    rv.D(rS) - (Docs) Write formatted document files
    rv.M(rS) - (Meta) Meta data for rivt file
    rv.S(rS) - (Skip) Skip rivt-string processing
    rv.Q(rS) - (Quit) Exit processing of rivt file

where **rS** is a triple quoted rivt string that uses *rivt markup* - a
lightweight markup language that wraps *restructuredtext*. *rivt docs* and
*reports* may be output as text, PDF or HTML files from the same *rivt file*.

A *rivt file* may be run from the command line as::

    python rvddss-filename.py

where *rvddss-* is the doc number and *dd* and *ss* are integers identifying the
report division and subdivision respectively.
See the `rivt User Manual <https://rivt.info>`_ for details.

The rivLib code base uses a last-letter naming convention to indicate variable
types where:

A = array
B = boolean
C = class instance
D = dictionary
F = float
I = integer
L = list
N = file name
P = path
S = string

"""
