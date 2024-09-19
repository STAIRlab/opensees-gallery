import openseespy.opensees as ops
#import opsvis as opsv
import math
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt



class StructuralElements:
    def __init__(self, axial_area, elastic_modulus, shear_modulus, torsional_constant, moment_of_inertia_y, moment_of_inertia_z):
        self.A = axial_area
        self.E = elastic_modulus
        self.G = shear_modulus
        self.J = torsional_constant
        self.Iweak = moment_of_inertia_y
        self.Istrong = moment_of_inertia_z


class slab:
    def __init__(self, elastic_modulus, poisson_ratio, thickness, density, mesh_size):
        self.E = elastic_modulus
        self.nu = poisson_ratio
        self.h = thickness
        self.rho = density
        self.mesh_size = mesh_size


def get_last_node_tag(model):
    """
    Returns the last node tag defined in the OpenSeesPy model.

    Returns:
        int: The tag of the last node.
    """
    all_node_tags = model.getNodeTags()
    if all_node_tags:  # Check if the list is not empty
        return all_node_tags[-1]
    else:
        return 0  # Return None if no nodes have been defined


def get_last_element_tag(model):
    """
    Returns the last element tag defined in the OpenSeesPy model.

    Returns:
        int: The tag of the last element.
    """
    all_ele_tags = model.getEleTags()
    if all_ele_tags:  # Check if the list is not empty
        return all_ele_tags[-1]
    else:
        return 0  # Return None if no nodes have been defined

def find_closest_node(model, midpoint):

    # Loop through all node tags to find the closest node
    for node_id in model.getNodeTags():
        coord = np.array(model.nodeCoord(node_id))

        if np.linalg.norm(coord - midpoint) < 10**-8:
            closest_node = node_id

    return closest_node

def target_node(model, target_coord):
    all_node_tags = model.getNodeTags()
    for node_id in all_node_tags:
        coord = np.array(model.nodeCoord(node_id))
        if np.array_equal(coord, np.array(target_coord)):
            return node_id
    return None

def create_slabs(model, corner_nodes, current_ele_id, slab_id, slab):
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
    min_distance = float('inf')
    closest_node = None
    closest_nodes = []
    for i in range(0, len(corner_nodes), 4):
        if i + 3 < len(corner_nodes):
            line_tags   = []
            node_coords = []
            node_ids    = []

            model.section('ElasticMembranePlateSection', slab_id, slab.E, slab.nu, slab.h, slab.rho)

            for j in range(4):
                start_node = corner_nodes[i + j]
                end_node = corner_nodes[i + (j + 1) % 4]
                line_tag = current_ele_id
                model.mesh('line', line_tag, 2, *[start_node, end_node], 0, 6, slab.mesh_size)
                line_tags.append(line_tag)
                current_ele_id += 1


                node_coords.append(np.array(model.nodeCoord(start_node)))


            # Create the shell element using the line meshes
            model.mesh('quad', current_ele_id, 4, *line_tags, 0, 6, slab.mesh_size, 'ShellMITC4', 1)
            current_ele_id += 1
            slab_id += 1

            # Calculate the midpoint of the slab
            midpoint = np.mean(node_coords, axis=0)

            # Find the closest node to the midpoint
            closest_node = find_closest_node(model, midpoint)
            closest_nodes.append(closest_node)

            # print("Midpoint of the slab:", midpoint)
            # print("Node closest to the midpoint:", closest_node)

    return current_ele_id, slab_id, closest_nodes


