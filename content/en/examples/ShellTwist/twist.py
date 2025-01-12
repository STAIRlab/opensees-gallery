
import veux
import opensees.openseespy as ops
import shps.rotor


def rotate(x, point):
    pass

def create_model():
    model = ops.Model(ndm=3, ndf=6)

    E, nu, h, rho = 29e6, 0.22, 1.0, 0.0
    model.nDMaterial('ElasticIsotropic', 1, E, nu)
    model.section('PlateFiber', 1, 1, 0.32)
    model.section('ElasticFrame', 2, E, nu, area=10, Iy=1, Iz=1, J=1)

    surface = model.surface((3,4),
                        #element=None,
                        element="ShellMITC4", args=(1,),
                        points={
                            1: [0.0, 0.0, 0.0],
                            2: [10., 0.0, 0.0],
                            6: [13., 5.0, 2.0],
                            3: [15., 10., 5.0],
                            4: [0.0, 10., 0.0],
        })

    tag = 3*4 + 1
    for nodes in surface.walk_edge():
        model.element("PrismFrame", tag, nodes, section=2, vertical=[0, 0, 1])
        tag += 1

    return model


model = create_model()



model_config = {
    "extrude_outline": "square"
}

veux.serve(veux.render(model, canvas="plotly", reference={"frame.surface"}, model_config=model_config))

