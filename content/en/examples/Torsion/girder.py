import numpy as np
import veux
from steel import GirderSection
from opensees.units.english import inch, foot, ft

if __name__ == "__main__":
    d = 6*ft
    section = GirderSection(
        # Typical Section No. 3 (pg 41/74)
        height         = 6.0*ft + 6*inch,
        web_slope      = 0.5,
        thickness_top  = 8.125      * inch,
        thickness_bot  = 6.25       * inch,
        width_top      = (1*ft+9*inch) + 4*ft
                       + 12*ft + 8*ft + (1*ft + 9*inch),
        width_webs     = [12*inch]*3,
        web_spacing    = 7*ft,
        overhang       = 4.0*ft
    )


    print(section.summary())

    if True:
        section = section.translate(section.torsion.centroid())
        print(section.summary())

    if True:
        ssc = section.translate(section.torsion.shear_center())
        print(np.linalg.norm(ssc.torsion.solution() + section.torsion.warping()));
        section = ssc

        print(section.summary())

    # 3) view warping modes
    artist = veux.create_artist((section.model.nodes, section.model.cells()), ndf=1)

    field = section.torsion.warping()
    artist.draw_surfaces(field = field, state=field, scale=1/100)
    R = artist._plot_rotation

    artist.canvas.plot_vectors([R@[*section.torsion.centroid(), 0] for i in range(3)], d/5*R.T)
    artist.canvas.plot_vectors([R@[*section.torsion.shear_center(), 0] for i in range(3)], d/5*R.T)
    artist.draw_outlines()
#   veux.serve(artist)
    artist.save("girder.glb")


