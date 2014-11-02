#!/usr/bin/python

import os
import glob
import datetime
import fnmatch
from xml.dom import minidom

def main():
    run_command = 'mpirun -np '
    
    path = '../'
    configfiles = [os.path.join(dirpath, f)
         for dirpath, dirnames, files in os.walk(path)
         for f in fnmatch.filter(files, 'test.xml')]
    
    for file in configfiles:
        xmldoc = minidom.parse(file)
        elementList = xmldoc.getElementsByTagName('exe')
        exe = elementList[0].firstChild.nodeValue
        print 'exe = ' + exe
        elementList = xmldoc.getElementsByTagName('np')
        np = elementList[0].firstChild.nodeValue
        print 'np = ' + np
        elementList = xmldoc.getElementsByTagName('recomp')
        recomp = elementList[0].firstChild.nodeValue
        print 'recomp = ' + recomp
        elementList = xmldoc.getElementsByTagName('decomp')
        decomp = elementList[0].firstChild.nodeValue
        print 'decomp = ' + decomp
        elementList = xmldoc.getElementsByTagName('diff')
        diff = elementList[0].firstChild.nodeValue
        print 'diff = ' + diff


    return

if __name__ == "__main__":
    main()
