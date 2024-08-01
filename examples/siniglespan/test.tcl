model basic 3 6
geomTransf Linear 1 1 0 0
section ElasticFrame 1 1 2 3 4 5 6
node 1 0 0 0
node 2 0 0 1
element PrismFrame 1 1 2 -section 1 -transform 1
print -json

