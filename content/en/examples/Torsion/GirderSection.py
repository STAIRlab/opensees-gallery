import opensees.units
import veux.plane
from opensees.units.english import inch, foot, ft
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