def eigenvalue_analysis(model, n_modes, plot_mode_shapes):


    """
    Perform a modal analysis on a structure modeled in OpenSees and print the results.

    Parameters:
    n_modes (int): Number of modes to analyze.
    plot_mode_shapes (bool): If True, plot the mode shapes for each mode.
    """
    lambdaN = model.eigen(n_modes)  # eigenvalue analysis for nEigenJ modes

    # Calculate circular frequencies (w) for each mode
    w = [math.sqrt(lambda_val) for lambda_val in lambdaN]

    # Set the font to Times New Roman
    plt.rcParams['font.serif'] = 'Times New Roman'
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams.update({
        'font.size': 16,  # General font size
        'axes.labelsize': 14,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14
    })

    # Assuming 'w' contains angular frequencies for each mode
    # Calculate natural frequencies (f) for each mode
    frequencies = [frequency / (2.0 * math.pi) for frequency in w]

    # Calculate periods (T) for each mode
    periods = [1 / frequency for frequency in frequencies]

    # Creating a DataFrame
    df = pd.DataFrame({
        'Frequency (Hz)': frequencies,
        'Period (s)': periods
    }, index=[f"Mode {i+1}" for i in range(len(frequencies))])


    print(df)
    print("Modal Analysis: Successful.")

    # for i in range(1, len(frequencies) + 1):
    #     opsv.plot_mode_shape(i)

    #     # Retrieve frequency and period for the current mode
    #     freq = df.loc[f"Mode {i}", 'Frequency (Hz)']
    #     period = df.loc[f"Mode {i}", 'Period (s)']

    #     # Setting the title using Greek letters for mode shapes
    #     plt.title(f'$\\phi_{{{i}}}$ - Freq: {freq:.2f} Hz, Period: {period:.2f} s', fontsize=12)

    return df, w



def model3D(model, modify, node_id, length_x, length_y, length_z, base_z, spacing, num_bay_x, num_bay_y, num_story, eleTag,
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
                    for corner in [(ix * length_x, iy * length_y, z),
                                   ((ix + 1) * length_x, iy * length_y, z),
                                   ((ix + 1) * length_x, (iy + 1) * length_y, z),
                                   (ix * length_x, (iy + 1) * length_y, z)]:

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
                                          node_map[corner], node_map[upper_corner],
                                          column.A, column.E, column.G, column.J,
                                          column.Iweak, column.Istrong, geoTag, '-mass', 463)
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



def create_model(spacing, num_bay_x, num_bay_y, num_story, target_coord,
                 length_x, length_y, length_z,
                 m_nsc, f_nsc, counter, slab_point):
    ndm = 3
    ndf = 6

