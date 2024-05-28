import sdof
import numpy as np

import opensees.openseespy as op
FREE  = 0
FIXED = 1
X, Y, RZ = 1, 2, 3


def plastic_sdof(material, motion, dt, xi=0.05, r_post=0.0):
    """
    Run seismic analysis of a nonlinear SDOF

    :param mass: mass
    :param k: spring stiffness
    :param f_yield: yield strength
    :param motion: list, acceleration values
    :param dt: float, time step of acceleration values
    :param xi: damping ratio
    :param r_post: post-yield stiffness
    :return:
    """
    mass, k, f_yield = material
    op.wipe()
     # 2 dimensions, 3 dof per node
    op.model('basic', '-ndm', 2, '-ndf', 3) 

    # Establish nodes
    bot_node = 1
    top_node = 2
    op.node(bot_node, 0., 0.)
    op.node(top_node, 0., 0.)

    # Fix bottom node
    op.fix(top_node, FREE,  FIXED, FIXED)
    op.fix(bot_node, FIXED, FIXED, FIXED)

    # Set out-of-plane DOFs to be slaved
    op.equalDOF(1, 2, *[2, 3])

    # nodal mass (weight / g):
    op.mass(top_node, mass, 0., 0.)

    # Define material
    bilinear_mat_tag = 1
    mat_type = "Steel01"
    mat_props = [f_yield, k, r_post]
    op.uniaxialMaterial(mat_type, bilinear_mat_tag, *mat_props)

    # Assign zero length element
    beam_tag = 1
    op.element('zeroLength', beam_tag, bot_node, top_node, "-mat", bilinear_mat_tag, "-dir", 1, '-doRayleigh', 1)

    # Define the dynamic analysis
    load_tag_dynamic = 1
    pattern_tag_dynamic = 1

    values = list(-1 * motion)  # should be negative

#   op.timeSeries('Path', load_tag_dynamic, dt=dt, values=values)
    op.timeSeries('Path', load_tag_dynamic, "-dt", dt, "-values", *values)

#   op.pattern('UniformExcitation', pattern_tag_dynamic, X, accel=load_tag_dynamic)
    op.pattern('UniformExcitation', pattern_tag_dynamic, X, "-accel", load_tag_dynamic)

    # set damping based on first eigen mode
    eig = op.eigen('-fullGenLapack', 1)
    try:
        angular_freq = eig**0.5
    except:
        angular_freq = eig[0]**0.5
    alpha_m = 0.0
    beta_k = 2 * xi / angular_freq
    beta_k_comm = 0.0
    beta_k_init = 0.0

    op.rayleigh(alpha_m, beta_k, beta_k_init, beta_k_comm)

    # Run the dynamic analysis

#   op.wipeAnalysis()

    op.algorithm('Newton')
#   op.system('SparseGeneral')
    op.numberer('RCM')
    op.constraints('Transformation')
    op.integrator('Newmark', 0.5, 0.25)
    op.analysis('Transient')

    tol = 1.0e-10
    iterations = 10
    op.test('EnergyIncr', tol, iterations, 0, 2)
    analysis_time = (len(values) - 1) * dt
    analysis_dt = 0.001
    outputs = {
        "time": [],
        "rel_disp": [],
        "rel_accel": [],
        "rel_vel": [],
        "force": []
    }

    while op.getTime() < analysis_time:
        curr_time = op.getTime()
        if op.analyze(1, analysis_dt) != 0:
            print(f"Failed at time {op.getTime()}")
            break

        outputs["time"].append(curr_time)
        outputs["rel_disp"].append(op.nodeDisp(top_node, 1))
        outputs["rel_vel"].append(op.nodeVel(top_node, 1))
        outputs["rel_accel"].append(op.nodeAccel(top_node, 1))
        op.reactions()
        outputs["force"].append(-op.nodeReaction(bot_node, 1))  # Negative since diff node

    op.wipe()
    for item in outputs:
        outputs[item] = np.array(outputs[item])

    return outputs


def main():
    """
    Create a plot of an elastic analysis, nonlinear analysis and closed form elastic

    :return:
    """
    import eqsig
    import matplotlib.pyplot as plt

    record_filename = 'test_motion_dt0p01.txt'
    dt = 0.01
    rec = np.loadtxt(record_filename)
    acc_signal = eqsig.AccSignal(rec, dt)
    period = 1.0
    xi = 0.05
    mass = 1.0
    f_yield = 1.5  # Reduce this to make it nonlinear
    r_post = 0.0

    periods = np.array([period])

    k = 4 * np.pi ** 2 * mass / period ** 2

    outputs = plastic_sdof((mass, k, f_yield), rec, dt, xi=xi, r_post=r_post)
    outputs_elastic = plastic_sdof((mass, k, f_yield * 100), rec, dt, xi=xi, r_post=r_post)
    ux_opensees = outputs["rel_disp"]
    ux_opensees_elastic = outputs_elastic["rel_disp"]
    print(outputs)

    bf, sps = plt.subplots(nrows=2)
    sps[0].plot(outputs["time"], ux_opensees, label="OpenSees fy=%.3gN" % f_yield, ls="-")
    sps[0].plot(outputs["time"], ux_opensees_elastic, label="OpenSees fy=%.3gN" % (f_yield * 100), ls="--")
    time = acc_signal.time
    acc_opensees_elastic = np.interp(time, outputs_elastic["time"], outputs_elastic["rel_accel"]) - rec


    resp_u, resp_v, resp_a = sdof.integrate(rec, dt, k, 2*xi*mass*np.sqrt(k/mass), mass, fy=f_yield)
    sps[0].plot(acc_signal.time, resp_u, label="sdof")
    sps[1].plot(acc_signal.time, resp_a, label="sdof")

#   resp_u, resp_v, resp_a = duhamels.response_series(motion=rec, dt=dt, periods=periods, xi=xi)
#   sps[0].plot(acc_signal.time, resp_u[0], label="Eqsig")
#   sps[1].plot(acc_signal.time, resp_a[0], label="Eqsig")  # Elastic solution
#   print("diff", sum(acc_opensees_elastic - resp_a[0]))
    sps[1].plot(time, acc_opensees_elastic, label="Opensees fy=%.2gN" % (f_yield * 100), ls="--")
    sps[0].legend()
    sps[1].legend()
    plt.show()


if __name__ == '__main__':
    main()

