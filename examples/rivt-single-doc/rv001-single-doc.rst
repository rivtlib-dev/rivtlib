.. header::

   2026-02-20 - 12:52PM  |   -   |  rv001-single-doc  v - 
[ 1i ] Load Combinations
--------------------------------------------------------------------------------

**Table 1**: ASCE 7-05 Load Effects

============= ================================================
Equation No.    Load Combination
============= ================================================
16-1           1.4(D+F)
16-2           1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R)
16-3           1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W)
============= ================================================
 


.. image:: C:/git/rivtlib-git/examples/rivt-single-doc/beam1.png
   :width: 30 %
   :align: center


.. class:: align-center 

   Beam Geometry

 
.. raw:: html

   <p align="right">Bending Stress **[Eq 1]**</p> 


 
.. code:: 

             M₁
     σ₁ = ──
          S₁


 

[ 2v ] Loads and Geometry
--------------------------------------------------------------------------------
==========  =========  ==========  ===================
variable        value     [value]  description
==========  =========  ==========  ===================
D_1          3.80 psf    0.18 kPA  joists DL
D_2          2.10 psf    0.10 kPA  plywood DL
D_3         10.00 psf    0.48 kPA  partitions DL
D_4          1.00 klf  14.59 kN_m  fixed machinery  DL
L_1         40.00 psf    1.92 kPA  ASCE7-O5 LL
==========  =========  ==========  =================== 

**Table 2**: Beam Geometry [file: beam1.csv]

==========  ========  =========  =============
variable       value    [value]  description
==========  ========  =========  =============
W_1          2.00 ft     0.61 m  beam spacing
S_1         14.00 ft     4.27 m  beam span
==========  ========  =========  =============

 


.. raw:: html

   <p align="right">dead load : ASCE7-05 2.3.2   **[Eq 2]**</p> 


.. code:: 

    dl_1 = 1.2*(D_4 + W_1*(D_1 + D_2 + D_3))

========  ==========
 dl_1      [dl_1 ]
========  ==========
1.24 klf  18.07 kN_m
========  ==========

========  =========  =======  ========  =====
  D_2        D_3       W_1      D_1      D_4
========  =========  =======  ========  =====
2.10 psf  10.00 psf  2.00 ft  3.80 psf   klf
========  =========  =======  ========  =====
 


.. raw:: html

   <p align="right">live load : ASCE7-05 2.3.2  **[Eq 3]**</p> 


.. code:: 

    ll_1 = 1.6*L_1*W_1

========  =========
 ll_1      [ll_1 ]
========  =========
0.13 klf  1.87 kN_m
========  =========

=========  =======
   L_1       W_1
=========  =======
40.00 psf  2.00 ft
=========  =======
 


.. raw:: html

   <p align="right">total load : ASCE7-05 2.3.2  **[Eq 4]**</p> 


.. code:: 

    omega_1 = dl_1 + ll_1

==========  ============
 omega_1     [omega_1 ]
==========  ============
 1.37 klf    19.94 kN_m
==========  ============

========  =============
  dl_1        ll_1
========  =============
1.24 klf  128.00 ft·psf
========  =============
 

[ 3v ] Beam Stress
--------------------------------------------------------------------------------
 
 
**[ Python file read:** sectprop.py **]**



 


.. raw:: html

   <p align="right">function: rect. S  **[Eq 5]**</p> 


.. code:: 

    section_1 = rectsect(10*inch, 18*inch)

============  ==============
 section_1     [section_1 ]
============  ==============
 540.00 in3    8849.01 cm3
============  ==============

 


.. raw:: html

   <p align="right">function: rect. I  **[Eq 6]**</p> 


.. code:: 

    inertia_1 = rectinertia(10*inch, 18*inch)

============  ==============
 inertia_1     [inertia_1 ]
============  ==============
 4860.0 in4    202288.5 cm4
============  ==============

 
 


.. raw:: html

   <p align="right">mid-span UDL moment  **[Eq 7]**</p> 


.. code:: 

             2        
          S_1 *omega_1
    m_1 = ------------
               8      

===========  =========
   m_1        [m_1 ]
===========  =========
33.47 ftkip  45.38 mkN
===========  =========

=========  ========
 omega_1     S_1
=========  ========
1.37 klf   14.00 ft
=========  ========
 


.. raw:: html

   <p align="right">bending stress  **[Eq 8]**</p> 


.. code:: 

              m_1   
    fb_1 = ---------
           section_1

============  =========
   fb_1        [fb_1 ]
============  =========
743.8 lb_in2   5.1 MPA
============  =========

===========  ============
 section_1       m_1
===========  ============
540.0 inch3  33.5 ft2·klf
===========  ============
 


.. raw:: html

   <p align="right">stress ratio  **[Eq 9]**</p> 


.. code:: 

    fb_1 < 20000*lb_in2


========  =====  ==============
  fb_1      <     20000*lb_in2
========  =====  ==============
0.74 ksi    <      20.00 ksi
  0.04    ratio      26.89
========  =====  ==============

.. raw:: html

   <p align="right">[92m>>> OK[00m</p> 


 

end of doc

