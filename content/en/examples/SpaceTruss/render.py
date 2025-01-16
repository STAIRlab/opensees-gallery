import sys
from revolve import revolve, create_truss, create_dome

if __name__ == "__main__":
    import veux

    design = "120"
    if len(sys.argv) > 1:
        design = sys.argv[1]

    nodes, elems = revolve(*create_dome(design))

    model  = create_truss(nodes, elems)
    artist = veux.render(model, vertical=3)

    if len(sys.argv) > 2:
        artist.save(sys.argv[2])
    else:
        # Show the rendering
        veux.serve(artist)
