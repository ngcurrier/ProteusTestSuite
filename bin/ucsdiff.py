#!/usr/bin/python

import h5py as h5
from multiprocessing import Process, Queue, Value
from time import sleep
import sys

# Returns the number of processors given a path and a casename
def getNumProcHDF5(path, casename):
    filename = path + casename + '.0.h5'
    try:
        h5f = h5.File(filename, "r")
    except:
        print('UCSDIFF could not open file ' + filename) 
        print('TEST FAILED')
        sys.exit(1)

    return h5f['Number Of Processors'][:][0]
    

def loadHDF5FileSolution(path, casename, procId):
    filename = path + casename + '.' + str(procId)  + '.h5'
    try:
        h5f = h5.File(filename, "r")
    except:
        print('UCSDIFF could not open file ' + filename)
        print('TEST FAILED')
        sys.exit(1)

    return h5f['Solution/variableQ']


class compareWorker(Process):

    def __init__(self, path, goldcase, diffcase, reltol, iproc):
        Process.__init__(self)
        self.path = path
        self.goldcase = goldcase
        self.diffcase = diffcase
        self.reltol = reltol
        self.iproc = iproc
        # NOTE: when a process is spawned all the variables are copied to the new processor
        #       we have to use value to set process variables across processes
        self.dieNow = Value('i', 0)
        self.hasDiedTol = Value('i', 0)
        
    def run(self):
        print "Evaluating process file: " + str(self.iproc)
        try:
            gs = loadHDF5FileSolution(self.path, self.goldcase, self.iproc)
        except:
            print('UCSDIFF could not load solution gold files')
            print('TEST FAILED')
            sys.exit(1)

        try:
            ds = loadHDF5FileSolution(self.path, self.diffcase, self.iproc)
        except:
            print('UCSDIFF could not load solution testing files')
            print('TEST FAILED')
            sys.exit(1)
    
        size = len(gs)
        sized = len(ds)
        varNames = gs.attrs['variable_names'].split(',')
        
        if(size != sized):
            raise ValueError("WARNING: gold case data size does not match diff'd case")
        if self.iproc == 0:
            print "Attributes: " + str(gs.attrs.keys())
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

            if self.dieNow.value:
                return 1
                
            if(relerror > self.reltol):
                # get the local index, and the strided node id
                procid = self.iproc
                localid = i%nVarsQ
                nodeid = i/nVarsQ 
                message = "FAILURE: Processor id - " + str(procid) + ", value indx - " + str(i) + ", local indx - " \
                          + str(localid) + ", local mesh node id - " + str(nodeid) + ", variable Name - " \
                          + str(varNames[localid]) + ", relative error - " + str(relerror) + "%, absolute error - " \
                          + str(abserror)
                print message
                self.hasDiedTol.value = 1
                break
                
    # This allows us to kill the thread from driver side
    def setDie(self):
        self.dieNow.value = 1

    def hasQuitHard(self):
        return self.hasDiedTol.value

    def getProc(self):
        return self.iproc
        
        
if __name__ == "__main__":
    NUMBER_OF_PROCESSES = 6

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
    # do this in a multithreaded way, it's slow
    processes = []
    for ip in range(0,np):
        p = compareWorker(path='./', goldcase=goldcase, diffcase=diffcase, reltol=reltol, iproc=ip)
        p.start()
        processes.append(p)
        
    # setup a watchdog
    running = True
    while running == True:
        ithread = 0
        anyRunning = False
        if len(processes) == 0:
            break
        for t in processes:
            if not t.is_alive():
                if t.hasQuitHard():
                    # send the kill command to all threads
                    for t in processes:
                        t.setDie()
                    break
            else:
                anyRunning = True
            ithread = ithread + 1
        if not anyRunning:
            break
        sleep(5)

    for t in processes:
        if t.hasQuitHard():
            print "TEST FAILED!"
            sys.exit(1)
        
    print "TEST PASSED!"
    sys.exit(0)
    
