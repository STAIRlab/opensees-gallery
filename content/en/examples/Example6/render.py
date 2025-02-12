import veux
from veux.stress import node_average
from opensees.helpers import find_node, find_nodes
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
        stress = {node: stress["sxx"] for node, stress in node_average(model, "stressAtNodes").items()}
        artist = veux.create_artist(model)
#       artist.draw_outlines()
        artist.draw_surfaces(state=model.nodeDisp,
                             field=stress,
                             scale=10
        )
        artist.draw_outlines(state=model.nodeDisp,
                             scale=10
        )

#       veux.serve(artist)
        artist.save(dir/f"{element}-displaced.glb")

