#!/usr/bin/python

import os
import glob
import datetime
import fnmatch
import subprocess
from xml.dom import minidom
from shutil import copyfile
import stat
import sys
from timeit import default_timer as timer
import collections

def main(numProcs):
    path = '../'
    # find all folders with test.xml present
    configfiles = [os.path.join(dirpath, f)
         for dirpath, dirnames, files in os.walk(path)
         for f in fnmatch.filter(files, 'test.xml')]

    configfiles.sort()
    print configfiles

    results = collections.OrderedDict()
    
    for file in configfiles:
        print 'TEST DEFINITION  --> ' + file
        dirt = file.rsplit('/',1)[0]
        # copy ucsdiff.py to test directory
        copyloc = dirt + '/ucsdiff.py'
        copyfile('./ucsdiff.py', copyloc)
        st = os.stat(copyloc)
        # make file executable
        os.chmod(copyloc, st.st_mode | stat.S_IEXEC)
        # change path to test directory
        os.chdir(dirt)
        print '** Directory: ' + os.getcwd()
        print '=================================='
        xmldoc = minidom.parse(file)
        elementList = xmldoc.getElementsByTagName('gridname')
        gridname = elementList[0].firstChild.nodeValue
        print '** exe = ' + 'ucs.x'
        print '** np = ' + str(numProcs)
        print '** recomp = ' + 'urecomp.x'
        print '** decomp = ' + 'udecomp.x'
        elementList = xmldoc.getElementsByTagName('diff')
        diff = elementList[0].firstChild.nodeValue
        print '** diff = ' + diff

        # do the decomp
        p = subprocess.Popen('udecomp.x ' + gridname + ' ' + str(numProcs), stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])

        # strip off the casename from recomp
        case = gridname.split('.')[-2]
        
        # do the solution
        print '----- RUNNING PROTEUS CFD ----- '
        start = timer()
        p = subprocess.Popen('mpiexec -np ' + str(numProcs) + ' ucs.x ' + case, stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])
        stop = timer()
        print '----- FINISHED RUNNING PROTEUS CFD ----- '
        print '----- RUNTIME: ' + str(stop-start) + '-----'
        
        # do the recomp
        p = subprocess.Popen('urecomp.x ' + case, stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])
        
        # do the ucsdiff operation
        print '----- RUNNING ERROR CHECKING -----'
        p = subprocess.Popen(diff, stdout=subprocess.PIPE, shell=True)
        comms = p.communicate()[0]
        if(comms.find('PASSED')):
            results[file] = 'PASSED'
        else:
            results[file] = 'FAILED'
        print str(comms)
        
    return results

if __name__ == "__main__":
    results = collections.OrderedDict()
    if(len(sys.argv) ==  2):
        results = main(int(sys.argv[1]))
    else:
        print('USAGE: ' + sys.argv[0] + ' <number of processors>')

    for res in results:
        print res + ' ' + results[res]
        
