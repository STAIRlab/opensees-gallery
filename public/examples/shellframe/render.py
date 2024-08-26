import os
import json
from pathlib import Path

import numpy as np
import pandas as pd
import sees



import model3D
#import model3D_Oregon as model3D


def render_model(model, file_name):

    temp_file = f"{file_name}.json"
    model.printModel("-JSON", "-file", temp_file)

    # Read in the JSON that OpenSees created
    with open(temp_file, "r") as f:
        model_dict = json.load(f)

    os.remove(temp_file)

    # Create the rendering
    artist = sees.render(model_dict,
                         vertical=3,
                         canvas="plotly") #"gltf")

    # Finally, save the rendering to the requested file
#   artist.save(file_name)
    sees.serve(artist)


def render_mode(model, mode_number, mode_scale, file_name):

    # Define a function that tells the renderer the displacement
    # at a given node. This will be invoked for each node
    def displ_func(tag):
        return [float(mode_scale)*ui for ui in model.nodeEigenvector(tag, mode_number)]


    temp_file = f"{file_name}.json"
    model.printModel("-JSON", "-file", temp_file)

    # Read in the JSON that OpenSees created
    with open(temp_file, "r") as f:
        model_dict = json.load(f)

    os.remove(temp_file)

    # Create the rendering
    artist = sees.render(model_dict, displ_func,
                         vertical=3,
                         canvas="gltf")

    # Finally, save the rendering to the requested file
    if file_name is not None:
        artist.save(file_name)
    else:
        sees.serve(artist)


# List of RSN numbers and scaling factors
rsn_numbers = [15, 20, 31, 68, 289, 740, 827, 864, 1083, 4013, 4844]
# rsn_numbers = [289]
peer_scaling = [3.4404, 1.7763, 5.3947, 2.6261, 2.4678, 4.7919, 2.7061, 1.4524, 3.2421, 4.0212, 3.4858]
# peer_scaling = [2.4678]
# List of slab points
# slab_points = ['Midpoint', 'Near column', 'Near beam']
slab_points = ['Slab 1 Column fnsc 10']
# Iterate over each slab point

n_modes = 20
plot_mode_shapes = True
m_nsc = 20
f_nsc = 10


spacing = 1
num_bay_x = 4
num_bay_y = 4
length_x = 8
length_y = 6
length_z = 4
num_story = 3
story_levels = [1,2,3]

x = 8; y = 0
target_coords = [[x,y, length_z*3]] #[[x,y,3],[x,y,6],[x,y,9]]


n = 1

for num_story in 6,:
    if num_story ==6:
        story_levels = story_levels + [4, 5, 6]
        target_coords[0][2] *= 2

    for slab_point in slab_points:
        # Iterate over multiple story levels
        for story_level, target_coord in zip(story_levels, target_coords):
            results = []
            counter = 0

            # Render just the model
#           render_model(model, None)
            for RSN_num, scale_factor in zip(rsn_numbers, peer_scaling):

                model = model3D.create_model(spacing,
                                     num_bay_x, num_bay_y, num_story, target_coord,
                                     length_x, length_y, length_z,
                                     m_nsc, f_nsc, counter, slab_point)


                print(f"\t{model.eigen(n_modes)}")

                for m in reversed(range(1,n_modes)):
                    glb_file = Path("./renderings")/f"model-s{num_story}-m{m:02}.glb"


                    scale = 10_000.0 if m < 3 else 1000.0
                    if False:
                        # Pick an appropriate scaling factor for the current mode.
                        # These were selected empirically.
                        scales = {
                                3: 5000,
                                4: 1000,
                                5: 1000,
                                6: 1000,
                                7: 1000, # torsion
                                8:  500*(num_stories/3), # vertical
                                9:  500*(num_stories/3), # vertical
                        }
                        scale = scales.get(m, 10_000)

                    # Render the `m`th mode with a scale of `scale`
                    render_mode(model, mode_number=m, mode_scale=scale, file_name=glb_file)
                    print(glb_file)

                n += 1
                break

            break

