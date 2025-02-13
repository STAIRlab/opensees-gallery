model basic -ndm 3 -ndf 6
section ElasticMembranePlateSection 1 10000.0 0.0 1.0 
node 1 0.0 0.0 0.0 
node 2 1.0 0.0 0.0 
node 3 2.0 0.0 0.0 
node 4 3.0 0.0 0.0 
node 5 4.0 0.0 0.0 
node 6 5.0 0.0 0.0 
node 7 6.0 0.0 0.0 
node 8 7.0 0.0 0.0 
node 9 8.0 0.0 0.0 
node 10 9.0 0.0 0.0 
node 11 10.0 0.0 0.0 
node 12 11.0 0.0 0.0 
node 13 12.0 0.0 0.0 
node 14 13.0 0.0 0.0 
node 15 14.0 0.0 0.0 
node 16 15.0 0.0 0.0 
node 17 16.0 0.0 0.0 
node 18 17.0 0.0 0.0 
node 19 18.0 0.0 0.0 
node 20 19.0 0.0 0.0 
node 21 20.0 0.0 0.0 
node 22 0.0 1.0 0.0 
node 23 1.0 1.0 0.0 
node 24 2.0 1.0 0.0 
node 25 3.0 1.0 0.0 
node 26 4.0 1.0 0.0 
node 27 5.0 1.0 0.0 
node 28 6.0 1.0 0.0 
node 29 7.0 1.0 0.0 
node 30 8.0 1.0 0.0 
node 31 9.0 1.0 0.0 
node 32 10.0 1.0 0.0 
node 33 11.0 1.0 0.0 
node 34 12.0 1.0 0.0 
node 35 13.0 1.0 0.0 
node 36 14.0 1.0 0.0 
node 37 15.0 1.0 0.0 
node 38 16.0 1.0 0.0 
node 39 17.0 1.0 0.0 
node 40 18.0 1.0 0.0 
node 41 19.0 1.0 0.0 
node 42 20.0 1.0 0.0 
element ASDShellQ4 1 1 2 23 22 1 -corotational 
element ASDShellQ4 2 2 3 24 23 1 -corotational 
element ASDShellQ4 3 3 4 25 24 1 -corotational 
element ASDShellQ4 4 4 5 26 25 1 -corotational 
element ASDShellQ4 5 5 6 27 26 1 -corotational 
element ASDShellQ4 6 6 7 28 27 1 -corotational 
element ASDShellQ4 7 7 8 29 28 1 -corotational 
element ASDShellQ4 8 8 9 30 29 1 -corotational 
element ASDShellQ4 9 9 10 31 30 1 -corotational 
element ASDShellQ4 10 10 11 32 31 1 -corotational 
element ASDShellQ4 11 11 12 33 32 1 -corotational 
element ASDShellQ4 12 12 13 34 33 1 -corotational 
element ASDShellQ4 13 13 14 35 34 1 -corotational 
element ASDShellQ4 14 14 15 36 35 1 -corotational 
element ASDShellQ4 15 15 16 37 36 1 -corotational 
element ASDShellQ4 16 16 17 38 37 1 -corotational 
element ASDShellQ4 17 17 18 39 38 1 -corotational 
element ASDShellQ4 18 18 19 40 39 1 -corotational 
element ASDShellQ4 19 19 20 41 40 1 -corotational 
element ASDShellQ4 20 20 21 42 41 1 -corotational 
fix  1 1 1 1 1 1 1 
fix 22 1 1 1 1 1 1 

pattern Plain 1  Linear {
  load 21 0 0 0 0 -261.79938779914943 0  
  load 42 0 0 0 0 -261.79938779914943 0 
}
constraints Transformation 
numberer RCM 
system UmfPack 
test NormDispIncr 1e-05 100 0 
algorithm Newton 
integrator LoadControl 0.025 
analysis Static 
analyze 40

puts "[nodeDisp 42 3] [nodeDisp 42 5]"