#   model = ops.Model(ndm=ndm, ndf=ndf)
    ops.wipe()
    ops.model("basic", "-ndm", ndm, "-ndf", ndf)
    model = ops

    #%% Structural elements

    W14X311 = StructuralElements(
        axial_area=0.059,
        elastic_modulus=1.999e11,
        shear_modulus=7.690e10,
        torsional_constant=5.421e-20,
        moment_of_inertia_y=6.701E-04,
        moment_of_inertia_z=1.802E-03
    )

    W10X60 = StructuralElements(
        axial_area=0.0114,
        elastic_modulus=1.999e11,
        shear_modulus=7.690e10,
        torsional_constant=5.421e-20,
        moment_of_inertia_y=1.419E-4,
        moment_of_inertia_z=4.826E-05
    )



    #%%

    modify = num_story - 2
    node_id = 1
    eleTag = 1
    node_map = {}  # Dictionary to map coordinates to node IDs
    column_set = set()  # Set to track created columns to avoid duplication
    beam_set = set()  # Set to track created beams to avoid duplication
    corners =[]
    corner_nodes = []
    slab_id = 1
    vecxz_to_geoTag = {}
    geoTag_counter = 0

    for i in range(0, num_story*length_z, length_z):
        current_node_id, current_ele_id, corner_nodes, geoTag_counter = \
                model3D(model, modify, node_id, length_x, length_y, length_z, i, spacing, num_bay_x, num_bay_y, num_story, eleTag,
                        geoTag_counter, vecxz_to_geoTag,
                        W14X311, W10X60,
                        node_map, column_set, beam_set,corners,corner_nodes)

        node_id = current_node_id
        eleTag = current_ele_id


    #%% ADDITIONAL MASS
    m1 = 0  # Mass in kg
    # m1 = 9076
    unique_nodes = set(corner_nodes)  # Convert to set to remove duplicates

    # all_node_tags = ops.getNodeTags()
    # Assign mass to each unique node
    for node_id in unique_nodes:
        model.mass(node_id, m1, m1, m1, 1.0e-10, 1.0e-10, 1.0e-10)


    #%% SLAB
    slabs = slab(
        elastic_modulus = 2.486E10,
        poisson_ratio = 0.2,
        thickness = 0.2,
        density = 2402.7696,
        mesh_size = spacing
        )

    # current_ele_id, slab_id, closest_nodes = create_slabs(model, corner_nodes, eleTag, slab_id, slabs)
    create_slabs(model, corner_nodes, eleTag, slab_id, slabs)


    # Tie nodes
    if True:
        for ndI in model.getNodeTags():
            XYZI = np.array(model.nodeCoord(ndI))
            for ndJ in model.getNodeTags():
                if ndI >= ndJ:
                    continue
                XYZJ = np.array(model.nodeCoord(ndJ))
                if np.linalg.norm(XYZJ-XYZI) < 1e-8:
                    model.equalDOF(ndI,ndJ,1,2,3,4,5,6)

    #
    # Non-structural component
    #
    target_node_id = target_node(model, target_coord)
    print(target_node_id, target_coord)
    slab_loc = model.nodeCoord(target_node_id)

    slab_nodetag = target_node_id
    allTags = model.getNodeTags()
    nsc_nodetag = allTags[-1] + 1

    L_nsc = 1.0 # m

    model.node(nsc_nodetag, slab_loc[0], slab_loc[1], slab_loc[2]+L_nsc)

    # W10X60

    axial_area_nsc = 1
    E_nsc = 4*math.pi**2*m_nsc*f_nsc**2
    G_nsc = 3846154
    Jxx_nsc = 0.1408
    Iy_nsc = 0.0833
    Iz_nsc = 0.0833

    all_eletag =model.getEleTags()
    nsc_eletag = all_eletag[-1] + 1

    # Local x-axis from nodal coordinates
    XYZI = model.nodeCoord(slab_nodetag)
    XYZJ = model.nodeCoord(nsc_nodetag)
    xaxis = np.subtract(XYZJ, XYZI)

    # Vectors in the local x-y and x-z planes
    vecxy = [0, 1, 0]
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

    model.element('elasticBeamColumn', nsc_eletag,
                  slab_nodetag, nsc_nodetag, axial_area_nsc,
                  E_nsc, G_nsc, Jxx_nsc, Iy_nsc, Iz_nsc, geoTag)

    model.mass(nsc_nodetag, 1.0e-10,1.0e-10, m_nsc , 1.0e-10, 1.0e-10, 1.0e-10)

    model.constraints('Plain')
    model.numberer('RCM')
    model.system('UmfPack')
    model.analysis("Transient")
    return model


