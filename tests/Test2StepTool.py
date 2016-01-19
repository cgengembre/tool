# -*- coding: Utf-8 -*-
import sys
sys.path.append('../sources')

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR

insert_tooth_dic = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 2.5e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 0.8e-3, 'angle_degrees': 90., 'nb_elementary_tools': 6, 'nb_slices': 1},
                                   {'seg_length' : 2.5e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx': 0 , 'dist_from_origin':-0.8e-3 }, #'mediatrice_seg_idx':0'bissectrice_arc_idx': 1
             'cut_face_thickness' : 5.E-4,
             'cut_face_nb_layers' : 1,
             #'clearance_face_thickness' : 2.E-3,
             #'clearance_face_nb_layers' : 1,
             #'clearance_face_angle_degrees' : 20.,
             'mcr_rf_cl_name' : "Macro Rake Face Cut Law Name",                
             #'mcr_cv_cl_name' : 'Macro Clearance Volume Cut Law Name',
         }

dent = Tooth.ToothInsert(**insert_tooth_dic)
dent.draw()


dentHelico = Tooth.ToothForHelicoidalMillType2(name = 'dent de fraise hélicoïdale de type 2',
         
         cut_face_thickness = 2.3E-3,
         cut_face_nb_layers = 1,
         mcr_rf_cl_name = "macro rake face cut law name",
         mcr_cv_cl_name = "macro clearance volume cut law name",
         
         
         clearance_face_thickness = 2.E-3,
         clearance_face_nb_layers = 2,
         clearance_face_angle_degrees = 30.,
        
         
         dist_from_origin = 4.0e-3, # futur radius of the mill...
         tool_tip_radius = 3.E-3,
         lenght_before = .5E-02,
         lenght_after  = 0., # 1.5E-03, #  lenght_after = 0.
         tool_tip_angle_degrees = 80.0, helix_angle_degrees = 10.0, # tool_tip_angle_degrees = 110.0, helix_angle_degrees = 10.0,

          
         seg_nb_elem_tool_before = 5, seg_nb_elem_tool_after = 3, arc_nb_elem_tool = 5,
         seg_nb_slice_before =1, seg_nb_slice_after = 1, arc_nb_slices = 2,
         
         nb_binding_slice = 1, nb_sweep = 1)
dentHelico.draw()



angles_toolstep_1 = range(0,360,120)
angles_toolstep_2 = range(0,360,90)


outil = Tool.Tool(name = 'Plaquette pour usinage tube2')

etage1 = Toolstep.ToolstepModel(name = 'Etage1')
for alpha in angles_toolstep_1 :
    frameEtage1 = etage1.foref.create_frame(
            name                  = 'Etage1 alpha = %f'%(alpha),
            father_frame_name     ="Canonical",
            frame_type            = FoR.FRAME_CYLINDRIC_NRA,
            axial_angle_degrees   = 0.,
            radius                = 0.,
            axial_position        = 0.,
            rot_normal_degrees = 30.,
            rot_radial_degrees = -30.,
            rot_axial_degrees  = alpha
           )
    etage1.addTooth(dent, frameEtage1)

etage2 = Toolstep.ToolstepModel(name = 'Etage2')
for alpha in angles_toolstep_2 :
    frameEtage2 = etage2.foref.create_frame(
            name                  = 'Etage2 alpha = %f'%(alpha),
            father_frame_name     ="Canonical",
            frame_type            = FoR.FRAME_CYLINDRIC_NRA,
            axial_angle_degrees   = 0.,
            radius                = 0.,
            axial_position        = 0.,
            rot_normal_degrees = 0.,
            rot_radial_degrees = 0.,
            rot_axial_degrees  = alpha
           )
    etage2.addTooth(dentHelico, frameEtage2)



frame = outil.foref.create_frame(
            name                  = 'Etage1 alpha = %f'%(alpha),
            father_frame_name     ="Canonical",
            frame_type            = FoR.FRAME_CYLINDRIC_NRA,
            axial_angle_degrees   = 0.,
            radius                = 0.,
            axial_position        = 0.,
            rot_normal_degrees = 0.,
            rot_radial_degrees = 0.,
            rot_axial_degrees  = 0.
           )
outil.addToolstep(name = 'z=O.', toolstep = etage1, frame = frame)

frame = outil.foref.create_frame(
            name                  = 'Etage2 alpha = %f'%(alpha),
            father_frame_name     ="Canonical",
            frame_type            = FoR.FRAME_CYLINDRIC_NRA,
            axial_angle_degrees   = 0.,
            radius                = 0.,
            axial_position        = 5.E-3,
            rot_normal_degrees = 0.,
            rot_radial_degrees = 0.,
            rot_axial_degrees  = 0.
           )
outil.addToolstep(name = 'z=0.1', toolstep = etage2, frame = frame)

outil.draw(0)
outil.write('mon_outil')






    
