#!/usr/bin/python

import h5py as h5

# Returns the number of processors given a path and a casename
def getNumProcHDF5(path, casename):
    filename = path + casename + '.0.h5'
    h5f = h5.File(filename, "r")

    return h5f['Number Of Processors'][:][0]
    

def loadHDF5FileSolution(path, casename, procId):
    filename = path + casename + '.' + str(procId)  + '.h5'
    h5f = h5.File(filename, "r")

    return h5f['Solution/variableQ']


if __name__ == "__main__":
    import sys

    if(len(sys.argv) != 4):
        raise ValueError("USE: " + sys.argv[0] + " <goldCaseName> <diffCaseName> <relError%>")
    
    goldcase = sys.argv[1]
    diffcase = sys.argv[2]
    reltol = float(sys.argv[3])
    path = './'

    print "--------------------------------------------------------"
    print "Examining Case: " + diffcase
    print "Gold Case: " + goldcase
    print "Relative Tolerance: " + str(reltol) + "%"
    print "--------------------------------------------------------"
   
    # check the number of processors are identical
    np = getNumProcHDF5(path, goldcase)
    npd = getNumProcHDF5(path, diffcase)
    
    if(np != npd):
        raise ValueError("WARNING: gold case and diff'd case do not match processor count")
    
    # now let's diff the gold case solution to the diff'd case
    for ip in range(0,np):
        print "Evaluating process file: " + str(ip)
        gs = loadHDF5FileSolution(path, goldcase, ip)
        ds = loadHDF5FileSolution(path, diffcase, ip)

        size = len(gs)
        sized = len(ds)
        if(size != sized):
            raise ValueError("WARNING: gold case data size does not match diff'd case")
        if ip == 0:
            print "Attributes: " + str(gs.attrs.keys())
            varNames = gs.attrs['variable_names'].split(',')
            print varNames
        # scalars and vector are numbered in sequence separately
        # a negative zero indicates that the value is NOT a scalar or vector represented
        # by that numbering list
        # e.g. scalars = [0,-1,-1,-1] & vectors = [-1, 0, 0, 0]
        # indicates a single scalar id 0 followed by a 3 component vector of id 0
        nVarsQ =  len(gs.attrs['scalars'])
        scalarsIds = gs.attrs['scalars']
        vectorsIds = gs.attrs['vectors']
        

        for i in range(0,size):
            # compute the relative error in percent
            abserror = ds[i] - gs[i]
            if(gs[i] > 1.0e-15):
                relerror = abs((ds[i] - gs[i])/(gs[i]))*100.0
            else:
                relerror  = abs(ds[i] - gs[i])

            if(relerror > reltol):
                # get the local index, and the strided node id
                procid = ip
                localid = i%nVarsQ
                nodeid = i/nVarsQ 
                print "Values", i, abserror, relerror, ds[i], gs[i]
                message = "Processor id - " + str(procid) + ", value indx - " + str(i) + ", local indx - " \
                          + str(localid) + ", local mesh node id - " + str(nodeid) + ", variable Name - " \
                          + str(varNames[localid]) + ", relative error - " + str(relerror) + "%, absolute error - " \
                          + str(abserror)
                raise ValueError("TEST FAILED: " + message )


    sys.exit(0)
