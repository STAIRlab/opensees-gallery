#!/usr/bin/bash

python -m sees $1 --extrude-outline square --show frame.surface --canvas gltf --vert 3 $@
