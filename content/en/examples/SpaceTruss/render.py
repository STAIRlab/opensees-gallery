from revolve import revolve, create_truss, dome120, dome600 

if __name__ == "__main__":
    import veux

    nodes, elems = revolve(*dome600())
    nodes, elems = revolve(*dome120())

    model  = create_truss(nodes, elems)
    artist = veux.render(model, vertical=3)

    # Show the rendering
    veux.serve(artist)
