

import sees

artist = sees.render("CableStayed01.json", canvas="gltf", vertical=3)

#sees.serve(artist)

artist.save("model.glb")


