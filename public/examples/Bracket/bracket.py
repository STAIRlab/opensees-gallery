import sys
import json
import opensees.openseespy as ops

def run(filename):
    with open(filename, "r") as f:
        mesh = json.load(f)

    model = ops.Model(ndm=3, ndf=3)
    for node,coord in enumerate(mesh["coordinates"]):
        model.node(int(node), *coord)

#                               matTag  E     nu   rho
    model.nDMaterial("ElasticIsotropic", 1, 100.0, 0.25, 1.27)

    for elem, conn in enumerate(mesh["elements"][0]["cells"]):
#       print(len(conn))
        model.element("stdBrick", elem, *conn, 1)

    model.export("model.vtk")
    model.print("-json", "model.json")

run(sys.argv[1])
