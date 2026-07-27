#! python3
""" This is a rivt doc example used in the tutorial at https://www.rivt.info. 

This example illustrates: 

    rivtlib markup

    - multiple API sections
    - footnotes
    - inline comments
    - Url links
    - Variable definitions
    - Table blocks and commands
    - Value table command
    - Metadata and layout block
    - Python function assignment
    - Image command
    - Publish command

    VSCode / Python features
    - cell labels
    - docstrings
    - extension modules    

"""

import rivtlib.rvapi as rv

# rv set_width = 80  ; character width of text output (80)
# rv no_tag = true ; if false, the API type is added to section number (true)
# rv private = true ; if false, default section heading changed to public (private)

# %% rv.I("""Summary and Loads
rv.I("""Summary and Loads

    This rivt file example calculates the maximum stress and deflection in a
    simply supported, uniformly loaded beam using E-B theory _[#]. It also
    serves as an annotated example of a single rivt doc with multiple sections
    that is not part of a report.

    The example illustrates the use of some of the most common API functions,
    commands and tags. Further details are provided in the 
    _[U] rivt user manual, https://www.rivt.info |.
    
    The file may be formatted as a text, PDF or HTML doc by changing the type
    parameter in the Doc API | PUBLISH | command at the end of each 
    rivt file (*rv.D()*). Published files are found in the 
    _published folder.
""")

# %% rv.I("""Load Combinations 
rv.I("""Load Combinations 

    ## Indented comments with double hashes will not appear in the doc
      
    Dead and live loads effects are taken from ASCE 7-05 _[#]

    _[[TABLE]]  Load Effects 
    ============= ================================================
    Equation No.    Load Combination
    ============= ================================================
    16-1           1.4(D+F)
    16-2           1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R)
    16-3           1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W)
    ============= ================================================
    _[[END]]
""")

# %% rv.V("""Loads and Geometry
rv.V("""Loads and Geometry 
    
    Successive value definitions are formatted as a table. Variable values are
    defined with the define operator. The line tag [T] labels and numbers the
    table.
    
    Define Unit Loads _[T]
    D_1 ==: 3.8 * p_sf | p_sf, kPA, 2 | joists DL         
    D_2 ==: 2.1 * p_sf | p_sf, kPA, 2 | plywood DL          
    D_3 ==: 10.0 * p_sf | p_sf, kPA, 2 | partitions DL       
    D_4 ==: 2 * 1.5 * k_ft | k_ft, kN_m, 2 | fixed machinery DL
    L_1 ==: 40 * p_sf | p_sf, kPA, 2 | ASCE7-O5 LL
    b_1 ==: 10 * inch | inch, mm, 2 | beam width
    h_1 ==: 18 * inch | inch, mm, 2 | beam depth
    E_1 ==: 29000 * k_si | k_si, MPA, 2 | modulus of elasticity
    Fb_1 ==: 20000 * p_si | p_si, MPA, 2 | allowable stress   
    
    The VALTABLE command reads variable values from a file in the rvsrc/data
    folder. The description is the table title, followed by the max
    column width. 

    | VALTABLE | beam1.csv | Beam Geometry, 40

    | IMAGE | beam1.png | Beam Diagram, 60, num, not

    Uniform Distributed Loads _[C]
    dl_1 <=: 1.2 * (spc_1 * (D_1 + D_2 + D_3) + D_4) | k_ft, kN_m, 2 | Dead load [ASCE7-05 2.3.2]

    ll_1 <=: 1.6 * spc_1 * L_1 | k_ft, kN_m, 2 | Live load [ASCE7-05 2.3.2]
    
    omega_1 <=: dl_1 + ll_1 | k_ft, kN_m, 2 | Total load [ASCE7-05 2.3.2]
    """)

# %% rv.V("""Beam Stress
rv.V("""Beam Response

    The following lines import the beam geometry from an external file, 
    calculate section properties from imported functions and calculate 
    the maximum moment, bending stress and mid-span deflection. 

    | PYTHON | sectprop.py | Beam functions

    section_1 :=: rectsect(b_1, h_1) | in3, cm3, 2 | rectangle - S (sectprop.py)

    inertia_1 :=: rectinertia(b_1, h_1) | in4, cm4, 1 | rectangle - I (sectprop.py)

    | IMAGE2 | ss-beam2.png, ss-beam1.png | Moment diagram, Deflection diagram,46,54,num,num

    Maximum bending stress formula _[B]
    
    ##  The line tag [M] formats the equation using utf-8 text.
    σ1 = M1 / S1 _[M]  
        
    m_1 <=: omega_1 * spn_1**2 / 8 | ftkips, mkN, 2 | Mid-span UDL moment 
    
    fb_1 <=: m_1 / section_1 | p_si, MPA, 1 | Bending stress 

    fb_1 < Fb_1 | k_si, 2, OK, >>> NOT OK | Stress ratio 

    delta_1 :=: midspan_delta(spn_1, omega_1, E_1, inertia_1) | inch, mm, 2 | mid-span deflection (sectprop.py)
        
    _[[ENDNOTES]]
    "Euler–Bernoulli beam theory", Wikipedia, Wikimedia Foundation. [Online].
    https://en.wikipedia.org/wiki/Euler_Bernoulli_beam_theory. 
    [Accessed: Jun. 15, 2026].

    ASCE/SEI 7-05, Minimum Design Loads for Buildings and Other Structures,
    American Society of Civil Engineers, 2005.
    _[[END]]]
    """)


# %% rv.D("""Publish Doc 
rv.D("""Publish Doc 
    
    A rivt file may be published as a text, PDF or HTML doc by specifying the
    PUBLISH type parameter as txt, pdf or html. 
    
    Published files are found in sub-folders of the _published folder. A text
    version of the doc or report is is always written to the rivt and
    _rivt-public folders as a README.txt file. READMEs are formatted and
    displayed on the first page of a GitHub repo.
    
    | PUBLISH | Example 1 - rivt Doc | txt
    
    _[[METADATA]] 
    [doc]
    ;-----------------------------------------
    authors = R Holland
    version = 1.0.0a17
    repo = https://github.com/rivt-info/rivt-example-01
    license = https://opensource.org/license/mit/
    copyright = --
    fork1_authors = --
    fork1_version = --
    fork1_repo = --
    fork1_license = https://opensource.org/license/mit/
    [layout]
    ;----------------------- cover page and runner settings
    ;--- add logo files to rvsrc/img folder, size is % page width
    subtitle =  UDL Beam
    copyright = --
    client = user example
    coverpage = true
    coverlogo_size = 30
    coverlogo = logo1.png
    runninglogo = logo2.png
    runninglabel = rivt
    project_ref = proj. 0001
    ;------------------------ PDF settings
    ;--- colors: red, blue, green, black, gray, brown, maroon, gray, olive, cyan
    pdf_link_color = brown
    pdf_link_underline = false
    pdf_pagesize = letter ; letter, legal, A4    
    pdf_margins = 1in, 1in, 1in, 1in ; top, right, bottom, left
    pdf_page = false ; if true, start sections on new page 
    ;----------------------- TOC levels
    ;--- 1: include subdivisions   2: include subdivisions and sections
    toc_level = 2
    [process]
    ;-----------------------------------------
    doc_verbose = true; if false minmize output during doc processing
    auto_cfg = true ; if false, config files are not updated from rivt file
    _[[END]]    
    """)

