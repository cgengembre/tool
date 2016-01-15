# -*- coding: Utf-8 -*-
import sys
sys.path.append('../sources')

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

insert_tool_dic = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 2.5e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 0.8e-3, 'angle_degrees': 90., 'nb_elementary_tools': 6, 'nb_slices': 1},
                                   {'seg_length' : 2.5e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx': 0 , 'dist_from_origin':-0.8e-3 }, #'mediatrice_seg_idx':0'bissectrice_arc_idx': 1
             'cut_face_thickness' : .5E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 1.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 20.,
             'generic_cut_law' : "Generic Cut Law Name",                
             'generic_clear_law' : 'Generic Clear Law Name',
             'cut_law_names' : "LC0"
         }

dent = Tooth.ToothInsert(**insert_tool_dic)
dent.draw()

outil = Tool.Tool(name = 'Plaquette pour usinage tube2')


frame = outil.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "Position Plaquette",
           father_frame_name  = "Canonical",
           frame_type         = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees  = 0.,
           radius             = 0.,
           axial_position     = 0.,
           rot_normal_degrees = - 90.,
           rot_radial_degrees = 0.,
           rot_axial_degrees  = 0.)
outil.addTooth(dent, frame)
outil.write('PlaquettePourTube2')
outil.draw()
    
