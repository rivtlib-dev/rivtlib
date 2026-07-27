
# --------------------------------------------------- metric
g = new_unit("G", 9.80665 * M / S**2, "gravity acceleration")
# ----------- pressure
PA = new_unit("PA", N / M**2, "pascal")
MPA = new_unit("MPA", PA * (10**6), "megapascals")
kPA = new_unit("kPA", PA * (10**3), "kilopascals")
# ----------- force
kN = new_unit("kN", N * (10**3), "kilonewton")
MN = new_unit("mN", N * (10**6), "meganewton")
km = new_unit("kM", M * (10**3), "kilometer")
kN_m3 = new_unit("kN_m3", kN / (M**3), "kilonewton per cubic meter")
kN_m = new_unit("kN_m", kN / M, "kilonewton per meter")
kN_cm = new_unit("kN_cm", kN / cm, "kilonewton per centimeter")
kN_cm2 = new_unit("kN_cm2", kN / (cm**2), "kilonewton per square centimeter")
mkN = new_unit("mkN", (kN * M), "meter-kilonewton")
# ----------- area
sqm = new_unit("sqm", (M**2), "square meter")
cm2 = new_unit("cm2", (cm**2), "square centimeter")
cm3 = new_unit("cm3", (cm**3), "cubic centimeter")
cm4 = new_unit("cm4", (cm**4), "cm to fourth power")
# ------------------------------------------------- imperial
# ----------- length
inch = new_unit("inch", M / 39.370079, "inch")
ft = new_unit("ft", M / 3.2808399, "foot")
miles = new_unit("miles", ft * 5280, "miles")
# ----------- mass
lbm = new_unit("lbm", KG / 2.2046226, "pound-mass")
# ----------- force
lbf = new_unit("lbf", 4.4482216 * N, "pound-force")
kips = new_unit("kips", lbf * 1000.0, "kilopound")
ftkips = new_unit("ft-kip", ft * lbf * 1000.0, "foot-kips")
inkips = new_unit("in-kips", inch * lbf * 1000.0, "inch-kips")
k_in = new_unit("k_in", kips / inch, "kips per inch")
k_ft = new_unit("k_ft", kips / ft, "kips per foot")
p_in = new_unit("lb_in", lbf / inch, "pounds per inch")
p_ft = new_unit("lb_ft", lbf / ft, "pounds per foot")
# ----------- area
sf = new_unit("sf", ft**2, "square feet")
in2 = new_unit("in2", inch**2, "square inches")
in3 = new_unit("in3", inch**3, "cubic inches")
in4 = new_unit("in4", inch**4, "inches to fourth")
# ----------- pressure
p_sf = new_unit("p_sf", lbf / ft**2, "pounds per square foot")
p_si = new_unit("p_si", lbf / inch**2, "pounds per square inch")
k_sf = new_unit("k_sf", kips / ft**2, "kips per square foot")
k_si = new_unit("k_si", kips / inch**2, "kips per square inch")
# ----------- density
p_ci = new_unit("p_ci", lbf / inch**3, "pounds per cubic inch")
p_cf = new_unit("p_cf", lbf / ft**3, "pounds per cubic ft")
# ----------- time
hr = new_unit("hr", 60 * 60 * sec, "hours")
# ----------- velocity
mph = new_unit("mph", miles / hr, "miles per hour")
fps = new_unit("fps", ft / sec, "feet per second")