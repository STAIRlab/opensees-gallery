#
# Adapted from a model by Goktug Tufekci
#
import sys
import math
from pathlib import Path

import numpy as np

import opensees.openseespy as ops


class ElasticSection:
    def __init__(self,
                 axial_area,
                 elastic_modulus,
                 shear_modulus,
                 torsional_constant,
                 moment_of_inertia_y,
                 moment_of_inertia_z):

        self.A       = axial_area
        self.E       = elastic_modulus
        self.G       = shear_modulus
        self.J       = torsional_constant
        self.Iweak   = moment_of_inertia_y
        self.Istrong = moment_of_inertia_z


class _Diaphragm:
    def __init__(self, elastic_modulus, poisson_ratio, thickness, density, mesh_size):
        self.E = elastic_modulus
        self.nu = poisson_ratio
        self.h = thickness
        self.rho = density
        self.mesh_size = mesh_size


def _target_node(model, target_coord):
    all_node_tags = model.getNodeTags()
    for node_id in all_node_tags:
        coord = np.array(model.nodeCoord(node_id))
        if np.array_equal(coord, np.array(target_coord)):
            return node_id
    return None


def _create_slabs(model, corner_nodes, slab_id, slab):
    """
    Create slab elements using corner nodes provided in groups of four.

    Parameters:
    corner_nodes (list): List of node IDs grouped by four, each group representing one slab.
    current_ele_id (int): Current starting element ID for slabs.
    slab_id (int): Current slab section ID.
    E_beam (float): Elastic modulus.
    nu (float): Poisson's ratio.
    h (float): Slab thickness.
    rho (float): Density of the slab material (set to zero if not needed).
    mesh_size (float): Mesh size for defining the line elements.
    """
    for i in range(0, len(corner_nodes), 4):
        if i + 3 < len(corner_nodes):

            model.section('ElasticMembranePlateSection', slab_id, slab.E, slab.nu, slab.h, slab.rho)
            points = {
                    j+1: model.nodeCoord(corner_nodes[i+j]) for j in range(4)
            }

            nx = int((points[2][0] - points[1][0])//slab.mesh_size)
            ny = int((points[3][1] - points[2][1])//slab.mesh_size)
            model.surface((nx,ny),
                  element="ShellMITC4", args=(1,),
                  points=points
            )


def _create_grid(model, modify, node_id, dimensions, subdivisions, base_z, spacing, eleTag,
            geoTag_counter, vecxz_to_geoTag,
            column, beam,
            node_map, column_set, beam_set,corners,corner_nodes):
    """
    Create nodes, columns, and beams in multiple square patterns in 3D space,
    with fixed nodes only at the ground level z = 0, and beams beginning from the first floor.

    Parameters:
    All parameters as previously defined, with the addition of:
    base_z (float): Base z-coordinate from which columns start.
    """
    length_x, length_y, length_z = dimensions
    num_bay_x, num_bay_y, num_story = subdivisions
    num_per_side_x = int(length_x / spacing) + 1
    num_per_side_y = int(length_y / spacing) + 1
    current_node_id = node_id
    current_ele_id = eleTag


    # Loop over the grid defined by num_bay_x and num_bay_y
    for ix in range(num_bay_x):
        for iy in range(num_bay_y):
            # Generate corners for each square at the base and subsequent levels
            for level in range(num_story-modify):  # Assuming two levels: ground and one above
                z = base_z + level * length_z
                for dx in [0, length_x]:
                    for dy in [0, length_y]:
                        x = ix * length_x + dx
                        y = iy * length_y + dy
                        coord = (x, y, z)
                        if coord not in node_map:
                            model.node(current_node_id, x, y, z)
                            node_map[coord] = current_node_id
                            if z == 0:  # Apply fixity only at the ground level
                                model.fix(current_node_id, 1, 1, 1, 1, 1, 1)
                            current_node_id += 1

                # Create columns from base level to the next level if not the top level
                if level < 1:  # Adjust if more levels are needed
                    for corner in [(      ix * length_x,       iy * length_y, z),
                                   ((ix + 1) * length_x,       iy * length_y, z),
                                   ((ix + 1) * length_x, (iy + 1) * length_y, z),
                                   (      ix * length_x, (iy + 1) * length_y, z)]:

                        upper_corner = (corner[0], corner[1], z + length_z)
                        if upper_corner not in node_map:
                            model.node(current_node_id, *upper_corner)
                            node_map[upper_corner] = current_node_id
                            current_node_id += 1

                        column_key = tuple(sorted([node_map[corner], node_map[upper_corner]]))

                        if column_key not in column_set:

                            # Local x-axis from nodal coordinates
                            XYZI = model.nodeCoord(node_map[corner])
                            XYZJ = model.nodeCoord(node_map[upper_corner])
                            xaxis = np.subtract(XYZJ, XYZI)

                            # Vectors in the local x-y and x-z planes
                            vecxy = [0, 1, 0]  # Assuming vecxy is global vertical
                            vecxz = np.cross(xaxis, vecxy)  # What OpenSees expects

                            vecxz_key = tuple(np.round(vecxz, decimals=6))

                            # Check if this vecxz has been used before
                            if vecxz_key in vecxz_to_geoTag:
                                geoTag = vecxz_to_geoTag[vecxz_key]
                            else:
                                geoTag = geoTag_counter
                                vecxz_to_geoTag[vecxz_key] = geoTag
                                geoTag_counter += 1  # Increment for the next new transformation

                                # Define the geometric transformation with the appropriate geoTag
                                model.geomTransf('Linear', geoTag, *vecxz)

                            model.element('elasticBeamColumn', current_ele_id,
                                          (node_map[corner], node_map[upper_corner]),
                                          column.A, column.E, column.G, column.J,
                                          column.Iweak, column.Istrong, geoTag, mass=463)
                            current_ele_id += 1
                            column_set.add(column_key)

                        corners.append(upper_corner)
                        corner_nodes.append(node_map[upper_corner])


    # Create beams at the first floor level
    z = base_z + length_z
    for ix in range(num_bay_x):
        for iy in range(num_bay_y):
            for side in range(4):
                prev_node = None
                num_steps = num_per_side_x if side % 2 == 0 else num_per_side_y
                for i in range(num_steps):
                    x, y = (ix * length_x + i * spacing, iy * length_y) if side == 0 else \
                           ((ix + 1) * length_x, iy * length_y + i * spacing) if side == 1 else \
                           (ix * length_x + length_x - i * spacing, iy * length_y + length_y) if side == 2 else \
                           (ix * length_x, iy * length_y + length_y - i * spacing)
                    coord = (x, y, z)
                    if coord not in node_map:
                        model.node(current_node_id, x, y, z)
                        node_map[coord] = current_node_id
                        current_node_id += 1
                    new_node_id = node_map[coord]

                    if prev_node is not None and tuple(sorted([prev_node, new_node_id])) not in beam_set:
                        # Local x-axis from nodal coordinates
                        XYZI  = model.nodeCoord(prev_node)
                        XYZJ  = model.nodeCoord(new_node_id)
                        xaxis = np.subtract(XYZJ, XYZI)

                        # Vectors in the local x-y and x-z planes
                        vecxy = [0, 1, 0] if side % 2 == 0 else [1, 0, 0] # Assuming vecxy is global vertical
                        vecxz = np.cross(xaxis, vecxy)  # What OpenSees expects

                        # Round the vecxz components to avoid floating-point precision issues
                        vecxz_key = tuple(np.round(vecxz, decimals=6))

                        # Check if this vecxz has been used before
                        if vecxz_key in vecxz_to_geoTag:
                            geoTag = vecxz_to_geoTag[vecxz_key]
                        else:
                            geoTag = geoTag_counter
                            vecxz_to_geoTag[vecxz_key] = geoTag
                            geoTag_counter += 1  # Increment for the next new transformation

                            # Define the geometric transformation with the appropriate geoTag
                            model.geomTransf('Linear', geoTag, *vecxz)

                        model.element('elasticBeamColumn', current_ele_id, prev_node, new_node_id, beam.A, beam.E, beam.G, beam.J, beam.Iweak, beam.Istrong, geoTag, '-mass', 90)
                        beam_set.add(tuple(sorted([prev_node, new_node_id])))
                        current_ele_id += 1

                    prev_node = new_node_id

    return current_node_id, current_ele_id, corner_nodes, geoTag_counter


def create_frame(divisions, dimensions=None, slab_mesh=None):

    if dimensions is None:
        dimensions = (8, 6, 4)

    if slab_mesh is None:
        slab_mesh = 2*dimensions[0] / divisions[0]

    num_bay_x, num_bay_y, num_story = divisions
    length_x, length_y, length_z = dimensions

    ndm = 3 # Number of spatial dimensions
    ndf = 6 # Degrees of freedom per node
    model = ops.Model(ndm=ndm, ndf=ndf)

    #%% Structural elements

    W14X311 = ElasticSection(
        axial_area=0.059,
        elastic_modulus=1.999e11,
        shear_modulus=7.690e10,
        torsional_constant=5.421e-20,
        moment_of_inertia_y=6.701E-04,
        moment_of_inertia_z=1.802E-03
    )

    W10X60 = ElasticSection(
        axial_area=0.0114,
        elastic_modulus=1.999e11,
        shear_modulus=7.690e10,
        torsional_constant=5.421e-20,
        moment_of_inertia_y=1.419E-4,
        moment_of_inertia_z=4.826E-05
    )

    #
    modify = num_story - 2
    node_id  = 1
    eleTag   = 1
    node_map = {}       # Dictionary to map coordinates to node IDs
    column_set = set()  # Set to track created columns to avoid duplication
    beam_set   = set()  # Set to track created beams to avoid duplication
    corners =[]
    corner_nodes = []
    slab_id = 1
    vecxz_to_geoTag = {}
    geoTag_counter = 0

    for i in range(0, num_story*length_z, length_z):
        current_node_id, current_ele_id, corner_nodes, geoTag_counter = \
                _create_grid(model, modify, node_id, 
                             dimensions, divisions,
                             i, slab_mesh, 
                             eleTag, geoTag_counter, vecxz_to_geoTag,
                             W14X311, W10X60,
                             node_map, 
                             column_set, beam_set, corners, corner_nodes)

        node_id = current_node_id
        eleTag = current_ele_id


    # ADDITIONAL MASS
    SMALL_MASS = 1.0e-10
    m1 = 0  # Mass in kg
    # m1 = 9076
    unique_nodes = set(corner_nodes)  # Convert to set to remove duplicates

    # Assign mass to each unique node
    for node_id in unique_nodes:
        model.mass(node_id, m1, m1, m1, SMALL_MASS, SMALL_MASS, SMALL_MASS)


    # SLAB
    slabs = _Diaphragm(
        elastic_modulus = 2.486E10,
        poisson_ratio = 0.2,
        thickness = 0.2,
        density   = 2402.7696,
        mesh_size = slab_mesh,
    )

    _create_slabs(model, corner_nodes, slab_id, slabs)

    # Tie nodes
    if False:
        for ndI in model.getNodeTags():
            XYZI = np.array(model.nodeCoord(ndI))
            for ndJ in model.getNodeTags():
                if ndI >= ndJ:
                    continue
                XYZJ = np.array(model.nodeCoord(ndJ))
                if np.linalg.norm(XYZJ-XYZI) < 1e-8:
                    print(f"Tieing {ndI} to {ndJ}", file=sys.stderr)
                    model.equalDOF((ndI,ndJ), tuple(range(1,ndf+1)))

    return model

def create_nsc(model, target_coord, m_nsc, f_nsc):
    #
    # Non-structural component
    #
    target_node_id = _target_node(model, target_coord)
    slab_loc = model.nodeCoord(target_node_id)

    slab_nodetag = target_node_id
    allTags = model.getNodeTags()
    nsc_nodetag = allTags[-1] + 1

    L_nsc = 1.0 # m

    model.node(nsc_nodetag, slab_loc[0], slab_loc[1], slab_loc[2] + L_nsc)

    # W10X60

    A_nsc = 1
    E_nsc = 4*math.pi**2*m_nsc*f_nsc**2
    G_nsc = 3846154
    Jxx_nsc = 0.1408
    Iy_nsc = 0.0833
    Iz_nsc = 0.0833

    all_eletag = model.getEleTags()
    nsc_eletag = all_eletag[-1] + 1

    # Local x-axis from nodal coordinates
    XYZI = model.nodeCoord(slab_nodetag)
    XYZJ = model.nodeCoord(nsc_nodetag)
    xaxis = np.subtract(XYZJ, XYZI)

    # Vectors in the local x-y and x-z planes
    vecxy = [0, 1, 0]
    vecxz = np.cross(xaxis, vecxy) # What OpenSees expects

    # Find an available geometric transformation tag (crude, can be better)
    geoTag = len(model.asdict()["StructuralAnalysisModel"]["properties"]["geomTransf"]) + 2

    # Define the geometric transformation with the appropriate geoTag
    model.geomTransf('Linear', geoTag, *vecxz)

    model.element('elasticBeamColumn', nsc_eletag, 
                  (slab_nodetag, nsc_nodetag), 
                  A_nsc, E_nsc, G_nsc, Jxx_nsc, Iy_nsc, Iz_nsc, geoTag)

    model.mass(nsc_nodetag, 1.0e-10, 1.0e-10, m_nsc , 1.0e-10, 1.0e-10, 1.0e-10)
    return model



def render_model(model, file_name=None):
    import veux

    # Create the rendering
    artist = veux.render(model,
                         vertical=3,
                         reference={"frame.surface"},
                         canvas="gltf") #"plotly")

    # Finally, save the rendering to the requested file
#   artist.save(file_name)
    veux.serve(artist)


def render_mode(model, mode_number, mode_scale, file_name=None):
    import veux

    # Define a function that tells the renderer the displacement
    # at a given node. This will be invoked for each node
    def displ_func(tag):
        return [float(mode_scale)*ui for ui in model.nodeEigenvector(tag, mode_number)]

    # Create the rendering
    artist = veux.render(model, displ_func,
                         vertical=3,
                         canvas="gltf")

    # Finally, save the rendering to the requested file
    if file_name is not None:
        artist.save(file_name)
    else:
        veux.serve(artist)

if __name__ == "__main__":

    n_modes   = 10
    slab_mesh =  1 # Size of
    num_bay_x =  4
    num_bay_y =  4
    num_story =  3
    length_x  =  8
    length_y  =  6
    length_z  =  4

    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(f"Usage: {sys.argv[0]} [num_story [num_bay_x [num_bay_y]]]")
            sys.exit(0)

        num_story = int(sys.argv[1])
    
    # Take optional 
    if len(sys.argv) > 2:
        num_bay_x = int(sys.argv[2])

    if len(sys.argv) > 3:
        num_bay_y = int(sys.argv[3])

    # Parsing complete; create the model


    model = create_frame(divisions=(num_bay_x, num_bay_y, num_story), 
                            dimensions=(length_x, length_y, length_z),
                            slab_mesh=slab_mesh)

    # Render the model in its reference configuration
    render_model(model)

    # model = create_nsc(model, target_coord, m_nsc, f_nsc)

    # Eigen analysis
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
        render_mode(model, mode_number=m, mode_scale=scale, file_name=None) #glb_file)
        print(glb_file)

