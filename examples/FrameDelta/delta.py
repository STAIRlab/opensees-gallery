import sympy as sp

L, Phi = sp.symbols("L Phi")



ab = sp.Matrix([[  1 / L , 1 ,-1 / L , 0 ],
                [  1 / L , 0 ,-1 / L , 1 ]])
# ac =  sp.Matrix([-1 ,    0   , 0 , 1 ,    0   , 0 ],
#                 [ 0 ,  1 / L , 1 , 0 , -1 / L , 0 ],
#                 [ 0 ,  1 / L , 0 , 0 , -1 / L , 1 ])


def expand(k):
    return ab.T*k*ab

def condense(K):
    return sp.Matrix([[K[1,1], K[1,3]],[K[3,1],K[3,3]]])
#   return ab*K*ab.T

def factor(A):
    g = sp.gcd(tuple(A))

    A_factored = sp.MatMul(g,(A/g),evaluate = False)
    return A_factored

def euler01():
    i = sp.symbols("1")
    return sp.Matrix(
              [[ 6/(5*L) ,    i/10 , -6/(5*L),   i/10 ],
               [ i/10    ,  2*L/15 ,  - i/10 ,  -L/30 ],
               [-6/(5*L) ,   -i/10 ,  6/(5*L),  -i/10 ],
               [ i/10    ,   -L/30 ,   -i/10 , 2*L/15 ]])
#   return sp.Matrix(
#             [[ 6/(5*L) , -i/10 , -6/(5*L) , -i/10 ],
#              [-i/10    ,  2*L/15 , i/10 , -L/30 ],
#              [-6/(5*L) ,  i/10 , 6/(5*L) , i/10  ],
#              [-i/10    , -L/30 , i/10 , 2*L/15 ]])

def shear01():
    c11 = 12*(6 + 10*Phi + 5*Phi**2)
    c12 = (-2 - 10*Phi - 5*Phi**2)*L**2
    c22 = (8 + 10*Phi + 5*Phi**2)*L**2

    return  sp.Matrix([[ c11,  6*L, -c11,  6*L],
                       [ 6*L,  c22, -6*L,  c12],
                       [-c11, -6*L,  c11, -6*L],
                       [ 6*L,  c12, -6*L,  c22]])/(60*L)

def shear02():
    EI, lam, psi = sp.symbols("EI, lambda, psi")
    psi = 1/(1+lam**2*Phi/12)
    eta = 2 - 2*sp.cos(lam) - psi*lam*sp.sin(lam)
    c1 = psi**2*lam**3 * sp.sin(lam)/eta
    c1, c2, c3, c4 = sp.symbols("c1, c2, c3, c4")

    return  sp.Matrix([[ c1 ,   c3*L ,  -c1 ,  c3*L   ],
                       [c3*L, c2*L**2, -c3*L,  c4*L**2],
                       [-c1 ,  -c3*L ,   c1 , -c3*L   ],
                       [c3*L, c4*L**2, -c3*L,  c2*L**2]])*(EI/L**3)




def display(Kg):

    kg = condense(Kg)
    kg.simplify()
    KD = Kg - expand(kg)
    KD.simplify()
    aka = expand(kg)
    aka.simplify()
#   print(sp.latex(Kg))
    print(r"$$K_{\delta} = ", sp.latex(Kg), "$$")
    print(r"$$k_{\delta} = ", sp.latex(kg), "$$")
    print(r"$$a^{\mathrm{t}} k_{\delta} a = ", sp.latex(aka), "$$")
    print(r"$$K_{\Delta} = ", sp.latex(KD), "$$")

#   print(r"\frac{1}{L}", sp.latex(L*kg))

display(euler01())

print("\n", "-"*10, "\n")

display(shear01())

print("\n", "-"*10, "\n")

display(shear02())

