#
# 3D portal frame with concentric bracing
#
import numpy as np
import xara
import xara.units.fps as units
from xara.units.fps import inch, kip, ksi

from xsection.library import from_aisc

import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

import veux
from veux.motion import Motion

def create_girder(model, nodes, tags):
    #
    # Nodes:
    #
    #   i                   j
    #   *==o-------------*==*
    #     n+1           n+3
    #     n+2
    #
    # Elements:
    #
    #   *==o-------------*==*
    #    e+1     e+2      e+3
    #
    n = max(tags["nodes"])
    e = max(tags["elements"])
    s = max(tags["sections"])

    #
    # Sections
    #
    tags["sections"].extend([s+1])
    shape = from_aisc("W27x84", units=units, mesh_scale=1/2.5)
#   veux.serve(veux.render(shape.model))
    model.section("ShearFiber", s+1)

    for fiber in shape.create_fibers(origin="centroid"):
        model.fiber(**fiber, material=1, section=s+1)



    #
    # Elements
    #
    tags["elements"].extend([e+1])
    model.element("ForceFrame", e+1, nodes, section=s+1, transform=2)


def create_column(model, nodes, tags):
    n = max(tags["nodes"])
    e = max(tags["elements"])
    s = max(tags["sections"])

    i, j = nodes

    #
    # Sections
    #
    tags["sections"].extend([s+1])
    shape = from_aisc("W14x176", units=units, mesh_scale=1/2.5)

    model.section("ShearFiber", s+1)
    for fiber in shape.create_fibers(origin="centroid"):
        model.fiber(**fiber, material=1, section=s+1)

    #
    # Elements
    #
    tags["elements"].extend([e+1])
    model.element("ForceFrame", e+1, (i, j), section=s+1, transform=1)



def create_brace_fixed(model, nodes, tags):
    """
    Create ne brace elements and 2 gusset elements, which requires ne+1 nodes.
    The first gusset element goes from i to n+1, and the second from n+ne+1 to j.
    The brace elements go from n+1 to n+ne+1.
    """
    n = max(tags["nodes"])
    e = max(tags["elements"])
    s = max(tags["sections"])
    ne = 5
    # Joint offset (bot, top)
    offset =  34.43*inch, 28.68*inch,

    #
    # Sections
    #
    # Reserve a new section tag
    tags["sections"].extend([s+1])
    # Load the section geometry
    shape = from_aisc("HSS10x10x5/8", units=units, mesh_scale=1/2.5)
    # Create the section in the model
    model.section("ShearFiber", s+1)

    # Populate the section with fibers using the shape. The 
    # mesh_scale parameter controls the number of generated fibers.
    # This will roughly create 2.5 fibers across the smallest dimension
    # of the section.
    for fiber in shape.create_fibers(origin="centroid"):
        model.fiber(**fiber, material=1, section=s+1)

    #
    # Nodes
    #

    # Get the coordinates of the nodes
    xi = np.array(model.nodeCoord(nodes[0]))
    xj = np.array(model.nodeCoord(nodes[1]))

    slope = xj - xi
    slope /= np.linalg.norm(slope)

    # Create the nodes
    for i, x in enumerate(np.linspace(xi+offset[0]*slope, xj-offset[1]*slope, ne+1)):
        tags["nodes"].extend([n+i+1])
        model.node(n+i+1, tuple(x.tolist()))

    #
    # Elements
    #
    # Create the gusset elements
    tags["elements"].extend([e+1, e+2])
    model.element("ForceFrame", e+1, (nodes[0],    n+1), section=s+1, transform=1)
    model.element("ForceFrame", e+2, (n+ne+1, nodes[1]), section=s+1, transform=1)

    # Create the flexible elements
    for i in range(ne):
        # Reserve a new element tag
        tags["elements"].extend([e+i+3])
        model.element("ForceFrame", e+i+3, (n+i+1, n+i+2), section=s+1, transform=1)

