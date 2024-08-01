import sees
from wrench import create_wrench

model = create_wrench()
#model.eigen(1)
model.analysis("Static")
model.integrator("LoadControl", 1)
model.analyze(1)

n = 1
#sees.serve(sees.render(model, lambda i: model.nodeEigenvector(i, n)))
sees.serve(sees.render(model, lambda i: [1000*u for u in model.nodeDisp(i)], canvas="gltf"))

