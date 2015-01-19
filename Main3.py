# -*- coding: Utf-8 -*-

from Tool import  Tooth #, Tool, Toolstep
# import FrameOfReference as FoR

dicInsert1 = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 1.0e-3, 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 4},
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
             'cutting_edge_geom': [{'seg_length' : 0.,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 1.0e-3, 'angle_degrees': 45, 'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'seg_length' : 0.,                      'nb_elementary_tools': 5},
                                  ],
             'insert_location': {'bissectrice_arc_idx':0 , 'dist_from_origin':4.0e-3 }, 
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 45.,

             'tooth_id': 0,
             'toolstep_id': 0
         }


plaquette = Tooth.ToothInsert(**dicInsert1Arc)
plaquette.draw()