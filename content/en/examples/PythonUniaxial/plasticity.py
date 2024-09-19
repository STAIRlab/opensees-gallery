# https://terje.civil.ubc.ca/g2-uniaxial-plasticity/
# ------------------------------------------------------------------------
# The following Python code is implemented by Professor Terje Haukaas at
# the University of British Columbia in Vancouver, Canada. It is made
# freely available online at terje.civil.ubc.ca together with notes,
# examples, and additional Python code. Please be cautious when using
# this code; it may contain bugs and comes without warranty of any kind.
# ------------------------------------------------------------------------

import numpy as np

class plasticityMaterial():

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    def __init__(self, mat):

        # Check length of input vector
        if len(mat) != 7:
            print('\n'"ERROR: Wrong number of inputs to uniaxial plasticity material")
            import sys
            sys.exit()

        # Material and geometry properties
        self.E = float(mat[1])         # Modulus of elasticity
        self.sy = float(mat[2])        # Yield stress
        self.H = float(mat[3])         # Kinematic hardening parameter
        self.K = float(mat[4])         # Linear isotropic hardening parameter
        self.delta = float(mat[5])     # Saturation isotropic hardening parameter
        self.sy_inf = float(mat[6])    # Asymptotic yield stress for saturation isotropic hardening

        # Trial history variables
        self.trialPlasticStrain = 0.0
        self.trialAlpha = 0.0
        self.trialBackStress = 0.0

        # Committed history variables
        self.committedPlasticStrain = 0.0
        self.committedAlpha = 0.0
        self.committedBackStress = 0.0

        # Commit stress for output
        self.trialStress = 0.0
        self.committedStress = 0.0

    # -------------------------------------------------
    # Set parameter
    # -------------------------------------------------
    def setParameter(self, parameter, value):

        if parameter == 'E':
            self.E = value
        elif parameter == 'fy':
            self.fy = value
        elif parameter == 'alpha':
            self.alpha = value
        else:
            print("Cannot set parameter", parameter, "in material")

    # -------------------------------------------------
    # State determination
    # -------------------------------------------------
    def state(self, eps):

        # This is a total strain material model; pick first column of the U-matrix
        totalStrain = eps[0]

        # Stress value if the step is elastic
        elasticStress = self.E * (totalStrain - self.committedPlasticStrain)

        # Yield function for assumed elastic stress state (frozen plastic flow)
        saturationIsotropicHardening = (self.sy_inf - self.sy) * (1 - np.exp(-self.delta * self.committedAlpha))
        linearIsotropicHardening = self.K * self.committedAlpha
        yieldFunction = abs(elasticStress-self.committedBackStress) - (self.sy + saturationIsotropicHardening + linearIsotropicHardening)

        # Elastic step
        if yieldFunction <= 0:
            self.trialStress = elasticStress
            self.trialPlasticStrain = self.committedPlasticStrain
            self.trialAlpha = self.committedAlpha
            stiffness = self.E

        # Plastic step
        else:

            # No need for Newton with only linear hardening
            if self.delta == 0:

                deltaGamma = (abs(elasticStress - self.committedBackStress) - self.sy - self.K * self.committedAlpha) / (self.E + self.H + self.K)

            else:

                # Solve for increment in plastic flow by a Newton scheme
                deltaGamma_new = 0.0
                deltaGamma_old = -1.0
                while abs(deltaGamma_new - deltaGamma_old) > 1E-6:

                    deltaGamma_old = deltaGamma_new

                    function = abs(elasticStress - self.committedBackStress) \
                               - self.H * deltaGamma_old \
                               - self.E * deltaGamma_old \
                               - self.sy - self.K * self.committedAlpha \
                               - self.K * deltaGamma_old \
                               - (self.sy_inf - self.sy) * (1.0 - np.exp(-self.delta * deltaGamma_old - self.delta * self.committedAlpha))

                    derivative = -self.H -self.E -self.K - self.delta * (self.sy_inf - self.sy) * np.exp(-self.delta * deltaGamma_old - self.delta * self.committedAlpha)

                    deltaGamma_new = deltaGamma_old - (function / derivative)

                deltaGamma = deltaGamma_new

            # Compute new state variables
            self.trialStress = elasticStress - self.E * deltaGamma * np.sign(elasticStress - self.committedBackStress)
            self.trialPlasticStrain = self.committedPlasticStrain + deltaGamma * np.sign(elasticStress - self.committedBackStress)
            self.trialAlpha = self.committedAlpha + deltaGamma
            self.trialBackStress = self.committedBackStress + self.H * deltaGamma * np.sign(elasticStress - self.committedBackStress)

            # Evaluate plastic stiffness
            saturationK = self.delta * (self.sy_inf-self.sy) * np.exp(-self.delta*(self.trialAlpha)+deltaGamma)
            hardeningStiffness = self.H + self.K + saturationK
            stiffness = self.E * hardeningStiffness / (self.E + hardeningStiffness)

        return self.trialStress, stiffness

    # -------------------------------------------------
    # DDM sensitivity analysis
    # -------------------------------------------------
    def stateDerivative(self, threeEps, ddmParameter):

        return 0.0, 0.0

    # -------------------------------------------------
    # Commit
    # -------------------------------------------------
    def commit(self):

        self.committedStress = self.trialStress
        self.committedPlasticStrain = self.trialPlasticStrain
        self.committedAlpha = self.trialAlpha
        self.committedBackStress = self.trialBackStress

    # -------------------------------------------------
    # Commit sensitivity history variables
    # -------------------------------------------------
    def commitSensitivity(self, threeEps, strainSensitivity, ddmParameter):

        return

    # -------------------------------------------------
    # Print response
    # -------------------------------------------------
    def getResponse(self):

        return self.committedStress

