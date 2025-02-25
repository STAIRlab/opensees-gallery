import veux
import numpy as np
import opensees.openseespy as ops



def Bathe(Path, R):
    """
    Sets up and runs Bathe's curved cantilever analysis with the Crisfield-Jelenic load paths.

    Parameters:
      Path     : integer selecting the load-step pattern (e.g., 2, 3, or 5)
      R        : 3x3 rotation matrix (numpy array)

    Returns a dictionary containing analysis results and model data.
    """
    model = ops.Model(ndm=3, ndf=6)

    # --- Element and Material Properties ---
    nen   = 2         # nodes per element
    ne    = 8         # total number of elements
    E     = 1e3
    A     = 1e4
    G     = 5e2
    I_val = A / 12
    J_val = 1e5 / (12 * 5)

    # Compute load vector P = R * [0; 600; 0] (since ExpSO3([0,0,0]) is identity)
    P = R@[0, 600, 0]

    tol = 1e-12

    # --- Define load steps based on Path ---
    if Path == 1:
        steps = [1/3] * 3
    elif Path == 2:
        steps = [0.5, 0.25, 0.25]
    elif Path == 3:
        steps = [1/10] * 10
    elif Path == 4:
        steps = [1/6] * 6
    elif Path == 5:
        steps = [1/8] * 8
    elif Path == 6:
        steps = [0.5, 0.25, 0.125, 0.0625, 0.0625]
    else:
        steps = [1.0]


    # --- Store element property data ---
    section = {
         "E": E,
         "A": A,
         "Ay": A,
         "Az": A,
         "Iz": I_val,
         "Iy": I_val,
         "G": G,
         "J": J_val,
    }


    #
    # Model Generation
    #
    # Total number of nodes
    nn = ne * (nen - 1) + 1
    rad = 100.0
    for i,arc in enumerate(np.linspace(0, np.pi/4, nn)):
        # Coordinates along the circular arc:
        x_local = rad * np.sin(arc)
        y_local = 0.0
        z_local = rad * (1 - np.cos(arc))
        # Rotate local coordinate into global system:
        coord = R.T@[x_local, y_local, z_local]
        model.node(i+1, tuple(coord))

    # Boundary Conditions
    # Fix the first node (all 6 DOFs)
    model.fix(1, (1, 1, 1, 1, 1, 1))

    #
    # Elements
    #
    model.geomTransf("Linear", 1,  tuple(R@[0, 0, 1]))
    model.section("ElasticFrame", 1, **section)

    # --- Create Elements ---
    for i in range(ne):
        n1 = i * (nen - 1) + 1
        n2 = n1 + 1
        tag = i + 1
        model.element(
            "ExactFrame", tag, (n1, n2), section=1, transform=1
        )

    # --- Define the Loading ---
    load = [P[0], P[1], P[2], 0, 0, 0]
    model.pattern("Plain", 1, "Linear", load={nn: load})

    # --- Set Up the Analysis ---
    model.system("BandGeneral")
    model.numberer("RCM")
    model.constraints("Plain")
    model.integrator("LoadControl", steps[0])
    model.algorithm("Newton")
#   model.test("NormUnbalance", tol, 50, 1)
    model.test("NormDispIncr", tol, 10)
    model.analysis("Static")

    #
    # Multi-Step Incremental Analysis
    #
    converged = True
    step_results = []
    for dlam in steps:
        model.integrator("LoadControl", dlam)
        ret = model.analyze(1)
        if ret != 0:
            converged = False
            print(f"Step with dLambda={dlam} did not converge.")
            break
        # Save displacement at the last node:
        disp = model.nodeDisp(nn)
        step_results.append(disp)

    # Collect results and return
    return {
         "converged": converged,
         "final_disp": model.nodeDisp(nn),
         "step_results": step_results,
         "load_steps": steps,
    }

def Print(Path, result, R):
    """
    Prints a summary row for the current analysis case.
    """
    if not result["converged"]:
        print(f" {len(result['step_results'])}")
    else:
        disp = result["final_disp"]
        # Print first three displacement components:
        print(f"{disp[0]:14.6f} {disp[1]:14.6f} {disp[2]:14.6f}")

# =============================================================================
# Main Script
# =============================================================================

def main():
    # Global rotation matrix
    R = np.eye(3)

    for path in [2, 5, 3]:
        Print(path, Bathe(path, R), R)


if __name__ == "__main__":
    main()

