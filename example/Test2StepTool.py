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
             'cut_law_names' : "Generic Cut Law Name",                
             #'generic_clear_law' : 'Generic Clear Law Name',
             'cut_law_names' : "LC0"
         }

dent = Tooth.ToothInsert(**insert_tooth_dic)
dent.draw()


dentHelico = Tooth.ToothForHelicoidalMillType2(name = 'dent de fraise hélicoïdale de type 2',
         
         cut_face_thickness = 2.3E-3,
         cut_face_nb_layers = 1,
         cut_law_names = "Ma belle loi de coupe",
         clear_law_names = "Ma belle loi de talonage",
         
         
         clearance_face_thickness = 2.E-3,
         clearance_face_nb_layers = 2,
         clearance_face_angle_degrees = 30.,
        
         
         dist_from_origin = 4.0e-3, # futur radius of the mill...
         rayonBec = 3.E-3,
         longProlongAvant = .5E-02,
         longProlongApres = 0., # 1.5E-03, #  longProlongApres = 0.
         anglePointeOutil = 80.0, angleHelice = 10.0, # anglePointeOutil = 110.0, angleHelice = 10.0,

          
         nbPartiesFlancAvant = 5, nbPartiesFlancApres = 3, nbPartiesDisque = 5,
         seg_nb_slice_before =1, seg_nb_slice_after = 1, arc_nb_slices = 2,
         
         nbCouchesLiaison = 1, nbSweep = 1)
dentHelico.draw()



angles_toolstep_1 = range(0,360,120)
angles_toolstep_2 = range(0,360,90)


outil = Tool.Tool(name = 'Plaquette pour usinage tube2')

etage1 = Toolstep.ToolstepModel(name = 'Etage1')
for alpha in angles_toolstep_1 :
    frameEtage1 = etage1.foref.create_frame(
            name                  = 'Etage1 alpha = %f'%(alpha),
            fatherFrameName       ="Canonical",
            frameType             = FoR.FRAME_CYLINDRIC_NRA,
            axialAngleDegrees     = 0.,
            radius                = 0.,
            axialPosition         = 0.,
            rotDegreAutourNormale = 30.,
            rotDegreAutourRadiale = -30.,
            rotDegreAutourAxiale  = alpha
           )
    etage1.addTooth(dent, frameEtage1)

etage2 = Toolstep.ToolstepModel(name = 'Etage2')
for alpha in angles_toolstep_2 :
    frameEtage2 = etage2.foref.create_frame(
            name                  = 'Etage2 alpha = %f'%(alpha),
            fatherFrameName       ="Canonical",
            frameType             = FoR.FRAME_CYLINDRIC_NRA,
            axialAngleDegrees     = 0.,
            radius                = 0.,
            axialPosition         = 0.,
            rotDegreAutourNormale = 0.,
            rotDegreAutourRadiale = 0.,
            rotDegreAutourAxiale  = alpha
           )
    etage2.addTooth(dentHelico, frameEtage2)



frame = outil.foref.create_frame(
            name                  = 'Etage1 alpha = %f'%(alpha),
            fatherFrameName       ="Canonical",
            frameType             = FoR.FRAME_CYLINDRIC_NRA,
            axialAngleDegrees     = 0.,
            radius                = 0.,
            axialPosition         = 0.,
            rotDegreAutourNormale = 0.,
            rotDegreAutourRadiale = 0.,
            rotDegreAutourAxiale  = 0.
           )
outil.addToolstep(name = 'z=O.', toolstep = etage1, frame = frame)

frame = outil.foref.create_frame(
            name                  = 'Etage2 alpha = %f'%(alpha),
            fatherFrameName       ="Canonical",
            frameType             = FoR.FRAME_CYLINDRIC_NRA,
            axialAngleDegrees     = 0.,
            radius                = 0.,
            axialPosition         = 5.E-3,
            rotDegreAutourNormale = 0.,
            rotDegreAutourRadiale = 0.,
            rotDegreAutourAxiale  = 0.
           )
outil.addToolstep(name = 'z=0.1', toolstep = etage2, frame = frame)

outil.draw(0)
outil.write('mon_outil')






    
