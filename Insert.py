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
            "epaisseurFaceCoupe" : 3.e-3,
            "nbCouchesFaceDeCoupe" : 2
         }
        On pourra en théorie mettre autant de segment que l'on veut. 
        S'il y a n segments il y aura n-1 arcs.
        """
        # 1 : on trnsforme dic en une structure de données plus pratique pour l'algo :
        self.dic = {}
        self.dic["nom"]= dic["nom"]
        self.dic["distanceOrigine"] = dic["distanceOrigine"]
        self.dic["epaisseurFaceCoupe"] = dic["epaisseurFaceCoupe"]
        self.dic["nbCouchesFaceDeCoupe"] = dic["nbCouchesFaceDeCoupe"]
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
        self.partiesEtMaillageFaceDeCoupe = []
        e = self.dic["epaisseurFaceCoupe"]
        nbCouchesFaceDeCoupe = self.dic["nbCouchesFaceDeCoupe"]
        if self.dic.has_key("bissectriceArc"):
            # calcule des aretes :
            idxArc = self.dic["bissectriceArc"]
            idxSeg = idxArc+1
            
            alpha = math.radians (self.dic["angleDegreArc"][idxArc])
            rayon = self.dic["rayonArc"][idxArc]
            centreArc = [0., self.dic["distanceOrigine"]] # dans (Op,zp,xp)
            
            current_angle = (math.pi-alpha)/2
            current_point = [rayon*math.cos (current_angle) + centreArc[0], rayon*math.sin (current_angle) + centreArc[1]]
             
            fistIdxMeshInPart = 0
            while idxSeg < len (self.dic["longSegment"]):
                ### Section arc :
                dicoPartie = {}
                nbPartiesArc = self.dic["nbPartiesArc"][idxArc]
                #   Arête :
                p1 = current_point 
                p2 = [rayon*math.cos (current_angle + alpha) + centreArc[0], rayon*math.sin (current_angle + alpha) + centreArc[1]]
                p3 = centreArc
                dicoPartie["tooth_id"] = 0
                dicoPartie["pnt_cut_edge"] = [[p1[1], 0., p1[0]], [p2[1], 0., p2[0]]]
                dicoPartie["pnt_in_cut_face"] = [p3[1], 0., p3[0]]
                dicoPartie["h_cut_max"] = 1.2*e
                dicoPartie["node"] = []
                dicoPartie["tri"] = []
                #   maillage :
                deltaAlpha = alpha/nbPartiesArc
                mesh_point = current_point
                mesh_angle = current_angle
                # Dans un premier temps, les triangles ont ttous pour sommet le centre de l'arc 
                # Les points :
                dicoPartie["node"].append([mesh_point[1],0,mesh_point[0]])
                for i in range (nbPartiesArc):
                    mesh_point = [rayon*math.cos (mesh_angle + (i+1)*deltaAlpha) + centreArc[0], rayon*math.sin (mesh_angle + (i+1)*deltaAlpha) + centreArc[1]]
                    dicoPartie["node"].append([mesh_point[1],0,mesh_point[0]])
                dicoPartie["node"].append([centreArc[1],0,centreArc[0]])
                # Les triangles :
                for i in range (self.dic["nbPartiesArc"][idxArc]):
                    dicoPartie["tri"].append([fistIdxMeshInPart+i,fistIdxMeshInPart+i+1, fistIdxMeshInPart + nbPartiesArc +1])
                
                self.partiesEtMaillageFaceDeCoupe.append (dicoPartie)
                ### Section Segment : 
                dicoPartie = {}
                # Le premier point du segment est p2.
                current_point = p2
                current_angle += alpha
                longSeg = self.dic["longSegment"][idxSeg]
                nbPartiesSeg = self.dic["nbPartieSeg"][idxSeg]
                deltaLongSeg = longSeg/nbPartiesSeg
                deltaEpaisseur = e/nbCouchesFaceDeCoupe
                # Arête :
                p1 = current_point
                p2 = [p1[0] - longSeg*math.cos(current_angle - math.pi/2), \
                      p1[1] - longSeg*math.sin(current_angle - math.pi/2)]
                p3 = [(p1[0]+p2[0])/2 - e*1.2*math.cos (current_angle), \
                      (p1[1]+p2[1])/2 - e*1.2*math.sin (current_angle)]
                dicoPartie["tooth_id"] = 0
                dicoPartie["pnt_cut_edge"] = [[p1[1], 0., p1[0]], [p2[1], 0., p2[0]]]
                dicoPartie["pnt_in_cut_face"] = [p3[1], 0., p3[0]]
                dicoPartie["h_cut_max"] = 1.2*e
                dicoPartie["node"] = []
                dicoPartie["tri"] = []
                # Maillage :
                mesh_point = p1
                
                # Les points :
                for j in range (nbCouchesFaceDeCoupe+1):
                    # on décale de j couches :
                    mesh_point_dep = [p1[0]-j*deltaEpaisseur*math.cos(current_angle), \
                                      p1[1]-j*deltaEpaisseur*math.sin(current_angle) ]
                    dicoPartie["node"].append([mesh_point_dep[1], 0., mesh_point_dep[0]])
                    for i in range(nbPartiesSeg):
                        next_mesh_point = [mesh_point_dep[0] - (i+1)*deltaLongSeg*math.cos(current_angle - math.pi/2), \
                                           mesh_point_dep[1] - (i+1)*deltaLongSeg*math.sin(current_angle - math.pi/2)]
                        dicoPartie["node"].append([next_mesh_point[1], 0., next_mesh_point[0]])
                # Les triangles =
                for j in range (nbCouchesFaceDeCoupe):
                    for i in range (nbPartiesSeg):
                        idxSommet1 = j*(nbPartiesSeg+1)+i
                        idxSommet2 = idxSommet1 + 1
                        idxSommet3 = idxSommet1 + nbPartiesSeg+1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                        idxSommet1 = idxSommet3
                        idxSommet2 = idxSommet2
                        idxSommet3 = idxSommet1 + 1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                self.partiesEtMaillageFaceDeCoupe.append (dicoPartie)
                idxArc += 1
                idxSeg += 1
                current_point = p2
                if idxArc < len (self.dic["rayonArc"]):
                    alpha = math.radians (self.dic["angleDegreArc"][idxArc])
                    rayon = self.dic["rayonArc"][idxArc]
                centreArc = [current_point[0] - rayon * math.cos(current_angle), \
                             current_point[1] - rayon * math.sin(current_angle)] # dans (Op,zp,xp)
            
    def showyou(self):
        bloc_util.view_bloc(self.partiesEtMaillageFaceDeCoupe)

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
            "bissectriceArc" : 1,
            # Numéro de l'arc pour definir axe x_p
            # Utiliser 'mediatriceSeg' pour un segment
            "distanceOrigine" : 4.0e-3,
            "epaisseurFaceCoupe" : 3.e-3,
            "nbCouchesFaceDeCoupe": 2
          }
    plaquette = Insert(dico)
    
    print plaquette.dic
    plaquette.showyou()