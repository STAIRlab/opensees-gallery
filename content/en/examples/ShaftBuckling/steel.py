import numpy as np

from shps.frame import patch, layer, create_mesh, GeneralSection

class Shape:
    def exterior(self):
        return self.create_model().exterior()

    def interior(self):
        return self.create_model().interior()

    def create_model(self):
        # NOTE: WideFlange overloads this to include shear warping;
        # Need to rethink how to do this generally

        mesh = self.create_mesh()

        return GeneralSection(mesh, warp_shear=False)

    def add_to(self, model, tag, mat_tag, type="ShearFiber", translate=(0,0)):
        print(translate)
        section = self.create_model().translate(translate)

        import veux
        _m = section.mesh
        # veux.serve(veux.render((_m.nodes, _m.cells())))

        # section = section.translate(section.torsion.centroid())
        print(section.summary())
        if type == "Elastic":
            cmm = section.torsion.cmm()
            cnn = section.torsion.cnn()
            A = cnn[0,0]
            model.section("ElasticFrame", tag,
                          E=mat_tag["E"],
                          G=mat_tag["G"],
                          A=A,
                          Ay=100*A,
                          Az=100*A,
                          Iy=cmm[1,1],
                          Iz=cmm[2,2],
                          J =section.torsion.torsion_constant()
            )
        else:
            model.section(type, tag, GJ=1e6)
            for fiber in section.fibers():
                y, z = fiber.location
                model.fiber(y, z, fiber.area, mat_tag, fiber.warp[0], fiber.warp[1], [0,0,0],  section=tag)
#               model.fiber(y, z, fiber.area, mat_tag, section=tag)

class WideFlange(Shape):
    def __init__(self, d, b, t=None, tw=None, tf=None, b2=None, t2=None):
        self.d  = d
        self.bf = bf = b
        if tf is None:
            tf = t
        self.tf = tf

        if b2 is None:
            b2 = b
        self.b2 = b2

        if t2 is None:
            t2 = tf
        self.t2 = t2

        if tw is None:
            tw = tf
        self.tw = tw

        # Area and moment of inertia
        self.A  = tw*(d - tf - t2) + bf*tf + b2*t2

#       Iy and Iz are wrong for tf !=  t2
#       self.Iy = tw*(d - tf - t2)**3/12.0 + bf*tf*(0.5*(d - tf))**2 + b2*t2*(0.5*(d - t2)) ** 2
        self.Iz = 2*tf*bf**3/12

    def shear_factor(self):
        b  = self.bf
        tf = self.tf
        tw = self.tw
        d  = self.d

        m = 2*b*tf/(d*tw)
        n = b/d
        return (10*(1+nu)*(1+3*m)**2)/((12+72*m + 150*m**2 + 90*m**3) + nu*(11+66*m + 135*m**2 + 90*m**3) + 30*n**2*(m + m**2) + 5*nu*n**2*(8*m+9*m**2))

    def create_mesh(self):
        bf = self.bf
        b2 = self.b2
        tf = self.tf
        t2 = self.t2
        tw = self.tw
        d  = self.d

        yoff = ( d - tf) / 2

        return create_mesh([
            patch.rect(corners=[[-bf/2,        yoff-tf/2],[bf/2,  yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
            patch.rect(corners=[[-tw/2,       -yoff+tf/2],[tw/2,  yoff-tf/2]]),# ,  divs=(nwt, nwl), rule=int_typ),
            patch.rect(corners=[[-b2/2, -(d - t2)/2-t2/2],[bf/2, -yoff+tf/2]]),# ,  divs=(nfl, nft), rule=int_typ),
        ], mesh_size=min(tf, tw)/4.0)

    def create_model(self):
        """
        Saritas and Filippou (2009) "Frame Element for Metallic Shear-Yielding Members under Cyclic Loading"
        """
        b  = self.bf
        tf = self.tf
        tw = self.tw
        d  = self.d

        # Shear from Saritas and Filippou (2009)
        # Ratio of total flange area to web area
        alpha = 2*b*tf/d/(2*tw)
        # NOTE: This is 1/beta_S where beta_S is Afsin's beta
        beta = (1+3*alpha)*(2/3)/((1+2*alpha)**2-2/3*(1+2*alpha)+1/5)
        def psi(y, z):
            # webs
            if abs(y) < (d/2-tf):
                return 0 #beta*((1+2*alpha) - (2*y/d)**2) - 1 #+ 1
            # flange
            else:
                return 0 #beta*(2*alpha)*(z/b) - 1

        mesh = self.create_mesh()

        return GeneralSection(mesh, warp_shear=psi)



class Rectangle(Shape):
    def __init__(self, b, d, m=1/10.0):
        self.b = b
        self.d = d
        self.m = m

    def create_mesh(self):
        b = self.b
        d = self.d
        return create_mesh(mesh_size=min(b,d)*self.m, patches=[
            patch.rect(corners=[[-b/2, -d/2], [b/2, d/2]]),
        ])


class Channel(Shape):
    """
    _  ___________
      |__________|
      | |
      | |
      |o|
      | |
      | |_________
      |__________|
    
    
    
    """
    def __init__(self, d, b, tf, tw=None):
        self.tf = tf
        self.tw = tw if tw is not None else tf
        self.d = d
        self.b = b

    def create_mesh(self):
        d = self.d
        b = self.b
        t = self.tf
        w = self.tw

        return create_mesh(mesh_size=min(w,t)/3.0, patches=[
            patch.rect(corners=[[-w/2,  d/2-t], [b-w/2,  d/2  ]]),
            patch.rect(corners=[[-w/2, -d/2+t], [  w/2,  d/2-t]]),
            patch.rect(corners=[[-w/2, -d/2  ], [b-w/2, -d/2+t]]),
        ])


def angle(t, b, d):
    mesh = create_mesh(mesh_size=t/2.5, patches=[
        patch.rect(corners=[[-t/2, -t/2], [b-t/2, t/2]]),
        patch.rect(corners=[[-t/2, -d+t/2], [t/2, -t/2]])
    ])
    return GeneralSection(mesh, warp_shear=False)




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
    d  = 100
    tw = 3
    bf = 75
    tf = 3

    mesh = WideFlange(d=d, b=bf, t=tf, tw=tw).create_model()

    print(mesh.summary())

#   from shps.frame.solvers.plastic import PlasticLocus
#   PlasticLocus(mesh).plot()#(phi=0.5, ip=5)
#   import matplotlib.pyplot as plt
#   plt.show()

    artist = veux.create_artist(((mesh.mesh.nodes, mesh.mesh.cells())), ndf=1)

    field = mesh.torsion.warping()
    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    artist.draw_origin()
#   R = artist._plot_rotation
#   artist.canvas.plot_vectors([R@[*geometry.centroid, 0] for i in range(3)], R.T)
    artist.draw_outlines()
    veux.serve(artist)

