
E = 2.0e5 # MPa
v = 0.27
G = 0.5*E/(1+v)

Iy  = 2.111e5
Iz  = 12.87e5
Ivv =  1.475e+06 # vv|xx
Irw = -1.475e+06 # mv|xx
Io  = Iy + Iz # 1.478e+06

Io + 2*Irw + Ivv
Isv = 2283. # = Io + 2*Irw + Ivv


print(f"{G*Isv = :1.3g}")
print(f"{G*Io = :1.3g}")