a = load ('node.out');
plot(a(:,1),a(:,2))
hold on
cd old_opensees
a = load ('node.out');
plot(a(:,1),a(:,2),'--r')
cd ..
a = load ('ddmCore19epsco.out');
plot(a(:,1),a(:,2))
hold on
cd old_opensees
a = load ('ddmCore19epsco.out');
plot(a(:,1),a(:,2),'--r')
cd ..
a = load ('ddmSteel19fy.out');
plot(a(:,1),a(:,2),'--r')
plot(a(:,1),a(:,2))
hold on
cd old_opensees
a = load ('ddmSteel19fy.out');
plot(a(:,1),a(:,2),'--r')
cd ..
a = load ('ddm9BeamE.out');
plot(a(:,1),a(:,2))
hold on
cd old_opensees
a = load ('ddm9BeamE.out');
plot(a(:,1),a(:,2),'--r')
