#!/usr/bin/env python
# -*- coding: Utf-8 -*-

import os
import sys

my_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(my_dir,'..','lib'))

if not os.path.isdir('OUT'): os.mkdir('OUT')

from tool import tool, toolstep, tooth
from frame_of_reference import frame_of_reference as FoR


if len (sys.argv) < 2:
    print 'usage : ' + os.path.filename(__file__) + "<PythonScrip>"
    print '                                       ^'
    print '                       python scrip creating the tool'
    exit(1)
    

print "executing file " + sys.argv[1]
execfile(sys.argv[1])
print "DONE"