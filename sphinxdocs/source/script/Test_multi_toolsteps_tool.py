# -*- coding: Utf-8 -*-
# =======================
# Create  the teeth :
# =======================

# An triangle insert tooth
# -----------------------

insert_tooth_tri_dic = {   
    'name' : 'ma plaquette',
    'cutting_edge_geom': [
        {'seg_length': 13.728, 
         'nb_elementary_tools': 2, 'nb_slices': 1},
        {'radius': 0.8, 'angle_degrees': 120., 
         'nb_elementary_tools': 5, 'nb_slices': 1},
        {'seg_length': 13.7287187,
         'nb_elementary_tools': 3, 'nb_slices': 1},
        {'radius': 0.8, 'angle_degrees': 120., 
         'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length': 6.7287187,
         'nb_elementary_tools': 1, 'nb_slices': 1} ],
    'insert_location': {'bissectrice_arc_idx': 0 , 
                        'dist_from_origin': 0.}, 
    'cut_face_thickness': 2.4,
    'cut_face_nb_layers': 1,
    'clearance_face_thickness': 1.4,
    'clearance_face_nb_layers': 1,
    'clearance_face_angle_degrees': 20.,
    'mcr_cv_cl_name': 'MCV0',
    'mcr_rf_cl_name': "LC0" }

insert_tooth_tri = tooth.Tooth_insert(**insert_tooth_tri_dic)

# An square insert tooth
# -----------------------

insert_tooth_sqr_dic = {   
    'name' : 'ma plaquette',
    'cutting_edge_geom': [
        {'seg_length': 11.1,
         'nb_elementary_tools': 2, 'nb_slices': 1},
        {'radius': 0.8, 'angle_degrees': 90.,
         'nb_elementary_tools': 5, 'nb_slices': 1},
        {'seg_length': 11.1,
         'nb_elementary_tools': 3, 'nb_slices': 1},
        {'radius': 0.8, 'angle_degrees': 90.,
         'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length': 11.1,
         'nb_elementary_tools': 1, 'nb_slices': 1},
        {'radius': 0.8, 'angle_degrees': 90.,
         'nb_elementary_tools': 3, 'nb_slices': 1},
        {'seg_length' : 7.1,
         'nb_elementary_tools': 1, 'nb_slices': 1} ],
    'insert_location': {'bissectrice_arc_idx': 0 , 
                        'dist_from_origin': 0.}, 
    'cut_face_thickness': 2.4,
    'cut_face_nb_layers': 1,
    'clearance_face_thickness': 1.4,
    'clearance_face_nb_layers': 1,
    'clearance_face_angle_degrees': 20.,
    'mcr_cv_cl_name': 'MCV0',
    'mcr_rf_cl_name': "LC0"
}
insert_tooth_sqr = tooth.Tooth_insert(**insert_tooth_sqr_dic)

# =======================
# Create the Toolsteps :
# =======================
toolstep1 = toolstep.ToolstepModel(name = 'toolstep1')
toolstep2 = toolstep.ToolstepModel(name = 'toolstep2')
toolstep3 = toolstep.ToolstepModel(name = 'toolstep3')


#
# Put the teeth in the toolsteps : 
#

# Toolstep1 :
for alpha in range(0,360,120) :
    frame = toolstep1.foref.create_frame(
           name                = 'toolstep1_'+str(alpha),
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [36.825, float(alpha), 0.], # r,teta,z
           nra                 = [30.,0.,0.]) # degrees
    	   
    toolstep1.addTooth(insert_tooth_sqr, frame)

# Toolstep2 :
for alpha in range(0,360,180) :
    frame = toolstep2.foref.create_frame(
           name                = 'toolstep2_'+str(alpha),
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [39., float(alpha), 0.],
           nra                 = [30.,0.,0.]) # degrees

    toolstep2.addTooth(insert_tooth_tri, frame)

# Toolstep3 :
for alpha in range(0,360,180) :    
    frame = toolstep3.foref.create_frame(
           name                = 'toolstep3_'+str(alpha),
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
      	   origin              = [39.65, 60.+alpha, 0.],
           nra                 = [35.,0.,0.]) # degrees

    toolstep3.addTooth(insert_tooth_sqr, frame, set_id = 1)

for alpha in range(0,360,180) :    
    frame = toolstep3.foref.create_frame(
           name                = 'toolstep3_'+str(alpha-45),
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [44.2, -45.+alpha, 14.],
           nra                 = [0.,0.,0.]) # degrees
    	   
    toolstep3.addTooth(insert_tooth_sqr, frame, set_id = 2)

# Create the tool :
tool_example = tool.Tool(name = 'Tree toolsteps tool')

# Put the toolsteps int the tool : 
frame_Etage = tool_example.foref.create_frame(
           name                = 'frame_Etage_1',
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [0., 0., 0.],
           nra                 = [0.,0.,0.]) # degrees

tool_example.addToolstep( 
           name  = 'toolstep 1', 
           tstep = toolstep1, 
           frame = frame_Etage )

frame_Etage = tool_example.foref.create_frame(
           name                = 'frame_Etage_2',
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [0., 0., 64.15],
           nra                 = [0.,0.,0.]) # degrees
    	   
tool_example.addToolstep(
           name = 'toolstep 2', 
           tstep = toolstep2, 
           frame = frame_Etage )

frame_Etage = tool_example.foref.create_frame(
           name                = 'frame_Etage_3',
    	   father_frame_name   = "Canonical",
    	   frame_type          = FoR.FRAME_CYLINDRICAL_NRA,
    	   origin              = [0., 0., 109.5],
           nra                 = [0.,0.,0.]) # degrees
tool_example.addToolstep(
           name = 'toolstep 3', 
           tstep = toolstep3, 
           frame = frame_Etage)
                  
tool_example.write("tool_3toolsteps")
tool_example.draw(1)
