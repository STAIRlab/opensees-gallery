# %%
# ---
# jupyter:
#   jupytext:
#     cell_markers: '"""'
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
"""
# Defining a Model

This section demonstrates the model definition process.

## Model Definition Overview

The overall procedure for defining the elements of a model can be
broken down into the following steps:

- Set active levels

- Define components

- Execute pre-processing methods

The model can be visualized at any step in the process to confirm its validity.

**To see all the available arguments of each of the following methods,
please read the API reference or their docstrings**.

Alternatively, use the `help()` function inside a python shell.
e.g. `help(mdl.add_level)`

You can also use `pydoc <osmg.name_of_module>` in a terminal window.
"""

# %%
# imports
import numpy as np
from osmg import model
import osmg.defaults as defaults
from osmg.gen.section_gen import SectionGenerator
from osmg.ops.section import ElasticSection
from osmg.gen.component_gen import BeamColumnGenerator
from osmg.ops.element import ElasticBeamColumn
from osmg.graphics.preprocessing_3d import show

# %%
# Instantiate a model
mdl = model.Model('example_model')
# help(mdl.add_level)

# %%
# Define levels.  Note: the first floor is index 0; then second floor is 
mdl.add_level(1, 0.00)                                  # 1st Floor
mdl.add_level(2, 20*12.00)                              # 2nd Floor
mdl.add_level(3, (20+14)*12.00)                         # 3rd Floor
mdl.add_level(4, (34+15)*12.00)                         # 4th Floor
mdl.add_level(5, (49+15)*12.00)                         # 5th Floor
for i in range(6,50):                                   # 6th-49th Floor
    mdl.add_level(i, (64+13*(i-4))*12.00)               
mdl.add_level(50, (64+13*(44)+25)*12.00)                # 50th Floor
mdl.add_level(51, (64+13*(44)+25+19)*12.00)             # 51st Floor
mdl.add_level(52, (64+13*(44)+25+19+18)*12.00)          # 52nd Floor
mdl.add_level(53, (64+13*(44)+25+19+18+18)*12.00)       # Roof

# %%
defaults.load_default_steel(mdl)
steel_phys_mat = mdl.physical_materials.retrieve_by_attr(
    'name', 'default steel')

# %%
# define line element sections
secg = SectionGenerator(mdl)
secg.load_aisc_from_database(
    'W',
    ["W24X94"],
    'default steel',
    'default steel',
    ElasticSection)


# %%
# Up to 45th floor
mdl.levels.set_active(range(1,46))         # Up to 45th floor

points = 12.0*np.array([[20.0,  0.00 ],
                        [65.0,  0.00 ],
                        [68.0,  3.00 ],
                        [88.0,  3.00 ],
                        [91.0,  0.00 ],
                        [136.0, 0.00 ],
                        [156.0, 20.0 ],
                        [156.0, 65.0 ],
                        [153.0, 68.0 ],
                        [153.0, 88.0 ],
                        [156.0, 91.0 ],
                        [156.0, 136.0],
                        [136.0, 156.0],
                        [91.0,  156.0],
                        [88.0,  153.0],
                        [68.0,  153.0],
                        [65.0,  156.0],
                        [20.0,  156.0],
                        [0.00,  136.0],
                        [0.00,  91.0 ],
                        [3.00,  88.0 ],
                        [3.00,  68.0 ],
                        [0.00,  65.0 ],
                        [0.00,  20.0 ],
                ])
npts = points.shape[0]

mcg = BeamColumnGenerator(mdl)
sec = mdl.elastic_sections.retrieve_by_attr('name', 'W24X94')
for pt in points:
    mcg.add_vertical_active(
        x_coord=pt[0], y_coord=pt[1],
        offset_i=np.zeros(3), offset_j=np.zeros(3),
        transf_type='Corotational',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='centroid',
        angle=0.00)

for i in range(npts):
    if i < npts-1:
        pair = (points[i],points[i+1])
    else:
        pair = (points[i],points[0])
    mcg.add_horizontal_active(
        xi_coord=pair[0][0],
        yi_coord=pair[0][1],
        xj_coord=pair[1][0],
        yj_coord=pair[1][1],
        offset_i=np.zeros(3),
        offset_j=np.zeros(3),
        snap_i='centroid',
        snap_j='centroid',
        transf_type='Linear',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='top_center',
        angle=0.00)


# %%
# 46th through 50th floor
mdl.levels.set_active(range(46,51))         # 46th through 50th floor

points = 12.0*np.array([[60.0,  10.00 ],
                        [65.0,  10.00 ],
                        [68.0,  13.00 ],
                        [88.0,  13.00 ],
                        [91.0,  10.00 ],
                        [96.0,  10.00 ],
                        [146.0, 60.0 ],
                        [146.0, 65.0 ],
                        [143.0, 68.0 ],
                        [143.0, 88.0 ],
                        [146.0, 91.0 ],
                        [146.0, 96.0 ],
                        [96.0,  146.0],
                        [91.0,  146.0],
                        [88.0,  143.0],
                        [68.0,  143.0],
                        [65.0,  146.0],
                        [60.0,  146.0],
                        [10.00,  96.0 ],
                        [10.00,  91.0 ],
                        [13.00,  88.0 ],
                        [13.00,  68.0 ],
                        [10.00,  65.0 ],
                        [10.00,  60.0 ],
                ])
