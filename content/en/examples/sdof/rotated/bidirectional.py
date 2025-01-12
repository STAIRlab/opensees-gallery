"""
author : JAWAD FAYAZ (email: jfayaz@uci.edu) (website: https://jfayaz.github.io)

------------------------------ Instructions -------------------------------------
This code develops the RotD50 Sa and RotD100 Sa Spectra of the Bi-Directional
Ground Motion records as '.AT2' files provided in the current directory

The two directions of the ground motion record must be named as 'GM1i' and 'GM2i',
where 'i' is the ground motion number which goes from 1 to 'n', 'n' being the total
number of ground motions for which the Spectra needs to be generated. The extension
of the files must be '.AT2'

For example: If the Spectra of two ground motion records are required, 4 files with
the following names must be provided in the given 'GM' folder:
    'GM11.AT2' - Ground Motion 1 in direction 1 (direction 1 can be either one of
                 the bi-directional GM as we are rotating the ground motions it does not matter)
    'GM21.AT2' - Ground Motion 1 in direction 2 (direction 2 is the other direction of the bi-directional GM)
    'GM12.AT2' - Ground Motion 2 in direction 1 (direction 1 can be either one of
                 the bi-directional GM as we are rotating the ground motions it does not matter)
    'GM22.AT2' - Ground Motion 2 in direction 2 (direction 2 is the other direction of the bi-directional GM)

The Ground Motion file must be a vector file with 4 header lines.The first 3 lines can have
any content, however, the 4th header line must be written exactly as per the following example:
    'NPTS=  15864, DT= 0.0050'



Make sure you have the following python libraries installed:
    IPython
    pandas
    numpy
    matplotlib.pyplot

INPUT:
This codes provides the option to have 3 different regions of developing the
Spectra of ground motions with different period intervals (discretizations)

The following inputs within the code are required:
    Int_T_Reg_1    --> Period Interval for the first region of the Spectrum
    End_T_Reg_1    --> Last Period of the first region of the Spectrum (where to end the first region)
    Int_T_Reg_2    --> Period Interval for the second region of the Spectrum
    End_T_Reg_2    --> Last Period of the second region of the Spectrum (where to end the second region)
    Int_T_Reg_3    --> Period Interval for the third region of the Spectrum
    End_T_Reg_3    --> Last Period of the third region of the Spectrum (where to end the third region)
    Plot_Spectra   --> whether to plot the generated Spectra of the ground motions (options: True, False)

OUTPUT:
The output will be provided in a saperate 'GMi_Spectra.txt' file for each
ground motion record, where 'i' denotes the number of ground motion in the same
of provided 'GM1i.AT2' and 'GM2i.AT2' files. The output files will be generated
in a saperate folder 'Spectra' which will be created in the current folder

The 'GMi_Spectra.txt' file will consist of space-saperated file with:
    'Periods (secs)' 'RotD50 Sa (g)' 'RotD100 Sa (g)'

===============================================================================


"""
"""
author : JAWAD FAYAZ (email: jfayaz@uci.edu) (website: https://jfayaz.github.io)

------------------------------ Instructions -------------------------------------
This code develops the RotD50 Sa and RotD100 Sa Spectra of the Bi-Directional
Ground Motion records as '.AT2' files provided in the current directory.
===============================================================================
"""
"""
author : JAWAD FAYAZ (email: jfayaz@uci.edu) (website: https://jfayaz.github.io)

------------------------------ Instructions -------------------------------------
This code develops the RotD50 Sa and RotD100 Sa Spectra of the Bi-Directional
Ground Motion records provided as arguments.
===============================================================================
"""

import sys
from pathlib import Path

import opensees.openseespy as op
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    plt.style.use("steel")
except Exception:
    pass


def read_gm_file(in_file):
    """
    Read a ground motion file and extract sampling interval, number of points, 
    and ground motion data.
    
    Parameters:
        in_file (str or Path): Path to the ground motion file.
    
    Returns:
        tuple: dt (float), num_pts (int), gm (np.ndarray)
    """
    with open(in_file, "r") as myfile:
        data = myfile.read().splitlines()
    # Extract number of points and dt from the 4th header line
    sp = data[3].split(' ')
    num_pts = int(sp[2].split(',')[0])
    dt = float(sp[4])
    header_lines = 4

    # Remove header lines and convert data to float array
    data = data[header_lines:]
    data = list(filter(str.strip, data))
    gm = np.array(list(map(float, data)))
    return dt, num_pts, gm


