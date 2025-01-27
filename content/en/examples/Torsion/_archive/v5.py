import veux
import shps.frame
from veux.plane import PlaneModel
from veux.frame import FrameArtist
from veux.canvas.gltf import GltfLibCanvas
from steel import GirderSection
from opensees.units.english import inch, foot, ft

if __name__ == "__main__":
    geometry = GirderSection(
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

    section = shps.frame.GeneralSection(geometry, mesh_size=[3*inch]*2, warp_shear=False)

    field = section.torsion2.warping(geometry)
    print(section.torsion2.warping_constant(field))

    field = section.torsion.warping()
    print(section.torsion.warping_constant())
#   print(section.torsion.torsion_constant(field))
#   print(section.torsion.torsion_constant(field))

    artist = FrameArtist(PlaneModel(section.mesh), canvas=GltfLibCanvas(), ndf=1)

    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    artist.plot_origin()
#   artist.draw_outlines()
    veux.serve(artist)

    # 3) view warping modes


    if False:
        # 1) create OpenSees fiber section
        for fiber in section.fibers:
            print(fiber.area)
            print(fiber.warp_mode)


        # 2) create OpenSees basic section
        elastic = section.linearize()

