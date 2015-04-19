# -*- coding: Utf-8 -*-
# 
from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

tool_name = 'Tool_PSA_manifold_11N1P'
#tool_name = 'Tool_PSA_manifold_12N'

# Evolution : 

# Pb points verts et position volumes en dépouille
# Toolstep_normal.draw() : ne fonctionne pas

# methode 'foref' dans Tool et Toolstep --> FoR
# methode 'create_frame' dans Tool et Toolstep --> create
# Choix de différents types de dessin pour permettre à l'utilisateur
# de vérifier son modèle d'outil, par exemple : 
# - outil complet couleur unique mais belle avec face de coupe
# - Une couleur par étage
# - Une couleur par type de dent (pb prise en compte pour lois de coupe)
# - Dessin des pts caractéristiques en option, (idem leur taille ?)


# Notion de dent composée du plusieurs parties différentes : 
#   tooth_element / tooth / toolstep / tool 

# ----------------------------------------------------------------------
# Creation of all insert types
# ----------------------------------------------------------------------

# "Normal' insert : includes 3 portions in order to take into account
#                   the evolution of the geometry of the cutting edge
#                   and to be able to have different cutting laws.

PlaquetteNormale_P_Utile = {   
             'name' : 'PlaquetteNormale_P_Utile',
             'cutting_edge_geom': 
               [{'seg_length' : 8.0e-3,                       
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
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

PlaquetteNormale_S = {   
             'name' : 'PlaquetteNormale_S',
             'cutting_edge_geom': 
               [{'seg_length' : 0.0e-3,                       
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
                    'nb_elementary_tools': 3, 'nb_slices': 1},
                {'seg_length' : 1.2e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 10., 
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'seg_length' : 1.2e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
                    'nb_elementary_tools': 3, 'nb_slices': 1},
                {'seg_length' : 0.0e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1}
               ],
             'insert_location': {'mediatrice_seg_idx': 1, 'dist_from_origin':0.0},
             'cut_face_thickness' : 2.8E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 5.,
            }

PlaquetteNormale_P_Inutile = {   
             'name' : 'PlaquetteNormale_P_Inutile',
             'cutting_edge_geom': 
               [{'seg_length' : 0.0e-3,                       
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
                    'nb_elementary_tools': 2, 'nb_slices': 1},
                {'seg_length' : 8.0e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1}
               ],
             'insert_location': {'mediatrice_seg_idx': 1, 'dist_from_origin':0.0},
             'cut_face_thickness' : 2.8E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 5.,
            }

# "Planing' insert : includes 2 portions in order to take into account
#                    the evolution of the geometry of the cutting edge
#                    and to be able to have different cutting laws.

PlaquettePlaneuse_P = {   
             'name' : 'PlaquettePlaneuse_P',
             'cutting_edge_geom': 
               [{'seg_length' : 8.0e-3,                       
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
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


PlaquettePlaneuse_S = {   
             'name' : 'PlaquettePlaneuse_S',
             'cutting_edge_geom': 
               [{'seg_length' : 0.0e-3,                       
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
                    'nb_elementary_tools': 3, 'nb_slices': 1},
                {'seg_length' : 8.0e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.5e-3, 'angle_degrees': 20., 
                    'nb_elementary_tools': 1, 'nb_slices': 1},
                {'seg_length' : 4.0e-3,
                    'nb_elementary_tools': 1, 'nb_slices': 1}
               ],
             'insert_location': {'mediatrice_seg_idx': 1, 'dist_from_origin':0.0},
             'cut_face_thickness' : 2.8E-3,
             'cut_face_nb_layers' : 1,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 1,
             'clearance_face_angle_degrees' : 5.,
            }


# Teeth creation

Insert_normal_PU = Tooth.ToothInsert(**PlaquetteNormale_P_Utile)
Insert_normal_S  = Tooth.ToothInsert(**PlaquetteNormale_S)
Insert_normal_PI = Tooth.ToothInsert(**PlaquetteNormale_P_Inutile)

Insert_planing_P = Tooth.ToothInsert(**PlaquettePlaneuse_P)
Insert_planing_S = Tooth.ToothInsert(**PlaquettePlaneuse_S)


# ----------------------------------------------------------------------
# Tool-steps creation
# ----------------------------------------------------------------------

# In order to have a specific coloring of the planing insert
# we introduce 2 tool-steps : one for the 'normal' inserts and
# one for the 'planing' insert.


if tool_name == 'Tool_PSA_manifold_11N1P' : 

    Toolstep_planing = Toolstep.ToolstepModel(name = 'Toolstep_planing')
    
    FoR_insert_planing_P = Toolstep_planing.foref.create_frame(
           name                  = 'FoR_insert_planing_P',
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = 0.0, 
    	   radius                = 43.482404e-3,
    	   axialPosition         = 2.922084e-3,
    	   rotDegreAutourNormale = 50.0,
    	   rotDegreAutourRadiale =  0.,
    	   rotDegreAutourAxiale  =  0. )
    Toolstep_planing.addTooth(Insert_planing_P, FoR_insert_planing_P, set_id = "planing_tooth") ## /!\ CGen. - FoR_insert_planing_P est un frame 

    FoR_insert_planing_S = Toolstep_planing.foref.create_frame(
           name                  = 'Insert_planing_S',
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = 0.0, 
    	   radius                = 35.454045e-3,
    	   axialPosition         = 0.0,
    	   rotDegreAutourNormale = 90.0,
    	   rotDegreAutourRadiale =  0.0,
    	   rotDegreAutourAxiale  =  0.0 )
    Toolstep_planing.addTooth(Insert_planing_S, FoR_insert_planing_S, set_id = "planing_tooth")
    
    
if tool_name == 'Tool_PSA_manifold_11N1P' : 

    angles_toolstep_normal = range(30,360,30)

elif tool_name == 'Tool_PSA_manifold_12N' : 

    angles_toolstep_normal = range(0,360,30)

Toolstep_normal = Toolstep.ToolstepModel(name = 'toolstep_normal')

for alpha in angles_toolstep_normal :

    FoR_insert_normal_PU = Toolstep_normal.foref.create_frame(
           name                  = 'PU_'+str(alpha),
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = alpha, 
    	   radius                = 43.482404e-3,
    	   axialPosition         = 2.922084e-3,
    	   rotDegreAutourNormale = 50.0,
    	   rotDegreAutourRadiale =  0.,
    	   rotDegreAutourAxiale  =  0. )
    Toolstep_normal.addTooth(Insert_normal_PU, FoR_insert_normal_PU, set_id = str(alpha))

    FoR_insert_normal_S = Toolstep_normal.foref.create_frame(
           name                  = 'S_'+str(alpha),
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = alpha, 
    	   radius                = 38.854045e-3,
    	   axialPosition         =  0.,
    	   rotDegreAutourNormale = 90.,
    	   rotDegreAutourRadiale =  0.,
    	   rotDegreAutourAxiale  =  0. )
    Toolstep_normal.addTooth(Insert_normal_S, FoR_insert_normal_S, set_id = str(alpha))

    FoR_insert_normal_PI = Toolstep_normal.foref.create_frame(
           name                  = 'PI_'+str(alpha),
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = alpha, 
    	   radius                = 33.352058e-3,
    	   axialPosition         =  3.808374e-3,
    	   rotDegreAutourNormale = 140.,
    	   rotDegreAutourRadiale =   0.,
    	   rotDegreAutourAxiale  =   0. )
    Toolstep_normal.addTooth(Insert_normal_PI, FoR_insert_normal_PI, set_id = str(alpha))


# ----------------------------------------------------------------------
# Creation de l'outil
# ----------------------------------------------------------------------

Tool_PSA = Tool.Tool(name = tool_name)

if tool_name == 'Tool_PSA_manifold_11N1P' : 
    FoR_toolstep_planing = Tool_PSA.foref.create_frame(
           name                  = 'FoR_toolstep_planing',
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = 0., 
    	   radius                = 0.,
    	   axialPosition         = 0.,
    	   rotDegreAutourNormale = 0.,
    	   rotDegreAutourRadiale = 0.,
    	   rotDegreAutourAxiale  = 0. )
    Tool_PSA.addToolstep(name = 'Toolstep_planing', 
                  toolstep = Toolstep_planing, 
                  frame = FoR_toolstep_planing)

FoR_toolstep_normal = Tool_PSA.foref.create_frame(
           name                  = 'FoR_toolstep_normal',
    	   fatherFrameName       = "Canonical",
    	   frameType             = FoR.FRAME_CYLINDRIC_NRA,
    	   axialAngleDegrees     = 0., 
    	   radius                = 0.,
    	   axialPosition         = 0.,
    	   rotDegreAutourNormale = 0.,
    	   rotDegreAutourRadiale = 0.,
    	   rotDegreAutourAxiale  = 0. )

Tool_PSA.addToolstep( name     = 'Toolstep_normal', 
                      toolstep = Toolstep_normal, 
                      frame    = FoR_toolstep_normal)

Tool_PSA.write()


Tool_PSA.draw()
