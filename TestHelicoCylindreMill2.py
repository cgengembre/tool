# -*- coding: Utf-8 -*-

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

# 1 creation d'une dent de fraise hélicoïdale cylindrique :
dent = Tooth.ToothForHelicoidalMillType2(name = 'dent de fraise hélicoïdale de type 2',
         
         cut_face_thickness = 2.3E-3,
         cut_face_nb_layers = 1,
         
         clearance_face_thickness = 2.E-3,
         clearance_face_nb_layers = 2,
         clearance_face_angle_degrees = 30.,
        
         
         dist_from_origin = 6.0e-3, # futur radius of the mill...
         rayonBec = 3.E-3,
         longProlongAvant = 5.E-03,
         longProlongApres = 0., # 1.5E-03, #  longProlongApres = 0.
         anglePointeOutil = 50.0, angleHelice = 10.0, # anglePointeOutil = 110.0, angleHelice = 10.0,

          
         nbPartiesFlancAvant = 5, nbPartiesFlancApres = 3, nbPartiesDisque = 5,
         seg_nb_slice_before =1, seg_nb_slice_after = 1, arc_nb_slices = 2,
         
         nbCouchesLiaison = 1, nbSweep = 1)
dent.draw()

fraise = Tool.Tool(name = 'fraise elicoidale de type 1')

for angle in [0., 60., 120., 180., 240., 300.  ]:
    frame = fraise.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "dent"+str(angle),
           fatherFrameName = "Canonical",
           frameType       = FoR.FRAME_CYLINDRIC_NRA,
           axialAngleDegrees  = 30.,
           radius             = 0.,
           axialPosition      = 0.,
           rotDegreAutourNormale = 0.,
           rotDegreAutourRadiale = 0.,
           rotDegreAutourAxiale  = angle)
    fraise.addTooth(dent, frame)
fraise.write('faise_helico_type1')
fraise.draw()
    