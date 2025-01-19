import veux
import numpy as np
from veux.plane import PlaneModel
from veux.frame import FrameArtist
from veux.canvas.gltf import GltfLibCanvas

from shps.frame import patch, layer, create_mesh, GeneralSection

def wide_flange(d, tf, bf, tw):
    yoff = ( d - tf) / 2
    zoff = (bf + tw) / 4
    return GeneralSection(create_mesh([
        patch.rect(corners=[[-bf/2, yoff-tf/2],[bf/2,  yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
        patch.rect(corners=[[-tw/2,-yoff+tf/2],[tw/2,  yoff-tf/2]]),# ,  divs=(nwt, nwl), rule=int_typ),
        patch.rect(corners=[[-bf/2,-yoff-tf/2],[bf/2, -yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
    ], mesh_size=min(tf, tw)/2.5), warp_shear=False)


if __name__ == "__main__":

    section = wide_flange(d=612, bf=229, tf=19.6, tw=11.9)
#   import matplotlib.pyplot as plt
#   plt.plot(*section.torsion.model.nodes.T, ".")
#   plt.axis("equal")
#   plt.show()


    field = section.torsion.warping()
#   print(f"{geometry.centroid = }")
    print(section.summary())

    from shps.frame.solvers.plastic import PlasticLocus
    PlasticLocus(section).plot()#(phi=0.5, ip=5)
    import matplotlib.pyplot as plt
    plt.show()

    artist = FrameArtist(PlaneModel((section.model.nodes, section.model.cells())), canvas=GltfLibCanvas(), ndf=1)

    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    artist.draw_origin()
#   R = artist._plot_rotation
#   artist.canvas.plot_vectors([R@[*geometry.centroid, 0] for i in range(3)], R.T)
    artist.draw_outlines()
    veux.serve(artist)

    # 3) view warping modes


    if False:
        # 1) create OpenSees fiber section
        for fiber in section.fibers:
            print(fiber.area)
            print(fiber.warp_mode)


        # 2) create OpenSees basic section
        elastic = section.linearize()

