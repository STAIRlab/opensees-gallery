clear all
clc
load node.out
load node1.out
load node2.out
load node3.out
load node4.out

a= load('ddmCore9epsco.out');
plot(a(3:end,1)-3,a(3:end,2))
hold on
plot(node(3:end,1)-3,(node1(3:end,2)-node(3:end,2))/(-0.01*0.005),'--r')
plot(node(3:end,1)-3,(node2(3:end,2)-node(3:end,2))/(-0.001*0.005),'g')
plot(node(3:end,1)-3,(node3(3:end,2)-node(3:end,2))/(-0.0001*0.005),'k')
plot(node(3:end,1)-3,(node4(3:end,2)-node(3:end,2))/(-0.00001*0.005),':')
legend('DDM','0.01','0.001','0.001','0.0001')
