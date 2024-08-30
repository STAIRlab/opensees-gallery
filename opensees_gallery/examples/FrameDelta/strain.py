
eps, u_xx, u_yx, u_zx = sp.symbols("epsilon, u_xx, u_yx, u_zx")
R = sum()

gam = R.T * sp.Vector([1 + eps*u_xx, eps*u_yx, eps*u_zx]) - sp.Vector([1, 0, 0])


