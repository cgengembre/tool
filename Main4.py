# -*- coding: Utf-8 -*-

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

# 1 creation d'une dent de fraise hélicoïdale cylindrique :
dent = Tooth.ToothForHelicoidalMillType1(name = 'toothMonoblocTyp1',
                                         nb_elementary_tools      = 1,
                                         nb_slices                = 4,
        
                                         cut_face_thickness       = 3.E-3,
                                         cut_face_nb_layers       = 2,
                                         clearance_face_thickness = 2.E-3,
                                         clearance_face_nb_layers = 2,
                                         clearance_face_angle_degrees = 45.,
        
                                         radius                   = 1.6E-3,
                                         height                   = 2.E-3,
                                         torsion_angle_degrees    = 30)
dent.draw()