def create_brace_hinged(model, nodes, tags):
    n = max(tags["nodes"])
    e = max(tags["elements"])
    s = max(tags["sections"])

    #
    # Nodes
    #
    # First we duplicate the given i and j nodes so that we can created
    # "pinned" connections at the ends of the brace (ie, no moment transfer).

    i = nodes[0]
    j = nodes[1]
    # Get the coordinates of the nodes that we'll copy
    xi = model.nodeCoord(i)
    xj = model.nodeCoord(j)
    # Reserve two new node tags
    tags["nodes"].extend([n+1, n+2])
    # Create the duplicate nodes
    model.node(n+1, tuple(xi))
    model.node(n+2, tuple(xj))
    # Constrain the translational DOFs of the new nodes to be
    # equal to the original nodes.
    model.equalDOF(i, n+1, (1,2,3))
    model.equalDOF(j, n+2, (1,2,3))

    #
    # Sections
    #
    # Reserve a new section tag
    tags["sections"].extend([s+1])
    # Load the section geometry
    shape = from_aisc("HSS10x10x5/8", units=units, mesh_scale=1/2.5)
    # Create the section in the model
    model.section("ShearFiber", s+1)
    # Populate the section with fibers using the shape. The 
    # mesh_scale parameter controls the number of generated fibers.
    # This will roughly create 2.5 fibers across the smallest dimension
    # of the section.
    for fiber in shape.create_fibers(origin="centroid"):
        model.fiber(**fiber, material=1, section=s+1)

    #
    # Elements
    #
    # Reserve a new element tag
    tags["elements"].extend([e+1])
    # Create the element using the new nodes (n+1 and n+2) and the section (s+1)
    model.element("ForceFrame", e+1, (n+1, n+2), section=s+1, transform=1)


def create_portal():
    E = 29e3*ksi
    fy = 50*ksi
    nu = 0.3
    K = E/(3*(1-2*nu))
    G = 0.5*E/(1+nu)

    width  = 360*inch
    height = 180*inch

    model = xara.Model(ndm=3, ndf=6)

    tags = {
        "nodes": [1, 2, 3, 4, 5],
        "elements": [0],
        "sections": [0],
        "materials": [0]
    }


    model.nDMaterial('J2BeamFiber', 1, E, nu, fy, 0.01*E, 0.0)
    # model.material("ElasticIsotropic", 1, E, nu)


    model.node(1, (      0,      0, 0))
    model.node(2, (  width,      0, 0))
    model.node(3, (      0, height, 0))
    model.node(4, (width/2, height, 0))
    model.node(5, (  width, height, 0))

    model.fix(1, (1, 1, 1, 1, 1, 1))
    model.fix(2, (1, 1, 1, 1, 1, 1))

    model.geomTransf("Linear", 1, (1, 0, 0))
    model.geomTransf("Linear", 2, (0, 1, 0))
    model.geomTransf("Linear", 3, (0, 0, 1))


    # Create elements using helper functions
    create_girder(model, (3, 4), tags)
    create_girder(model, (5, 4), tags)

    create_column(model, (1, 3), tags)
    create_column(model, (2, 5), tags)

    create_brace_fixed(model, (1, 4), tags)
    create_brace_fixed(model, (2, 4), tags)

    return model


def pushover_analysis(model):
    model.pattern("Plain", 1, "Linear", loads={3: (50*kip, 1*kip, 0,  0, 0, 0)})
    model.integrator("LoadControl", 1)
    model.test("NormDispIncr", 1.0e-8, 20, 0)
    model.analysis("Static")

    artist = veux.create_artist(model, vertical=2)

    motion = Motion(artist)

    u = []
    p = []

    for i in range(1, 100):
        if model.analyze(1) != 0:
            break
        print(model.getTime())
        u.append(model.nodeDisp(5, 1))
        p.append(model.getTime())
        motion.advance(time=model.getTime()/50)
        motion.draw_sections(rotation=model.nodeRotation, position=model.nodeDisp)


    fig, ax = plt.subplots()
    ax.plot(u,p)
    fig.savefig("img/pushover.png")
    plt.show()

    motion.add_to(artist.canvas)
    return artist


if __name__ == "__main__":

    analyze = True

    model = create_portal()

    if analyze:
        pushover_analysis(model)

        artist = veux.create_artist(model)
        artist.draw_nodes()
        artist.draw_outlines(state=model.nodeDisp, scale=1)
        veux.serve(artist)
    else:

        artist = veux.create_artist(model)
        artist.draw_nodes()
        artist.draw_axes(extrude=True)
        artist.draw_sections()
        veux.serve(artist)