def beam_sdof(period):
    """
    Set up and analyze a single degree-of-freedom (SDOF) beam model 
    for a given period using OpenSeesPy.
    
    Parameters:
        period (float): The target period for the SDOF system.
    """
    # SDOF parameters
    length_val = 1.0
    diameter = 2
    radius = diameter / 2
    area = np.pi * (radius**2)
    elastic_modulus = 1.0
    shear_modulus = 1.0
    moment_inertia_z = np.pi * (radius**4) / 4
    polar_moment = np.pi * (radius**4) / 2
    moment_inertia_y = np.pi * (radius**4) / 4
    stiffness = 3 * elastic_modulus * moment_inertia_z / (length_val**3)
    mass_val = stiffness * (period**2) / (4 * np.pi**2)
    omega = np.sqrt(stiffness / mass_val)

    # Model setup
    op.model('basic', ndm=3, ndf=6)
    op.node(1, 0.0, 0.0, 0.0)
    op.node(2, 0.0, 0.0, length_val)
    op.geomTransf('Linear', 1, 0.0, 1.0, 0.0)
    op.fix(1, 1, 1, 1, 1, 1, 1)
    op.uniaxialMaterial("Elastic", 11, elastic_modulus)
    op.element("ElasticBeamColumn", 12, 1, 2, area, elastic_modulus,
               shear_modulus, polar_moment, moment_inertia_y, moment_inertia_z, 1)
    op.mass(2, mass_val, mass_val, 0.0, 0.0, 0.0, 0.0)

    # Eigenvalue analysis to verify period
    eigen_values = op.eigen(1)
    omega = np.sqrt(eigen_values[0])
    calculated_period = 2 * np.pi / omega
    # Printing handled by caller based on verbosity if needed

    # Rayleigh damping
    damping_ratio = 0.05
    alpha_m = 0.0
    beta_k_curr = 0.0
    beta_k_comm = 2.0 * damping_ratio / omega
    beta_k_init = 0.0
    op.rayleigh(alpha_m, beta_k_curr, beta_k_init, beta_k_comm)


def plot_spectra(plot_title, spectra_type, gm_index, spectra_df, verbose, save=False):
    """
    Plot and save the spectra for a given ground motion.

    Parameters:
        plot_title (str): Title of the plot.
        spectra_type (str): Column name of the spectrum data to plot.
        gm_index (int): Ground motion index.
        spectra_df (DataFrame): DataFrame containing the spectra data.
        verbose (bool): If True, prints status messages.
    """
    fig, ax = plt.subplots(figsize=(18, 12))
    ax.plot(spectra_df['Period(s)'], spectra_df[spectra_type], '.-', label=f'GM{gm_index}')
    ax.set_xlabel('Period (sec)', fontsize=30)
    ax.set_ylabel(spectra_type, fontsize=30)
    ax.set_title(plot_title, fontsize=40)
    ax.grid(True)
    ax.set_xlim(0, np.ceil(spectra_df['Period(s)'].max()))
    ax.set_ylim(0, np.ceil(spectra_df[spectra_type].max()))
    ax.legend(fontsize=30)

    if save:
        img_dir = Path("./img/")
        img_dir.mkdir(exist_ok=True)
        fig.savefig(img_dir / f"{plot_title.replace(' ', '_')}_{gm_index}.png")
        if verbose:
            print(f"Saved plot for {plot_title} of GM{gm_index}", file=sys.stderr)


