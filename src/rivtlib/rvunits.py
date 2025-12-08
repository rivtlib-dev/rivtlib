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
sec = S = new_unit("sec", 0, "second")
HZ = new_unit("Hz", 1 / S, "hertz")
# length
m = M = new_unit("m", 0, "meter")
nm = new_unit("nm", 10**-9 * M, "nanometer")
um = new_unit("um", 10**-6 * M, "micrometer")
mm = new_unit("mm", 10**-3 * M, "millimeter")
cm = new_unit("cm", 10**-2 * M, "centimeter")
dm = new_unit("dm", 10**-1 * M, "decimeter")
# mass
kg = KG = new_unit("kg", 0, "kilogram")
gram = new_unit("gram", 10**-3 * KG, "gram")
rad = new_unit("rad", M / M, "radian")
sr = new_unit("sr", M**2 / M**2, "steradian")
mol = new_unit("mol", 0, "mole")
# force
N = new_unit("N", M * KG / S**2, "newton")
cd = new_unit("cd", 0, "candela")
lm = new_unit("lm", cd * sr, "lumen")
lx = new_unit("lx", lm / M**2, "lux")
# charge
J = new_unit("J", N * M, "joule")
W = new_unit("W", J / S, "watt")
A = new_unit("A", 0, "ampere")
mA = new_unit("mA", 10**-3 * A, "milliampere")
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
km = new_unit("kM", M * (10**3), "kilometer")
kN_m3 = new_unit("kN_m3", kN / (M**3), "kilonewton per cubic meter")
kN_m = new_unit("kN_m", kN / (M), "kilonewton per meter")
mkN = new_unit("mkN", (kN * M), "meter-kilonewton")
# area
sqm = new_unit("sqm", (M**2), "square meter")
cm2 = new_unit("cm2", (cm**2), "square centimeter")
cm3 = new_unit("cm3", (cm**3), "cubic centimeter")
cm4 = new_unit("cm4", (cm**4), "cm to fourth power")
#
# ------------------------------ imperial
#
# length
inch = new_unit("inch", M / 39.370079, "inch")
ft = new_unit("ft", M / 3.2808399, "foot")
miles = new_unit("miles", ft * 5280, "miles")
# mass
lbm = new_unit("lbm", KG / 2.2046226, "pound-mass")
# force
lbf = new_unit("lbf", 4.4482216 * N, "pound-force")
kips = new_unit("kips", lbf * 1000.0, "kilopound")
ftkips = new_unit("ftkip", ft * lbf * 1000.0, "foot-kips")
inkips = new_unit("inkips", inch * lbf * 1000.0, "inch-kips")
kli = new_unit("kli", kips / inch, "kips per inch")
klf = new_unit("klf", kips / ft, "kips per foot")
pli = new_unit("pli", lbf / inch, "pounds per inch")
plf = new_unit("plf", lbf / ft, "pounds per foot")
# area
sf = new_unit("sf", ft**2, "square feet")
in2 = new_unit("in2", inch**2, "square inches")
in3 = new_unit("in3", inch**3, "cubic inches")
in4 = new_unit("in4", inch**4, "inches to fourth power")
# pressure
psf = new_unit("psf", lbf / ft**2, "pounds per square foot")
psi = new_unit("psi", lbf / inch**2, "pounds per square inch")
ksf = new_unit("ksf", kips / ft**2, "kips per square foot")
ksi = new_unit("ksi", kips / inch**2, "kips per square inch")
# density
pci = new_unit("pci", lbf / inch**3, "pounds per cubic inch")
pcf = new_unit("pcf", lbf / ft**3, "pounds per cubic ft")
# time
hr = new_unit("hr", 60 * 60 * sec, "hours")
# velocity
mph = new_unit("mph", miles / hr, "miles per hour")
fps = new_unit("fps", ft / sec, "feet per second")
