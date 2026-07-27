#! python
# %% import
import rivtlib.rvapi as rv

# rv setpublic: False

# %% rv.I("""Summary
rv.I("""Summary  
    
    This rivt example calculates the maximum stress and deflection in a simply
    supported, uniformly loaded beam. It also serves as an annotated example of
    a *single doc* with multiple sections (a *single doc* does not use the
    report generating script).
    
    The example illustrates the use of some of the most common API functions,
    commands and tags. Further details are provided in the _[U] rivt user manual,
    https://www.rivt.info|.

    The file may be formatted as a text, PDF or HTML doc by changing the type
    parameter in the *| PUBLISH |* command of the *Doc API (rv.D)* at the end
    of the file. Published files are found in the respective sub-folders of the
    *_published* folder.
    
    """)

# %% rv.I("""Load Combinations
rv.I("""Load Combinations 

    This is an inline table using the restructured text syntax. The line tag
    *[T]* numbers the table.

    ASCE 7-05 Load Effects _[T]
    ============= ================================================
    Equation No.    Load Combination
    ============= ================================================
    16-1           1.4(D+F)
    16-2           1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R)
    16-3           1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W)
    ============= ================================================

    When an inline table is in a *[[TABLE]]* block it produces the same output
    as above, and also writes the table to a CSV file in the *_stored* folder.

    _[[TABLE]]  ASCE 7-05 Load Effects(2)
    ============= ================================================
    Equation No.    Load Combination
    ============= ================================================
    16-1           1.4(D+F)
    16-2           1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R)
    16-3           1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W)
    ============= ================================================
    _[[END]]

    The *| IMAGE |* command inserts an image file with caption, scale (as
    percentage) and numbered options.

    | IMAGE | beam1.png | Beam Geometry, 50, nonum

    The line  tag *[E]* right justifies the label and adds an equation number.

    Bending Stress _[E]

    The line tag *[M]* formats the equation using utf-8 text.

    σ1 = M1 / S1 _[M]
    """)

# %% rv.V("""Loads and Geometry
rv.V("""Loads and Geometry 
    
    Variable values are defined with the define operator.  Successive lines of 
    value definiiions are formatted as a table. The line tag *[T]* numbers
    the table.
    
    Unit Loads _[T]
    D_1 ==: 3.8*psf | psf, kPA, 2 | joists DL         
    D_2 ==: 2.1*psf | psf, kPA, 2 | plywood DL          
    D_3 ==: 10.0*psf | psf, kPA, 2 | partitions DL       
    D_4 ==: 2*0.5*klf |klf, kN_m, 2 | fixed machinery  DL
    L_1 ==: 40*psf | psf, kPA, 2 | ASCE7-O5 LL 
    
    The *| VALTABLE |* command reads variable values from the file in the
    SrC/Vals folder. The text is used as the table title. The range specifies
    the starting and ending line to be read from the file (0:0 means all lines). 
    The *num;nonum* parameter specifies whether theimported table is numbered.

    | VALTABLE | beam1.csv | Beam Geometry, 0:0

    Uniform Distributed Loads
    dl_1 <=: 1.2 * (W_1 * (D_1 + D_2 + D_3) + D_4) | klf, kN_m, 2 | dead load : ASCE7-05 2.3.2

    ll_1 <=: 1.6 * W_1 * L_1 | klf, kN_m, 2 | live load : ASCE7-05 2.3.2
    
    omega_1 <=: dl_1 + ll_1 | klf, kN_m, 2 | total load : ASCE7-05 2.3.2
    """)

# %% rv.V("""Beam Stress
rv.V("""Beam Stress
    **Section Properties**

    ## indented comments with double hashes will not appear in the doc

    | PYTHON | sectprop.py | nodoc

    yy = 10*inch

    section_1 :=: rectsect(yy, 18*inch) | in3, cm3, 2 | S-rectangle

    inertia_1 :=: rectinertia(10*inch, 18*inch) | in4, cm4, 1 | I-rectangle

    **Bending Stress**

    m_1 <=: omega_1 * S_1**2 / 8 | ftkips, mkN, 2 | mid-span UDL moment _[E]

    fb_1 <=: m_1 / section_1 | lb_in2, MPA, 1 | bending stress _[E]

    fb_1 < 20000*lb_in2 | ksi, 2, >>> OK, >>> NOT OK | stress ratio _[E]
    """)


rv.V("""Beam deflection  

    text
    """)

# %% rv.D("""Publish Doc
rv.D("""Publish Doc 
    
    _[[METADATA]] 
    [doc]
    authors = rholland
    version = 0.8.1
    repo = https://github.com/rivt-info/rivt-single-doc
    license = https://opensource.org/license/mit/
    fork1_authors = _authors_
    fork1_version = _version_
    fork1_repo = _repo_
    fork1_license = https://opensource.org/license/mit/
    
    [layout]
    logoname = logo.png
    pdf_footer = docname, author1;author2, date, time, version
    pdf_pagesize = letter
    pdf_margins = 1in, 1in, 1in, 1in
    pdf_header = totalpages
    pdf_cover = cover.rst
    text_width=80    
    _[[END]]
    
    | PUBLISH | Single Doc Example 1 | pdf
    """)
