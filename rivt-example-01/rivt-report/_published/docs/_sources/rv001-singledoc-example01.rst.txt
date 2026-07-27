**Example 1 - rivt Doc**
================================================================================


.. raw:: pdf

   PageBreak

      



.. _Summary:

**0.1** | Summary
================================================================================
 
This rivt file example calculates the maximum stress and deflection in a
simply supported, uniformly loaded beam using E-B theory  [1]_ . It also
serves as an annotated example of a single rivt doc with multiple sections
that is not part of a report.
 
The example illustrates the use of some of the most common API functions,
commands and tags. Further details are provided in the 
**<** `rivt user manual <https://www.rivt.info>`__ **>** .
 
The file may be formatted as a text, PDF or HTML doc by changing the type
parameter in the PUBLISH command at the end of each rivt file (Doc-API
rv.D). Published files are found in the _published folder.
 
 


--------------



.. _Load Combinations:

**0.1 - 2** | Load Combinations
--------------------------------------------------------------------------------
 
 
Dead and live loads effects are taken from ASCE 7-05  [2]_ 
 

|

**Table 1**: Load Effects (stored: t001-1.csv) 

============= ================================================ 
Equation No.    Load Combination 
============= ================================================ 
16-1           1.4(D+F) 
16-2           1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R) 
16-3           1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W) 
============= ================================================ 

 
 


--------------



.. _Loads and Geometry:

**0.1 - 3** | Loads and Geometry
--------------------------------------------------------------------------------
 
Successive value definitions are formatted as a table. Variable values are
defined with the define operator. The line tag [T] labels and numbers the
table.
 

**Table 2**: Define Unit Loads


==========  ===============  =============  =====================
variable    value            [value]        description
==========  ===============  =============  =====================
D_1         3.80 psf         0.18 kPA       joists DL
D_2         2.10 psf         0.10 kPA       plywood DL
D_3         10.00 psf        0.48 kPA       partitions DL
D_4         3.00 klf         43.78 kN_m     fixed machinery DL
L_1         40.00 psf        1.92 kPA       ASCE7-O5 LL
b_1         10.00 inch       254.00 mm      beam width
h_1         18.00 inch       457.20 mm      beam depth
E_1         29000.00 ksi     199947.96 MPA  modulus of elasticity
Fb_1        20000.00 lb_in2  137.90 MPA     allowable stress
==========  ===============  =============  =====================
 
The VALTABLE command reads variable values from a file in the rvsrc
folder. The description is the table title, followed by the max
column width. 
 
|

**Table 3**: Beam Geometry (rvsrc/beam1.csv)

==========  ========  =========  =============
variable    value     [value]    description
==========  ========  =========  =============
spc_1       2.00 ft   0.61 m     beam spacing
spn_1       16.00 ft  4.88 m     beam span
==========  ========  =========  =============


 

.. figure:: c:/git/rivt-example-01-git/rivt-report/rvsrc/img/beam1.png
   :width: 60%
   :align: center

   **Fig. 1** - Beam Diagram   
    


 

.. rst-class:: align-center

**Uniform Distributed Loads**



|


**Eq. 1:**  Dead load [ASCE7-05 2.3.2]

.. code-block:: text 

           dl₁ = 1.2⋅(D₄ + spc₁⋅(D₁ + D₂ + D₃))

           dl₁ = 3.64 klf     [dl₁] = 53.09 kN_m   | Dead load [ASCE7-05 2.3.2]

           D₄                  D₂          D₃             spc₁          D₁
           ——————————————————  ——————————  —————————————  ————————————  —————————
           3.00 klf            2.10 psf    10.00 psf      2.00 ft       3.80 psf
           —————               —————       —————          —————         —————
           fixed machinery DL  plywood DL  partitions DL  beam spacing  joists DL
           ——————————————————  ——————————  —————————————  ————————————  —————————


 


|


**Eq. 2:**  Live load [ASCE7-05 2.3.2]

.. code-block:: text 

           ll₁ = 1.6⋅L₁⋅spc₁

           ll₁ = 0.13 klf     [ll₁] = 1.87 kN_m   | Live load [ASCE7-05 2.3.2]

           L₁           spc₁
           ———————————  ————————————
           40.00 psf    2.00 ft
           —————        —————
           ASCE7-O5 LL  beam spacing
           ———————————  ————————————


 


|


**Eq. 3:**  Total load [ASCE7-05 2.3.2]

.. code-block:: text 

           ω₁ = dl₁ + ll₁

           ω₁ = 3.77 klf     [ω₁] = 54.96 kN_m   | Total load [ASCE7-05 2.3.2]

           ll₁                         dl₁
           ——————————————————————————  ——————————————————————————
           128.00 ft·psf               3.64 klf
           —————                       —————
           Live load [ASCE7-05 2.3.2]  Dead load [ASCE7-05 2.3.2]
           ——————————————————————————  ——————————————————————————


 
 


