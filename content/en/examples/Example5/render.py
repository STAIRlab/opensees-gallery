
import sees
from Example5 import create_model, analyze

if __name__ == "__main__":

    model = create_model()
    ok = analyze(model)

    if (ok != 0):
        print("analysis FAILED")

    else:
        print("analysis SUCCESSFUL")


        # Plot the deformed state of the structure

        artist = sees.render(model, vertical=3, canvas="gltf")
        artist = sees.render(model, model.nodeDisp, vertical=3, canvas=artist.canvas)

        artist.save("displaced.glb")
#       sees.serve(artist)

