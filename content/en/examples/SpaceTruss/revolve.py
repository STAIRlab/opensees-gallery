
from math import pi, sin, cos, sqrt
import opensees.openseespy as ops

def dome120():
    # Number of repeated segments
    s  = 12
    # Number of nodes per segment
    n  = 4

    scale = 1/100

    r1 = 273.26*scale
    r2 = 492.12*scale
    r  = 625.59*scale

    h  = 275.59*scale
    h1 = 196.85*scale
    h2 = 118.11*scale

    c2 = cos(pi/s)
    s2 = sin(pi/s)

    nodes = {
            0: (   0 ,  0.0 , h ),
            1: (   r1,  0.0 , h1),
            2: (   r2,  0.0 , h2),
            3: (   r ,  0.0 , 0 ),
            4: (r2*c2, r2*s2, h2),
    }

    elems = [
            (0,   1),
            (1,   2),
            (2,   3),
            (3,   4),
            (2,   4),
            (1,   4),
            (1+n, 4),
            (1+n, 1),
            (3+n, 4),
            (2+n, 4),
            (1+n, 4)
    ]
    return nodes, elems, {3}, s, {0}


def dome600():
    # Number of repeated segments
    s = 24
    # Number of nodes per segment
    n = 9

    nodes = {
            1: ( 1.0, 0.0, 7.0) ,
            2: ( 1.0, 0.0, 7.5) ,
            3: ( 3.0, 0.0, 7.25) ,
            4: ( 5.0, 0.0, 6.75) ,
            5: ( 7.0, 0.0, 6.0) ,
            6: ( 9.0, 0.0, 5.0) ,
            7: (11.0, 0.0, 3.5) ,
            8: (13.0, 0.0, 1.5) ,
            9: (14.0, 0.0, 0.0)
    }

    elems = [
        (1, 2),
        (1, 3),
        (1, 1+n),
        (1, 2+n),
        (2, 3),
        (2, 2+n),
        (3, 2+n),
        (3, 3+n),
        (3, 4),
        (4, 3+n),
        (4, 4+n),
        (4, 5),
        (5, 4+n),
        (5, 5+n),
        (5, 6),
        (6, 5+n),
        (6, 6+n),
        (6, 7),
        (7, 6+n),
        (7, 7+n),
        (7, 8),
        (8, 7+n),
        (8, 8+n),
        (8, 9),
        (9, 8+n)
    ]

    return nodes, elems, {9}, s, {}


def revolve(ref_nodes, ref_elems, fixed, count, key_nodes=None):

    nodes = {}
    elems = []
    if key_nodes is None:
        key_nodes = set()

    nn = len(ref_nodes) - len(key_nodes)

    for i in range(count):
        angle = 2*pi*i/count
        cs = cos(angle)
        sn = sin(angle)

        if 0 in ref_nodes:
            node = ref_nodes[0]
            nodes[0] = (cs*node[0] - sn*node[1],
                        sn*node[0] + cs*node[1],
                           node[2])

        # Create nodes
        for j,node in ref_nodes.items():
            if j:
                nodes[j+i*nn] = (cs*node[0] - sn*node[1],
                                 sn*node[0] + cs*node[1],
                                    node[2])


            for elem in ref_elems:
                elems.append(tuple(
                    node if node in key_nodes else (node-1+i*nn)%(count*nn)+1 for node in elem
                ))

    return nodes, elems


def create_truss(nodes, elems):
    model = ops.Model(ndm=3, ndf=3)
    model.uniaxialMaterial('Elastic', 1, 3000)  # Elastic material
    area = 1.0
    for tag, node in nodes.items():
        model.node(tag, node)

    for tag, nodes in enumerate(elems):
        model.element("Truss", tag, nodes, area, 1)

    return model

