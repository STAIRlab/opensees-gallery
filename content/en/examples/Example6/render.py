import veux
from pathlib import Path

if __name__ == "__main__":
    from Example6 import create_model, static_analysis

    dir = Path(".")
    for element in "quad",:# "SSPquad", "bbarQuad", "enhancedQuad":

        model, (l1, l2) = create_model()
        static_analysis(model)

        #
        # Render the model in the undeformed state
        #
        artist = veux.render(model, canvas="gltf")

        # Save the rendering using the GLTF2.0 format
#       artist.save(dir/f"{element}.glb")
        veux.serve(artist)

        #
        # Render the deformed state of the structure
        #
        state = {i: model.nodeDisp(i) for i in model.getNodeTags()}
        artist = veux.render(model, model.nodeDisp,
                             canvas="gltf",
                             scale=10,
                             displaced={"plane.outline"}
        )

        veux.serve(artist)
#       artist.save(dir/f"{element}-displaced.glb")

