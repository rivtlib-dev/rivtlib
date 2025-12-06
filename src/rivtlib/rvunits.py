"""Unit definitions

create rv-custom-units.py file in doc or report folder to add units
"""

import importlib.util
import sys
from pathlib import Path

from rivtlib.unum.core import Unum, new_unit

# from rivt.unum.core import *
# from rivt.unum.utils import *
# from rivt.unum.utils import uarray

rvpath = importlib.util.find_spec("rivtlib")
rivpath = Path(rvpath.origin).parent
unumpath = Path(rivpath, "unum")
sys.path.append(str(rivpath))
sys.path.append(str(unumpath))


# print(sys.path)
# print(dir())

Unum.set_format(
    mul_separator=" ",
    div_separator="",
    unit_format="%s",
    value_format="%.2f",
    unitless="",  # hide empty
    superscript=False,
    auto_norm=True,
)

# standard SI units ==== DO NOT MODIFY BETWEEN DOUBLE LINES  ============
#
# temperature - relative degree, not offset
K = new_unit("K", 0, "kelvin")
CELSIUS = new_unit("deg C", K, "degree Celsius")
FAHR = new_unit("degF", K * 9.0 / 5, "degree Fahrenheit")
# time
SEC = S = new_unit("SEC", 0, "second")
HZ = new_unit("Hz", 1 / S, "hertz")
# length
M = new_unit("M", 0, "meter")
NM = new_unit("nm", 10**-9 * M, "nanometer")
UM = new_unit("um", 10**-6 * M, "micrometer")
MM = new_unit("mm", 10**-3 * M, "millimeter")
CM = new_unit("cm", 10**-2 * M, "centimeter")
DM = new_unit("dm", 10**-1 * M, "decimeter")
# mass
KG = new_unit("kg", 0, "kilogram")
GRAM = new_unit("gram", 10**-3 * KG, "gram")
RAD = new_unit("rad", M / M, "radian")
SR = new_unit("sr", M**2 / M**2, "steradian")
MOL = new_unit("mol", 0, "mole")
# force
N = new_unit("N", M * KG / S**2, "newton")
CD = new_unit("cd", 0, "candela")
LM = new_unit("lm", CD * SR, "lumen")
LX = new_unit("lx", LM / M**2, "lux")
# charge
J = new_unit("J", N * M, "joule")
W = new_unit("W", J / S, "watt")
A = new_unit("A", 0, "ampere")
MA = new_unit("mA", 10**-3 * A, "milliampere")
C = new_unit("C", S * A, "coulomb")
VO = new_unit("V", W / A, "volt")
F = new_unit("F", C / VO, "farad")
OHM = new_unit("ohm", VO / A, "ohm")
SIEMENS = new_unit("siemens", A / VO, "siemens")
WB = new_unit("Wb", VO * SIEMENS, "weber")
TS = new_unit("TS", WB / M**2, "tesla")
HENRY = new_unit("H", WB / A, "henry")
#
# ============  DO NOT MODIFY FILE ABOVE THIS LINE  ===========================
#
# -------------------------------- metric
#
G = new_unit("G", 9.80665 * M / S**2, "gravity acceleration")
# pressure
PA = new_unit("PA", N / M**2, "pascal")
MPA = new_unit("MPA", PA * (10**6), "megapascals")
kPA = new_unit("kPA", PA * (10**3), "kilopascals")
# force
kN = new_unit("kN", N * (10**3), "kilonewton")
MN = new_unit("mN", N * (10**6), "meganewton")
kM = new_unit("kM", M * (10**3), "kilometer")
kN__M3 = new_unit("kN__M3", kN / (M**3), "kilonewton per cubic meter")
kN__M = new_unit("kN__M", kN / (M), "kilonewton per meter")
kN_M = new_unit("kN_M", (kN * M), "meter-kilonewton")

# area
SQM = new_unit("SQM", (M**2), "square meter")
CM2 = new_unit("CM2", (CM**2), "square centimeter")
CM3 = new_unit("CM3", (CM**3), "cubic centimeter")
CM4 = new_unit("CM4", (CM**4), "cm to fourth power")

#
# ------------------------------ imperial
#
# length
IN = new_unit("IN", M / 39.370079, "inch")
FT = new_unit("FT", M / 3.2808399, "foot")
MILES = new_unit("MILES", FT * 5280, "miles")
# mass
LBM = new_unit("LBM", KG / 2.2046226, "pound-mass")
# force
LBF = new_unit("LBF", 4.4482216 * N, "pound-force")
KIP = new_unit("KIP", LBF * 1000.0, "kilopound")
KIP_FT = new_unit("KIP_FT", FT * LBF * 1000.0, "foot-kips")
KIP_IN = new_unit("KIP_IN", IN * LBF * 1000.0, "inch-kips")
KIP__IN = new_unit("KIP__IN", KIP / IN, "kips per inch")
PLI = new_unit("PLI", LBF / IN, "pounds per inch")
PLF = new_unit("PLF", LBF / FT, "pounds per foot")
KIP__FT = new_unit("KIP__FT", KIP / FT, "kips per foot")
# area
SF = new_unit("SF", FT**2, "square feet")
IN2 = new_unit("IN2", IN**2, "square inches")
IN3 = new_unit("IN3", IN**3, "cubic inches")
IN4 = new_unit("IN4", IN**4, "inches to fourth power")
# pressure
PSF = new_unit("PSF", LBF / FT**2, "pounds per square foot")
PSI = new_unit("PSI", LBF / IN**2, "pounds per square inch")
KSF = new_unit("KSF", KIP / FT**2, "kips per square foot")
KSI = new_unit("KSI", KIP / IN**2, "kips per square inch")
# density
PCI = new_unit("PCI", LBF / IN**3, "pounds per cubic inch")
PCF = new_unit("PCF", LBF / FT**3, "pounds per cubic ft")
# time
HR = new_unit("HR", 60 * 60 * S, "hours")
# velocity
MPH = new_unit("MPH", MILES / HR, "miles per hour")
FPS = new_unit("FPS", FT / SEC, "feet per second")