npts = points.shape[0]

for pt in points:
    mcg.add_vertical_active(
        x_coord=pt[0], y_coord=pt[1],
        offset_i=np.zeros(3), offset_j=np.zeros(3),
        transf_type='Corotational',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='centroid',
        angle=0.00)
    
for i in range(npts):
    if i < npts-1:
        pair = (points[i],points[i+1])
    else:
        pair = (points[i],points[0])
    mcg.add_horizontal_active(
        xi_coord=pair[0][0],
        yi_coord=pair[0][1],
        xj_coord=pair[1][0],
        yj_coord=pair[1][1],
        offset_i=np.zeros(3),
        offset_j=np.zeros(3),
        snap_i='centroid',
        snap_j='centroid',
        transf_type='Linear',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='top_center',
        angle=0.00)



# %%
# 51st floor
mdl.levels.set_active([51])         # 51st floor

points = 12.0*np.array([[70.0,  15.0 ],
                        [86.0,  15.0 ],
                        [141.0, 73.0 ],
                        [141.0, 86.0 ],
                        [86.0,  141.0],
                        [73.0,  141.0],
                        [15.0,  86.0 ],
                        [15.0,  73.0 ],
                ])
npts = points.shape[0]

for pt in points:
    mcg.add_vertical_active(
        x_coord=pt[0], y_coord=pt[1],
        offset_i=np.zeros(3), offset_j=np.zeros(3),
        transf_type='Corotational',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='centroid',
        angle=0.00)
    
for i in range(npts):
    if i < npts-1:
        pair = (points[i],points[i+1])
    else:
        pair = (points[i],points[0])
    mcg.add_horizontal_active(
        xi_coord=pair[0][0],
        yi_coord=pair[0][1],
        xj_coord=pair[1][0],
        yj_coord=pair[1][1],
        offset_i=np.zeros(3),
        offset_j=np.zeros(3),
        snap_i='centroid',
        snap_j='centroid',
        transf_type='Linear',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='top_center',
        angle=0.00)
    

# %%
# 52nd floor
mdl.levels.set_active([52])         # 52nd floor

points = 12.0*np.array([[73.0,  20.0 ],
                        [83.0,  20.0 ],
                        [136.0, 73.0 ],
                        [136.0, 83.0 ],
                        [83.0,  136.0],
                        [73.0,  136.0],
                        [20.0,  83.0 ],
                        [20.0,  73.0 ],
                ])
npts = points.shape[0]

for pt in points:
    mcg.add_vertical_active(
        x_coord=pt[0], y_coord=pt[1],
        offset_i=np.zeros(3), offset_j=np.zeros(3),
        transf_type='Corotational',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='centroid',
        angle=0.00)
    
for i in range(npts):
    if i < npts-1:
        pair = (points[i],points[i+1])
    else:
        pair = (points[i],points[0])
    mcg.add_horizontal_active(
        xi_coord=pair[0][0],
        yi_coord=pair[0][1],
        xj_coord=pair[1][0],
        yj_coord=pair[1][1],
        offset_i=np.zeros(3),
        offset_j=np.zeros(3),
        snap_i='centroid',
        snap_j='centroid',
        transf_type='Linear',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='top_center',
        angle=0.00)


# %%
# Roof
mdl.levels.set_active([53])         # Roof

points = 12.0*np.array([[76.0,  25.0 ],
                        [80.0,  25.0 ],
                        [131.0, 76.0 ],
                        [131.0, 80.0 ],
                        [80.0,  131.0],
                        [76.0,  131.0],
                        [25.0,  80.0 ],
                        [25.0,  76.0 ],
                ])
npts = points.shape[0]

for pt in points:
    mcg.add_vertical_active(
        x_coord=pt[0], y_coord=pt[1],
        offset_i=np.zeros(3), offset_j=np.zeros(3),
        transf_type='Corotational',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='centroid',
        angle=0.00)
    
for i in range(npts):
    if i < npts-1:
        pair = (points[i],points[i+1])
    else:
        pair = (points[i],points[0])
    mcg.add_horizontal_active(
        xi_coord=pair[0][0],
        yi_coord=pair[0][1],
        xj_coord=pair[1][0],
        yj_coord=pair[1][1],
        offset_i=np.zeros(3),
        offset_j=np.zeros(3),
        snap_i='centroid',
        snap_j='centroid',
        transf_type='Linear',
        n_sub=4,
        section=sec,
        element_type=ElasticBeamColumn,
        placement='top_center',
        angle=0.00)


# %%
# fixing the base
for node in mdl.levels[1].nodes.values():
    node.restraint = [True, True, True, False, False, False]



