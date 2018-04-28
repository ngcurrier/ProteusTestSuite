#!/usr/bin/python
# This script runs over the h5 files in the folder and converts them to gold files for test scripts

import glob
import os
from shutil import copyfile
from subprocess import call

def main():
    for file in glob.glob("*.h5"):
        oldfile = file
        # drop the extension
        newfile = oldfile.replace('.h5','')
        # ignore any gold files present
        if oldfile.find('gold') != -1:
            continue
        # next value is the process ID
        loc = newfile.rfind('.')
        if loc ==  -1:
            print 'FAILURE!!!!, wrong string format'
            exit()
        else:
            procid = newfile[loc+1:]
            newfile = newfile[0:loc]
            newfile.rfind('.')
            newfile = newfile + '.gold.' + procid  + '.h5'
            print oldfile + ' --> ' + newfile
        copyfile(oldfile, newfile)
    
    
if __name__ == "__main__":
    print '------ REBLESSING ALL FILES IN DIRECTORY------'
    main()
    response = raw_input('Would you like to checkin the update? (y/n)')
    if response != 'y' and response != 'n':
        print 'Valid response is only (y/n), exiting'
        exit()
    if response ==  'y':
        print '------------- COMMITING ------------------'
        os.system('git commit -m "Commiting new gold files" *gold.*.h5')

