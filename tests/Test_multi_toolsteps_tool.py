# -*- coding: Utf-8 -*-
# =======================
# Create  the teeth :
# =======================

# An triangle insert tooth
# -----------------------

insert_tooth_tri_dic = {   
    'name' : 'ma plaquette',
    'cutting_edge_geom': [
        {'seg_length' : 13.7287187,                      'nb_elementary_tools': 2, 'nb_slices': 1},
        {'radius'     : 0.8, 'angle_degrees': 120., 'nb_elementary_tools': 5, 'nb_slices': 1},
        {'seg_length' : 13.7287187,                      'nb_elementary_tools': 3, 'nb_slices': 1},
        {'radius'     : 0.8, 'angle_degrees': 120., 'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length' : 6.7287187,                      'nb_elementary_tools': 1, 'nb_slices': 1},
        #{'seg_length' : 13.7287187,                      'nb_elementary_tools': 1, 'nb_slices': 1},
        #{'radius'     : 0.8, 'angle_degrees': 120., 'nb_elementary_tools': 3, 'nb_slices': 1},
        #{'seg_length' : 0.,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                         ],
    'insert_location': {'bissectrice_arc_idx': 0 , 'dist_from_origin': 0.}, #'mediatrice_seg_idx':0'bissectrice_arc_idx': 1
    'cut_face_thickness' : .8,
    'cut_face_nb_layers' : 1,
    'clearance_face_thickness' : .6,
    'clearance_face_nb_layers' : 1,
    'clearance_face_angle_degrees' : 20.,
    'mcr_cv_cl_name' : 'MCV0',
    'mcr_rf_cl_name' : "LC0"
}
insert_tooth_tri = tooth.Tooth_insert(**insert_tooth_tri_dic)

# An square insert tooth
# -----------------------

insert_tooth_sqr_dic = {   
    'name' : 'ma plaquette',
    'cutting_edge_geom': [
        {'seg_length' : 11.1,                      'nb_elementary_tools': 2, 'nb_slices': 1},
        {'radius'     : 0.8, 'angle_degrees': 90., 'nb_elementary_tools': 5, 'nb_slices': 1},
        {'seg_length' : 11.1,                      'nb_elementary_tools': 3, 'nb_slices': 1},
        {'radius'     : 0.8, 'angle_degrees': 90., 'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length' : 11.1,                      'nb_elementary_tools': 1, 'nb_slices': 1},
        {'radius'     : 0.8, 'angle_degrees': 90., 'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length' : 7.1,                      'nb_elementary_tools': 1, 'nb_slices': 1},
        #{'seg_length' : 11.1,                      'nb_elementary_tools': 1, 'nb_slices': 1},
        #{'radius'     : 0.8, 'angle_degrees': 90., 'nb_elementary_tools': 3, 'nb_slices': 1},
        #{'seg_length' : 0.,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                         ],
    'insert_location': {'bissectrice_arc_idx': 0 , 'dist_from_origin': 0.}, #'mediatrice_seg_idx':0'bissectrice_arc_idx': 1
    'cut_face_thickness' : .8,
    'cut_face_nb_layers' : 1,
    'clearance_face_thickness' : .6,
    'clearance_face_nb_layers' : 1,
    'clearance_face_angle_degrees' : 20.,
    'mcr_cv_cl_name' : 'MCV0',
    'mcr_rf_cl_name' : "LC0"
}
insert_tooth_sqr = tooth.Tooth_insert(**insert_tooth_sqr_dic)

# =======================
# Create the Toolsteps :
# =======================
toolstep1 = toolstep.ToolstepModel(name = 'toolstep1')
toolstep2 = toolstep.ToolstepModel(name = 'toolstep2')
toolstep3 = toolstep.ToolstepModel(name = 'toolstep3')
toolstep4 = toolstep.ToolstepModel(name = 'toolstep4')

#
# Put the teeth in the toolsteps : 
#

# Toolstep1 :
for alpha in range(0,360,180) : # for alpha in range(0,360,120) :
    frame = toolstep1.foref.create_frame(
           name                  = 'toolstep1_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 36.825,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 30.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    toolstep1.addTooth(insert_tooth_sqr, frame)

# Toolstep2 :
for alpha in range(0,360,180) :
    frame = toolstep2.foref.create_frame(
           name                  = 'toolstep2_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, 
    	   radius                = 39.,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 30.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    toolstep2.addTooth(insert_tooth_tri, frame)

# Toolstep3 :

for alpha in range(0,360,180) :    
    frame = toolstep3.foref.create_frame(
           name                  = 'toolstep3_'+str(alpha),
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = alpha, # 60.+alpha, 
    	   radius                = 39.65,
    	   axial_position        = 0.,
    	   rot_normal_degrees = 35.,
    	   rot_radial_degrees =  0.,
    	   rot_axial_degrees  =  0. )
    toolstep3.addTooth(insert_tooth_sqr, frame)

# Toolstep4 :
#
#for alpha in range(0,360,180) :    
#    frame = toolstep4.foref.create_frame(
#           name                  = 'toolstep4_'+str(alpha),
#    	   father_frame_name     = "Canonical",
#    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
#    	   axial_angle_degrees   = 60.+alpha, 
#    	   radius                = 39.65,
#    	   axial_position        = 109.5,
#    	   rot_normal_degrees = 35.,
#    	   rot_radial_degrees =  0.,
#    	   rot_axial_degrees  =  0. )
#    toolstep3.addTooth(insert_tooth_sqr, frame)

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
                  tstep = toolstep1, 
                  frame = frame_Etage)

frame_Etage = tool_example.foref.create_frame(
           name                  = 'frame_Etage_2',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 64.15,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
tool_example.addToolstep(name = 'toolstep 2', 
                  tstep = toolstep2, 
                  frame = frame_Etage)

frame_Etage = tool_example.foref.create_frame(
           name                  = 'frame_Etage_3',
    	   father_frame_name     = "Canonical",
    	   frame_type            = FoR.FRAME_CYLINDRIC_NRA,
    	   axial_angle_degrees   = 0., 
    	   radius                = 0.,
    	   axial_position        = 109.5,
    	   rot_normal_degrees = 0.,
    	   rot_radial_degrees = 0.,
    	   rot_axial_degrees  = 0. )
tool_example.addToolstep(name = 'toolstep 3', 
                  tstep = toolstep3, 
                  frame = frame_Etage)
                  
tool_example.write("OUT_tool_3toolsteps")
tool_example.draw(1)