# %% [markdown]
"""
## Preprocessing
"""

# %% [markdown]
"""
Now that all the intended elements have been defined, we can apply
pre-processing methods to the model.

Some common methods are the following:

* `rigid_diaphragms` assigns rigid diaphragm constraints to all
  specified levels. Only primary nodes are affected (not internal
  nodes of component assemblies).

* `self_weight`, `self_mass` assign self-weight loads and lumped
  self-mass to all the elements / nodes.

Loads, mass, and diaphragm constraints are load_case-specific.
"""


# %%
# imports
from osmg.load_case import LoadCase
from osmg.preprocessing.self_weight_mass import self_weight
from osmg.preprocessing.self_weight_mass import self_mass


# %%
testcase = LoadCase('test', mdl)


# %%
self_weight(mdl, testcase)
self_mass(mdl, testcase)


# %%
testcase.rigid_diaphragms(range(1,53))


# %%
# visualize the model and add mode shapes
fig = show(mdl, testcase, extrude=True, global_axes=False)
fig.update_layout(legend = dict(font=dict(size=20, family="Times")))
fig.write_html("out/twin.html")

import json
with open('out/shape_summary_table.json', 'r') as readfile:
    shape_summary_table = json.load(readfile)
shapes = [value['FDD'] for value in shape_summary_table.values()]
dates = list(shape_summary_table.keys())
channel_numbers = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
instrumented_floors = [14,22,35,49,53]
n_instrumented_floors = len(instrumented_floors)
north_core_channels = [9,11,14,17,20]       # Direction 1
north_outr_channels = [9,12,15,18,20]       # Direction 1
east_core_channels  = [8,10,13,16,19]       # Direction 2
core_coordinates = (156.0*12/2, 156.0*12/2)
outr_coordinates = (156.0*12, 156.0*12/2)

import plotly.graph_objects as go
from numpy import array as arr
level_heights = [mdl.levels[level].elevation for level in instrumented_floors]
# list_of_nodes = testcase.parent_nodes.values()
x_core_coords = arr([core_coordinates[0], *[core_coordinates[0] for height in level_heights]])
x_outr_coords = arr([156.0,156.0,156.0,156.0,146.0,131.0])*12
y_coords = arr([core_coordinates[1], *[core_coordinates[1] for height in level_heights]])
z_coords = arr([0, *level_heights])

MODE_SCALE = 2e3

fig.add_trace(go.Scatter3d(x=x_core_coords, y=y_coords, z=z_coords, name=f"core channels", mode="lines", opacity=1, line={'width':8, 'color':'gray'}))
for date,shape in zip(dates,shapes):
    # Core
    x_shape = x_core_coords + MODE_SCALE*arr([0, *[shape[channel_numbers.index(c)] for c in east_core_channels]])
    y_shape = y_coords + MODE_SCALE*arr([0, *[shape[channel_numbers.index(c)] for c in north_core_channels]])
    z_shape = z_coords
    # fig.add_trace(go.Scatter3d(x=x_shape, y=y_shape, z=z_shape, name="mode shape", mode="lines", line_shape='spline', marker={'color':'red'}, line={'width':10}))
    fig.add_trace(go.Scatter3d(x=x_shape, y=y_shape, z=z_shape, name=f"{date}", mode="lines", line={'width':8}))
fig.write_html("out/modes_core.html")

fig = show(mdl, testcase, extrude=True, global_axes=False)
fig.update_layout(legend = dict(font=dict(size=20, family="Times")))
fig.add_trace(go.Scatter3d(x=x_outr_coords, y=y_coords, z=z_coords, name=f"slab edge channels", mode="lines", opacity=1, line={'width':8, 'color':'gray'}))
for date,shape in zip(dates,shapes):
    # Outrigger
    x_shape = x_outr_coords + MODE_SCALE*arr([0, *[shape[channel_numbers.index(c)] for c in east_core_channels]])
    y_shape = y_coords + MODE_SCALE*arr([0, *[shape[channel_numbers.index(c)] for c in north_outr_channels]])
    z_shape = z_coords
    fig.add_trace(go.Scatter3d(x=x_shape, y=y_shape, z=z_shape, name=f"{date}", mode="lines", line={'width':8}))
fig.write_html("out/modes_slab.html")

# # %%
# # make a modal analysis load case
# modalcase = LoadCase('modal', mdl)
# self_mass(mdl, modalcase)
# modalcase.rigid_diaphragms(range(1,53))

# # %%
# # solve the modal analysis
# from osmg import solver
# modal_analysis = solver.ModalAnalysis(
#     mdl, {modalcase.name: modalcase}, num_modes=4)
# modal_analysis.run()

# # %%
# # modal analysis results
# print(modal_analysis.results[modalcase.name].periods)

# # %%
# # mode shapes
# from osmg.graphics.postprocessing_3d import show_deformed_shape
# show_deformed_shape(
#     modal_analysis, modalcase.name, 3, 0.00,
#     extrude=False, animation=False)
# %%
