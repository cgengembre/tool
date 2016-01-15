# -*- coding: Utf-8 -*-
import sys
sys.path.append('../sources')

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

# 1 creation d'une dent de fraise hélicoïdale cylindrique :
dent = Tooth.ToothForHelicoidalMillType1(name = 'toothMonoblocTyp1',
                                         nb_elementary_tools      = 3,
                                         nb_slices                = 4,
                                         cut_law_names = "Ma belle loi de coupe",
                                         clear_law_names = "Ma belle loi de talonage",
                                         cut_face_thickness       = 2.E-3,
                                         cut_face_nb_layers       = 2,
                                         clearance_face_thickness = 2.E-3,
                                         clearance_face_nb_layers = 2,
                                         clearance_face_angle_degrees = 30.,
        
                                         radius                   = 3.6E-3,
                                         height                   = 2.E-3,
                                         torsion_angle_degrees    = 40.)
dent.draw()

fraise = Tool.Tool(name = 'Helicoidal mill type 1')

for angle in [0., 60., 120., 180., 240., 300.  ]:
    frame = fraise.base_toolstep.foref.create_frame(name =  "dent"+str(angle),
           father_frame_name = "Canonical",
           frame_type        = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees = 30.,
           radius              = 0.,
           axial_position      = 0.,
           rot_normal_degrees = 0.,
           rot_radial_degrees = 0.,
           rot_axial_degrees  = angle)
    fraise.addTooth(dent, frame)
fraise.write('faise_helico_type1')
fraise.draw()
    