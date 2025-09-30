#! python
# %% Start
import rivtlib.rvapi as rv

# %%
rv.I("""rivt Test

    This is a test of the rivt instalation. It calculates the maximum bending
    moment on simply supported beam.

    ASCE 7-05 Load Effects _[T]

    =============   ==============================================
    Equation No.    Load Combination
    =============   ==============================================
    16-1            1.4(D+F)
    16-2            1.2(D+F+T) + 1.6(L+H) + 0.5(Lr or S or R)
    16-3            1.2(D+F+T) + 1.6(Lr or S or R) + (f1L or 0.8W)
    =============   ==============================================

    | IMAGE | rvlocal | beam.png | Beam Geometry _[F],  0.5
    """)

# %%
rv.V("""Loads and Geometry

    _[[V]] Dead loads _[V]
    D_1 = 3.8*PSF | PSF, KPA | joists          
    D_2 = 2.1*PSF | PSF, KPA | plywood          
    D_3 = 10.0*PSF | PSF, KPA | partitions       
    D_4 = 0.5*KLF | KLF, KNLM | fixed machinery  
    _[[Q]]


    _[[V]] Live Loads _[V]
    L_1 = 40*PSF  | PSF, KPA | ASCE7-O5  
    _[[Q]]


    _[[V]] Beam tributary width and span _[V]
    w_1 = 2*FT | FT, M | beam spacing  
    l_1 = 14*FT | FT, M | beam span 
    """)

rv.V("""Calculate Beam Moment - UDL

    Maximum bending moment

    Total UDL factored dead load  _[E]
    DL_1 = 1.2 * (w_1 *(D_1 + D_2 + D_3) + D_4) |

    Total UDL factored live load    #- 01
    LL_1 = 1.6 * w_1 * L_1

    factored UDL    #- 01
    omega_1 = DL_1 + LL_1

    Bending moment at mid-span    #- 02
    M_1 = omega_1 * l_1**2 / 8
    """)

# %%
rv.D("""Publish Doc

    | DOC | rvlocal | rpdf | rivDoc1.ini 
    """)
