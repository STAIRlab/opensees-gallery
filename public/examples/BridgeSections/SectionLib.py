"""
Dependencies:
- `shapely` is used for shape-building operations (merging, 
  diffing polygons, add holes, etc.)
- `pygmsh` is used for meshing
"""
from math import pi, sin, cos, sqrt
import numpy as np

from opensees.section import section, patch, layer

#
# Geometry Building
#
def GirderSection(
    web_slope,
    thickness_top,
    thickness_bot,
    height,
    width_top,
    width_webs,
    web_centers,
    units
    ):
    # 1. Create the section object
    #------------------------------------------------------
    #                                ^y
    #    |  4'0"   |       12'0"     |             (sym)         |
    # _  |_______________________________________________________|
    #    |_____  _______________ _________ _______________  _____|
    #          \ \             | |       | |             / /
    #5'6"       \ \            | |   |   | |            / /
    #            \ \___________| |_______| |___________/ /
    # _           \__________________+__________________/  ---> x
    #
    #             |                                     |
    # units = elle.units.UnitHandler("english_engineering")
    ft = units.ft

    # 2. Dimensions
    #------------------------------------------------------

    # center-to-center height
    c2c_height = height - thickness_top/2 - thickness_bot/2
    inside_height = height - thickness_bot - thickness_top

    # width of bottom flange
    width_bot = width_top -  \
            2*(0.0*ft + web_slope*(inside_height + thickness_bot))

    # 3. Build section
    #------------------------------------------------------
    girder_section = section.FiberSection(shapes=[
        # add rectangle patch for top flange
        patch.rect(corners=[
            [-width_top/2, c2c_height - thickness_top/2],
            [+width_top/2, c2c_height + thickness_top/2]]),

        # add rectangle patch for bottom flange
        patch.rect(corners=[
            [-width_bot/2,  -thickness_bot/2],
            [+width_bot/2,  +thickness_bot/2]]),

        # sloped outer webs
        patch.rhom(
            height = inside_height,
            width  = 1.0*ft,
            slope  = -1/web_slope,
            center = [
                -width_bot/2-inside_height/2*web_slope+0.5*ft,
                 (thickness_bot + inside_height)/2
            ]
        ),
        patch.rhom(
            height = inside_height,
            width  = 1.0*ft,
            slope  = 1/web_slope,
            center = [
                 width_bot/2+inside_height/2*web_slope-0.5*ft,
                 (thickness_bot + inside_height)/2
            ]
        ),
    ] + [
    # vertical inner webs[
        patch.rect(corners=[
            [loc - width/2,        0.0 + thickness_bot/2],
            [loc + width/2, c2c_height - thickness_top/2]]
        )
        for width, loc in zip(width_webs, web_centers)
    ])

    return girder_section

def RegularPolygon(n, Rcol):
    phi =  2*pi/n
    R = Rcol/cos(phi/2)
    vertices = [
        [R*cos(i*phi-phi/2),  R*sin(i*phi-phi/2)]
        for i in range(n)
    ]
    return patch._Polygon(vertices)

#
# Meshing
#

# PyMesh
# PyGMSH

#
# IO
#
def sees2shapely(section):
    """
    Generate `sectionproperties` geometry objects 
    from `anabel` patches.
    """
    # import sectionproperties.pre.geometry as SP_Sections
    import shapely.geometry
    from shapely.ops import unary_union
    shapes = []
    # meshes = []
    if hasattr(section, "patches"):
        patches = section.patches
    else:
        patches = [section]
    for patch in patches:
        name = patch.__class__.__name__.lower()
        if name in ["quad", "poly", "rect", "_polygon"]:
            points = np.array(patch.vertices)
            width,_ = points[1] - points[0]
            _,height = points[2] - points[0]
            shapes.append(shapely.geometry.Polygon(points))
        else:
            n = 64
            x_off, y_off = 0.0, 0.0
            # calculate location of the point
            external = [[
                0.5 * patch.extRad * np.cos(i*2*np.pi*1./n - np.pi/8) + x_off,
                0.5 * patch.extRad * np.sin(i*2*np.pi*1./n - np.pi/8) + y_off
                ] for i in range(n)
            ]
            if patch.intRad > 0.0:
                internal = [[
                    0.5 * patch.intRad * np.cos(i*2*np.pi*1./n - np.pi/8) + x_off,
                    0.5 * patch.intRad * np.sin(i*2*np.pi*1./n - np.pi/8) + y_off
                    ] for i in range(n)
                ]
                shapes.append(shapely.geometry.Polygon(external, [internal]))
            else:
                shapes.append(shapely.geometry.Polygon(external))

    if len(shapes) > 1:
        return unary_union(shapes)
    else:
        return shapes[0]