def dynamic_analysis(spacing, num_bay_x, num_bay_y, num_story, target_coord,
                         length_x, length_y, length_z,
                         n_modes, plot_mode_shapes,
                         dt, npts, eq_data, m_nsc, RSN_num, f_nsc, counter, slab_point, gm_sf):

    model = create_model(spacing, num_bay_x, num_bay_y, num_story, target_coord,
                         length_x, length_y, length_z,
                         n_modes, plot_mode_shapes,
                         m_nsc, f_nsc, counter, slab_point)




    # opsv.plot_model()

    df, w = eigenvalue_analysis(n_modes, plot_mode_shapes=True)


    #%% DAMPING
    zeta = 0.02  # percentage of critical damping
    a0 = zeta * 2.0 * w[0] * w[1] / (w[0] + w[1])  # mass damping coefficient based on first and second modes
    a1 = zeta * 2.0 / (w[0] + w[1])  # stiffness damping coefficient based on first and second modes
    # assign damping to frame beams and columns

    model.rayleigh(a0, a1, 0, 0)


    # zeta_nsc = 0.02

    # a0_nsc = zeta_nsc * 2.0 * w[3] * w[4] / (w[3] + w[4])  # mass damping coefficient based on first and second modes
    # a1_nsc = zeta_nsc * 2.0 / (w[3] + w[4])  # stiffness damping coefficient based on first and second modes
    # # assign damping to frame beams and columns

    # ops.region(1, '-eleRange', 1, 120, '-rayleigh',a0, a1,0,0)
    # ops.region(2, '-ele', 121, '-rayleigh', a0_nsc, a1_nsc, 0,0)

    # if w[0] <= f_nsc < w[1]:
    #     a0 = zeta_nsc * 2.0 * w[0] * w[1] / (w[3] + w[4])
    #     a1 = zeta_nsc * 2.0 / (w[0] + w[1])
    # elif w[1] <= f_nsc < w[2]:
    #     a0 = zeta_nsc * 2.0 * w[1] * w[2] / (w[1] + w[2])
    #     a1 = zeta_nsc * 2.0 / (w[1] + w[2])
    # elif w[2] <= f_nsc < w[3]:
    #     a0 = zeta_nsc * 2.0 * w[2] * w[3] / (w[2] + w[3])
    #     a1 = zeta_nsc * 2.0 / (w[2] + w[3])
    # elif w[3] <= f_nsc < w[4]:
    #     a0 = zeta_nsc * 2.0 * w[3] * w[4] / (w[3] + w[4])
    #     a1 = zeta_nsc * 2.0 / (w[3] + w[4])    


    # elif w[9] <= f_nsc < w[10]:
    #     a0 = zeta_nsc * 2.0 * w[9] * w[10] / (w[9] + w[10])
    #     a1 = zeta_nsc * 2.0 / (w[9] + w[10])



    #%% DYNAMIC ANALYSIS

    GM_direction = 3
    timeSeries_tag = 2
    pattern_tag = 2

    G = gm_sf * 9.81
    model.timeSeries('Path', timeSeries_tag, '-dt', dt, '-values', *eq_data, '-factor', G)
    model.pattern('UniformExcitation', pattern_tag, GM_direction, '-accel', timeSeries_tag)

    #%% DATA DIRECTORY
    Output = "Acc Output"
    NSCacc_path = f'Acc Output/absNSCacc_RSN{RSN_num}.out'
    slabacc_path = f'Acc Output/absSlabacc_RSN{RSN_num}.out'
    os.makedirs(Output, exist_ok = True)
    # NSC
    model.recorder('Node','-file', NSCacc_path ,'-timeSeries',timeSeries_tag,'-time', '-node', nsc_nodetag, '-dof',3, 'accel' )

    # Slab
    model.recorder('Node','-file',slabacc_path,'-timeSeries', timeSeries_tag,'-time', '-node', slab_nodetag, '-dof',3, 'accel' )


    # Dyanmic analysis parameters
    model.wipeAnalysis()
    model.constraints('Plain')
    model.numberer('RCM')
    model.system('UmfPack')
    model.test('NormDispIncr', 1.0e-8, 50)
    model.algorithm('NewtonLineSearch')
    model.integrator('Newmark', 0.5, 0.25)
    model.analysis('Transient')

    ok = model.analyze(npts, dt)
    if ok == 0:
        print("Dynamic analysis complete")
    else:
        print("Dynamic analysis did not converge")


    NSC_data = np.genfromtxt(NSCacc_path, delimiter=' ', invalid_raise=False, filling_values=np.nan)
    slab_data = np.genfromtxt(slabacc_path, delimiter=' ', invalid_raise=False, filling_values=np.nan)

    # t = NSC_data[:, 0]   # Time data
    NSC_acc = NSC_data[:, 1]  # NSC acceleration data
    slab_acc = slab_data[:, 1]  # Slab acceleration data
    print(f"Analysis completed successfully for RSN{RSN_num}.")

    # Max NSC accelerations
    max_NSCacc = np.max(np.absolute(NSC_acc))

    # Max slab accelerations
    max_slabacc = np.max(np.absolute(slab_acc))


    return max_NSCacc, max_slabacc

# plt.close('all')  
# dynamic_analysis()
