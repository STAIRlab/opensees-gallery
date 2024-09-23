import sees
import opensees.openseespy as ops

def render_model(model, file_name, canvas="plotly"):

    # Create the rendering
    artist = sees.render(model, show={"frame.axes"}, canvas=canvas)

    if file_name is not None:
        # Finally, save the rendering to the requested file
        artist.save(file_name)
    else:
        sees.serve(artist)



def render_mode(model, mode_number, mode_scale, file_name=None, canvas="plotly"):

    # Define a function that tells the renderer the displacement
    # at a given node. This will be invoked for each node
    def displ_func(tag: int)->list:
        return [float(mode_scale)*ui for ui in model.nodeEigenvector(tag, mode_number)]

    # Create the rendering
    artist = sees.render(model, displ_func, canvas=canvas)

    # Finally, save the rendering to the requested file
    if file_name is not None:
        artist.save(file_name)
    else:
        sees.serve(artist)


if __name__ == "__main__":
    import sys
    model = ops.Model()
    with open(sys.argv[1], "r") as f:
        model.eval(f.read())

    save_file = None
    if len(sys.argv) == 2:
       render_model(model, save_file)

    else:
        mode = int(sys.argv[2])

        if len(sys.argv) > 3:
            scale = float(sys.argv[3])
        else:
            scale = 100

        model.eigen(mode)

        for node in model.getNodeTags():
            print(node, model.nodeEigenvector(node, mode))

        render_mode(model, mode, scale, save_file)


