#!/usr/bin/env python
# -*- coding: Utf-8 -*-

# C'est modifier 26juin2020 !!!

# This file is part of the python package 'tool', itself part of nessy2m.
# 
# Copyright (C) 2010-2016
# Christophe GENGEMBRE (christophe.gengembre@ensam.eu)
# Philippe LORONG (philippe.lorong@ensam.eu)
# Amran/Lounes ILLOUL (amran.illoul@ensam.eu)
# Arts et Metiers ParisTech, Paris, France
#
# nessy2m is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nessy2m is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with nessy2m.  If not, see <http://www.gnu.org/licenses/>.
#
# Please report bugs of this package to christophe.gengembre@ensam.eu 

#--------------------------------------------------------------------------------------------------
# Christophe Gengembre
# 8 sept. 2014
#-------------------------------------------------------------------------------------------------- 
# History
# CGen. 23 juin 2020 : Test pour premier commit sous git...
#--------------------------------------------------------------------------------------------------

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
