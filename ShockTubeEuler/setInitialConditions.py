def setInitialConditions(Qinf, neqn, naux, Qset, CoordsXYZ):
    import numpy as np

    #print Qinf[0]
    
    #Qinf is the raw value of farfield variables (non-dimensional) - DO NOT MODIFY
    #print neqn+ naux
    qinfSize = neqn + naux
    #print 'Vector size', qinfSize
    
    #Coords array(non-dimensional) [x,y,z]
    x = CoordsXYZ[0]
    y = CoordsXYZ[1]
    z = CoordsXYZ[2]
    #print x,y,z

    #Note that computeAuxiliaryVariables() is called after the set to ensure consistency
    #You do not have to set those locations to anything meaningful
    naux = qinfSize - neqn
    #print naux
    
    gamma = 1.4
    gm1 = gamma - 1.0
    Q0 = Qinf[0]
    Q1 = Qinf[1]
    Q2 = Qinf[2]
    Q3 = Qinf[3]
    Q4 = Qinf[4]

    # These are Sod's shock tube conditions (non-dim)
    u = 0.0
    rhol = 8
    pl = 10.0/gamma
    el = pl/gm1 + 0.5*rhol*u*u
    rhor = 1.0
    pr = 1.0/gamma
    er = pr/gm1 + 0.5*rhor*u*u

    #print 'rho ', rho, 'E ', E
    
    #Qset should be set to desired values (non-dimensional)
    if z > 2.0:
        Qset[0] = rhor
        Qset[1] = 0.0
        Qset[2] = 0.0
        Qset[3] = 0.0
        Qset[4] = er
    else:
        Qset[0] = rhol;
        Qset[1] = 0;
        Qset[2] = 0;
        Qset[3] = 0;
        Qset[4] = el;
        
    return 1
