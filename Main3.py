# -*- coding: Utf-8 -*-

from Tool import  Tooth #, Tool, Toolstep
# import FrameOfReference as FoR

dicInsert1 = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 1.E-3, 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 4}, # radius = 1.E-3
                                   {'seg_length' : 5.0e-3,                      'nb_elementary_tools': 5},
                                   {'radius'     : 2.0e-3, 'angle_degrees': 30, 'nb_elementary_tools': 3, 'nb_slices': 3},
                                   {'seg_length' : 8.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'mediatrice_seg_idx':0 , 'dist_from_origin':4.0e-3 }, #'bissectrice_arc_idx': 1
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 2,
             'clearance_face_angle_degrees' : 45.,

             'tooth_id': 0,
             'toolstep_id': 0
         }
dicInsert1Arc = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : .0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 2.0e-3, 'angle_degrees': 45, 'nb_elementary_tools': 1, 'nb_slices': 3},
                                   {'seg_length' : 0.e-3,                      'nb_elementary_tools': 5},
                                  ],
             'insert_location': {'bissectrice_arc_idx':0 , 'dist_from_origin':2.0e-3 }, 
             'cut_face_thickness' :0.75E-3,
             'cut_face_nb_layers' : 3   ,
             'clearance_face_thickness' :3.12E-3,
             'clearance_face_nb_layers' :4,
             'clearance_face_angle_degrees' : 40.,

             'tooth_id': 0,
             'toolstep_id': 0
         }

#dicInsert1Arc['clearance_face_thickness'] = 2.E-2 # pour tester la pointe en dessous
#dicInsert1Arc['cut_face_thickness'] = .25E-2 # Maillage face arrière
#dicInsert1Arc['clearance_face_thickness'] = 0.5E-2 # pas de pointe en dessous

plaquette = Tooth.ToothInsert(**dicInsert1) #Arc)

plaquette.draw()