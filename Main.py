# -*- coding: Utf-8 -*-
#
#

# Outil, piece, trajectoire.
# 1: création de l'outil

from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR
#fraise = Tool.FraiseMonoblocType1 (idNoeudMaitre      = 1,    # Champ facultatif
#  loiDeCoupe         = "nomLoiCoupe",
#  angleAxialInitial  = 0.0,
#  diametreFraise     = 6.0e-3,
#  longueurSuivantAxe = 10.0e-3, deltaBetaDegres = 90.0,
#  epaisseurFaceCoupe = 1.5e-3,
#  nbDents            = 8, nbParties = 6,
#  nbTranches         = 3, nbCouchesFaceCoupe = 5,
#  nbCouchesLiaison   = 1, nbSweep = 1)
dic = {  
                "nbParties" : 10, 
                "nbTranches" : 3, 
                "nbCouchesFaceCoupe" : 4,
                "nbCouchesLiaison" : 1,
                "nbSweep" :1,
                # Parametres géométriques
                "angleAxialInitial" : 0.0, 
                "angleHelice" : 40.0,
                "idNoeudMaitre" : 1,
                "loiDeCoupe" : ["Loi1","Loi2","Loi3"],
                "diametreFraise" : 6.0E-3,
                "epaisseurFaceCoupe" : 0.5e-3,
                "nbDents" : 1,
                # parmetres propres à la fraise boule.
                "angleSecteurCoupe" : 180.,
                "angleDebutSecteur" :  0.0#,
                #"rayonTore" : 4.0E-3 # rayonTore = -1. => fraise boule,
                                           # 0<rayonTore<diametreFraise/2 => fraise torique.
      }
 
# fraise = Tool.ToreMonoblocMill(dic)                # Parametres pour la structure de données
##fraise = Tool.MonoblocMillType1 (dic)
 
# 2: affichage de l'outil avec viewer3D
## fraise.showyou()

# Test de fraise à plaquette :
dico1 = {
    	    "nom" : "nomModelGeomPlaquette",
            "longSegment1" : 6.0e-3, "nbPartieSeg1"   :  4,
            "rayonArc1"    : 1.0e-3, "angleDegreArc1" : 45, "nbPartiesArc1":3,
            "longSegment2" : 5.0e-3, "nbPartieSeg2"   :  5,
            "rayonArc2"    : 2.0e-3, "angleDegreArc2" : 30, "nbPartiesArc2":3,
            "longSegment3" : 8.0e-3, "nbPartieSeg3"   : 4,
            "bissectriceArc" : 2,
            # Numéro de l'arc pour definir axe x_p
            # Utiliser 'mediatriceSeg' pour un segment
            "distanceOrigine" : 4.0e-3,
            "epaisseurFaceCoupe" : 3.e-3,
            "nbCouchesFaceDeCoupe": 2
            }
dicPlaquette1Segment ={
    	    "nom" : "nomModelGeomPlaquette",
            "longSegment1" : 6.0e-3, "nbPartieSeg1"   :  4,
            #"bissectriceArc" : 2,
            "mediatriceSeg": 1,
            # Numéro de l'arc pour definir axe x_p
            # Utiliser 'mediatriceSeg' pour un segment
            "distanceOrigine" : 4.0e-3,
            "epaisseurFaceCoupe" : 3.e-3,
            "nbCouchesFaceDeCoupe": 2
           } 
dicPlaquetteEquerre = {
    	    "nom" : "nomModelGeomPlaquette",
            "longSegment1" : 4.0e-3, "nbPartieSeg1"   :  16,
            "rayonArc1"    : 1.0e-3, "angleDegreArc1" : 90, "nbPartiesArc1":3,
            "longSegment2" : 1.4e-3, "nbPartieSeg2"   :  7,
            "mediatriceSeg" : 1,
            # Numéro de l'arc pour definir axe x_p
            # Utiliser 'mediatriceSeg' pour un segment
            "distanceOrigine" : 4.0e-3,
            "epaisseurFaceCoupe" : 1.e-3,
            "nbCouchesFaceDeCoupe": 2
            }
            
            
dicInsert1 = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 4},
                                   {'radius'     : 1.0e-3, 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 4},
                                   {'seg_length' : 5.0e-3,                      'nb_elementary_tools': 5},
                                   {'radius'     : 2.0e-3, 'angle_degrees': 30, 'nb_elementary_tools': 3, 'nb_slices': 3},
                                   {'seg_length' : 8.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx': 1, 'dist_from_origin':4.0e-3 },
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 2,
             'clearance_face_angle_degrees' : 45.,

             'tooth_id': 0,
             'toolstep_id': 0
         }
