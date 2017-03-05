# -*- coding: Utf-8 -*-

my_insert_dic = {
    # Mandatory data : 
    'name' : 'ma plaquette',
    'cutting_edge_geom': [
        {'seg_length': 6.0e-3, 
         'nb_elementary_tools': 1, 'nb_slices': 1},
        {'radius': 1.E-3, 'angle_degrees': 45, 
         'nb_elementary_tools': 3, 'nb_slices': 4},
        {'seg_length': 5.0e-3,
         'nb_elementary_tools': 5, 'nb_slices': 1},
        {'radius': 2.0e-3, 'angle_degrees': 30, 
         'nb_elementary_tools': 3, 'nb_slices': 3},
        {'seg_length': 8.0e-3,
         'nb_elementary_tools': 1, 'nb_slices': 4} ],
    'insert_location': {'mediatrice_seg_idx':0 , 
                        #'bissectrice_arc_idx': 1,
                        'dist_from_origin':4.0e-3 },
    'cut_face_thickness' : 3.E-3,
    'mcr_rf_cl_name' : 'mcl_rake_face',
    # optional data :
    'cut_face_nb_layers' : 2, # default: 1
    # Mandatory if clearance volume is given:
    'clearance_face_thickness' : 2.E-3,
    'clearance_face_angle_degrees' : 30.,
    'mcr_cv_cl_name' : 'mcl_rake_face',
    # Option for clearance volume :
    'clearance_face_nb_layers' : 2, # default: 1
}

my_insert = tooth.Tooth_insert(**my_insert_dic) 

my_insert.draw()

my_tool = tool.Tool(name = 'inserts_mill')
for angle in range(0,360, 120):
    frame = my_tool.base_toolstep.foref.create_frame(
           name              =  "tooth"+str(angle),
           father_frame_name = "Canonical",
           frame_type        = FoR.FRAME_CYLINDRICAL_NRA,
           origin            = [ 2.E-2, 30.+angle, 0.],
           nra               = [20.,-30.,0.]) # degrees

    my_tool.addTooth(my_insert, frame)

my_tool.write('inserts_mill')
my_tool.draw(2)