import opensees.units
from opensees.section import section, patch, torsion, sect2gmsh


def GirderSection(
    thickness_top  : float,
    thickness_bot  : float,
    height         : float,
    width_top      : float,
    width_webs     : list,
    web_spacing    : float,
    web_slope      : float = 0.0,
    overhang       : float = None,
    material       = None,
    ):
    #                                ^ y
    #                                |
    # _  |_______________________________________________________|
    #    |_____  _______________ _________ _______________  _____|
    #          \ \             | |       | |             / /
    #           \ \            | |   |   | |            / /
    #            \ \___________| |_______| |___________/ /
    # _           \__________________+__________________/  ---> x
    #             |                                     |

    spacing = opensees.units.units.spacing

    # Dimensions
    #------------------------------------------------------
    inside_height = height - thickness_bot - thickness_top


    # width of bottom flange
    if overhang:
        width_bot = width_top - \
                  2*(overhang + web_slope*(inside_height + thickness_bot))
    else:
        width_bot = web_centers[-1] - web_centers[0] \
                  + width_webs[1]/2 + width_webs[0]/2

    # number of internal web *spaces*
    niws = len(width_webs) - 3

    # list of web centerlines?
    web_centers   = [
        -width_bot/2 - inside_height/2*web_slope + 0.5*width_webs[1],
        *niws @ spacing(web_spacing, "centered"),
         width_bot/2 + inside_height/2*web_slope - 0.5*width_webs[-1]
    ]

    # Build section
    #------------------------------------------------------
    girder_section = section.FiberSection(shapes=[
        # add rectangle patch for top flange
        patch.rect(corners=[
            [-width_top/2, height - thickness_top],
            [+width_top/2, height                ]]),

        # add rectangle patch for bottom flange
        patch.rect(corners=[
            [-width_bot/2,        0.0      ],
            [+width_bot/2,  +thickness_bot]]),

        # sloped outer webs
        patch.rhom(
            height = inside_height,
            width  = width_webs[0],
            slope  = -web_slope,
            center = [web_centers[0], thickness_bot + inside_height/2]
        ),
        patch.rhom(
            height = inside_height,
            width  = width_webs[-1],
            slope  = web_slope,
            center = [web_centers[-1], thickness_bot + inside_height/2]
        )
    ] + [
        patch.rect(corners=[
            [loc - width/2,        thickness_bot],
            [loc + width/2,  height - thickness_top]]
        )
        for width, loc in zip(width_webs[1:-1], web_centers[1:-1])
    ])
    return girder_section


if __name__ == "__main__":
    import opensees.render.mpl as render
    from opensees.units.english import inch, foot, ft

    painter = GirderSection(
        web_slope      = 0.5,
        thickness_top  = (7 + 1/2)  * inch,
        thickness_bot  = (5 + 1/2)  * inch,
        height         = 5*ft + 8*inch,
        width_top      = 2*26 * ft,
        width_webs     = [12*inch]*7,
        web_spacing    = 7*ft + 9*inch,
        overhang       = 2*ft + 6*inch
    )

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

    hayward6 = GirderSection(
        height         = 6.0*ft + 6*inch,
        web_slope      = 0.5,
        thickness_top  = 8.0        * inch,
        thickness_bot  = 6.0        * inch,
        width_top      = (1*ft+9*inch) + (5*ft+3*inch)
                       + 36*ft + (9*ft + 3*inch) + (1*ft + 9*inch),
        width_webs     = ([12]*6) * inch,
        web_spacing    = 9*ft,
        overhang       = 4.0*ft
    )

    hayward_single = GirderSection(
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

    meloland = GirderSection(
        thickness_top  = (7 + 1/3)  * inch,
        thickness_bot  = (6 + 1/8)  * inch,
        height         =     5.5    * foot,
        width_top      =    2*17    * foot,
        width_webs     = ([8.0]*4)  * inch,
        web_spacing    = 8*foot + 9*inch,
        overhang       = 3*foot + 10.5*inch
        # web_slope = 0.5
    )

    crowley = GirderSection(
        thickness_top  = (6 + 3/4)  * inch,
        thickness_bot  = (5 + 1/2)  * inch,
        height         =     5.5    * foot,
        width_top      = 40*foot+(1*foot+5*inch)*2,
        width_webs     = [8.0*inch]*6, # not sure about the web widths
        web_spacing    = 7*ft + 2*inch,
        overhang       = 3*foot + 2*inch
        # web_slope = 0.5
    )

    # overhang = 2.5*ft
    for sect in hayward_single, hayward8, hayward6, painter, meloland, crowley:
        mesh = sect2gmsh(sect, [3*inch]*2)
        solution = torsion.solve_torsion(sect, mesh)
#       torsion.plot(mesh, solution, scale=1.0, show_edges=True)
        ax = render.section(sect)#, set_limits=True)

        import veux.plane
        veux.plane.render(mesh, solution, ax=ax, show_edges=False, show_scale=False)
        render.show()

