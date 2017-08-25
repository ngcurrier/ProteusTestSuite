ProteusTestSuite
================

This repository contains test cases for the ProteusCFD solver. While not complete,
it is hoped that these test cases will help new users become useful with the 
software quickly.

Test suite setup
===============

A test script is prepared and can be found in ./bin.  The script requires a recent
python install and that ucs.x, urecomp.x, and udecomp.x are runnable from the command
line.  If you are using a bash environment and have check proteusCFD out from the
git repository (by running 'git clone https://github.com/ngcurrier/ProteusCFD.git'), you
can add the following line to your ~/.bashrc file.

PATH=$PATH:~/ProteusCFD/bin:~/bin

where ~/ points to your home directory. If ProteusCFD is in another location this line
must be modified with that complete path.

After modifying you ~/.bashrc run:

'source ~/.bashrc'

to update your environment.

Also, to run all chemical tests you must build the hdf5 chemical properties database by
checking out the ProteusCFD repository and doing the following:
1) cd ProteusCFD/chemdata
2) ./chemdb.py
3) Create a symlink to the database where ProteusCFD will look.
   * ln -s /home/<your username>/chemdata/chemdb.hdf5  /usr/local/database/chemdb.hdf5

Running test script
==================

'cd ./bin'
'./runTests.py' (if the file is not executable do a chmod u+x runTests.py'

Results
========

The script runs in parallel and will report diagnostics on some of the tests cases
which are set up correctly. Test files are in each case directory and are titled 'test.xml'.