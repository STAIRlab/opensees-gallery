import veux
from plane_taper import create_model

model = create_model((10,2))
artist = veux.render(model)

artist.save("model.glb")
veux.serve(artist)

