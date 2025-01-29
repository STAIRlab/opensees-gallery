

def create_model_1d():
    import opensees.openseespy as ops

    k = 60
    m = 2
    g = 386.4

    ops.model('basic','-ndm', 1,'-ndf',1)
    
    ops.node(1,0)
    ops.fix(1,1)
    ops.node(2,0)
    ops.mass(2,m)
    ops.node(3,0)
    ops.fix(3,1)
    
    ops.uniaxialMaterial('Elastic',1,k)
    
    ops.element('zeroLength',1,1,2,'-mat',1,'-dir',1)
    ops.element('zeroLength',2,2,3,'-mat',1,'-dir',1)
    
    
    ops.timeSeries('Path',1,'-dt',0.02,'-filePath','tabasFN.txt','-factor',g)
    ops.timeSeries('Path',2,'-dt',0.02,'-filePath','tabasFP.txt','-factor',g)
    
    ops.pattern('MultipleSupport',1)
    ops.groundMotion(1,'Plain','-accel',1)
    ops.imposedMotion(1,1,1) # node, dof, gmTag
    ops.groundMotion(2,'Plain','-accel',2)
    ops.imposedMotion(3,1,2)
