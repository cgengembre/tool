# -*- coding: Utf-8 -*-

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

# 1 creation d'une dent de fraise hélicoïdale cylindrique :
dent = Tooth.ToothForHelicoidalMillType1(name = 'toothMonoblocTyp1',
                                         nb_elementary_tools      = 1,
                                         nb_slices                = 4,
        
                                         cut_face_thickness       = 1.E-3,
                                         cut_face_nb_layers       = 2,
                                         clearance_face_thickness = 2.E-3,
                                         clearance_face_nb_layers = 2,
                                         clearance_face_angle_degrees = 30.,
        
                                         radius                   = 3.6E-3,
                                         height                   = 2.E-3,
                                         torsion_angle_degrees    = 30)
dent.draw()

fraise = Tool.Tool(name = 'fraise elicoidale de type 1')

for angle in [0., 60., 120., 180., 240., 300.  ]:
    frame = fraise.foref.create_frame(name =  "dent"+str(angle),
           fatherFrameName = "Canonical",
           frameType       = FoR.INSERT_FRAME_AROUND_A_MILL,
           axialAngleDegrees  = 30.,
           radius             = 0.,
           axialPosition      = 0.,
           rotDegreAutourNormale = 0.,
           rotDegreAutourRadiale = 0.,
           rotDegreAutourAxiale  = angle)
    fraise.addTooth(dent, frame)
fraise.write('faise_helico_type1')
fraise.draw()
    