import veux
import numpy as np

import shps.frame
from shps.frame import patch, layer, create_mesh

if __name__ == "__main__":
    # Pilkey
    t =  0.2
    w = t
    b = 10.0
    h = 10.0

    #
    t =  1.0
    w = t
    b = 8.50
    h = 19.0

#   t =  12.7
#   w = t
#   b = 74.0
#   h = 305.0

    # Lacarbonara, Example 6.4
#   t = 10.5
#   w = 7.5
#   h = 160
#   b = 65
    mesh = create_mesh(mesh_size=min(w,t)/3.5, patches=[
        patch.rect(corners=[[0,  h/2-t], [b,  h/2  ]]),
        patch.rect(corners=[[0, -h/2+t], [w,  h/2-t]]),
        patch.rect(corners=[[0, -h/2  ], [b, -h/2+t]]),
    ])

    section = shps.frame.GeneralSection(mesh, warp_shear=False)

#   section = section.translate(section.torsion.centroid()).translate([-18.4, 0])
#   print(section.summary())

    section = section.translate(section.torsion.shear_center())
    print(section.summary())

    section = section.translate(section.torsion.centroid())
    print(section.summary())

    # 1) create basic section
    basic = section.linearize()

    field = section.torsion.warping()

    # 3) view warping modes
    artist = veux.create_artist((section.model.nodes, section.model.cells()), ndf=1)

    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([[0,0,0] for i in range(3)], h/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], h/5*R.T)
    artist.draw_outlines()
    veux.serve(artist)

