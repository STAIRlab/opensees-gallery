import opensees.units
import veux.plane
#import opensees.render.mpl as render
from opensees.units.english import inch, foot, ft
from opensees.section import section, patch, torsion, sect2gmsh
from GirderSection import GirderSection, inch, ft, torsion, sect2gmsh



if __name__ == "__main__":

    hayward8 = GirderSection(
        height         = 8.0*foot,
        web_slope      = 0.5,
        thickness_top  = 8.0        * inch,
        thickness_bot  = 6.0        * inch,
        width_top      = (1*ft+9*inch) + (5*ft+3*inch)
                       + 36*ft + (9*ft + 3*inch) + (1*ft + 9*inch),
        width_webs     = ([12]*6) * inch,
        web_spacing    = 9*ft,
        overhang       = 4.0*ft
    )

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
#   ax = render.section(sect)#, set_limits=True)

    artist = veux.plane.render(mesh, field, show_edges=False, show_scale=False)
    artist.show()
#   render.show()