def spectra(
    gm_file_list,
    int_t_reg_1=0.1,
    end_t_reg_1=1,
    int_t_reg_2=0.2,
    end_t_reg_2=2,
    int_t_reg_3=0.5,
    end_t_reg_3=5,
    verbose=True
):
    """
    Generate RotD50 and RotD100 spectra for provided ground motion files.
    
    Parameters:
        gm_file_list (list of tuples): Each tuple contains paths for two files
                                       corresponding to a ground motion in two directions.
        int_t_reg_1 (float): Period interval for the first region.
        end_t_reg_1 (float): End period for the first region.
        int_t_reg_2 (float): Period interval for the second region.
        end_t_reg_2 (float): End period for the second region.
        int_t_reg_3 (float): Period interval for the third region.
        end_t_reg_3 (float): End period for the third region.
        verbose (bool): If True, print status messages to stderr.
    
    Returns:
        list: A list of DataFrames containing spectra for each ground motion.
    """
    op.wipe()
    gravity = 386.1

    num_gms = len(gm_file_list)
    if verbose:
        print(f'\nGenerating Spectra for {num_gms} provided GMs\n', file=sys.stderr)

    gm_response = []

    # Define period ranges for the spectra once, used for all ground motions
    periods = np.concatenate([
        np.arange(int_t_reg_1, end_t_reg_1 + int_t_reg_1, int_t_reg_1),
        np.arange(end_t_reg_1 + int_t_reg_2, end_t_reg_2 + int_t_reg_2, int_t_reg_2),
        np.arange(end_t_reg_2 + int_t_reg_3, end_t_reg_3 + int_t_reg_3, int_t_reg_3)
    ])

    for eq_index, (gm_file1, gm_file2) in enumerate(gm_file_list, start=1):
        if verbose:
            print(f'Generating Spectra for GM: {eq_index} ...', file=sys.stderr)

        gm_spectra = pd.DataFrame(columns=['Period(s)', 'RotD50Sa(g)', 'RotD100Sa(g)'])

        for idx, period in enumerate(periods, start=1):
            gm_spectra.loc[idx - 1, 'Period(s)'] = period

            # Read ground motion files for both directions
            dt1, num_pts1, gm_data1 = read_gm_file(gm_file1)
            dt2, num_pts2, gm_data2 = read_gm_file(gm_file2)
            # Assuming dt1==dt2 and num_pts1==num_pts2 for both directions
            dt, num_pts = dt1, num_pts1

            gm_x = gm_data1
            gm_y = gm_data2
            gm_xy_mat = np.column_stack((gm_x, gm_x, gm_y, gm_y))

            gm_direction = [1, 1, 2, 2]
            gm_fact = [np.cos(0.0), np.sin(0.0), np.sin(0.0), np.cos(0.0)]
            id_tag = 2

            beam_sdof(period)

            for i in range(1, 5):
                op.timeSeries('Path', id_tag + i, dt=dt,
                              values=list(gm_xy_mat[:, i - 1]),
                              factor=gm_fact[i - 1] * gravity)
                op.pattern('UniformExcitation', id_tag + i, gm_direction[i - 1],
                           accel=id_tag + i)

            op.wipeAnalysis()
            op.constraints('Penalty', 1e18, 1e18)
            op.system("SparseGeneral")
            op.algorithm("Linear")
            op.integrator("TRBDF2")
            op.analysis("Transient")

            dt_analysis = dt * 10
            t_max_analysis = dt * num_pts
            t_final = int(t_max_analysis / dt_analysis)
            t_current = op.getTime()

            u1 = [0.0]
            u2 = [0.0]
            ok = 0

            while ok == 0 and t_current < t_final:
                ok = op.analyze(1, dt_analysis)
                if ok != 0:
                    raise Exception("Failed to converge")
                t_current = op.getTime()
                u1.append(op.nodeDisp(2, 1))
                u2.append(op.nodeDisp(2, 2))

            disp_xy = np.column_stack((u1, u2))

            rot_disp = np.zeros((180, 1))
            for theta in range(0, 180):
                angle_rad = np.deg2rad(theta)
                rot_matrix = np.array([
                    [np.cos(angle_rad), np.sin(-angle_rad)],
                    [np.sin(angle_rad), np.cos(angle_rad)]
                ])
                rotated = disp_xy @ rot_matrix
                rot_disp[theta, 0] = np.max(rotated[:, 0])

            omega = 2 * np.pi / period
            rot_acc = rot_disp * (omega**2) / gravity
            gm_spectra.loc[idx - 1, 'RotD50Sa(g)'] = np.median(rot_acc)
            gm_spectra.loc[idx - 1, 'RotD100Sa(g)'] = np.max(rot_acc)

            op.wipe()

        gm_response.append(gm_spectra)
        if verbose:
            print(f'Generated Spectra for GM: {eq_index}\n', file=sys.stderr)

    return gm_response


if __name__ == "__main__":
    # Expecting sys.argv to contain file paths for ground motions in pairs
    # Example: python script.py GM11.AT2 GM21.AT2 GM12.AT2 GM22.AT2 ...
    args = sys.argv[1:]
    if len(args) % 2 != 0 or not args:
        print("Please provide an even number of ground motion files as arguments.", file=sys.stderr)
        sys.exit(1)

    # Group files into pairs
    gm_file_list = [(args[i], args[i+1]) for i in range(0, len(args), 2)]

    # Generate spectra for provided ground motions
    gm_responses = spectra(gm_file_list)

    # Optionally plot the spectra
    verbose = True
    for idx, gm_spectra in enumerate(gm_responses, start=1):
        plot_spectra('RotD50 Spectra', 'RotD50Sa(g)', idx, gm_spectra, verbose)
        plot_spectra('RotD100 Spectra', 'RotD100Sa(g)', idx, gm_spectra, verbose)
        plt.show()

