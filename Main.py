# -*- coding: Utf-8 -*-
#
#

# Outil, piece, trajectoire.
# 1: création de l'outil
import Tools
import Insert
import FrameOfReference as Fom
#fraise = Tools.FraiseMonoblocType1 (idNoeudMaitre      = 1,    # Champ facultatif
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
 
# fraise = Tools.ToreMonoblocMill(dic)                # Parametres pour la structure de données
##fraise = Tools.MonoblocMillType1 (dic)
 
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
dicFramePlaquette = {
            "name"            : "repere plaquette ",
    	   "fatherFrameName" : "Canonical",
    	   "frameType"       : Fom.INSERT_FRAME_AROUND_A_MILL,
    	   "axialAngleDegrees"  : 90.,
    	   "radius"             : 20.0E-3,
    	   "axialPosition"      : 5.0E-3,
    	   "rotDegreAutourNormale" : 0.,
    	   "rotDegreAutourRadiale" : 20.,
    	   "rotDegreAutourAxiale"  : 0.
    	   }
    	   
dicFraisePlaquettes = {
           "name" : "fraisePlaquette",
           "insert" : dicPlaquetteEquerre,
           "insertFrame" : dicFramePlaquette,
           "nbDents" : 8
          }
          
#def test():
#    fraise_avec_plaquettes  = Tools.WithInsertsMill(dicFraisePlaquettes)
#    fraise_avec_plaquettes.showyou()

fraise_avec_plaquettes  = Tools.WithInsertsMill(dicFraisePlaquettes)
fraise_avec_plaquettes.showyou()