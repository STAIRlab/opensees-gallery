import numpy as np
import veux
import opensees.openseespy
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass


def arch_model3D():
    """
    """

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
        y = R*np.cos(angle) - R*np.cos(th/2)

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


    model.fix( 1, (1, 1, 0, 1, 1, 0))
    model.fix(nn, (1, 1, 0, 1, 1, 0))
    for i in model.getNodeTags():
        model.fix(i, dof=3)

    # Create a load pattern that scales linearly
    model.pattern("Plain", 1, "Linear")

    # Add a nodal load to the pattern
    model.load(mid, (0.0, -1.0, 0.0, 0, 0, 0), pattern=1)


#   model.system("ProfileSPD")
    model.system("FullGeneral")
#   model.system("BandGeneral") # TODO: Broken?
    # model.system("Umfpack", det=True)

#   model.test("NormUnbalance", 1e-6, 25, 0)
    model.test("NormDispIncr", 1e-8, 25, 1)
    model.algorithm("Newton")
    model.analysis("Static")


    return model, mid

def arc_control(model, dx, *args,  a=0):
    model.integrator("ArcLength", dx, a, det=True, exp=0.0, reference="point")


def save_state(model, states, time):
    # time = model.getTime()
    states.append({
            "Time": time,
            "U": {
                # The code 4 indicates incremental displacements
                node: model.nodeDisp(node) for node in model.getNodeTags()
            },
            "DU": {
                # The code 4 indicates incremental displacements
                node: [model.nodeResponse(node, i+1, 4) for i in range(6)]
                for node in model.getNodeTags()
            }
    })
    return states

def analyze(model, mid, increment, steps, dx, *args):
    # Initialize some variables
    dof = 2
    xy = []      # Container to hold solution history (i.e., load factor and displacement at `node`)
    status = 0   # Convergence flag; Model.analyze() will return 0 if successful.
    states = []

    # Configure the first load increment strategy; explained below
    increment(model, dx, *args)

    for step in range(steps):

        # 1. Perform Newton-Raphson iterations until convergence for 1 load
        #    increment
        status = model.analyze(1)

        # 2. Store the displacement and load factor
        xy.append([-model.nodeDisp(mid, dof), model.getTime()])

        # 3. If the iterations failed, try cutting
        #    the increment arc-length in half
        if status != 0:
            dx *= 0.5
            increment(model, dx, *args)
        else:
            save_state(model, states, step)

    return np.array(xy).T, states


def animate(model, states):
    import veux
    import veux.motion
    states = {"ConvergedHistory": states}
    artist = veux.motion._animate(model, states, vertical=3, model_config={
        "extrude_default": "square",
        "extrude_scale": 500
    })
    return artist


if __name__ == "__main__":

    model, node = arch_model3D()
    # artist = veux.render(model, show={"frame.surface"}, model_config={
    #     "extrude_default": "square",
    #     "extrude_scale": 100
    # })
    # artist.draw_origin()
    # veux.serve(artist)

    (x, y), states = analyze(model, node, arc_control, 110, 45)

    artist = animate(model, states)

    veux.serve(artist)
#   artist.save("solution.glb")

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


