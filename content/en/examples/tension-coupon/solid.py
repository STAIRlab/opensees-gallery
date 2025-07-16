import xara
import veux
import numpy as np
from veux.config import NodeStyle, MeshStyle
from xara.helpers import find_nodes
from xara.post import NodalStress
from openbim.inp import create_model, parser, Part
import matplotlib.pyplot as plt
try:
    plt.style.use("veux-web")
except:
    pass

if __name__ == "__main__":
    L = 0.084 - -0.084
    h = 0.008*2
    w = 0.005
    A = 0.005*(0.008*2)

    model = xara.Model(ndm=3, ndf=3)

    model.nDMaterial("J2", 1, Fy=60, E=29e3, nu=0.27, Hiso=0.005*29e3, Fsat=90, Hsat=16.93)
    # model.nDMaterial("ElasticIsotropic", 1, E=29e3, nu=0.27)

    part = Part(parser.load("coupon.inp"))
    for node in part.find_nodes():
        model.node(node.id, node.location)

    face_j = [node for node in find_nodes(model, x=+0.084)]
    face_i = [node for node in find_nodes(model, x=-0.084)]

    for cell in part.find_cells():
        model.element("bbarBrick", cell.id, cell.nodes, 1)
#       model.element("stdBrick", cell.id, cell.nodes, 1)

    for node in face_i:
        model.fix(node, (1, 1, 1))

    model.pattern("Plain", 1, "Linear")

    yi, yj =  0.000, 0.005
    zi, zj = -0.008, 0.008
    for node in face_j:
        if model.nodeCoord(node, 2) in {yi, yj} and model.nodeCoord(node, 3) in {zi, zj}:
            model.load(node,  (1/4, 0, 0), pattern=1)
            continue

        if model.nodeCoord(node, 2) in {yi, yj}  or model.nodeCoord(node, 3) in {zi, zj}:
            model.load(node,  (1/2, 0, 0), pattern=1)
            continue

        model.load(node, (1, 0, 0), pattern=1)

    steps = 50
    model.integrator("LoadControl", 3/2*(60*A)/(steps*len(face_j)))
    model.test("NormDispIncr", 1e-10, 20, 2)
    model.system("Umfpack")
    model.analysis("Static")

    u,p = [], []
    for i in range(steps): # 15
        if model.analyze(1) != 0:
            print(f"Analysis failed at time = {model.getTime()}")
            break

        u.append(model.nodeDisp(node,1))
        p.append(model.getTime())

    artist = veux.create_artist(model, ndm=3, ndf=3)

    for node in face_i:
        artist.canvas.plot_nodes([model.nodeCoord(node)], style=NodeStyle(color="black", scale=1/200))
    for node in face_j:
        artist.canvas.plot_nodes([np.array(model.nodeCoord(node))+model.nodeDisp(node)], style=NodeStyle(color="red", scale=1/200))

    # artist.draw_surfaces(style=MeshStyle(color="gray", alpha=0.5))
    # artist.draw_nodes()
    artist.draw_surfaces(state=model.nodeDisp,
                        field=NodalStress(model, "sxx"),
                        style=MeshStyle(color="white")
                        )
    veux.serve(artist)
#   try:
#   except:
#       pass

    plt.plot(u, p)
    plt.savefig("img/plot.png")
    plt.show()
