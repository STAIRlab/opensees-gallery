import veux
import numpy as np
from steel import channel

if __name__ == "__main__":
    # G, S & W
    t =  0.2
    w = t
    b = 10.0
    h = 10.0

    # 
    # Pilkey ?
#   t =  1.0
#   w = t
#   b = 8.50
#   h = 19.0

#   t =  12.7
#   w = t
#   b = 74.0
#   h = 305.0

    # Lacarbonara, Example 6.4
    t = 10.5
    w = 7.5
    h = 160
    b = 65
    section = channel(t=t, w=w, h=h, b=b)

#   section = section.translate(section.torsion.centroid()).translate([-18.4, 0])
#   print(section.summary())

    if False:
        section = section.translate(section.torsion.shear_center())
        print(section.summary())

    if True:
        section = section.translate(section.torsion.centroid())
        print(section.summary())

    # 1) create basic section
    basic = section.linearize()

    field = section.torsion.warping()

    # 3) view warping modes
    artist = veux.create_artist((section.mesh.nodes, section.mesh.cells()), ndf=1)

    field = {node: value/100.0 for node, value in enumerate(field)}

    artist.draw_surfaces(field = field, state=field)
    artist.draw_outlines()
    R = artist._plot_rotation

    artist.canvas.plot_vectors([[0,0,0] for i in range(3)], h/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], h/5*R.T)
    artist.draw_outlines()
    veux.serve(artist)

