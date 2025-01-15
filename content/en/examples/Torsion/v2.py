import veux
from veux.plane import PlaneModel
from veux.frame import FrameArtist
from veux.canvas.gltf import GltfLibCanvas
from GirderSection import GirderSection, inch, ft, torsion, sect2gmsh

def mesh2model(nodes, cells):
    import opensees.openseespy as ops

    for i, node in enumerate(nodes):
        pass
    pass

if __name__ == "__main__":
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

    mesh = sect2gmsh(section, [3*inch]*2)
    field = torsion.solve_torsion(section, mesh)

    artist = FrameArtist(PlaneModel(mesh), canvas=GltfLibCanvas(), ndf=1)

    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
#   artist.draw_outlines()
    veux.serve(artist)
#   artist.save("a.glb")

