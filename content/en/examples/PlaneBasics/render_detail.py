"""
A more advanced script demonstrating how to use veux in Python

To use this script run:
    python render_detail.py [file.glb]

where

    file.glb is an optional argument specifying a path to save the
             rendering to. If this argument is omitted, the rendering
             will be served on localhost like described in
             render_basics.py

For example,
    python render_detail.py

"""
import sys
import veux
from veux.config import SketchConfig, NodeStyle
from plane_taper import create_model


if __name__ == "__main__":

    model = create_model((10,2))[0]


    # Render the structure
    # Instead of the `show` argument, we use the `artist_config`
    # argument to pass extra information about the rendering.
    # In particular, we are scaling the extruded cross section
    # by a factor of 5, and the node marker size by a factor of 2000.
    artist = veux.render(
                 model,
                 vertical=3,   # the "3" coordinate is vertical
                 artist_config={"sketches": {
                     "default": SketchConfig({
                       "node": {
                           "marker": {"show": True, "style": NodeStyle(scale=10.0)},
                       }
                     })
                 }}
            )

    # If a second command line argument is passed, treat it as
    # The name of a file to save the rendering to. Otherwise,
    # just serve the rendering.
    if len(sys.argv) > 1:
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

