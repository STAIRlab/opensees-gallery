import numpy as np
import opensees.openseespy

# Create the model
def arch_model():

    # Define model parameters
    L      = 5000
    Rise   = 500
    Offset = 200

    # Define material parameters
    E = 200
    A = 1e4
    I = 1e8

    # Compute radius
    R  = Rise/2 + (2*L)**2/(8*Rise)
    th = 2*np.arcsin(L/R)

    #
    # Build the model
    #
    model = opensees.openseespy.Model(ndm=2, ndf=3)

    # Create nodes
    ne  = 10
    nen =  2             # nodes per element
    nn  = ne*(nen-1)+1
    mid = (nn+1)//2      # midpoint node

    for i, angle in enumerate(np.linspace(-th/2, th/2, nn)):
        tag = i + 1

        # Compute x and add offset if midpoint
        x = R*np.sin(angle)
        if tag == mid:
            x -= Offset

        # Compute y
        y = R*np.cos(angle)

        # create the node
        model.node(tag, x, y)

    model.section("ElasticFrame", 1, A=A, E=E, Iy=I, Iz=I, J=2*I, G=E)

    # Create elements
    transfTag = 1
    model.geomTransf("Corotational", transfTag)
    for i in range(ne):
        tag   = i+1
        nodes = (i+1, i+2)
        model.element("ExactFrame", tag, nodes, section=1, transform=transfTag)


    model.fix( 1, 1, 1, 0)
    model.fix(nn, 1, 1, 0)

    # Create a load pattern that scales linearly
    model.pattern("Plain", 1, "Linear")

    # Add a nodal load to the pattern
    model.load(mid, 0.0, -1.0, 0.0, pattern=1)


    # model.system("ProfileSPD")
    # model.system("FullGeneral")
    # model.system("BandGeneral")
    model.system("Umfpack", det=True)

    model.test("NormUnbalance", 1e-6, 25, 0)
    model.algorithm("Newton")
    model.analysis("Static")


    return model, mid


def arch_model3D():

    # Define model parameters
    L      = 5000
    Rise   = 500
    Offset = 200

    # Define material parameters
    E = 200
    A = 1e4
    I = 1e8

    # Compute radius
    R  = Rise/2 + (2*L)**2/(8*Rise)
    th = 2*np.arcsin(L/R)

    #
    # Build the model
    #
    model = opensees.openseespy.Model(ndm=3, ndf=6)

    # Create nodes
    ne  = 10
    nen =  2             # nodes per element
    nn  = ne*(nen-1)+1
    mid = (nn+1)//2      # midpoint node

    for i, angle in enumerate(np.linspace(-th/2, th/2, nn)):
        tag = i + 1

        # Compute x and add offset if midpoint
        x = R*np.sin(angle)
        if tag == mid:
            x -= Offset

        # Compute y
        y = R*np.cos(angle)

        # create the node
        model.node(tag, x, y, 0)

    model.section("ElasticFrame", 1, A=A, E=E, Iy=I, Iz=I, J=2*I, G=E, Ay=A*100, Az=A*100)

    # Create elements
    transfTag = 1
    model.geomTransf("Corotational", transfTag, (0, 0, 1))
    for i in range(ne):
        tag   = i+1
        nodes = (i+1, i+2)
        model.element("PrismFrame", tag, nodes, section=1, transform=transfTag)


    model.fix( 1, 1, 1, 0, 1, 1, 0)
    model.fix(nn, 1, 1, 0, 1, 1, 0)
    for i in model.getNodeTags():
        model.fix(i, dof=3)

    # Create a load pattern that scales linearly
    model.pattern("Plain", 1, "Linear")

    # Add a nodal load to the pattern
    model.load(mid, 0.0, -1.0, 0.0, 0, 0, 0, pattern=1)


    model.system("ProfileSPD")
    # model.system("FullGeneral")
    # model.system("BandGeneral")
    # model.system("Umfpack", det=True)

    model.test("NormUnbalance", 1e-6, 25, 0)
    model.algorithm("Newton")
    model.analysis("Static")


    return model, mid

def arc_control(model, dx, *args,  a=0):
    model.integrator("ArcLength", dx, a, det=True, exp=0.0, reference="point")


def analyze(model, mid, increment, steps, dx, *args):
    # Initialize some variables
    dof = 2
    xy = []      # Container to hold solution history (i.e., load factor and displacement at `node`)
    status = 0   # Convergence flag; Model.analyze() will return 0 if successful.

    # Configure the first load increment strategy; explained below
    increment(model, dx, *args)

    for step in range(steps):

        # 1. Perform Newton-Raphson iterations until convergence for 1 load
        #    increment
        status = model.analyze(1)

        # 2. Store the displacement and load factor
        xy.append([model.nodeDisp(mid, dof), model.getTime()])

        # 3. If the iterations failed, try cutting
        #    the increment arc-length in half
        if status != 0:
            dx *= 0.5
            increment(model, dx, *args)

    return np.array(xy).T


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    model, node = arch_model3D()

    model.print("-json")

    x, y = analyze(model, node, arc_control, 110, 45)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


