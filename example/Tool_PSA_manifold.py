# -*- coding: Utf-8 -*-
# 


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
#                   and to be able to have different cuttings.

PlaquetteNormale_P_Utile = {   
            'mcr_rf_cl_name' : 'A',
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
            'mcr_rf_cl_name' : 'B',   
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
             'mcr_rf_cl_name' : 'C', 
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
             'mcr_rf_cl_name' : 'D',
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
             'mcr_rf_cl_name' : 'E',   
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

Insert_normal_PU = tooth.Tooth_insert(**PlaquetteNormale_P_Utile)
Insert_normal_S  = tooth.Tooth_insert(**PlaquetteNormale_S)
Insert_normal_PI = tooth.Tooth_insert(**PlaquetteNormale_P_Inutile)

Insert_planing_P = tooth.Tooth_insert(**PlaquettePlaneuse_P)
Insert_planing_S = tooth.Tooth_insert(**PlaquettePlaneuse_S)


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
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0.0, 
    	   radius                = 43.482404e-3,
    	   axial_position        = 2.922084e-3,
    	   rot_normal_degrees = 50.0,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    Toolstep_planing.addTooth(Insert_planing_P, FoR_insert_planing_P, set_id = "planing_tooth") ## /!\ CGen. - FoR_insert_planing_P est un frame 

    FoR_insert_planing_S = Toolstep_planing.foref.create_frame(
           name                  = 'Insert_planing_S',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0.0, 
    	   radius                = 35.454045e-3,
    	   axial_position        = 0.0,
    	   rot_normal_degrees = 90.0,
    	   rot_radial_degrees =  0.0,
    	   rot_axial_degrees  =  0.0 )
    Toolstep_planing.addTooth(Insert_planing_S, FoR_insert_planing_S, set_id = "planing_tooth")
    
    
if tool_name == 'Tool_PSA_manifold_11N1P' : 

    angles_toolstep_normal = range(30,360,30)

elif tool_name == 'Tool_PSA_manifold_12N' : 

    angles_toolstep_normal = range(0,360,30)

Toolstep_normal = Toolstep.ToolstepModel(name = 'toolstep_normal')

for alpha in angles_toolstep_normal :

    FoR_insert_normal_PU = Toolstep_normal.foref.create_frame(
           name                  = 'PU_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 43.482404e-3,
    	   axial_position        = 2.922084e-3,
    	   rot_normal_degrees = 50.0,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    Toolstep_normal.addTooth(Insert_normal_PU, FoR_insert_normal_PU, set_id = str(alpha))

    FoR_insert_normal_S = Toolstep_normal.foref.create_frame(
           name                  = 'S_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 38.854045e-3,
    	   axial_position        =  0.,
    	   rot_normal_degrees = 90.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    Toolstep_normal.addTooth(Insert_normal_S, FoR_insert_normal_S, set_id = str(alpha))

    FoR_insert_normal_PI = Toolstep_normal.foref.create_frame(
           name                  = 'PI_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 33.352058e-3,
    	   axial_position        =  3.808374e-3,
    	   rot_normal_degrees = 140.,
    	   rot_radial_degrees =   0.,
    	   rot_axial_degrees  =   0. )
    Toolstep_normal.addTooth(Insert_normal_PI, FoR_insert_normal_PI, set_id = str(alpha))


# ----------------------------------------------------------------------
# Creation de l'outil
# ----------------------------------------------------------------------

Tool_PSA = Tool.Tool(name = tool_name)

if tool_name == 'Tool_PSA_manifold_11N1P' : 
    FoR_toolstep_planing = Tool_PSA.foref.create_frame(
           name                  = 'FoR_toolstep_planing',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
    Tool_PSA.addToolstep(name = 'Toolstep_planing', 
                  toolstep = Toolstep_planing, 
                  frame = FoR_toolstep_planing)

FoR_toolstep_normal = Tool_PSA.foref.create_frame(
           name                  = 'FoR_toolstep_normal',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )

Tool_PSA.addToolstep( name     = 'Toolstep_normal', 
                      toolstep = Toolstep_normal, 
                      frame    = FoR_toolstep_normal)

Tool_PSA.write()


Tool_PSA.draw(1)
