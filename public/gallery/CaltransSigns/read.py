import sys
import meshio


mesh = meshio.read(sys.argv[1])

print(mesh)