--------------



.. _Beam Response:

**0.1 - 4** | Beam Response
--------------------------------------------------------------------------------
 
The following lines import the beam geometry from an external file, 
calculate section properties from imported functions and calculate 
the maximum moment, bending stress and mid-span deflection. 
 

**Table 4**: Beam functions (rvsrc/sectprop.py)


==========================  ============================================
Function                    Docstring
==========================  ============================================
rectsect(b, d)              section modulus of rectangle
rectinertia(b, d)           moment of inertia of rectangle
midspan_delta(ln, w, e, i)  mid-span deflection of simply supported beam
                            with UDL
==========================  ============================================

 


|


**Eq. 4:**  rectangle - S (sectprop.py)

.. code-block:: text 

           section₁ = rectsect(b₁, h₁)

           section₁ = 540.00 in3     [section₁] = 8849.01 cm3   | rectangle - S (sectprop.py)

           b₁          h₁
           ——————————  ——————————
           10.00 inch  18.00 inch
           —————       —————
           beam width  beam depth
           ——————————  ——————————


 


|


**Eq. 5:**  rectangle - I (sectprop.py)

.. code-block:: text 

           inertia₁ = rectinertia(b₁, h₁)

           inertia₁ = 4860.0 in4     [inertia₁] = 202288.5 cm4   | rectangle - I (sectprop.py)

           b₁          h₁
           ——————————  ——————————
           10.0 inch   18.0 inch
           —————       —————
           beam width  beam depth
           ——————————  ——————————


 

.. list-table::
    :widths: 46 54
    :header-rows: 0

    * - .. figure:: c:/git/rivt-example-01-git/rivt-report/rvsrc/img/ss-beam2.png
            :width: 100%

            **Fig. 2 -** Moment diagram 
     
      - .. figure:: c:/git/rivt-example-01-git/rivt-report/rvsrc/img/ss-beam1.png
            :width: 100%
            
            **Fig. 3 -** Deflection diagram 

                     

 
**Maximum bending stress formula**


 

|

**Eq.6:**  

.. code-block:: text 

                M₁
           σ₁ = ──
                S₁




 


|


**Eq. 7:**  Mid-span UDL moment

.. code-block:: text 

                       2
                ω₁⋅spn₁ 
           m₁ = ────────
                   8    

           m₁ = 120.52 ftkip     [m₁] = 163.40 mkN   | Mid-span UDL moment

           spn₁       ω₁
           —————————  ———————————————————————————
           16.00 ft   3.77 klf
           —————      —————
           beam span  Total load [ASCE7-05 2.3.2]
           —————————  ———————————————————————————


 


|


**Eq. 8:**  Bending stress

.. code-block:: text 

                    m₁   
           fb₁ = ────────
                 section₁

           fb₁ = 2678.2 lb_in2     [fb₁] = 18.5 MPA   | Bending stress

           section₁                     m₁
           ———————————————————————————  ———————————————————
           540.0 inch3                  120.5 ft2·klf
           —————                        —————
           rectangle - S (sectprop.py)  Mid-span UDL moment
           ———————————————————————————  ———————————————————


 

|
|

**Eq.9:** Stress ratio

.. code-block:: text 

  ▮ fb₁ < Fb₁
  ▮
  ▮ [1] fb₁    [2] Fb₁    ratio [1]/[2]    check    reference
  ▮ —————————  —————————  ———————————————  ———————  ————————————
  ▮ 2.68 ksi   20.00 ksi  0.13             OK       Stress ratio
  ▮ —————————  —————————  ———————————————  ———————  ————————————

 


|


**Eq. 10:**  mid-span deflection (sectprop.py)

.. code-block:: text 

           δ₁ = midspan_δ(spn₁, ω₁, E₁, inertia₁)

           δ₁ = 0.04 inch     [δ₁] = 1.00 mm   | mid-span deflection (sectprop.py)

           spn₁       E₁                     ω₁                           inertia₁
           —————————  —————————————————————  ———————————————————————————  ———————————————————————————
           16.00 ft   29000.00 ksi           3.77 klf                     4860.00 inch4
           —————      —————                  —————                        —————
           beam span  modulus of elasticity  Total load [ASCE7-05 2.3.2]  rectangle - I (sectprop.py)
           —————————  —————————————————————  ———————————————————————————  ———————————————————————————


 
 

--------------------------------------------------------------------------------

.. [1] "Euler–Bernoulli beam theory," Wikipedia, Wikimedia Foundation. [Online].https://en.wikipedia.org/wiki/Euler_Bernoulli_beam_theory.[Accessed: Jun. 15, 2026].


.. [2] ASCE/SEI 7-05, Minimum Design Loads for Buildings and Other Structures,American Society of Civil Engineers, 2005.


