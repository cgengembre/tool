# -*- coding: Utf-8 -*-

my_tooth = tooth.Tooth_toroidal_mill(
         name = 'tooth_toroidal_mill',
         cut_face_thickness = 1.5E-3,
         cut_face_nb_layers = 1,
         mcr_rf_cl_name = "MCL1",
         #mcr_cv_cl_name = "MCV1",
         #clearance_face_thickness = 2.E-3,
         #clearance_face_nb_layers = 2,
         #clearance_face_angle_degrees = 30.,
         dist_from_origin = 6.0e-3, # futur radius of the mill...
         tool_tip_radius = 3.E-3,
         lenght_before = 5.E-03,
         lenght_after = 1.E-03, 
         tool_tip_angle_degrees = 50.0, 
         helix_angle_degrees = 15., 
         seg_nb_elem_tool_before = 5, seg_nb_elem_tool_after = 3, arc_nb_elem_tool = 5,
         seg_nb_slice_before = 1, seg_nb_slice_after = 1, arc_nb_slices = 2,         
         nb_binding_slice = 1 )
         
# my_tooth.draw()

my_tool = tool.Tool(name = 'toroidal_mill')
for angle in [0., 60., 120., 180., 240., 300.  ]:
    frame = my_tool.base_toolstep.foref.create_frame(name =  "tooth"+str(int(angle)),
           father_frame_name  = "Canonical",
           frame_type          = FoR.FRAME_CYLINDRIC_NRA,
           axial_angle_degrees = 30.,
           radius              = 0.,
           axial_position      = 0.,
           rot_normal_degrees = 0.,
           rot_radial_degrees = 0.,
           rot_axial_degrees  = angle)
    my_tool.addTooth(my_tooth, frame)

my_tool.write('toroidal_mill')
my_tool.draw(2)
    
