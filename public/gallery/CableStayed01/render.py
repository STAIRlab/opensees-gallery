

import sees

artist = sees.render("CableStayed01.json", canvas="plotly", vertical=3)

#sees.serve(artist)

artist.save("model.glb")

