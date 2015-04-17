# -*- coding: Utf-8 -*-

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

dicInsert1 = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                  ],
             'insert_location': {'mediatrice_seg_idx':0 , 'dist_from_origin':4.0e-3 }, #'bissectrice_arc_idx': 1
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 20.,
             'generic_cut_law' : "Generic Cut Law Name",                
             'generic_clear_law' : 'Generic Clear Law Name'
         }

dent = Tooth.ToothInsert(**dicInsert1)
dent.draw()

outil = Tool.Tool(name = 'outil elicoidale de type 1')

for angle in [0., 180. ]:
    frame = outil.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "dent"+str(angle),
           fatherFrameName = "Canonical",
           frameType       = FoR.FRAME_CYLINDRIC_NRA,
           axialAngleDegrees  = 30.,
           radius             = 0.,
           axialPosition      = 0.,
           rotDegreAutourNormale = 0.,
           rotDegreAutourRadiale = 0.,
           rotDegreAutourAxiale  = angle)
    outil.addTooth(dent, frame)
outil.write('faise_helico_type1')
outil.draw()
    