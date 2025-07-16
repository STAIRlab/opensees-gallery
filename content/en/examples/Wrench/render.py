import veux
from veux.stress import node_average
from model import create_wrench

if __name__ == "__main__":
    model = create_wrench()
    #model.eigen(1)
    model.analysis("Static")
    model.integrator("LoadControl", 0.05)
    model.analyze(1)

    n = 1
    #veux.serve(veux.render(model, lambda i: model.nodeEigenvector(i, n)))
    stress = {node: stress["sxx"] for node, stress in node_average(model, "stressAtNodes").items()}
    artist = veux.create_artist(model, canvas="gltf")
    artist.draw_surfaces(state=lambda i: [10*u for u in model.nodeDisp(i)],
                         field=stress)
    veux.serve(artist)

