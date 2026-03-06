rivtlib
========

**rivtlib is alpha software. Some features are not complete and the program has
a number of bugs.**

rivt is an open source software project that simplifies sharing and reuse of
engineering documents. This has always been a challenge because engineering
documents typically include text, images, tables, calculations, models
and computer code, which adds to complexity when assembling documents and 
reports.

The primary use case for rivt is producing engineering documents that lie
somewhere between back of envelope notes and calculations, and formal journal
publications. In other words, it produces formatted, organized documents that
are easy to edit.

The second use case is when flexibilty is needed to produce documents in a
variety of formats including text, PDF or HTML. A *rivt file* publishes a
*rivt doc* as a text, PDF or HTML file. A *rivt file* is a Python file
(.py) that imports the *rivtlib* Python package and includes rivt markup. A
collection of *rivt docs* may be linked and collated as a *rivt report*. The
*rivt user manual* is `here <https://rivt.info>`__.

Use Cases
-----------

*rivt files* can function as a front and back end for:

#. software control
#. visualization
#. instrumentation

*rivt docs* can be used for:

#. internal communication
#. research documentation
#. government permits
#. technical reports
#. funding applications

*rivt* is compatible with collaborative tools and may be used for:

#. teaching
#. presentations
#. real time collaboration

The table below summarizes and compares limitations between different software
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