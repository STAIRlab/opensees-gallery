import sys
import veux, veux.motion
from xsection.library import Rectangle
from Example5 import create_model, analyze

if __name__ == "__main__":

    model = create_model("forceBeamColumn")
    analyze(model)

    # Plot the deformed state of the structure

    artist = veux.create_artist(model, vertical=3, model_config={
                                "frame_shape": Rectangle(2,2),
                                "frame_samples": 3
                                })

    artist.draw_outlines()
    motion = veux.motion.Motion(artist)

    motion.draw_sections()
#   motion.advance(1)
    motion.draw_sections(position=lambda _: [0,0,0],
                         rotation=lambda _: [0,0,0,1])

    motion.add_to(artist.canvas)


    # Check the number of arguments that were passed when this
    # script was invoked on the command line.
    if len(sys.argv) > 1:
        print(f"Saving to {sys.argv[1]}")
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

