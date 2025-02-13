import veux
import matplotlib.pyplot as plt
import numpy as np
from steel import angle

import shps.frame
from shps.frame import patch, layer

if __name__ == "__main__":

    d = 1.95
    section = angle(t=0.1, b=1.05, d=d)
    #
    d = 150
    section = angle(t=15, b=80, d=d).rotate(np.pi)

    print(section.summary())

    if True:
        section = section.translate(section.torsion.centroid())
        print(section.summary())

    if False:
        ssc = section.translate(section.torsion.shear_center())
        print(np.linalg.norm(ssc.torsion.solution() + section.torsion.warping()));
        section = ssc

        print(section.summary())

    plt.spy(section.torsion.section_tensor())
    plt.show()

    # 3) view warping modes
    artist = veux.create_artist((section.mesh.nodes, section.mesh.cells()), ndf=1)

    field = section.torsion.warping()
    artist.draw_surfaces(field = field, state=field, scale=1/100)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([R@[*section.torsion.centroid(), 0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)
    artist.draw_outlines()
    veux.serve(artist)

