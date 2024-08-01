import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import pandas as pd
import sees
import json

start_total = datetime.datetime.now()

plt.close('all')

import model3D


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
                         canvas="gltf")

    # Finally, save the rendering to the requested file
    artist.save(file_name)

def render_mode(model, mode_number, mode_scale, file_name):
    model.eigen(mode_number)

    # Define a function that tells the renderer the displacement
    # at a given node. This will be invoked for each node
    def displ_func(tag):
        return [mode_scale*j for j in model.nodeEigenvector(tag, mode_number)]


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
plot_mode_shapes=False
m_nsc = 20
f_nsc = 10


spacing = 1
num_bay_x = 3
num_bay_y = 3
length_x = 6
length_y = 6
length_z = 3
num_story = 3
story_levels = [1,2,3]

x = 0; y = 0
target_coords = [[x,y,3],[x,y,6],[x,y,9]]

n = 1
for slab_point in slab_points:
    # Iterate over multiple story levels
    for story_level, target_coord in zip(story_levels, target_coords):
        results = []
        counter = 0

        for RSN_num, scale_factor in zip(rsn_numbers, peer_scaling):

            start_ind = datetime.datetime.now()

#           z_h = 3.0 * story_level + 1
#           file_name = f'RSN{RSN_num}-UP.txt'

#           max_NSCacc, max_slabacc = model3D.dynamic_analysis(
#                                    spacing, num_bay_x, num_bay_y, num_story, target_coord,
#                                    length_x, length_y, length_z,
#                                    n_modes, plot_mode_shapes,
#                                    dt, npts, eq_data, m_nsc, RSN_num,
#                                    f_nsc, counter, slab_point, scale_factor)

            model = model3D.create_model(spacing, num_bay_x, num_bay_y, num_story, target_coord,
                                 length_x, length_y, length_z,
                                 m_nsc, f_nsc, counter, slab_point)


            glb_file = f"model-{n:04}.glb"
            # Render just the model
#           render_model(model, glb_file)

            # Render the 2nd mode with a scale of 10
            render_mode(model, mode_number=1, mode_scale=1000, file_name=None) #glb_file)

            n += 1
            break

        break

