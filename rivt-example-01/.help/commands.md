
Commands read and format files

(ctrl+click (#links))

API Scope           Command                                                
========= ====================================================================== 
rv.R       | COPY |  abs src path | abs dest path | file pattern [](#COPY)
rv.R       | SHELL |  abs path | os, wait                        [](#SHELL)
rv.I, V    | TEXT |  rel path | type                             [](#TEXT)      
rv.I, V    | TABLE |  rel path | title,width,head;nohead,num;non       
rv.I, V    | IMAGE |  rel path | caption, scale, num;non, time;not     
rv.I, V    | IMAGE2 |  rel path1, rel path2 | c1,c2,s1,s2,n1,n2        
rv.V       | PYTHON |  rel path | rivt;namespace                       
rv.V       | VALTABLE |  rel path | title, width, num;non              
rv.V       | FUNCTION |  function, arg, var, type | label               
rv.D       | ATTACHPDF |  rel path | front;back, title                 
rv.D       | PUBLISH |  doc title | type                               
========= ====================================================================== 

Parent paths for commands

================ =========================== ======
   Command           Parent Path [1]          R/W
================ =========================== ======
| COPY |                os root                R
| SHELL |               os root                R
| IMAGE |            rivt-report/              R
| IMAGE2 |           rivt-report/              R
| TABLE |            rivt-report/              R
| VALTABLE |         rivt-report/  [2,3]       R
| TEXT |             rivt-report/  [4]         R
| PYTHON |           rivt-report/              R
| ATTACHPDF |        rivt-report/              R
| PUBLISH |          _published/   [5]         W
================ =========================== ======

[1] relative file paths in commands generally begin with rvsrc/ 
[2] authored values are read from rvsrc/subdirectories
[3] values written by rivt may be read from rv_stor/vals  
[4] sections stored by rivt may be read from rv_stor/sect  
[5] docs are written to subdirectories of _published


#SHELL
-------------------------------------------

The SHELL command runs shell scripts including .cmd, .bat and .sh files. The
*os* parameter specifies the operating system: *win*, *mac* or *linux*. The
*wait; nowait* specifies whether rivt file processing waits for the script to
complete before continuing.

If the *doc* is part of a report and no path is specified, the file is assumed to
be in the default folder */src/run/* . Otherwise the path is specified relative
to the report root (rivt file folder). If the doc is a single doc the file is
read from the rivt file folder.

.. code-block:: text

    Syntax:
        | SHELL | relative file path | file name

    Example:
        | SHELL | rvsrc | sap.cmd

=========== ==========================
API Scope     rv.R
File Types    .cmd, .bat, .sh, .bsh 
Doc Types     text, PDF, HTML
=========== ==========================

.. _Text file:

#TEXT
------------------------------------------

The TEXT command reads and formats text and code files. The language parameter
specifies formatting and syntax coloring.  Language types include:

Inserts formatted text from file into doc. 

- *literal*
- *python*
- *topic*
- *bold*
- *italic*

The *literal* type inserts text into the *doc* without formatting. Paths are
relative to the rivit-report the report root (rivt file folder). If the doc is
a single doc the file is read from the rivt file folder.

.. topic:: | TEXT |

    .. code-block:: text

        Syntax:
            | MARKUP | relative path | type
        Example:
            | MARKUP | rvsrc/quote.txt | literal

=========== =====================================
API Scope     rv.I, rv.V
File Types    txt, py 
Doc Types     text, PDF, HTML
=========== =====================================

.. _Table file:

#TABLE
------------------------------------------

The TABLE command reads csv, xls, and rst files and outputs formatted tables.
The title may be ommited by inserting a hyphen "-". The width parameter
specifies the maximum character width of a column. The align parameter
specifies the cell justification - left, center, right. The number parameter
specifies whether the table is numbered. For csv files, the head parameter
specifies whether the first row is a column header.

If a *doc* is part of a report and no path is specified, the file is assumed to
be in the default folder */src/data/* . Otherwise the path needs to be specified
relative to the report root (rivt file folder). If the doc is a 
single doc the file is read from the rivt file folder.

.. topic:: | TABLE |   

    .. code-block:: text

        Syntax:
            | TABLE | rel path | title, max width, rows, l;c;r, head;nohead, num;nonum 

        Example:
            | TABLE | file1.csv | Forces, 30, 0:0, c, nohead, num 

=========== ==========================
API Scope     rv.I, rv.V
File Types    csv, xls, rst
Doc Types     text, PDF, HTML
=========== ==========================

.. _Image file:

Image file
-------------------------------------------

The IMAGE command reads a PNG or JPEG file and centers it in the *doc*. The
scale parameter is a decimal fraction of the page width. The caption may be
ommited by using a single hyphen. The *num;nonum* parameter specifies whether
to assign a figure number. The image path is inserted in the text *doc* instead
of the image.

If a *doc* is part of a report and no path is specified, the file is assumed to
be in the default folder */src/img/* . Otherwise the path needs to be specified
relative to the report root (rivt file folder). If the doc is a single doc 
the file is read from the rivt file folder.

.. code-block:: text

    Syntax:
        | IMAGE | relative path | caption, scale, num;nonum

    Example:
        | IMAGE | file1.png | Map, 0.5, num

=========== ==========================
API Scope     rv.V, rv.I
File Types    PNG, JPG 
Doc Types     PDF, HTML
=========== ==========================

.. _Adjacent images:

Adjacent images
--------------------------------------------------

 

The IMAGE2 command reads two PNG or JPEG file and places them side by side in
the *doc*. The scale parameters are a decimal fraction of the page width. The
captions may be ommited by using a single hyphen for either or both images. The
*fig;nofig* parameters specify whether to assign a figure number to either or
both images. The image path is inserted in the text *doc* instead
of the image.

If a *doc* is part of a report and no path is specified, the file is assumed to
be in the default folder */src/img/* . Otherwise the path needs to be specified
relative to the report root (rivt file folder). If the doc is a 
single doc the file is read from the rivt file folder.

.. code-block:: text

    Syntax:
        | IMAGE2 | relative path | cap1, cap2, scale1, scale2, num;nonum, num;nonum

    Example:
        | IMAGE2 | file1.png, file2.png | Map, Photo, .5,.5, num, num

=========== ==========================
API Scope     rv.I, rv.V
File Types    PNG, JPG jenn
Doc Types     PDF, HTML
=========== ==========================

.. _Values file:

Valtable file
------------------------------------------------

 

The VALTABLE command imports and defines values from a *csv* or *xls* file. 
The file format is:: 

    var = value, unit1, unit2, decimal, label

The path variable is either from *src* or *stored* depending on if the values
were generated by rivtlib or provided by the author. The title parameter is the
table title. A hyphen omits the title. The *rows* parameter specifies the rows
to import. The *num; nonum* parameter specifies whether to assign a table
number to the values table.

If a *doc* is part of a report and no path is specified, the file is assumed to
be in the default folder */src/vals/* . Otherwise the path needs to be
specified relative to the report root (rivt file folder). If the values are
read from prior calculated values, they will be found in the */stored/vals*
folder. If the doc is a single doc the file is read from the rivt file
folder.

.. code-block:: text

    Syntax:
        | VALTABLE | relative path | title, rows, *num;nonum*

    Example:
        If read from the default folder:
        | VALTABLE | newvals.csv | Beam Properties, 1:10, num
        If read from the stored folder:
        | VALTABLE | /stored/vals/vA01-2.csv | Beam Properties, 1-10, num

=========== ==========================
API Scope     rv.V
File Types    .csv, .xls, 
Doc Types     text, PDF, HTML
=========== ==========================


.. _Python file:

Python file
-------------------------------------------

 

Executes Python code in the *rivt namespace* or user specified namespace. File
paths used in the script are relative to the root *rivt* folder.

.. code-block:: text

    Syntax:
        | PYTHON | relative path | *rvspace*; user space

    Example:
        | PYTHON | script1.py | rv-space

=========== ==========================
API Scope     rv.V, rv.T
File Types    .csv
Doc Types     text, PDF, HTML
=========== ==========================


.. _Function value:

Function
-------------------------------------------

Executes Python functions imported by the PYTHON command. 
Function args are defined and named by the [[ARG]] block. 

.. code-block:: text

    Syntax:
        | FUNCTION | func name, args, return var, type | label

    Example:
        | FUNCTION | bending1, beamprops, result1, str | beam design

=========== ==========================
API Scope     rv.V
File Types    .py
Doc Types     text, PDF, HTML
=========== ==========================


.. _Copy file:

#COPY
-------------------------------------------

Copy files using absolute paths. -rvsrc- is an alias for the rvsrc folder.
OS alias may also be used e.g. %USERPROFILE% on Windows.

.. code-block:: text

    Syntax:
        | COPY | abs src path | abs dest path | file name and wildcards
    Example:
        | COPY | -rvsrc-/scripts | %USERPROFILE%/venv1

=========== ==========================
API Scope     Tools
File Types    *.*
Doc Types     text, PDF, HTML
=========== ==========================


.. _Attach PDF:

Attach PDF
-------------------------------------------

Appends or prepends a PDF file to the *doc*. The title parameter generates an
Appendix cover page with the specified title. A "-" omits the over page. For
HTML *docs* the file is inserted as a donwload link.

.. topic:: | ATTACHPDF |

    .. code-block:: text

        Syntax:
            | ATTACHPDF | relative path | *front;back*, title
  
        Example:
            | ATTACHPDF | relative path | *front;back*, title


=========== ==========================
API Scope     rv.D
File Types    tex, html, text, pdf
Doc Types     text, PDF, HTML
=========== ==========================

.. _Publish doc:

Publish doc
-------------------------------------------

 

Publishes a *doc*. 

    Syntax:
        | PUBLISH | ini relative path | rst2pdf, texpdf, tex, hmtl

    Example:
        | PUBLISH | ini relative path | rst2pdf

=========== ==========================
API Scope     rv.D
File Types    tex, html, text, pdf
Doc Types     text, PDF, HTML
=========== ==========================

