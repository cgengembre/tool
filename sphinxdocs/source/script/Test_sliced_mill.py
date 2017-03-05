# -*- coding: Utf-8 -*-

file_gtooth = 'sliced_tooth.gtooth'
bm_tooth = tooth.Tooth_sliced(
                         # Mandatory data :    
                         name = 'ball_mill_tooth',
                         cutting_edge_geom = file_gtooth,
                         nb_elementary_tools = 4,
                         nb_slices_per_elt = 5,
                         clearance_face1_nb_layers = 1,
                         clearance_face2_nb_layers = 1,
                         mcr_rf_cl_name = 'mcl_cut_face', 
                         cut_face_thickness= 1.E-3,
                         # Optional data :
                         cut_face_nb_layers = 1, # default: 1
                         mcr_cv_cl_name = 'mcl_clear_face'  # if not specified, clearance volume is
                                                            # not generated
 )

bm_tooth.draw()

bm_tool = tool.Tool(name = 'ball_mill_tool')
for angle in [0., 90., 180., 270.]:
    frame = bm_tool.toolstep_dic['base_toolstep'].toolstep.foref.create_frame(name =  "tooth_"+str(angle),
           father_frame_name = "Canonical",
           frame_type       = FoR.FRAME_CYLINDRICAL_NRA,
           origin              = [0., float(angle), 0.],
           nra                 = [0.,0.,0.]) # degrees 
    bm_tool.addTooth(bm_tooth, frame)

bm_tool.write('sliced_ball_mill')

bm_tool.draw(2)


