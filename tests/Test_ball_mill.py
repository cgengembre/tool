# -*- coding: Utf-8 -*-

dic_bm_tooth = {
        'name' : 'ball_mill_tooth',
        'cut_face_thickness' : 0.80E-3,
        'cut_face_nb_layers' : 2,
        'clearance_face_thickness' : 1.5E-3,
        'clearance_face_nb_layers' : 2,
        'clearance_face_angle_degrees' : 1.20,
        'mcr_rf_cl_name' : 'mcl_rake_face',
        'mcr_cv_cl_name' : 'mcl_clear_face',
        'radius' : 4.E-3,
        'nb_slices' : 3,
        'cutting_angle_degrees' : 160., 
        'nb_elementary_tools': 20,  
        'helix_angle' : 20., # or  torsion_angle_degrees
        'init_angle_degrees' : 5. 
        }

bm_tooth = tooth.Tooth_ball_mill(**dic_bm_tooth)

bm_tooth.draw()

bm_tool = tool.Tool(name = 'Ball_mill_tool')

for angle in range (0, 360, 90) :
    frame = bm_tool.base_toolstep.foref.create_frame(name = "Tooth position "+str(angle)+" degrees",
           father_frame_name   = "Canonical",
           frame_type          = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees = 0.,
           radius              = 0.,
           axial_position      = 0.,
           rot_normal_degrees  = 0.,
           rot_radial_degrees  = 0.,
           rot_axial_degrees   = float(angle) )
    bm_tool.addTooth(bm_tooth, frame)

bm_tool.write('Ball_mill_tool')
bm_tool.draw()
    
