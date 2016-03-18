# -*- coding: Utf-8 -*-

dic_bm_tooth = {
        # Mandatory data : 
        'name' : 'ball_mill_tooth',
        'radius' : 4.E-3,
        'init_angle_degrees' : 5. ,
        'cutting_angle_degrees' : 160., 
        'cut_face_thickness' : 0.80E-3,
        'nb_elementary_tools': 20,  
        'mcr_rf_cl_name' : 'mcl_rake_face',
        # optional data :
        'helix_angle_degrees': 20., # default: 0.0
        'cut_face_nb_layers' : 2,   # default: 1
        'nb_slices'          : 3,   # default: 1       
        # mandatory data if clearance volume is present
        #'mcr_cv_cl_name' : 'mcl_clear_face',
        #'clearance_face_thickness' : 1.5E-3,
        #'clearance_face_angle_degrees' : 1.20,
        # optional data
        #'clearance_face_nb_layers' : 2 # default: 1
        
        }

bm_tooth = tooth.Tooth_ball_mill(**dic_bm_tooth)

bm_tooth.draw()

bm_tool = tool.Tool(name = 'Ball_mill_tool')


## TODO : modify waited dic :  
            # "origin"        : [radius, teta_degrees, zO] # dans le fatherFrame
            # "nra_rotations" : [normal_angle_degrees, radial_angle_degrees, axial_angle_degrees]
for angle in range (0, 360, 90) :
    frame = bm_tool.base_toolstep.foref.create_frame(name = "Tooth position "+str(angle)+" degrees",
           father_frame_name   = "Canonical",
           frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
           origin              = [0., float(angle), 0.],
           nra                 = [0.,0.,0.]) # degrees
    bm_tool.addTooth(bm_tooth, frame)

bm_tool.write('Ball_mill_tool')
bm_tool.draw()