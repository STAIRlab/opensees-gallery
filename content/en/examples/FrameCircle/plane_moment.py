import numpy as np
import veux

def _fix_node(model, node, type):
    ndf = model.getNDF()
    reactions = [0 for _ in range(ndf)]

    long, tran, vert = range(3)
    if ndf == 6:
        bend = vert+3
        # always fix out-of-plane rotation, which spins
        # about the transverse DOF
        reactions[tran+3] = 1
        reactions[long+3] = 1 # torsion
        reactions[2] = 1
    else:
        bend = vert


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

    elif type == "slide":
        reactions[tran] = 0
        reactions[long] = 0 if node > 1 else 1
        reactions[bend] = 1

    elif type == "free":
        pass

    model.fix(node, *reactions)
    return reactions


def create_prism(length:    float,
                 element:   str,
                 section:   dict,
                 boundary:  tuple,
                 geometry:  str = None,
                 transform: str = None,
                 divisions: int = 1,
                 rotation = None, 
                 ndm=3):
    import opensees.openseespy as ops

    L  = length

    # Number of elements discretizing the column
    ne = divisions

    elem_type  = element
    geom_type  = transform

    nn = ne + 1

    model = ops.Model(ndm=ndm)

    for i in range(1, nn+1):
        x = (i-1)/float(ne)*L
        if ndm == 3:
            location = (x, 0.0, 0.0)
        else:
            location = (x, 0.0)

        if rotation is not None:
            location = tuple(rotation@location)

        model.node(i, location)

        model.mass(i, *[1.0]*model.getNDF())


    # Define boundary conditions
    if isinstance(boundary[0], str):
        _fix_node(model,  1, boundary[0])
    else:
        model.fix(1, boundary[0])

    if isinstance(boundary[1], str):
        _fix_node(model, nn, boundary[1])
    else:
        model.fix(nn, boundary[1])

    #
    # Define cross-section 
    #
    sec_tag = 1
    properties = []
    for k,v in section.items():
        properties.append("-" + k)
        properties.append(v)

    model.section("FrameElastic", sec_tag, *properties)

    # Define geometric transformation
    geo_tag = 1
    if ndm == 3:
        vector = (0,  0, 1)
    #   vector = (0,  -1, 0)
        if rotation is not None:
            vector = tuple(map(float, rotation@vector))
    else:
        vector = ()

    model.geomTransf(geom_type, geo_tag, *vector)

    # Define elements
    for i in range(1, ne+1):
        if geometry is None or geometry == "Linear" or "Exact" in elem_type:
            model.element(elem_type, i, (i, i+1),
                        section=sec_tag,
                        transform=geo_tag)
        else:
            model.element(elem_type, i, (i, i+1),
                        section=sec_tag,
                        order={"Linear": 0, "delta": 1}[geometry],
                        transform=geo_tag)

    return model


def analyze_moment(scale=1/8, steps=1, ne=5, element="ExactFrame"):

    steps = 1
    E  = 1.0
    I  = 2.0
    length = 1.0
    model = create_prism(
        length = length,
        element = element,
        section = dict(
            E   = E,
            G   = 1.0,
            A   = 2.0,
            J   = 2.0,
            Iy  = I,
            Iz  = I,
            Ay  = 2.0,
            Az  = 2.0),
        boundary = ("fix","free"),
        transform = "Linear",
        divisions = ne
    )

    model.test("EnergyIncr", 1e-12, 10, 1)

    model.pattern("Plain", 1, "Linear", load={
        ne+1: [0, 0, 0] + [0, 0, -1]}
    )

    model.integrator("LoadControl", 2*np.pi*(E*I/length)*scale/steps)
    model.analysis("Static")


    for i in range(steps):
        if model.analyze(1) != 0:
            raise RuntimeError(f"Failed at step {i}")


    return model



if __name__ == "__main__":
    # Analyze 1/8th of a rotation to compare with the exact solution
    model = analyze_moment(1/8)
    print(model.nodeDisp(6))
    artist = veux.create_artist(model)
    artist.draw_axes()
    artist.draw_outlines()
    artist.draw_outlines(state=model.nodeDisp)

    # Rather than continue the analysis from where we left off, we
    # create a new model and start over again just to show that the
    # ExactFrame element can solve 2 loops in only a single analysis 
    # step
    model = analyze_moment(2.0)
    artist.draw_outlines(state=model.nodeDisp)
    print(model.nodeDisp(6))
    veux.serve(artist)

    import matplotlib.pyplot as plt
    try:
        plt.style.use("typewriter")
    except:
        pass

    fig,ax = plt.subplots()
    load = np.linspace(0, 2.0, 100)
    ne = 5
    ax.plot(load, [-analyze_moment(m, ne=ne).nodeDisp(ne+1,2) for m in load], label=f"ExactFrame, {ne = }")
    ax.plot(load, [0]+[-1/(m*2*np.pi)*(np.cos(m*2*np.pi)-1) for m in load[1:]], label="Analytic")
    ax.set_xlabel(r"Load factor $\lambda$")
    ax.set_ylabel(r"Displacement $u_2$")
    ax.legend()
#   fig.savefig("img/displacement.png")
    plt.show()
