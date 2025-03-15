"""
template 1 for rivt docs and reports

Args:
    cover(str,str) : restructured text cover page string
    content(str) : restructured text table of contents string
    mainPageS() : restructured text contents string 
    imgS(str) : cover page image in ../../docs/_styles/
    
"""


def cover(covtitleS, covsubS, covbottomS, imgS):

    fS = """



|
|


.. class:: title

   **""" + covtitleS + """**

   
.. class:: center

   **""" + covsubS + """**

   
|
|
|
|


.. image::  ../../docs/_styles/""" + imgS + """
   :width: 30%
   :align: center

|
|
|
|
|
|

|


.. class:: bottom

   **""" + covbottomS + """**

   
"""
    return fS


def content(covtitleS):

    fS = """

.. raw:: pdf

   PageBreak mainPage

.. class:: title


   """ + covtitleS + """


.. contents:: Contents 


"""
    return fS


def mainpage():

    fS = """

.. raw:: pdf

   PageBreak mainPage

   
"""
    return fS
