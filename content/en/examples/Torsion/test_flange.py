import numpy as np

from steel import wide_flange


if __name__ == "__main__":
    import veux
    from veux.frame import FrameArtist
    from veux.canvas.gltf import GltfLibCanvas

    d = 612
    b = 229
    tf = 19.6
    tw = 11.9
    print(f"Av = {tw*d}")
    section = wide_flange(d=d, b=b, t=tf, tw=tw)

    print(section.summary())

    artist = FrameArtist(((section.mesh.nodes, section.mesh.cells())), canvas=GltfLibCanvas(), ndf=1)

    field = section.torsion.warping()
    field = {node: value for node, value in enumerate(field)}

    artist.draw_surfaces(field = field)
    artist.draw_origin()
#   R = artist._plot_rotation
#   artist.canvas.plot_vectors([R@[*geometry.centroid, 0] for i in range(3)], R.T)
    artist.draw_outlines()
    veux.serve(artist)

