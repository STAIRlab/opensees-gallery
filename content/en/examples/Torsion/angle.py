import veux
import numpy as np

import shps.frame
from shps.frame import patch, layer

if __name__ == "__main__":
    t = 0.1
    b = 1.05
    d = 1.95
    mesh = shps.frame.create_mesh(mesh_size=t/2.5, patches=[
        patch.rect(corners=[[-t/2, -t/2], [b, t/2]]),
        patch.rect(corners=[[-t/2, -d  ], [t/2, -t/2]])
    ])

    section = shps.frame.GeneralSection(mesh, warp_shear=False)
    section = section.translate(section.torsion.centroid())

    field = section.torsion.warping()
    print(section.summary())

    # 3) view warping modes
    artist = veux.create_artist((section.model.nodes, section.model.cells()), ndf=1)

#   field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([R@[*section.torsion.centroid(), 0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)
    artist.draw_outlines()
    veux.serve(artist)