dicInsert1Arc = {   'name' : 'ma plaquette',
             'cutting_edge_geom': [{'seg_length' : .0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                                   {'radius'     : 2.0e-3, 'angle_degrees': 180, 'nb_elementary_tools': 5, 'nb_slices': 2},
                                   {'seg_length' : 0.e-3,                      'nb_elementary_tools': 5},
                                  ],
             'insert_location': {'bissectrice_arc_idx':0 , 'dist_from_origin':2.0e-3 }, 
             'cut_face_thickness' :0.75E-3,
             'cut_face_nb_layers' : 3   ,
             'clearance_face_thickness' :3.12E-3,
             'clearance_face_nb_layers' :4,
             'clearance_face_angle_degrees' : 40.,

             'tooth_id': 0,
             'toolstep_id': 0
         }

dicFramePlaquette = {
            "name"            : "repere plaquette ",
    	   "fatherFrameName" : "Canonical",
    	   "frameType"       : FoR.INSERT_FRAME_AROUND_A_MILL,
    	   "axialAngleDegrees"  : 90.,
    	   "radius"             : 20.0E-3,
    	   "axialPosition"      : 3.0E-3,
    	   "rotDegreAutourNormale" : 0.,
    	   "rotDegreAutourRadiale" : -20.,
    	   "rotDegreAutourAxiale"  : 0.
    	   }
dicFrameEtage = {
            "name"            : "repere etage1",
           "fatherFrameName" : "Canonical",
           "frameType"       : FoR.INSERT_FRAME_AROUND_A_MILL,
           "axialAngleDegrees"  : 0.,
           "radius"             : 0.,
           "axialPosition"      : 7.0E-3,
           "rotDegreAutourNormale" : 0.,
           "rotDegreAutourRadiale" : 0.,
           "rotDegreAutourAxiale"  : 0.
           }
dicFraisePlaquettes = {
           "name" : "fraisePlaquette",
           "insert" : dicInsert1, #dicPlaquetteEquerre,
           "insertFrame" : dicFramePlaquette,
           "nbDents" : 8
          }
          
#def test():
#    fraise_avec_plaquettes  = Tool.WithInsertsMill(dicFraisePlaquettes)
#    fraise_avec_plaquettes.showyou()

# Exemple 1 :
# fraise_avec_plaquettes  = Tool.WithInsertsMill(dicFraisePlaquettes)
# fraise_avec_plaquettes.showyou()

# Exemple 2 :

### Fraise à plaquettes
#fraise  = Tool.Tool(name='fraise')
#plaquette = Insert.Insert(**dico1_nouveau_1)
#angles = [0,10, 90, 100, 180, 190, 270, 280  ]
#for alpha in angles :
#    dicFramePlaquette['axialAngleDegrees'] = alpha
#    dicFramePlaquette['name'] = 'reperePlaquette alpha = %f'%(alpha)
#    frame = fraise.tool_for.create_frame(**dicFramePlaquette)
#    fraise.addTooth(plaquette, frame)
#fraise.draw()
### Outil à étages
angles = [0, 90,  180,  270  ]
angles2 = [10, 100,  190, 280  ]
plaquette = Tooth.ToothInsert(**dicInsert1)
plaquette.draw()
plaquetteArc = Tooth.ToothInsert(**dicInsert1Arc)
plaquette.draw()

outil = Tool.Tool(name = 'toolstep_tool1')
etage = Toolstep.ToolstepModel(name = 'Un modele d etage')
for alpha in angles :
    dicFramePlaquette['axialAngleDegrees'] = alpha
    dicFramePlaquette['name'] = 'reperePlaquette alpha = %f'%(alpha)
    frame = outil.tool_for.create_frame(**dicFramePlaquette)
    etage.addTooth(plaquette, frame)
for alpha in angles2 :
    dicFramePlaquette['axialAngleDegrees'] = alpha
    dicFramePlaquette['name'] = 'reperePlaquette alpha = %f'%(alpha)
    frame = outil.tool_for.create_frame(**dicFramePlaquette)
    etage.addTooth(plaquetteArc, frame)
for z in [3.0E-3, 1.6E-2]:
    dicFrameEtage['axialPosition'] = z
    dicFrameEtage['name'] = 'pour z = %f'%(z)
    frame = outil.tool_for.create_frame(**dicFrameEtage)
    outil.addToolstep(name = 'z=%f'%z, toolstep = etage, frame = frame)
outil.draw()
    