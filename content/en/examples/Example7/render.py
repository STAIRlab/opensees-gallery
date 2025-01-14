import veux

if __name__ == "__main__":
    from Example7 import create_model, static_analysis

    model = create_model()
    static_analysis(model)

    #
    # Render the model in the undeformed state
    #

    model_config = {
        "extrude_outline": "square",
        "extrude_scale": 2.0
    }
    artist = veux.render(model,
                         show={"frame.surface", "plane.surface"},
                         model_config=model_config)

    # Save the rendering using the GLTF2.0 format
    veux.serve(artist)
#   artist.save("model.glb")

    #
    # Render the deformed state of the structure
    #
    artist = veux.render(model, model.nodeDisp,
                         canvas="gltf",
                         scale=200,
                         reference={"plane.outline"},
                         displaced={"plane.surface", "plane.outline"},
    )

    veux.serve(artist)
#   artist.save("gravity.glb")

