import veux
import opensees.openseespy as ops
from portal import create_portal, gravity_analysis, pushover_analysis

if __name__ == "__main__":
    # Create the model
    model = create_portal()
#   model.print(json="model.json")

    # perform analysis under gravity loads
    status = gravity_analysis(model)

    veux.serve(veux.render(model, model.nodeDisp, ndf=3, scale=10, canvas="gltf"))

    if status == ops.successful:
        print("Gravity analysis completed SUCCESSFULLY\n")
    else:
        print(f"Gravity analysis FAILED ({status = })\n")

    status = pushover_analysis(model)
    # Print a message to indicate if analysis successful or not
    if status == ops.successful:
        print(f"\nPushover analysis completed SUCCESSFULLY\n")
    else:
        print(f"Pushover analysis FAILED ({status = })\n")

    # Print the state at node 3
    model.print("node", 3)

    veux.serve(veux.render(model, model.nodeDisp, ndf=3, canvas="gltf"))


