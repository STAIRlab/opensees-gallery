#!/usr/bin/env python

# Animating "Snap-Through" in a Shallow Arch
from pathlib import Path
import imageio
from veux import render
from arch import arch_model
import matplotlib.pyplot as plt
try:
    plt.style.use("steel")
except:
    pass

# Step 1: Create the model

model,mid = arch_model()

# Retrieve the model geometry as a dictionary for rendering
mesh = model.asdict()

# Step 2: Configure the analysis

nstep = 8000  # Number of analysis steps
nplot =  100  # Number of plots

model.system("ProfileSPD")
model.integrator("MinUnbalDispNorm",  1.0, 15, -10, 10)
model.analysis("Static")

xy = []

# Perform the analysis

for i in range(nstep):

    model.analyze(1)

    xy.append([-model.nodeDisp(mid, 2), model.getTime()])

    if not i%(nstep/nplot):
        # Render a frame of the animation
        fig = plt.figure()
        grid = fig.add_gridspec(4,4)

        ax = fig.add_subplot(grid[:2,:])
        ax.set_autoscale_on(True)
        ax.set_axis_off()

        # Collect the response at each node
        resp = {
            i: model.nodeDisp(i) for i in model.getNodeTags()
        }

        render(mesh, resp, noshow=True, view="elev", scale=1, ndf=3,
               canvas={"ax": ax, "ndm": 2},
               vert=3)

        ax2 = fig.add_subplot(grid[2:,:])
        ax2.plot(*zip(*xy))
        ax2.set_ylim([-500, 1500])
        ax2.set_xlim([0, 1000])

        fig.tight_layout()

        # Save the figure to a .jpg file
        fig.savefig(f"out/{i:0>4}.jpg")
        plt.close()

#
# Stich frames into a video
#

# Collect the image files
images = [
    imageio.imread(i) for i in sorted(Path("./out/").glob("*.jpg"))
]

imageio.mimsave('arch.gif', images, duration = 5.5, loop=10)
# imageio.mimsave('mygif.mp4', images)#, duration = 5.5)

