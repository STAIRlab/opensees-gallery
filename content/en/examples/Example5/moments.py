import sys
import veux
from Example5 import create_model, analyze


def create_field(model,  w: float = 0):
    def field(tag, x):
        p  = model.eleResponse(tag, "forces")
        L  = 0
#       qi = p[0*6+i]
#       qj = p[1*6+i]
        M = lambda i: p[0*6+i]*(x-1) + p[1*6+i]*x + (1-x)*x * (-w) * L*L/2
        return [M(3), M(4), M(5)]
    return field

if __name__ == "__main__":

    model = create_model()
    analyze(model)

    # Plot the deformed state of the structure

    artist = veux.create_artist(model, vertical=3)
    artist.draw_outlines()
    artist.draw_diagrams(field=create_field(model), scale=1/20)

    # Check the number of arguments that were passed when this
    # script was invoked on the command line.
    if len(sys.argv) > 1:
        print(f"Saving to {sys.argv[1]}")
        artist.save(sys.argv[1])
    else:
        veux.serve(artist)

