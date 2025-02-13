# 2D/3D Column
#
#  
#    long
#     ^
#    -o-
#     |
#     |
#     |
#     |
#    -o- -> tran
#
from math import cos,sin,sqrt,pi
import numpy as np
import scipy.optimize
import opensees.openseespy as ops

# Effective length factors
FACTORS = {
    "pin-pin":     1,
    "fix-roll":   1,
    "fix-fix":     0.5,
    "fix-pin":     0.7,
    "fix-free":    2,
    "pin-roll":   2,
}

def buckle_factor(boundary, phi=0):
    if boundary == "pin-pin":
        return np.pi

    if boundary == "fix-roll":
        return np.pi

    if boundary == "fix-fix":
        return 2*np.pi

    if boundary == "fix-pin":
        f = lambda x: np.tan(x) - x/(1 + x**2*phi/12)
        sol = scipy.optimize.root_scalar(f, x0=0.7, bracket=(np.pi, 1.45*np.pi))
        if sol.converged:
            return sol.root

    if boundary == "fix-free":
        return np.pi/2

    if boundary == "pin-roll":
        return np.pi/2


def fix_node(model, node, type):
    ndf = model.getNDF()
    reactions = [0 for _ in range(ndf)]

    tran, long = 0, 1
    if ndf == 6:
        bend = 2+3
        # always fix out-of-plane rotation, which spins
        # about the transverse DOF
        reactions[2] = 1
        reactions[tran+3] = 1
        reactions[long+3] = 1
    else:
        bend = 2


    if node > 1:
        vert = 0
    else:
        vert = 1

    if type == "fix":
        reactions[tran] = 1
        reactions[long] = 0 if node > 1 else 1
        reactions[bend] = 1

    elif type == "pin":
        reactions[tran] = 1
        reactions[long] = 0 if node > 1 else 1
        reactions[bend] = 0

    elif type == "roll":
        reactions[tran] = 0
        reactions[long] = 0 if node > 1 else 1
        reactions[bend] = 1

    elif type == "free":
        pass

    model.fix(node, *reactions)


def create_column(boundary="pin-pin", elem_data=None, ndm=2):
    if elem_data is None:
        elem_data = {}

    elem_type  = elem_data.get("type",      "forceBeamColumnCBDI")
    geom_type  = elem_data.get("transform", "Corotational")
    use_shear  = elem_data.get("shear", False)
    kinematics = elem_data.get("order", 0)

    E  = 29000.0
    G =  11200.0
#   A  = 9.12e3
    A  = 112.0
    I  = 110.0
    Ay = 3/6*A
    Az = 3/6*A
    L  = 60.0

    # Number of elements discretizing the column
    ne = 10 # 4

    nIP = 5 # number of integration points along each element
    nn = ne + 1

    model = ops.Model(ndm=ndm)

    # Define nodes with unit mass so that the
    # dynamic eigenvalue problem becomes equivalent
    # to a standard one
    for i in range(1, nn+1):
        y = (i-1)/float(ne)*L
        if ndm == 3:
            location = (0.0, y, 0.0)
        else:
            location = (0.0, y)

        model.node(i, location)

        model.mass(i, *[1.0]*model.getNDF())


    # Define boundary conditions
    fix_node(model,  1, boundary.split("-")[0])
    fix_node(model, nn, boundary.split("-")[1])

    # Define cross-section 
    sec_tag = 1
#   properties = {"E": E, "A": A, "Iz": I}
    properties = [E, A, I]
    if ndm == 3:
        #                    Iy       J
        properties.extend([ 2*I, "-J", 100*I, "-G", G])

    if use_shear:
        properties.extend(["-Ay", Ay, "-G", G])
        if ndm == 3:
            properties.extend(["-Az", Az])

    model.section("FrameElastic", sec_tag, *properties)

    # Define geometric transformation
    geo_tag = 1
    if ndm == 3:
        vector = (0, 0, 1)
    else:
        vector = ()

    model.geomTransf(geom_type, geo_tag, *vector)

    # Define elements
    for i in range(1, ne+1):
        model.element(elem_type, i, (i, i+1),
                      section=sec_tag,
                      transform=geo_tag,
                      order=kinematics)


    # Define loads
    if use_shear:
        phi = 12*E*I/(Ay*G*L**2)
        lam = buckle_factor(boundary, phi)
        kL = L/lam
        euler_load = E*I/kL**2  / (1 + lam**2*phi/12)
    else:
#       kL = FACTORS[boundary]*L
        kL = L/buckle_factor(boundary)
        euler_load = E*I/kL**2
    model.pattern('Plain', 1, "Linear")
    if ndm == 2:
        load = (0.0, -euler_load, 0.0)
    else:
        load = (0.0, -euler_load, 0.0, 0, 0, 0)

    model.load(nn, *load, pattern=1)

    return model, euler_load


def linearized_buckling(model, peak_load):
    # Analysis Options
#   model.system('UmfPack')
    model.test('NormUnbalance', 1.0e-6, 20, 0)
    model.algorithm('Newton')
    model.integrator('LoadControl', load_step)
    model.analysis('Static')


def buckling_analysis(model, peak_load):
    # Apply a load from zero to peak_load until 
    # the stiffness becomes singular (first eigenvalue is zero)

    load_step     = 0.01
    PeakLoadRatio = 1.50

    # Analysis Options
#   model.system('UmfPack')
#   model.constraints('Transformation')
#   model.test('NormUnbalance', 1.0e-6, 20, 0)
    model.test("EnergyIncr", 1e-8, 20, 9)
    model.algorithm('Newton')
    model.integrator('LoadControl', load_step)
    model.analysis('Static')

#   print(pd.DataFrame(model.getTangent()))

    lam_0 = model.getTime()
    eig_0 = model.eigen(1)

    limit_load = None
    failed = False
    for i in range(1, int(PeakLoadRatio/load_step)+1):
        if model.analyze(1) != 0:
            print(f"  Analysis failed at step {i} with load at {model.getTime()}")
            failed = True
#           break

        lam =  model.getTime()
        eig =  model.eigen(1)[0]

        if eig <= 0.0 or failed:
            if eig_0 != eig:
                # linear interpolation
                lam_i = lam_0 + (lam - lam_0)*eig_0/(eig_0-eig)
            else:
                lam_i = lam

            limit_load = lam_i * peak_load
            break

        lam_0 = lam
        eig_0 = eig

    return limit_load


if __name__ == "__main__":

    for ndm in 3,:
        for elem in "PrismFrame", "MixedFrame", "ExactFrame":
    #               "forceBeamColumn", "forceBeamColumnCBDI":
            print(f"\n{elem:10}      Shear    Order     Theory   Computed       Error")


            for boundary in FACTORS:

                orders = (0,2) if "Exact" not in elem else (1,)

                for shear in False, True:
                    for order in orders:

                        if not shear and "Exact" in elem:
                            continue

                        elem_data = {
                            "type": elem,
                            "shear": shear,
                            "order": order,
                            "transform": "Corotational"
                        }

                        model, euler_load  = create_column(boundary, elem_data, ndm=ndm)
                        limit_load   = buckling_analysis(model, euler_load)

                        print(f"  {boundary:10} {shear:8} {order:8} ", end="")
                        if limit_load is None:
                            print(f"No singularity found.")
                        else:
                            print(f"{euler_load:10.2f} {limit_load:10.2f} {100*(limit_load/euler_load-1):10.3f} %")

