# -*- coding: Utf-8 -*-

# 1 creation d'une dent de fraise hélicoïdale cylindrique :
dent = tooth.ToothForHelicoidalMillType2(name = 'dent de fraise hélicoïdale de type 2',
         
         cut_face_thickness = 2.3E-3,
         cut_face_nb_layers = 1,
         mcr_rf_cl_name = "macro loi de coupe",
         #mcr_cv_cl_name = "Nom Macro loi de talonage",
         
         
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
dent.draw()

fraise = tool.Tool(name = 'fraise elicoidale de type 1')

for angle in [0., 60., 120., 180., 240., 300.  ]:
    frame = fraise.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "dent"+str(angle),
           father_frame_name  = "Canonical",
           frame_type          = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees = 30.,
           radius              = 0.,
           axial_position      = 0.,
           rot_normal_degrees = 0.,
           rot_radial_degrees = 0.,
           rot_axial_degrees  = angle)
    fraise.addTooth(dent, frame)
fraise.write('faise_helico_type1')
fraise.draw(2)
    
