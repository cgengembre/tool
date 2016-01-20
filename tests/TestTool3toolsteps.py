# -*- coding: Utf-8 -*-
# =======================
# Create  the teeth :
# =======================

# An insert tooth
# -----------------------

insert_tooth_dic = {   'name' : 'ma plaquette',
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
             'mcr_cv_cl_name' : 'MCV0',
             'mcr_rf_cl_name' : "LC0"
         }
insert_tooth = tooth.ToothInsert(**insert_tooth_dic)

# a helico cylindric tooth ball end :
# ----------------------------------------------

helico_tooth = tooth.ToothForHelicoidalMillType2(name = 'dent de fraise hélicoïdale de type 2',
         
         cut_face_thickness = 2.3E-3,
         cut_face_nb_layers = 1,
         mcr_rf_cl_name = "nom macro de loi de coupe",
         #mcr_cv_cl_name = "Macro loi de talonage",
         
         
         #clearance_face_thickness = 2.E-3,
         #clearance_face_nb_layers = 2,
         #clearance_face_angle_degrees = 30.,
        
         
         dist_from_origin = 6.0e-3, # futur radius of the mill...
         tool_tip_radius = 3.E-3,
         lenght_before = 5.E-03,
         lenght_after = 0., # 1.5E-03, #  lenght_after = 0.
         tool_tip_angle_degrees = 50.0, helix_angle_degrees = 10.0, # tool_tip_angle_degrees = 110.0, helix_angle_degrees = 10.0,

          
         seg_nb_elem_tool_before = 5, seg_nb_elem_tool_after = 3, arc_nb_elem_tool = 5,
         seg_nb_slice_before =1, seg_nb_slice_after = 1, arc_nb_slices = 2,
         
         nb_binding_slice = 1, nb_sweep = 1)
helico_tooth.draw()


# a tooth created from slices : 
# ----------------------------------------------
ball_tooth_dic = {'name' : 'dent boule SNECMA',
        'nb_elementary_tools': 30,
        'nb_slices' : 1,
        'mcr_rf_cl_name' : 'Nom macro cutlaw',
        'mcr_cv_cl_name' : 'Nom macro clearlaw',
        'cut_face_thickness' : 1.40E-3,
        'cut_face_nb_layers' : 2,
        'clearance_face_thickness' : 2.E-3,
        'clearance_face_nb_layers' : 2,
        'clearance_face_angle_degrees' : 1.20,
        
        'radius' : 4.E-3,
        'helix_angle' : 20., # or  torsion_angle_degrees
        'angle_secteur_de_coupe' : 100.,
        'angle_debut_secteur' : 5.# 90-51.3,
        }

ball_tooth = tooth.ToothForHelicoidalBallMill(**ball_tooth_dic)
ball_tooth.draw()

# =======================
# Create the Toolsteps :
# =======================
etage1 = toolstep.ToolstepModel(name = 'Etage1')
etage2 = toolstep.ToolstepModel(name = 'Etage2')
etage3 = toolstep.ToolstepModel(name = 'Etage3')



# Put the teeth in thes toolsteps : 
for alpha in range(0,360,120) :
    frame = etage1.foref.create_frame(
           name                  = 'etage1_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 4.e-3,
    	   axial_position        = 2.e-3,
    	   rot_normal_degrees = 50.0,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    etage1.addTooth(insert_tooth, frame)



for alpha in range(0,360,180) :
    frame = etage2.foref.create_frame(
           name                  = 'etage2_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 30. + alpha, 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    etage2.addTooth(ball_tooth, frame)
    
frame = etage3.foref.create_frame(
           name                  = 'etage3_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 30. + alpha, 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
etage3.addTooth(helico_tooth, frame)


#
# Create the tool :
#
tool_example = tool.Tool(name = 'Tree toolsteps tool')

# Put the toolsteps int the tool : 
frame_Etage = tool_example.foref.create_frame(
           name                  = 'frame_Etage_1',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
tool_example.addToolstep(name = 'toolstep 1', 
                  tstep = etage1, 
                  frame = frame_Etage)

frame_Etage = tool_example.foref.create_frame(
           name                  = 'frame_Etage_2',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 3.E-2,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
tool_example.addToolstep(name = 'toolstep 2', 
                  tstep = etage2, 
                  frame = frame_Etage)

frame_Etage = tool_example.foref.create_frame(
           name                  = 'frame_Etage_3',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 4.E-2,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
tool_example.addToolstep(name = 'toolstep 3', 
                  tstep = etage3, 
                  frame = frame_Etage)
                  
tool_example.write("OUT_tool_3toolsteps")
tool_example.draw(1)
