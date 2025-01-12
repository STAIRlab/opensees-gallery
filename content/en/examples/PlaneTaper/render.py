import veux
from plane_taper import create_model

model = create_model((10,2))[0]
artist = veux.render(model, vertical=3)

artist.save("model.glb")
veux.serve(artist)

