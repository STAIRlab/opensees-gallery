import sees

if __name__ == "__main__":
    from Example7 import create_model, static_analysis

    model = create_model()
    static_analysis(model)

    #
    # Render the model in the undeformed state
    #
    artist = sees.render(model, canvas="gltf")

    # Save the rendering using the GLTF2.0 format
#   sees.serve(artist)
    artist.save("model.glb")

    #
    # Render the deformed state of the structure
    #
    artist = sees.render(model, model.nodeDisp,
                         canvas="gltf",
                         scale=200,
                         verbose=True,
                         reference={"plane.outline"},
                         displaced={"plane.surface", "plane.outline"},
    )

#   sees.serve(artist)
    artist.save("gravity.glb")

