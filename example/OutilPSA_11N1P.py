# -*- coding: Utf-8 -*-
# 
import sys
sys.path.append('../sources')

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR


# ----------------------------------------------------------------------
# Creation des dents
# ----------------------------------------------------------------------

# Dents normales
PlaquetteNormale_P_Utile = {   
             'name' : 'PlaquetteNormale_P_Utile',
             'cutting_edge_geom': [{'seg_length' : 8.0e-3,                       
                                        'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 1.5e-3, 
                                        'angle_degrees': 20., 
                                        'nb_elementary_tools': 3, 'nb_slices': 1},
                                   {'seg_length' : 0.0e-3,
                                        'nb_elementary_tools': 1, 'nb_slices': 1}
                                  ],
             'insert_location': {'mediatrice_seg_idx': 0, 'dist_from_origin':0.0},
             'cut_face_thickness' : 2.8E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 5.,
         }


# Dent planeuse


plaquette = Tooth.ToothInsert(**PlaquetteNormale_P_Utile)

plaquette.draw()
# ----------------------------------------------------------------------
# Creation des etages
# ----------------------------------------------------------------------

angles = range(0,360,30)

etage = Toolstep.ToolstepModel(name = 'EtageUnique')
for alpha in angles :
    frame = etage.foref.create_frame(
           name                  = 'P_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 43.482404e-3,
    	   axial_position        = 2.922084e-3,
    	   rot_normal_degrees = 50.0,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    etage.addTooth(plaquette, frame)

# ----------------------------------------------------------------------
# Creation de l'outil
# ----------------------------------------------------------------------

outil = Tool.Tool(name = 'OUtilPSA')

frame_Etage = outil.foref.create_frame(
           name                  = 'frame_Etage',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )


outil.addToolstep(name = 'Etage_Unique', 
                  toolstep = etage, 
                  frame = frame_Etage)

outil.write('OUtilPSA.py')

outil.draw(1)
