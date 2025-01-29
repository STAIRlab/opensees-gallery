import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import pandas as pd
import xlsxwriter

import warnings
import shutup; shutup.please()

start_total = datetime.datetime.now()

plt.close('all')

import readGM
import model3D

# List of RSN numbers and scaling factors
rsn_numbers = [15, 20, 31, 68, 289, 740, 827, 864, 1083, 4013, 4844]
# rsn_numbers = [289]
peer_scaling = [3.4404, 1.7763, 5.3947, 2.6261, 2.4678, 4.7919, 2.7061, 1.4524, 3.2421, 4.0212, 3.4858]
# peer_scaling = [2.4678]
# List of slab points
# slab_points = ['Midpoint', 'Near column', 'Near beam']
slab_points = ['Slab 1 Column fnsc 10']
# Iterate over each slab point

n_modes = 20; plot_mode_shapes=False
m_nsc = 20; f_nsc = 10


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
for slab_point in slab_points:
    # Define path for the Excel file
    output_file_path = f'{slab_point} results.xlsx'


    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:

        # Iterate over multiple story levels
        for story_level, target_coord in zip(story_levels, target_coords):
            results = []
            counter = 0

            for RSN_num, scale_factor in zip(rsn_numbers, peer_scaling):

                start_ind = datetime.datetime.now()

                z_h = 3.0 * story_level + 1
                file_name = f'RSN{RSN_num}-UP.txt'
                dt, npts, eq_data = readGM.readGM_txt(file_name)
                PGA = 9.81 * scale_factor * np.max(np.absolute(eq_data))




                max_NSCacc, max_slabacc = model3D.dynamic_analysis(spacing, num_bay_x, num_bay_y, num_story, target_coord,
                                         length_x, length_y, length_z,
                                         n_modes, plot_mode_shapes,
                                         dt, npts, eq_data, m_nsc, RSN_num, f_nsc, counter, slab_point, scale_factor)

                warnings.filterwarnings('ignore')

                PFA = max_slabacc
                PCA = max_NSCacc
                PFA_PGA = PFA / PGA if PGA != 0 else 'DIV/0!'
                PCA_PGA = PCA / PGA if PGA != 0 else 'DIV/0!'
                PCA_PFA = PCA / PFA if PFA != 0 else 'DIV/0!'

                results.append([RSN_num, 'GM', z_h, PGA, PFA, PCA, PFA_PGA, PCA_PGA, PCA_PFA])
                counter += 1
                end_ind = datetime.datetime.now()




            print(f"Analysis for Story Level {story_level}")
            # Create a DataFrame from the results
            df = pd.DataFrame(results, columns=['RSN', 'GM', 'z/h', 'PGA [m/s^2]', 'PFA [m/s^2]', 'PCA [m/s^2]', 'PFA/PGA', 'PCA/PGA', 'PCA/PFA'])

            # Sheet name based on the story level
            sheet_name = f'Story {story_level}'
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Data saved to {output_file_path}")

end_total = datetime.datetime.now()


print('Execution time: {end_total - start_total} seconds')
