rivtlib
========

**rivtlib is alpha software. Some features are not complete and the program has
bugs.**

*rivt* is an extensible, open source tool for writing and sharing engineering
documents. This has always been a challenge because engineering documents are
complex. They may include text, images, tables, calculations, models and
computer code. 

A *rivt file* is a Python file (.py) that imports the *rivtlib* Python package
and includes *rivt markup*. *Markup* publishes the file as a 
**text, PDF or HTML doc** that can be assembled and 
linked, with other *docs*, into a *rivt report*.

The primary use case for *rivt* is producing clear, acurate engineering
documents that are: 

#. Easier to write and format than LaTeX, Excel, Word or other general purpose word processors.

#. Do not need to be formatted to the precise standards of a formal journal publication.

A second use case is when documents may need to be produced in a variety of
formats from the same input file. For futher details please refer to the 
`rivt user manual <https://rivt.info>`__.

Use Cases
-----------

In addition to publishing engineering documents for:

#. internal communication.
#. research documentation.
#. government permits.
#. technical reports.
#. funding applications.
#. teaching.
#. presentations.

*rivt* can: 

#. function as a front and back end for external software. 
#. be used for real time collaboration.

The table below compares limitations between different software
programs. *rivt* is designed to address these limitations and serve as a
complement or replacement to existing software.


Software Comparison
--------------------

============ ========= ======== ======== ========= ========= ============= 
Program      Rep [1]_  Ver [2]_ Txt [3]_ Comp [4]_  CP [5]_   Collab [6]_  
============ ========= ======== ======== ========= ========= ============= 
Matlab         no       no         no      no          no       no   
Mathcad        no       no         no      no          no       no   
Mathematica    no       no         no      no          no       no   
Cloud SaaS    limited   no         no      no          yes      limited  
Excel         limited   no         no      yes         no       yes 
Jupyter        no       no         no      yes         yes      yes  
**rivt**      **yes**  **yes**   **yes**  **yes**   **yes**    **yes**
============ ========= ======== ======== ========= ========= ============= 


.. [1] Report generation
.. [2] Native version control
.. [3] Plain text, readable input files
.. [4] Forward and backward compatibility
.. [5] Cross-platform
.. [6] Collaboration support