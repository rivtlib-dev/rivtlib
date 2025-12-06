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
SEC = S = new_unit("s", 0, "second")
HZ = new_unit("Hz", 1 / S, "hertz")
# length
M = new_unit("m", 0, "meter")
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
PA = new_unit("pa", N / M**2, "pascal")
MPA = new_unit("mpa", PA * (10**6), "megapascals")
KPA = new_unit("kpa", PA * (10**3), "kilopascals")
# force
KN = new_unit("kN", N * (10**3), "kilonewton")
MN = new_unit("mN", N * (10**6), "meganewton")
KM = new_unit("km", M * (10**3), "kilometer")
KNCM = new_unit("kN/M^3", KN / (M**3), "kilonewton per cubic meter")
KNLM = new_unit("kN/m", KN / (M), "kilonewton per meter")
KN_M = new_unit("kN-m", (KN * M), "meter-kilonewton")

# area
SQM = new_unit("sq_m", (M**2), "square meter")
CM2 = new_unit("cm^2", (CM**2), "square centimeter")
CM3 = new_unit("cm^3", (CM**3), "cubic centimeter")

#
# ------------------------------ imperial
#
# length
IN = new_unit("in", M / 39.370079, "inch")
FT = new_unit("ft", M / 3.2808399, "foot")
MILES = new_unit("miles", FT * 5280, "miles")
# mass
LBM = new_unit("lbm", KG / 2.2046226, "pound-mass")
# force
LBF = new_unit("lbf", 4.4482216 * N, "pound-force")
KIP = new_unit("kip", LBF * 1000.0, "kilopound")
KIP_FT = new_unit("kip-ft", FT * LBF * 1000.0, "foot-kips")
KIP_IN = new_unit("kip-in", IN * LBF * 1000.0, "inch-kips")
KLI = new_unit("kips/in", KIP / IN, "kips per inch")
PLI = new_unit("lbf/in", LBF / IN, "pounds per inch")
PLF = new_unit("lbf/ft", LBF / FT, "pounds per foot")
KLF = new_unit("kip/ft", KIP / FT, "kips per foot")
# area
SF = new_unit("sqft", FT**2, "square feet")
IN2 = new_unit("in^2", IN**2, "square feet")
IN3 = new_unit("in^3", IN**3, "square feet")
# pressure
PSF = new_unit("psf", LBF / FT**2, "pounds per square foot")
PSI = new_unit("psi", LBF / IN**2, "pounds per square inch")
KSF = new_unit("ksf", KIP / FT**2, "kips per square foot")
KSI = new_unit("ksi", KIP / IN**2, "kips per square inch")
# density
PCI = new_unit("pci", LBF / IN**3, "pounds per cubic inch")
PCF = new_unit("pcf", LBF / FT**3, "pounds per cubic ft")
# time
HR = new_unit("hr", 60 * 60 * S, "hours")
# velocity
MPH = new_unit("mph", MILES / HR, "miles per hour")
FPS = new_unit("fps", FT / SEC, "feet per second")
