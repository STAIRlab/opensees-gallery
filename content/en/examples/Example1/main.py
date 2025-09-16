# ===----------------------------------------------------------------------===//
# 
#         OpenSees - Open System for Earthquake Engineering Simulation    
#                Structural Artificial Intelligence Laboratory
# 
# ===----------------------------------------------------------------------===//
#
# Basic Truss
#
import veux
import xara

def create_truss():
    # Create a Model (with two-dimensions and 2 DOF/node)
    model = xara.Model(ndm=2, ndf=2)

    # Create nodes
    model.node(1, (  0.0,  0.0))
    model.node(2, (144.0,  0.0))
    model.node(3, (168.0,  0.0))
    model.node(4, ( 72.0, 96.0))

    # set the boundary conditions
    model.fix(1, (1, 1))
    model.fix(2, (1, 1))
    model.fix(3, (1, 1))

    # Define materials for truss elements
    # -----------------------------------
    # Create Elastic material with Young's modulus E = 3000.0
    model.uniaxialMaterial("Elastic", 1, 3000.0)

    # Define elements
    # ---------------
    # Create truss elements - command: element truss trussID node1 node2 A matID
    model.element("Truss", 1, (1, 4), 10.0, 1)
    model.element("Truss", 2, (2, 4),  5.0, 1)
    model.element("Truss", 3, (3, 4),  5.0, 1)

    return model

if __name__ == "__main__":
    model = create_truss()

    # Assign the load to a "Plain" load pattern and scale its load factor linearly in time.
    model.pattern("Plain", 1, "Constant", load={4: [100, -50.0]})

    # Setup the strategy for incrementing loads
    model.integrator("LoadControl", 1.0)

    # Set the analysis type to Static
    model.analysis("Static")


    # ------------------------------
    # Perform the analysis
    # ------------------------------
    model.analyze(1)

    # print the current state at node 4 and at all elements
    u4 = model.nodeDisp(4)
    print(f"u4 = {u4}")

    # ------------------------------
    # Render the model
    # ------------------------------
    artist = veux.render(model, canvas="gltf")
    artist.draw_outlines(state=model.nodeDisp, scale=10.0)
    veux.serve(artist)
    artist = veux.render(model, model.nodeDisp, canvas="plotly")

    veux.serve(artist)