def sect2mesh(section):
    import meshio
    return meshio.Mesh(
        section.mesh_nodes,
        cells={"triangle6": section.mesh_elements}
)

def sees2gmsh(sect, size, **kwds):
    import pygmsh
    if isinstance(size, int): size = [size]*2
    shape = sees2shapely(sect)
    with pygmsh.geo.Geometry() as geom:
        geom.characteristic_length_min = size[0]
        geom.characteristic_length_max = size[1]
        coords = np.array(shape.exterior.coords)
        holes = [
            geom.add_polygon(np.array(h.coords)[:-1], size[0], make_surface=False).curve_loop
            for h in shape.interiors
        ]
        if len(holes) == 0:
            holes = None

        poly = geom.add_polygon(coords[:-1], size[1], holes=holes)
        # geom.set_recombined_surfaces([poly.surface])
        mesh = geom.generate_mesh(**kwds)
    mesh.points = mesh.points[:,:2]
    for blk in mesh.cells:
        blk.data = blk.data.astype(int)
    # for cell in mesh.cells:
    #     cell.data = np.roll(np.flip(cell.data, axis=1),3,1)
    return mesh

def sees2sectprop(girder_section):
    import sectionproperties.pre.geometry as SP_Sections
    from sectionproperties.analysis.section import Section as CrossSection
    shapes = sees2shapely(girder_section)
    try:
        geom = SP_Sections.Geometry(shapes)
    except ValueError:
        geom = SP_Sections.CompoundGeometry(shapes)

    # geom.plot_geometry();
    return geom
        
#
# Analysis
#
def SP_Model(sect, mesh):
    from sectionproperties.analysis.section import Section
    geom = sees2sectprop(sect)
    geom.create_mesh(mesh)
    return Section(geom, time_info=False)


# ipyvtklink pyvista 
# pythreejs
# pacman -S xorg-server-xvfb

def plot(mesh, values=None, scale=1.0, show_edges=None, savefig:str=None,**kwds):
    from matplotlib import cm
    import pyvista as pv
    pv.set_jupyter_backend("panel")


    pv.start_xvfb(wait=0.05)
    mesh = pv.utilities.from_meshio(mesh)
    if values is not None:
        point_values = scale*values
        mesh.point_data["u"] = point_values
        mesh = mesh.warp_by_scalar("u", factor=scale)
        mesh.set_active_scalars("u")
    if show_edges is None:
        show_edges = True #if sum(len(c.data) for c in mesh.cells) < 1000 else False
    if not pv.OFF_SCREEN:
        plotter = pv.Plotter(notebook=True)
        plotter.add_mesh(mesh,
           show_edges=show_edges,
           cmap=cm.get_cmap("RdYlBu_r"),
           lighting=False,
           **kwds)
        # if len(values) < 1000:
        #     plotter.add_mesh(
        #        pv.PolyData(mesh.points), color='red',
        #        point_size=5, render_points_as_spheres=True)
        if savefig:
            plotter.show(screenshot=savefig)
        else:
            plotter.show()


if __name__ == "__main__":
    from sees.section import render

    from opensees.units.units import spacing
    from opensees.units.english import inch, ft
    import opensees.units.english as units

    section = GirderSection(
        web_slope      = 2, #0.5,
        thickness_top  = (7 + 1/2) * inch,
        thickness_bot  = (5 + 1/2) * inch,
        height         = 5*ft + 8*inch,
        width_top      = 2*26 * ft,
        width_webs     = ([12]*5) * inch,
        web_centers    = 4 @ spacing(7*ft + 9*inch, "centered"),
        units          = units)

    render(section)
    import sees.section
    sees.section.show()
