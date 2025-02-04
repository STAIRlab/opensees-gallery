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
import opensees.openseespy as ops

def create_truss():
    # Create a Model (with two-dimensions and 2 DOF/node)
    model = ops.Model(ndm=2, ndf=2)

    # Create nodes - command: node nodeId xCrd yCrd
    model.node(1, (  0.0,  0.0))
    model.node(2, (144.0,  0.0))
    model.node(3, (168.0,  0.0))
    model.node(4, ( 72.0, 96.0))

    # set the boundary conditions - command: fix nodeID xRestrnt? yRestrnt?
    model.fix(1, (1, 1))
    model.fix(2, (1, 1))
    model.fix(3, (1, 1))

    # Define materials for truss elements
    # -----------------------------------
    # Create Elastic material prototype - command: uniaxialMaterial Elastic matID E
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
    model.pattern("Plain", 1, "Linear", load={4: [100, -50.0]})

    # Set the algorithm to "Linear"
    model.algorithm("Linear")

    # Create the integration scheme, the LoadControl scheme using steps of 1.0
    model.integrator("LoadControl", 1.0)

    # Create the analysis object 
    model.analysis("Static")

    model.analyze(1)

    # Render the model
    artist = veux.render(model, canvas="gltf")
    artist.draw_outlines(state=model.nodeDisp, scale=10.0)
    veux.serve(artist)
    artist = veux.render(model, model.nodeDisp, canvas="plotly")

    veux.serve(artist)

