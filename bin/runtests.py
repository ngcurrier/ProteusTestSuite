#!/usr/bin/python

import os
import glob
import datetime
import fnmatch
import subprocess
from xml.dom import minidom

def main():
    run_command = 'mpirun -np '
    
    path = '../'
    # find all folders with test.xml present
    configfiles = [os.path.join(dirpath, f)
         for dirpath, dirnames, files in os.walk(path)
         for f in fnmatch.filter(files, 'test.xml')]

    print configfiles
    
    for file in configfiles:
        print 'TEST DEFINITION  --> ' + file
        dirt = file.rsplit('/',1)[0]
        # change path to test directory
        os.chdir(dirt)
        print '** Directory: ' + os.getcwd()
        print '=================================='
        xmldoc = minidom.parse(file)
        elementList = xmldoc.getElementsByTagName('exe')
        exe = elementList[0].firstChild.nodeValue
        print '** exe = ' + exe
        elementList = xmldoc.getElementsByTagName('np')
        np = elementList[0].firstChild.nodeValue
        print '** np = ' + np
        elementList = xmldoc.getElementsByTagName('recomp')
        recomp = elementList[0].firstChild.nodeValue
        print '** recomp = ' + recomp
        elementList = xmldoc.getElementsByTagName('decomp')
        decomp = elementList[0].firstChild.nodeValue
        print '** decomp = ' + decomp
        elementList = xmldoc.getElementsByTagName('diff')
        diff = elementList[0].firstChild.nodeValue
        print '** diff = ' + diff

        # do the decomp
        p = subprocess.Popen(decomp, stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])

        # strip off the casename from recomp
        case = recomp.split()[-1]
        
        # do the solution
        print '----- RUNNING PROTEUS CFD ----- '
        p = subprocess.Popen('mpiexec -np ' + np + ' ' + exe + ' ' + case, stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])
        print '----- FINISHED RUNNING PROTEUS CFD ----- '

        
        # do the recomp
        p = subprocess.Popen(recomp, stdout=subprocess.PIPE, shell=True)
        print str(p.communicate()[0])
        
        print

    return

if __name__ == "__main__":
    main()
