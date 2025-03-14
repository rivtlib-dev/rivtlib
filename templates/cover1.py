"""
template 1 for rivt docs and reports

Params:
    coverS : restructured text cover page string
    contentS : restructured text table of contents string
    mainPageS : restructured text contents string 
    imgS : cover page image in ../../docs/_styles/
    
"""

imgS = "rivt01.png"
covertitleS = "a"
coversubtitle = "b"


# cover template
coverS = """

.. class:: center


|
|

""" + covertitleS + """
########################

|
|
|

   **""" + coversubtitle + """**
   
|
|
|
|
|
|
|


.. image:: """ + "../../docs/_styles/" + imgS + """
   :width: 30%
   :align: center

   
"""

# toc template
contentS = """

.. raw:: pdf

   PageBreak mainPage


.. contents::   My Document Title 


"""

# pages template
mainpageS = """

.. raw:: pdf

   PageBreak mainPage

   
"""
