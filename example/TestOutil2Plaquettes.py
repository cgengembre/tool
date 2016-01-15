# -*- coding: Utf-8 -*-
import sys
sys.path.append('../sources')

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

dicInsert1 = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                  ],
             'insert_location': {'mediatrice_seg_idx':0 , 'dist_from_origin':4.0e-3 }, #'bissectrice_arc_idx': 1
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 1,
             #'clearance_face_thickness' : 2.E-3,
             #'clearance_face_nb_layers' : 1,
             #'clearance_face_angle_degrees' : 20.,
             'cut_law_names' : "Generic Cut Law Name",                
             'clear_law_names' : 'Generic Clear Law Name'
         }

dent = Tooth.ToothInsert(**dicInsert1)
dent.draw()

outil = Tool.Tool(name = 'outil elicoidale de type 1')

for angle in [0., 180. ]:
    frame = outil.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "dent"+str(angle),
           father_frame_name = "Canonical",
           frame_type         = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees = 30.,
           radius              = 0.,
           axial_position      = 0.,
           rot_normal_degrees = 0.,
           rot_radial_degrees = 0.,
           rot_axial_degrees  = angle)
    outil.addTooth(dent, frame)
outil.toolstep_dic['base_toolstep'].toolstep.draw()
outil.write('Outil2plaquettesSimples')
outil.draw()
    