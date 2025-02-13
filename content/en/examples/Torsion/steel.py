import numpy as np

from shps.frame import patch, layer, create_mesh, GeneralSection

def rectangle(b, d):
    mesh = create_mesh(mesh_size=t/2.5, patches=[
        patch.rect(corners=[[-b/2, -d/2], [b/2, d/2]]),
    ])
    return GeneralSection(mesh, warp_shear=False)


def channel(t, w, h, b):
    mesh = create_mesh(mesh_size=min(w,t)/2.5, patches=[
        patch.rect(corners=[[0,  h/2-t], [b,  h/2  ]]),
        patch.rect(corners=[[0, -h/2+t], [w,  h/2-t]]),
        patch.rect(corners=[[0, -h/2  ], [b, -h/2+t]]),
    ])

    return GeneralSection(mesh, warp_shear=False)

def angle(t, b, d):
    mesh = create_mesh(mesh_size=t/2.5, patches=[
        patch.rect(corners=[[-t/2, -t/2], [b-t/2, t/2]]),
        patch.rect(corners=[[-t/2, -d+t/2], [t/2, -t/2]])
    ])
    return GeneralSection(mesh, warp_shear=False)


def wide_flange(d, b, t=None, tw=None, tf=None):
    """
    Saritas and Filippou (2009) "Frame Element for Metallic Shear-Yielding Members under Cyclic Loading"
    """
    bf = b
    if tf is None:
        tf = t
    else:
        t = tf
    if tw is None:
        tw = tf

    yoff = ( d - tf) / 2
    zoff = (bf + tw) / 4

    # Shear from Saritas and Filippou (2009)
    # Ratio of total flange area to web area
    alpha = 2*b*tf/d/(2*tw);
    # NOTE: This is 1/beta_S where beta_S is Afsin's beta
    beta = (1+3*alpha)*(2/3)/((1+2*alpha)**2-2/3*(1+2*alpha)+1/5)
    def psi(y, z):
        # webs
        if abs(y) < (d/2-tf):
            return beta*((1+2*alpha) - (2*y/d)**2) - 1 #+ 1
        # flange
        else:
            return 0 # beta*(2*alpha)*(z/b) - 1

    mesh = create_mesh([
        patch.rect(corners=[[-bf/2, yoff-tf/2],[bf/2,  yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
        patch.rect(corners=[[-tw/2,-yoff+tf/2],[tw/2,  yoff-tf/2]]),# ,  divs=(nwt, nwl), rule=int_typ),
        patch.rect(corners=[[-bf/2,-yoff-tf/2],[bf/2, -yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
    ], mesh_size=min(tf, tw)/2.5)

    return GeneralSection(mesh, warp_shear=psi)


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

    import opensees.units
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
    girder_section = [
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
    ]

    mesh = create_mesh(girder_section, mesh_size=min(thickness_bot, thickness_top, *width_webs)/3.0)

    return GeneralSection(mesh, warp_shear=False)


if __name__ == "__main__":
    import veux
    from veux.plane import PlaneModel
    from veux.frame import FrameArtist
    from veux.canvas.gltf import GltfLibCanvas

    section = wide_flange(d=612, b=229, t=19.6, tw=11.9)

    print(section.summary())

    from shps.frame.solvers.plastic import PlasticLocus
    PlasticLocus(section).plot()#(phi=0.5, ip=5)
    import matplotlib.pyplot as plt
    plt.show()

    artist = FrameArtist(PlaneModel((section.model.nodes, section.model.cells())), canvas=GltfLibCanvas(), ndf=1)

    field = section.torsion.warping()
    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    artist.draw_origin()
#   R = artist._plot_rotation
#   artist.canvas.plot_vectors([R@[*geometry.centroid, 0] for i in range(3)], R.T)
    artist.draw_outlines()
    veux.serve(artist)

