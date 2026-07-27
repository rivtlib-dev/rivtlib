
**Format line of text**

(ctrl+click (#links))

========== ==================================================== 
API Scope             Line Tag                                  
========== ==================================================== 
rv.I                   text \*word word\* text                  
rv.I                   text \*\*word word\*\* text              
rv.I                   text **_[D] label, filename |** text     
rv.I                   text **_[G] glossary term |** text       
rv.I                   text **_[S] label, section |** text      
rv.I                   text **_[U] label, url |** text          
rv.I,V                 text **_[#]** text                       
rv.I,V                 text **_[R]**                            
rv.I,V                 text **_[B]**                            
rv.I,V                 text **_[C]**                            
rv.I,V                **title _[T]**                            
rv.I,V            **text math _[M]** description                
rv.I,V           **LaTeX math _[L]** description                
rv.I,V                 text **_[V] var_name |** text            
all                     **##** text                             
========== ==================================================== 

..  _Bold center text:

**[2]** Bold center text
-------------------------------------------

Center line of text within the page margins.

.. topic:: _[C]
    
    .. code-block:: text

        Syntax:
            text _[C]

        Example:
            This text wil be centered. _[C]

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================

-------------------------------

..  _Bold text:

**[2]** Bold text
-------------------------------------------

Bold line of text.

.. topic:: _[C]
    
    .. code-block:: text

        Syntax:
            text _[B]

        Example:
            This line of text wil be bold. _[B]

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================

..  _Right justify:

**[2]** Right justify text
-------------------------------------------

Right justify line of text within the page margins.

.. topic:: _[R]
    
    .. code-block:: text

        Syntax:
            text _[C]

        Example:
            This text wil be right justified. _[R]

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================

-------------------------------

..  _Download link:

**[3]** Download link
-------------------------------------------

Insert a download link.

.. topic:: _[D]
    
    .. code-block:: text

        Syntax:
            text _[D] label, filename | text

        Example:
            This is a link to _[D] my file, my_file.pdf | for download.

=========== ==========================
API Scope     Insert
Doc Types     text, PDF, HTML
=========== ==========================


-------------------------------

.. _Text math:

**[4]** Text math
-----------------------------------------

Format math expression into text.

.. topic:: _[M]

    .. code-block:: text

        Syntax:
            text math expression  _[M]

        Example:
            f(x,y) = sin(x)**2 + y/5 _[M]

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================

-------------------------------

.. _LaTeX math:

**[5]** LaTeX math 
-----------------------------------------

Format LaTeX math expression.

.. topic:: _[L]

    .. code-block:: text

        Syntax:
            LaTeX math expression  _[L]

        Example:
            \frac{1}{\sqrt{x}} _[L]

=========== ==========================
API Scope     Insert, Values
Doc Types     PDF, HTML
=========== ==========================


-------------------------------

..  _Endnote number:

**[6]**  Endnote number
-------------------------------------

Assign endnote number to the text in order of processing. Endnotes
are defined with the block tag _[[ENDNOTE]] and are listed at the end of the
*doc*. 
    
.. topic:: _[#] 

    .. code-block:: text

        Syntax:
            text _[#] more text

        Example:
            This is a sentence with an endnote _[#] tag.

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================


-------------------------------

.. _Term link:

**[7]** Glossary link
------------------------------------------

Link a term to the glossary.

.. topic:: _[G] 

    .. code-block:: text

        Syntax:
            text _[G] glossary term

        Example:
            A definition of _[G] namespace
            is provided in the glossary.

=========== ==========================
API Scope     Insert, Values
Doc Types     PDF, HTML
=========== ==========================


-------------------------------

.. _Section link:

**[8]** Section link
-----------------------------------------

Create a link to the section label defined in the API header with optional
link text. If the text is ommitted the section label is used for the link.

.. topic:: _[S]

        .. code-block:: text

        Syntax:
            text _[S] link text, section title |

        Example:
            This creates a link to _[S] Section Title, actual section label
            which provides more detail.

=========== ==========================
API Scope     Insert, Values
Doc Types     PDF, HTML
=========== ==========================


-------------------------------

.. _URL link:

**[9]** URL link
-----------------------------------------

Link to a an external site with optional link text. If the link text is 
ommitted the url will be inserted as the link term.

.. topic::  _[U] 

    .. code-block:: text

        Syntax:
            text _[U] link label,external url |

        Example:
            text _[U]  github, https://www.github.com 

   
=========== ==========================
API Scope     Insert, Values
Doc Types     PDF, HTML
=========== ==========================


-------------------------------


.. _Substitute value:

**[10]** Substitute value
------------------------------------------

Insert the value of  _[V] var_name | in the line.

.. topic:: _[V]

    .. code-block:: text

        Syntax:
            text _[V] var_name | more text

        Example:
            The value of my_var is _[V] is my_var|.
            The value of my_var is 5.

=========== ==========================
API Scope     Insert, Values
Doc Types     text, PDF, HTML
=========== ==========================


-------------------------------

.. _Number table:

**[11]** Table number
------------------------------------------

    Label and number tables.

.. topic:: _[T]

    .. code-block:: text

        Syntax:
            Table Title  _[T]

        Example:
            A New Table _[T]


=========== ==========================
API Scope     Insert
Doc Types     text, PDF, HTML
=========== ==========================

