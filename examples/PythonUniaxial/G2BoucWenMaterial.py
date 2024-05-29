# https://terje.civil.ubc.ca/g2-bouc-wen-material/
# ------------------------------------------------------------------------
# The following Python code is implemented by Professor Terje Haukaas at
# the University of British Columbia in Vancouver, Canada. It is made
# freely available online at terje.civil.ubc.ca together with notes,
# examples, and additional Python code. Please be cautious when using
# this code; it may contain bugs and comes without warranty of any kind.
# ------------------------------------------------------------------------

import numpy as np

class BoucWenMaterial():

    # -------------------------------------------------
    # Constructor
    # -------------------------------------------------
    def __init__(self, mat):

        # Material parameters
        self.E = float(mat[1])
        self.fy = float(mat[2])
        self.alpha = float(mat[3])
        self.eta = int(mat[4])
        self.beta = float(mat[5])
        self.gamma = float(mat[6])
        self.tolerance = 1e-12
        self.maxNumIter = 100

        # Trial variables
        self.trialDeps = 0.0
        self.trialStress = 0.0
        self.trialZ = 0.0

        # Committed variables
        self.committedDeps = 0.0
        self.committedStress = 0.0
        self.committedZ = 0.0

        # History variables
        self.trialStrainSensitivity = [0.0]
        self.committedStrainSensitivity = [0.0]

        self.trialdzdtheta = [0.0]
        self.committeddzdtheta = [0.0]

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
        elif parameter == 'eta':
            self.eta = value
        elif parameter == 'beta':
            self.beta = value
        elif parameter == 'gamma':
            self.gamma = value
        else:
            print('\n'"Cannot set parameter", parameter, "in material")

    # -------------------------------------------------
    # Initial stiffness
    # -------------------------------------------------
    def initialStiffness(self):

        return self.E

    # -------------------------------------------------
    # State determination
    # -------------------------------------------------
    def state(self, threeEps):

        # Use both current trial strain and the strain increment
        epsn1 = threeEps[0]
        deltaeps = threeEps[1]
        self.trialDeps = deltaeps

        # Pick up input parameters, for ease of notation
        E = self.E
        fy = self.fy
        alpha = self.alpha
        eta = self.eta
        beta = self.beta
        gamma = self.gamma
        tolerance = self.tolerance
        maxNumIter = self.maxNumIter

        # Continue if there is a strain increment
        if np.abs(deltaeps) > 0.0:

            # Yield strain
            epsy = fy / E

            # Newton-Raphson to solve the Backward Euler equation
            iter = 0
            delta_z = 1.0
            f = 0.0
            fPrime = 0.0
            while np.abs(delta_z) >= tolerance and iter < maxNumIter:

                # Function whose root is sought, and its derivative
                zAbs = np.abs(self.trialZ)
                signum = np.sign(self.committedZ * deltaeps)
                f = self.trialZ - self.committedZ - (1.0 - (gamma + beta * signum) * zAbs**eta) * deltaeps / epsy
                fPrime = 1.0 + eta * np.sign(self.trialZ) * (gamma + beta * signum) * zAbs**(eta-1) * deltaeps / epsy

                # Take a Newton step
                delta_z = f / fPrime
                self.trialZ -= delta_z

                # Increment the counter
                iter += 1

            # Issue an error message if the Newton-Raphson scheme did not converge
            if iter == maxNumIter:
                print('\n'"The Newton-Raphson algorithm in Bouc-Wen did not converge")
                import sys
                sys.exit()

            # Result of the Newton iterations
            zn1 = self.trialZ
            zn1Abs = np.abs(zn1)
            zn1Sign = np.sign(zn1)
            signum = np.sign(self.committedZ * deltaeps)

            # Stress
            self.trialStress = alpha * E * epsn1 + (1-alpha) * fy * zn1

            # Continuum tangent
            dzn1depsContinuum = (1 - (gamma + beta * signum) * zn1Abs**eta) / epsy

            # Algorithmically consistent derivative of the Newton fraction f/f'
            dfdeps = -(1-(gamma + beta*signum)*zn1Abs**eta)/epsy
            dfPrimedeps = eta * zn1Sign * (gamma + beta * signum) * zn1Abs**(eta-1) / epsy
            dzn1depsNewtonFraction = -(dfdeps/fPrime - f/fPrime**2 * dfPrimedeps)

            # Differentiate f=0
            dzn1depsConsistent = (zn1Abs*(-1 + (gamma + beta * signum)*zn1Abs**eta))/(-(epsy*zn1Abs) + (epsn1-deltaeps)*eta*(gamma + beta * signum)*zn1Abs**eta*zn1Sign - epsn1*eta*(gamma + beta * signum)*zn1Abs**eta*zn1Sign)

            # Written differently
            dzn1depsWrittenDifferently = dzn1depsContinuum / (1 + (gamma + beta * signum) * eta * zn1Abs**(eta-1) * zn1Sign * deltaeps / epsy)

            # Tangent stiffness
            tangent = alpha * E + (1-alpha) * fy * dzn1depsConsistent

        else:
            self.trialStress = alpha * E * epsn1
            tangent = E

        return self.trialStress, tangent

    # -------------------------------------------------
    # DDM sensitivity analysis
    # -------------------------------------------------
    def stateDerivative(self, threeEps, ddmParameter, ddmIndex, ddmIsHere, dKflag='none'):

        # Get current strain and strain increment
        epsn1 = threeEps[0]
        deltaeps = threeEps[1]
        epsn = epsn1 - deltaeps

        # Extend DDM storage arrays in the first increment
        if ddmIndex > len(self.trialdzdtheta) - 1:
            self.trialStrainSensitivity.append(0)
            self.trialdzdtheta.append(0)
            self.committedStrainSensitivity.append(0)
            self.committeddzdtheta.append(0)

        # Get material parameters
        E = self.E
        fy = self.fy
        epsy = fy / E
        alpha = self.alpha
        eta = self.eta
        beta = self.beta
        gamma = self.gamma

        # Set basic derivatives depending on what ddmParameter is
        dEdtheta = 0
        dfydtheta = 0
        dalphadtheta = 0
        depsydtheta = 0
        if ddmParameter == 'E' and ddmIsHere:
            dEdtheta = 1
            depsydtheta = - fy / E ** 2
        elif ddmParameter == 'fy' and ddmIsHere:
            dfydtheta = 1
            depsydtheta = 1 / E
        elif ddmParameter == 'alpha' and ddmIsHere:
            dalphadtheta = 1

        # Do calculations if there is a strain increment
        if np.abs(deltaeps) > 0.0:

            # Pick up results from the Newton algorithm in the state determination
            zn1 = self.trialZ
            zn1Abs = np.abs(zn1)
            zn1Sign = np.sign(zn1)
            signum = np.sign(self.committedZ * deltaeps)

            # DERIVATIVE OF STRESS (conditional)
            depsndtheta = self.committedStrainSensitivity[ddmIndex]
            dzndtheta = self.committeddzdtheta[ddmIndex]
            depsn1dtheta = 0  # Zero here means conditional derivatives
            gammaBetaSignum = gamma + beta*signum
            dzn1dtheta = (zn1Abs*(depsydtheta*epsn - depsydtheta*epsn1 + depsn1dtheta*epsy - \
                depsndtheta*epsy + dzndtheta*epsy**2 - \
                depsydtheta*epsn*gammaBetaSignum*zn1Abs**eta + \
                depsydtheta*epsn1*gammaBetaSignum*zn1Abs**eta - \
                depsn1dtheta*epsy*gammaBetaSignum*zn1Abs**eta + \
                depsndtheta*epsy*gammaBetaSignum*zn1Abs**eta))/(epsy*(epsy*zn1Abs - \
                epsn*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign + \
                epsn1*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign))
            dsigman1dtheta = dalphadtheta * E * epsn1 + alpha * dEdtheta * epsn1 - dalphadtheta * fy * zn1 + (1-alpha) * dfydtheta * zn1 + (1-alpha) * fy * dzn1dtheta

            # DERIVATIVE OF STIFFNESS
            if dKflag == 'Initial':
                dKdtheta = dEdtheta
                dKdu = 0.0
            else:

                # dKdtheta (conditional)
                dzn1deps = (zn1Abs*(-1 + gammaBetaSignum*zn1Abs**eta))/(-(epsy*zn1Abs) + \
                    epsn*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign - \
                    epsn1*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign)
                
                ddzn1depsdtheta = -((depsydtheta*zn1Abs**2 - depsydtheta*gammaBetaSignum*zn1Abs**(2 + \
                    eta) + depsydtheta*dzn1deps*epsn*eta*gammaBetaSignum*zn1Abs**(1 + \
                    eta)*zn1Sign - \
                    depsydtheta*dzn1deps*epsn1*eta*gammaBetaSignum*zn1Abs**(1 + \
                    eta)*zn1Sign + \
                    depsn1dtheta*dzn1deps*epsy*eta*gammaBetaSignum*zn1Abs**(1 + \
                    eta)*zn1Sign - \
                    depsndtheta*dzn1deps*epsy*eta*gammaBetaSignum*zn1Abs**(1 + \
                    eta)*zn1Sign + dzn1dtheta*epsy*eta*gammaBetaSignum*zn1Abs**(1 + \
                    eta)*zn1Sign + \
                    dzn1deps*dzn1dtheta*epsn*epsy*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign**\
                    2 - dzn1deps*dzn1dtheta*epsn1*epsy*eta*gammaBetaSignum*zn1Abs**eta*\
                    zn1Sign**2 - \
                    dzn1deps*dzn1dtheta*epsn*epsy*eta**2*gammaBetaSignum*zn1Abs**eta*\
                    zn1Sign**2 + \
                    dzn1deps*dzn1dtheta*epsn1*epsy*eta**2*gammaBetaSignum*zn1Abs**eta*\
                    zn1Sign**2)/(epsy*zn1Abs*(epsy*zn1Abs - \
                    epsn*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign + \
                    epsn1*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign)))

                dKdtheta = dalphadtheta * E + alpha * dEdtheta - dalphadtheta * fy * dzn1deps + (1-alpha) * dfydtheta * dzn1deps + (1-alpha) * fy * ddzn1depsdtheta

                # dKdeps (unconditional)
                ddzn1depsdeps = -((dzn1deps*eta*gammaBetaSignum*zn1Abs**(-1 + eta)*zn1Sign*(-2*zn1Abs \
                    - dzn1deps*epsn*zn1Sign + dzn1deps*epsn1*zn1Sign + \
                    dzn1deps*epsn*eta*zn1Sign - \
                    dzn1deps*epsn1*eta*zn1Sign))/(-(epsy*zn1Abs) + \
                    epsn*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign - \
                    epsn1*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign))

                dKdu = (1-alpha) * fy * ddzn1depsdeps

        else:
            dsigman1dtheta = dalphadtheta * E * epsn1 + alpha * dEdtheta * epsn1
            dKdtheta = dEdtheta
            dKdu = 0.0

        return dsigman1dtheta, dKdtheta, dKdu

    # -------------------------------------------------
    # Commit
    # -------------------------------------------------
    def commit(self):

        # Related to response
        self.committedDeps = self.trialDeps
        self.committedZ = self.trialZ
        self.committedStress = self.trialStress

        # Related to DDM
        self.committedStrainSensitivity[:] = self.trialStrainSensitivity[:]
        self.committeddzdtheta[:] = self.trialdzdtheta[:]

    # -------------------------------------------------
    # Commit sensitivity history variables
    # -------------------------------------------------
    def commitSensitivity(self, threeEps, strainSensitivity, ddmParameter, ddmIndex, ddmIsHere):

        # Get strain values
        epsn1 = threeEps[0]
        deltaeps = threeEps[1]
        epsn = epsn1 - deltaeps

        # Store the strain sensitivity
        self.trialStrainSensitivity[ddmIndex] = strainSensitivity

        # Pick up input parameters
        E = self.E
        fy = self.fy
        epsy = fy / E
        eta = self.eta
        beta = self.beta
        gamma = self.gamma

        # Set basic derivatives
        depsydtheta = 0
        if ddmParameter == 'E' and ddmIsHere:
            depsydtheta = - fy / E**2
        elif ddmParameter == 'fy' and ddmIsHere:
            depsydtheta = 1 / E

        # Proceed if there is a strain increment
        if np.abs(deltaeps) > 0.0:

            # Get ready to calculate unconditional z-derivatives
            zn1Abs = np.abs(self.trialZ)
            zn1Sign = np.sign(self.trialZ)
            signum = np.sign(self.committedZ * deltaeps)
            depsn1dtheta = strainSensitivity
            depsndtheta = self.committedStrainSensitivity[ddmIndex]
            dzndtheta = self.committeddzdtheta[ddmIndex]
            gammaBetaSignum = gamma + beta * signum
            dzn1dtheta = (zn1Abs*(depsydtheta*epsn - depsydtheta*epsn1 + depsn1dtheta*epsy - \
                depsndtheta*epsy + dzndtheta*epsy**2 - \
                depsydtheta*epsn*gammaBetaSignum*zn1Abs**eta + \
                depsydtheta*epsn1*gammaBetaSignum*zn1Abs**eta - \
                depsn1dtheta*epsy*gammaBetaSignum*zn1Abs**eta + \
                depsndtheta*epsy*gammaBetaSignum*zn1Abs**eta))/(epsy*(epsy*zn1Abs - \
                epsn*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign + \
                epsn1*eta*gammaBetaSignum*zn1Abs**eta*zn1Sign))
            self.trialdzdtheta[ddmIndex] = dzn1dtheta

        else:
            self.trialdzdtheta[ddmIndex] = 0.0

        return

    # -------------------------------------------------
    # Print response
    # -------------------------------------------------
    def getResponse(self):

        return self.committedStress
