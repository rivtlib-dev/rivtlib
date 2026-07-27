
**Format or run blocks of text or scripts**

(ctrl+click (#links))

=========== ==================================================
API Scope         Block Tag                    
=========== ==================================================
rv.I,V       _[[TEXT]] type]         [](#Text-Block)                   
rv.I,V       _[[TABLE]] label        [](#Table-Block)                    
rv.V         _[[ARGS]] arg dict name [](#Argument-Block)           
rv.V         _[[PYTHON]] label       [](#Python-Block)              
rv.T         _[[WRITE]] var name                
rv.T         _[[SHELL]] os, wait;nowait
rv.D         _[[METADATA]] label                
all          _[[END]]                           
=========== ==================================================


# Text-Block
---------------------------------------

_[[TEXT]] type

    Inserts formatted text into doc. 

    - text
    - python
    - topic
    - bold
    - italic
    - endnotes

    Syntax:    
        _[[TEXT]] type
        text
        ...
        _[[END]]

    Example:    
        _[[TEXT]] literal
        This is a line of text.
            This is another line indented.
                A third line. 
        This text will be formatted as typed.
        _[[END]]

=========== ==========================
API Scope     Insert, Values
Doc Types     PDF, HTML
=========== ==========================


# Table-Block
------------------------------------------------

_[[TABLE]] label

Reads and formats restructured text table and writes contents
to csv file in the _stored/Vals folder.

        Syntax:
            _[[TABLE]] label
            reST table
            ...
            _[[END]]  
    
        Example:
            _[[TABLE]] my_table
            =====  ======
            Name   Age
            =====  ======
            John   25
            Jane   30
            =====  =====
            _[[END]]

=========== ==========================
API Scope     Insert
Doc Types     text, PDF, HTML
=========== ==========================


# Argument-Block
---------------------------------------

_[[ARGS]] arg_dictionary_name | list of units
    
    Organizes function arguments into a dictionary that may be passed
    to the FUNCTION command.

        Syntax:    
            _[[ARGS]] arg_dictionary_name | list of units
            arg1 = A # label
            arg2 = B # label
            ...
            _[[END]]

        Example:    
            _[[ARGS]] beam1 | units: inch, pounds
            ln_1 = 10*12 # beam length
            P_1 = 1.1*1000 # beam load
            ...
            _[[END]]

=========== ==========================
API Scope     Values
Doc Types     text, PDF, HTML
=========== ==========================


# Python-Block
---------------------------------------

_[[PYTHON]] label
        
Runs a Python script. Results are typically written to the default folder
rv_stor through an alias and then imported as needed using the TEXT 
or IMAGE command.

    Syntax:    
        _[[PYTHON]] label
        code line 1
        code line 2
        ...
        _[[END]]

    Example:    
        _[[PYTHON]] loop
        str1 = ""
        for i in range(10):
            str1+="  " + str(i)
        with open("rv_stor/numbers.txt", "w") as f1:
            f1.write(str1)    
        _[[END]]

=========== ==========================
API Scope     Values
Doc Types     text, PDF, HTML
=========== ==========================


# Write -Block 
------------------------------------------------

_[[WRITE]] rel file path

Updates variables in templates and writes file to report folder. 

        Syntax:    
            _[[WRITE]] relative file path
            text or script
            ...
            _[[END]]

        Example:    
            _[[WRITE]] rvsrc/script.py
            for i in range(2):
                print(f"{vars}",i) 
            _[[END]]

=========== ==========================
API Scope     Tools
Doc Types     text, PDF, HTML
=========== ==========================


# Shell-Block
------------------------------------

_[[SHELL]] win;mac;linux,wait; nowait,open; close

Runs shell scripts that run external programs. The shell parameters include
specifying the operating system, process control and terminal window control.
The os parameter specifies the terminal type. The wait parameter specifies
whether rivt file processing waits for the script to complete before
continuing. The open parameter specifies whether to keep the shell window open
after execution.

        Syntax:
            _[[SHELL]] win;mac;linux,wait; nowait,open; close
            shell command
            ...
            _[[END]]
    
        
        Example:
            _[[SHELL]] win,nowait,open
            dir
            path
            _[[END]]

=========== ==========================
API Scope     Tools
Doc Types     text, PDF, HTML
=========== ==========================


Metadata
-------------------

 
.. topic:: _[[METADATA]]
    
    *Metadata* is written to the *rvAnn-apilog.py* file and is converted
    internally to a Python dictionary rvmetaD with key name taken from the
    label e.g. *docnameS* or *authorsD*.

    ..  code-block:: text

        Synatax - defaults:
            _[[METADATA]] optional label
            docname = ""
            authors = "" 
            version = 0.0.0
            email = ""
            repo = ""
            license = https://opensource.org/license/mit
            fork1 = author, version, email, repo
            fork2 = author, version, email, repo
            _[[END]]

        Example:
            _[[METADATA]]
            docname = Bearing Pressures 
            authors = rholland, rward
            version = 0.1.1
            email = rholland@email.com
            repo = https://github.com/rivt-info/rivt-simple-doc
            license = https://opensource.org/license/mit
            _[[END]]

=========== ==========================
API Scope     Docs
Doc Types     text, PDF, HTML
=========== ==========================


 End block
------------------------------------------------

 

.. topic:: _[[END]] 
    
    Terminates a block tag.

    .. code-block:: text

        Syntax:
            _[[NEWPAGE]] optional label 

        Example:    
            _[[END]] 


=========== ==========================
API Scope     All
Doc Types     text, PDF, HTML
=========== ==========================
