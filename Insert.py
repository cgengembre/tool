# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 12 oct. 2014


import math
import numpy as np
import bloc_util

class Insert :
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self, dic):
        """
        Structure de dic :
    	{
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
            "epaisseurFaceCoupe" : 3.e-3
        }
        On pourra en théorie mettre autant de segment que l'on veut. 
        S'il y a n segments il y aura n-1 arcs.
        """
        # 1 : on trnsforme dic en une structure de données plus pratique pour l'algo :
        self.dic = {}
        self.dic["nom"]= dic["nom"]
        self.dic["distanceOrigine"] = dic["distanceOrigine"]
        self.dic["epaisseurFaceCoupe"] = dic["epaisseurFaceCoupe"]
        if dic.has_key("bissectriceArc"):
            self.dic["bissectriceArc"] = dic["bissectriceArc"]-1
        else : self.dic["mediatriceSeg"] = dic["mediatriceSeg"]-1
        
        # une première passe pour compter le nombre de segments :
        nbSeg = 0
        for key in dic.keys():
            if key[0:-1] == "longSegment" :
                if nbSeg < int (key[-1]) : nbSeg = int(key[-1])
        
        # initialisation des listes :
        self.dic["longSegment"] = [i for i in range(nbSeg)]
        self.dic["nbPartieSeg"] = [i for i in range(nbSeg)]
        self.dic["rayonArc"] = [i for i in range(nbSeg-1)]
        self.dic["angleDegreArc"] = [i for i in range(nbSeg-1)]
        self.dic["nbPartiesArc"] = [i for i in range(nbSeg-1)]
        
        # Une passe pour remplir les listes :
        for key in dic.keys():
            
            if key[0:-1] == "longSegment" :
                self.dic["longSegment"][int(key[-1])-1] = dic[key]
                
            if key[0:-1] == "nbPartieSeg" :
                self.dic["nbPartieSeg"][int(key[-1])-1] = dic[key]
                
            if key[0:-1] == "rayonArc" :
                self.dic["rayonArc"][int(key[-1])-1] = dic[key]
                
            if key[0:-1] == "angleDegreArc" :
                self.dic["angleDegreArc"][int(key[-1])-1] = dic[key]
                
            if key[0:-1] == "nbPartiesArc" :
                self.dic["nbPartiesArc"][int(key[-1])-1] = dic[key]
        # Calcul des points dans le plan (Op, zp, xp):
        self.__generePartiesEtMaillagePlaquette__()

# --------------------------------------------------------------------------------------------------        
    def __generePartiesEtMaillagePlaquette__(self):
        # On effectue  tous les calculs dans le repère (Op,zp,xp).
        # On ajoute yp lors de la creation des dictionnaires à passer en entrée de donnnées.
        if self.dic.has_key("bissectriceArc"):
            # calcule des aretes :
            idxArc = self.dic["bissectriceArc"]
            idxSeg = idxArg+1
            
            alpha = math.radians (self.dic["angleDegreArc"][idxArc])
            rayon = self.dic["rayonArc"][idxArc]
            centreArc = [0., self.dic["distanceOrigine"]] # dans (Op,zp,xp)
            
            point = [rayon*math.cos ((math.pi-alpha)/2), rayon*math.sin ((math.pi-alpha)/2) + centreArc[1]]
            while idxSeg < len (self.dic["longSegment"]):
                
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
        
if __name__ == "__main__":
    dico = {
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
            "epaisseurFaceCoupe" : 3.e-3
          }
    plaquette = Insert(dico)
    print plaquette.dic