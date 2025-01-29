from math import cos,sin,sqrt,pi
import opensees.openseespy as model

def rotPanelZone2D(eleID, nodeR, nodeC, E, Fy, dc, bf_c, tf_c, tp, db, Ry, As):
    """
    Procedure that creates a rotational spring and constrains the corner nodes of a panel zone

    The equations and process are based on: Krawinkler Model for Panel Zones

    Reference:  Gupta, A., and Krawinkler, H. (1999). "Seismic Demands for Performance Evaluation of Steel Moment Resisting Frame Structures,"
               Technical Report 132, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA.

    Written by: Dimitrios Lignos
    Date: 11/09/2008

    Formal arguments
          eleID   - unique element ID for this zero length rotational spring
          nodeR   - node ID which will be retained by the multi-point constraint
          nodeC   - node ID which will be constrained by the multi-point constraint
          E       - modulus of elasticity
          Fy      - yield strength
          dc      - column depth
          bf_c    - column flange width
          tf_c    - column flange thickness
          tp      - panel zone thickness
          db      - beam depth
          Ry      - expected value for yield strength --> Typical value is 1.2
          as      - assumed strain hardening
    """

    # Trilinear Spring
    # Yield Shear
    Vy =  0.55 * Fy * dc * tp
    # Shear Modulus
    G =  E/(2.0 * (1.0 + 0.30))
    # Elastic Stiffness
    Ke =  0.95 * G * tp * dc
    # Plastic Stiffness
    Kp =  0.95 * G * bf_c * (tf_c * tf_c) / db

    # Define Trilinear Equivalent Rotational Spring
    # Yield point for Trilinear Spring at gamma1_y
    gamma1_y =  Vy/Ke
    M1y = gamma1_y * (Ke * db)
    # Second Point for Trilinear Spring at 4 * gamma1_y
    gamma2_y =  4.0 * gamma1_y
    M2y = M1y + (Kp * db) * (gamma2_y - gamma1_y)
    # Third Point for Trilinear Spring at 100 * gamma1_y
    gamma3_y =  100.0 * gamma1_y
    M3y = M2y + (As * Ke * db) * (gamma3_y - gamma2_y)


    # Hysteretic Material without pinching and damage (same mat ID as Ele ID)
    model.uniaxialMaterial('Hysteretic', eleID,
                            M1y, gamma1_y,
                            M2y, gamma2_y,
                            M3y, gamma3_y,
                           -M1y , -gamma1_y,
                           -M2y , -gamma2_y,
                           -M3y , -gamma3_y,
                            1, 1, 0.0, 0.0, 0.0)

    model.element('ZeroLength', eleID nodeR nodeC mat=eleID,  dir=6, )

    model.equalDOF(nodeR, nodeC, 1, 2)

    # Left Top Corner of PZ
    nodeR_1 =  nodeR - 2
    nodeR_2 =  nodeR_1 + 1
    # Right Bottom Corner of PZ
    nodeR_6 =  nodeR + 3
    nodeR_7 =  nodeR_6 + 1
    # Left Bottom Corner of PZ
    nodeL_8 =  nodeR + 5
    nodeL_9 =  nodeL_8 + 1

	#          retained constrained DOF_1 DOF_2 
    model.equalDOF(nodeR_1, nodeR_2,   1,    2)
    model.equalDOF(nodeR_6, nodeR_7,   1,    2)
    model.equalDOF(nodeL_8, nodeL_9,   1,    2)

"""
#
# This routine creates a uniaxial material spring with deterioration
# 
# Spring follows: Bilinear Response based on Modified Ibarra Krawinkler Deterioration Model 
#
# Written by: Dimitrios G. Lignos, Ph.D.
#
# Variables
#     $eleID =     Element Identification (integer)
#     $nodeR =     Retained/master node
#     $nodeC =     Constrained/slave node
#     $K =         Initial stiffness after the modification for n (see Ibarra and Krawinkler, 2005)
#     $asPos =     Strain hardening ratio after n modification (see Ibarra and Krawinkler, 2005)
#     $asNeg =     Strain hardening ratio after n modification (see Ibarra and Krawinkler, 2005)
#     $MyPos =     Positive yield moment (with sign)
#     $MyNeg =     Negative yield moment (with sign)
#     $LS =         Basic strength deterioration parameter (see Lignos and Krawinkler, 2009)
#     $LK =         Unloading stiffness deterioration parameter (see Lignos and Krawinkler, 2009)
#     $LA =         Accelerated reloading stiffness deterioration parameter (see Lignos and Krawinkler, 2009)
#     $LD =         Post-capping strength deterioration parameter (see Lignos and Krawinkler, 2009)
#     $cS =         Exponent for basic strength deterioration
#     $cK =         Exponent for unloading stiffness deterioration
#     $cA =         Exponent for accelerated reloading stiffness deterioration
#     $cD =         Exponent for post-capping strength deterioration
#     $th_pP =     Plastic rotation capacity for positive loading direction
#     $th_pN =     Plastic rotation capacity for negative loading direction
#     $th_pcP =     Post-capping rotation capacity for positive loading direction
#     $th_pcN =     Post-capping rotation capacity for negative loading direction
#     $ResP =     Residual strength ratio for positive loading direction
#     $ResN =     Residual strength ratio for negative loading direction
#     $th_uP =     Ultimate rotation capacity for positive loading direction
#     $th_uN =     Ultimate rotation capacity for negative loading direction
#     $DP =         Rate of cyclic deterioration for positive loading direction
#     $DN =         Rate of cyclic deterioration for negative loading direction
#
# References:
#        Ibarra, L. F., and Krawinkler, H. (2005). “Global collapse of frame structures under seismic excitations,” Technical Report 152, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA.
#         Ibarra, L. F., Medina, R. A., and Krawinkler, H. (2005). “Hysteretic models that incorporate strength and stiffness deterioration,” International Journal for Earthquake Engineering and Structural Dynamics, Vol. 34, No.12, pp. 1489-1511.
#         Lignos, D. G., and Krawinkler, H. (2010). “Deterioration Modeling of Steel Beams and Columns in Support to Collapse Prediction of Steel Moment Frames”, ASCE, Journal of Structural Engineering (under review).
#         Lignos, D. G., and Krawinkler, H. (2009). “Sidesway Collapse of Deteriorating Structural Systems under Seismic Excitations,” Technical Report 172, The John A. Blume Earthquake Engineering Research Center, Department of Civil Engineering, Stanford University, Stanford, CA.
#
"""
#
def RotSpring2DModIKModel(model, eleID, nodeR, nodeC, K, asPos, asNeg, MyPos, MyNeg, LS, LK, LA, LD, cS, cK, cA, cD, th_pP, th_pN, th_pcP, th_pcN, ResP, ResN, th_uP, th_uN, DP, DN):
#
# Create the zero length element
    model.uniaxialMaterial(Bilin,  eleID,  K,  asPos, asNeg, MyPos, MyNeg, LS, LK, LA, LD, cS, cK, cA, cD, th_pP, th_pN, th_pcP, th_pcN, ResP, ResN, th_uP, th_uN, DP, DN)

    model.element("ZeroLength", eleID, nodeR, nodeC, mat=eleID, dir=6)

# Constrain the translational DOF with a multi-point constraint
#                      retained constrained DOF_1 DOF_2 ... DOF_n
    model.equalDOF(nodeR, nodeC, 1, 2)

