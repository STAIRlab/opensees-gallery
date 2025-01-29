import veux
from Example8 import model

artist = veux.render(model, model.nodeDisp, scale=200, canvas="gltf", ndf=3)
#                    reference={"solid.outline"},
#                    displaced={"solid.outline", "solid.surface"})

#artist.save("model.glb")
veux.serve(artist)
