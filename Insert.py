# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 12 oct. 2014


import math
import numpy as np
from Tooth import Tooth

class Insert(Tooth) :
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
         autre : 
         {   
             'name' : 'ma plaquette',
             'tooth_id': 0,
             'storey_id': 0,
             
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2,

             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                'nb_elementary_tools': 4, 'nb_slices': 1}, # même nbSlices pour chaque el. tool
                                   {'angle_degrees': 45, 'radius':1.0e-3, 'nb_elementary_tools': 4, 'nb_slices': 1},
                                   {'seg_length' : 5.0e-3,                'nb_elementary_tools': 5, 'nb_slices': 1},
                                   {'angle_degrees': 30, 'radius':2.0e-3, 'nb_elementary_tools': 4, 'nb_slices': 1},
                                   ...
                                   {'seg_length' : 8.0e-3,                'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx'|'mediatrice_seg_idx': 2, 'dist_from_origin':4.0e-3 }
         }
         On pourra en théorie mettre autant de segment que l'on veut. 
         S'il y a n segments il y aura n-1 arcs.
        """
        Tooth.__init__(self, dic) 
        ## On compte le nombre d'elementary_tools :
        self.nb_elementary_tools = 0 # par prudence ...
        for ceg_dic in dic['cutting_edge_geom']:
            self.nb_elementary_tools += ceg_dic['nb_elementary_tools']

        # 1 : on transforme dic en une structure de données plus pratique pour l'algo :
        
        if dic.has_key('cutting_edge_geom'):
            # partie "commune" entre self.dic et dic :
            
            self.dic["dist_from_origin"] = dic['insert_location']["dist_from_origin"]
            if dic["insert_location"].has_key("bissectrice_arc_idx"):
                self.dic["bissectrice_arc_idx"] = dic["insert_location"]["bissectrice_arc_idx"]
            else : self.dic["mediatrice_seg_idx"] = dic["insert_location"]["mediatrice_seg_idx"]
            # On determine le nombre de segments
            nbSeg = 1+len (dic['cutting_edge_geom'])/2
            ## Gestion du nb_slice qui est facultatif :
            for ceg_dic in dic['cutting_edge_geom']: #
                if not ceg_dic.has_key('nb_slices'): # tous les dico de dic['cutting_edge_geom']
                    ceg_dic['nb_slices'] = 1         # on maintenant une clé 'nb_slices'
            ## Controle du contenu de dic :
            for ceg_dic in dic['cutting_edge_geom']:
                print ceg_dic

            # Construction des liste 
            self.dic['seg_length_list'] = [dic['cutting_edge_geom'][2*i]['seg_length'] for i in range (nbSeg)]
            self.dic['seg_nb_elementary_tools_list'] = [dic['cutting_edge_geom'][2*i]['nb_elementary_tools'] for i in range (nbSeg)]
            self.dic['seg_nb_slices_list'] = [dic['cutting_edge_geom'][2*i]['nb_slices'] for i in range (nbSeg)]
            #self.dic['seg_length_list'] = [dic['cutting_edge_geom'][2*i]['seg_length'] for i in range (nbSeg)]
            ##
            self.dic['arc_angle_degrees_list'] = [dic['cutting_edge_geom'][2*i+1]['angle_degrees'] for i in range (nbSeg-1)]
            self.dic['arc_nb_elementary_tools_list'] = [dic['cutting_edge_geom'][2*i+1]['nb_elementary_tools'] for i in range (nbSeg-1)]            
            self.dic['radius_list'] = [dic['cutting_edge_geom'][2*i+1]['radius'] for i in range (nbSeg-1)]
            self.dic['arc_nb_slices_list'] = [dic['cutting_edge_geom'][2*i+1]['nb_slices'] for i in range (nbSeg-1)]
        else:

            self.dic["dist_from_origin"] = dic["distanceOrigine"]
            if dic.has_key("bissectriceArc"):
                self.dic["bissectrice_arc_idx"] = dic["bissectriceArc"]-1
            else : self.dic["mediatrice_seg_idx"] = dic["mediatriceSeg"]-1
            
            # une première passe pour compter le nombre de segments :
            nbSeg = 0
            for key in dic.keys():
                if key[0:-1] == "longSegment" :
                    if nbSeg < int (key[-1]) : nbSeg = int(key[-1])
            
            # initialisation des listes :
            self.dic["seg_length_list"] = [i for i in range(nbSeg)]
            self.dic["seg_nb_elementary_tools_list"] = [i for i in range(nbSeg)]
            self.dic["radius_list"] = [i for i in range(nbSeg-1)]
            self.dic["arc_angle_degrees_list"] = [i for i in range(nbSeg-1)]
            self.dic["arc_nb_elementary_tools_list"] = [i for i in range(nbSeg-1)]
            
            # Une passe pour remplir les listes :
            for key in dic.keys():
                
                if key[0:-1] == "longSegment" :
                    self.dic["seg_length_list"][int(key[-1])-1] = dic[key]
                    
                if key[0:-1] == "nbPartieSeg" :
                    self.dic["seg_nb_elementary_tools_list"][int(key[-1])-1] = dic[key]
                    
                if key[0:-1] == "rayonArc" :
                    self.dic["radius_list"][int(key[-1])-1] = dic[key]
                    
                if key[0:-1] == "angleDegreArc" :
                    self.dic["arc_angle_degrees_list"][int(key[-1])-1] = dic[key]
                    
                if key[0:-1] == "nbPartiesArc" :
                    self.dic["arc_nb_elementary_tools_list"][int(key[-1])-1] = dic[key]
        # Calcul des points dans le plan (Op, zp, xp):
        print self.dic
        self.__generePartiesEtMaillagePlaquette__()
# --------------------------------------------------------------------------------------------------
    def __generePartiesEtMaillageArc__(self, idxArc, current_point, current_angle, next_point, next_angle):
        dicoPartie = {}
        print "__generePartiesEtMaillageArc__  -  idxArc = %d\n"%(idxArc) 
        nbPartiesArc = self.dic["arc_nb_elementary_tools_list"][idxArc]
        rayon = self.dic["radius_list"][idxArc]
        alpha = math.radians(self.dic["arc_angle_degrees_list"][idxArc])
        e  = self.dic["cut_face_thickness"]
        centreArc = [current_point[0] - rayon * math.cos(current_angle), \
                     current_point[1] - rayon * math.sin(current_angle)] # dans (Op,zp,xp)
        
        nbCouches = self.dic['cut_face_nb_layers']
        epCouche = e/nbCouches
        
        nbSlices = self.dic['arc_nb_slices_list'][idxArc]
        if rayon > 0:
            #   Arête :
            cur_point_local = [current_point[0], current_point[1]]
            cur_angle_local = current_angle
            deltaAlpha = alpha/nbPartiesArc
            sliceAngle = deltaAlpha/nbSlices
            for k in range (nbPartiesArc):
                dicoPartie = {}
                p1 = cur_point_local 
                p2 = [rayon*math.cos (cur_angle_local + deltaAlpha) + centreArc[0], rayon*math.sin (cur_angle_local + deltaAlpha) + centreArc[1]]
                p3 = centreArc
                dicoPartie["tooth_id"] = 0
                dicoPartie["pnt_cut_edge"] = [[p1[1], 0., p1[0]], [p2[1], 0., p2[0]]]
                dicoPartie["pnt_in_cut_face"] = [p3[1], 0., p3[0]]
                dicoPartie["h_cut_max"] = 1.2*e
                dicoPartie["node"] = []
                dicoPartie["tri"] = []
                #   maillage :
                mesh_point = cur_point_local
                mesh_angle = cur_angle_local
                # Dans un premier temps, les triangles ont ttous pour sommet le centre de l'arc 
                # Les points :
                # dicoPartie["node"].append([mesh_point[1],0,mesh_point[0]])
                nbCouchesReel = nbCouches
                for j in range (nbCouches+1):
                    distanceCentre = rayon - j*epCouche
                    if distanceCentre > 0:
                        for i in range(nbSlices+1):
                            mesh_point = [distanceCentre*math.cos (mesh_angle + i*sliceAngle) + centreArc[0], \
                                          distanceCentre*math.sin (mesh_angle + i*sliceAngle) + centreArc[1]]
                            dicoPartie["node"].append([mesh_point[1],0,mesh_point[0]])
                    else:
                        dicoPartie["node"].append([centreArc[1],0,centreArc[0]])
                        nbCouchesReel = j-1
                        break
                # Les triangles :
                for j in  range (nbCouchesReel):
                    for i in range (nbSlices):
                        idxSommet1 = j*(nbSlices+1)+i
                        idxSommet2 = idxSommet1 + 1
                        idxSommet3 = idxSommet1 + nbSlices+1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                        idxSommet1 = idxSommet3
                        idxSommet2 = idxSommet2
                        idxSommet3 = idxSommet1 + 1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                if nbCouchesReel < nbCouches:
                    for i in range (nbSlices):
                        idxSommet1 = nbCouchesReel*(nbSlices+1)+i
                        idxSommet2 = idxSommet1+1
                        idxSommet3 = (nbCouchesReel+1)*(nbSlices+1)
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                    
                self.elementary_tools_list.append (dicoPartie)
                cur_point_local[0],cur_point_local[1] = p2[0], p2[1]
                cur_angle_local = cur_angle_local + deltaAlpha
            next_angle[0] = current_angle + alpha
            next_point[0],next_point[1] = p2[0], p2[1]
        else:
            next_point[0],next_point[1] = current_point[0], current_point[1]
            next_angle[0] = current_angle + alpha
        
# --------------------------------------------------------------------------------------------------               
    def __generePartiesEtMaillageSegment__(self, idxSeg, current_point, current_angle, next_point):
        

        longSeg = self.dic["seg_length_list"][idxSeg]
        if longSeg > 0:
            nbPartiesSeg = self.dic["seg_nb_elementary_tools_list"][idxSeg]
            nbCouchesFaceDeCoupe = self.dic["cut_face_nb_layers"]
            e = self.dic["cut_face_thickness"]
            deltaLongSeg = longSeg/nbPartiesSeg
            deltaEpaisseur = e/nbCouchesFaceDeCoupe
            # nbSlices commun à chaque el. tool. du segment.
            nbSlices = self.dic['seg_nb_slices_list'][idxSeg]
            deltaLongET = deltaLongSeg / nbSlices
            cur_point_local = [current_point[0], current_point[1]]
            for k in range(nbPartiesSeg):
                dicoPartie = {}

                # Arête :
                p1 = cur_point_local
                p2 = [p1[0] - deltaLongSeg*math.cos(current_angle - math.pi/2), \
                      p1[1] - deltaLongSeg*math.sin(current_angle - math.pi/2)]
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
                    for i in range(nbSlices):
                        next_mesh_point = [mesh_point_dep[0] - (i+1)*deltaLongET*math.cos(current_angle - math.pi/2), \
                                           mesh_point_dep[1] - (i+1)*deltaLongET*math.sin(current_angle - math.pi/2)]
                        dicoPartie["node"].append([next_mesh_point[1], 0., next_mesh_point[0]])
                # Les triangles =
                for j in range (nbCouchesFaceDeCoupe):
                    for i in range (nbSlices):
                        idxSommet1 = j*(nbSlices+1)+i
                        idxSommet2 = idxSommet1 + 1
                        idxSommet3 = idxSommet1 + nbSlices+1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                        idxSommet1 = idxSommet3
                        idxSommet2 = idxSommet2
                        idxSommet3 = idxSommet1 + 1
                        dicoPartie["tri"].append([idxSommet1,idxSommet2,idxSommet3])
                self.elementary_tools_list.append (dicoPartie)
                cur_point_local = p2
            next_point[0],next_point[1] = p2[0], p2[1]
        else:
            next_point[0],next_point[1] = current_point[0], current_point[1]
# --------------------------------------------------------------------------------------------------

    def __calculPremierPointEtAngle__(self, pointEtAngle):
        if self.dic.has_key("bissectrice_arc_idx"):
            idxArc = self.dic["bissectrice_arc_idx"]
            idxSeg = idxArc
            
            alpha = math.radians (self.dic["arc_angle_degrees_list"][idxArc])
            
            rayon = self.dic["radius_list"][idxArc]
            centreArc = [0., self.dic["dist_from_origin"]] # dans (Op,zp,xp)
            
            current_angle = (math.pi+alpha)/2
            current_point = [rayon*math.cos (current_angle) + centreArc[0], rayon*math.sin (current_angle) + centreArc[1]]
        else : ##  self.dic doit avoir la clef "mediatriceSeg"
            idxSeg = self.dic["mediatrice_seg_idx"]
            current_point = [self.dic["seg_length_list"][idxSeg]/2.,self.dic["dist_from_origin"]]
            current_angle = math.pi/2.
            
            idxSeg -= 1
            idxArc = idxSeg
            
            if len(self.dic["radius_list"]) > 0:
                rayon = self.dic["radius_list"][idxArc]
                centreArc = [current_point[0], current_point[1] - rayon]
                alpha = math.radians (self.dic["arc_angle_degrees_list"][idxArc])
        ## Code commun pour trouver le premier point :
        while idxArc >= 0:
            # arc :
            current_angle -= alpha
            current_point = [rayon*math.cos (current_angle) + centreArc[0], rayon*math.sin (current_angle) + centreArc[1]]
            # segment :
            longSeg = self.dic["seg_length_list"][idxSeg]
            current_point[0] += longSeg * math.cos(current_angle+math.pi/2.)
            current_point[1] += longSeg * math.sin(current_angle+math.pi/2.)
            
            idxArc -=1
            idxSeg -=1
            if idxArc > 0:
                alpha = math.radians (self.dic["arc_angle_degrees_list"][idxArc])
                rayon = self.dic["radius_list"][idxArc]
                centreArc[0] = current_point[0] - rayon*math.cos(current_angle)
                centreArc[1] = current_point[1] - rayon*math.sin(current_angle)
        pointEtAngle [0] = current_point[0]
        pointEtAngle [1] = current_point[1]
        pointEtAngle [2] = current_angle
# --------------------------------------------------------------------------------------------------        
    def __generePartiesEtMaillagePlaquette__(self):
        # On effectue  tous les calculs dans le repère (Op,zp,xp).
        # On ajoute yp lors de la creation des dictionnaires à passer en entrée de donnnées.
        self.elementary_tools_list = []
        e = self.dic["cut_face_thickness"]
        nbCouchesFaceDeCoupe = self.dic["cut_face_nb_layers"]
        pointEtAngle = [0.,0.,0.] # contiendra [z,x, alpha]
        current_point = [0.,0.]
        self.__calculPremierPointEtAngle__(pointEtAngle)
        current_point[0], current_point[1], current_angle = pointEtAngle[0],pointEtAngle[1],pointEtAngle[2]  
        
        idxSeg = 0
        idxArc = 0
        
        next_point = [0.,0.]
        next_angle = [0.]
        while idxArc < len (self.dic["radius_list"]):
            ### Section segment
            self.__generePartiesEtMaillageSegment__(idxSeg, current_point, current_angle, next_point)
            current_point = next_point
            
            ### Section arc :
            self.__generePartiesEtMaillageArc__(idxArc, current_point, current_angle, next_point, next_angle)
            ### Section Segment : 
            current_point = next_point
            current_angle = next_angle[0]
            idxArc += 1
            idxSeg += 1
        ### derniere section segment :    
        self.__generePartiesEtMaillageSegment__(idxSeg, current_point, current_angle, next_point)
        
        print '<CGen> self.elementary_tools_list :'
        for ddd in self.elementary_tools_list:
            print ddd

class ToothForHelicoidalMillType2(Insert):
    def __init__(self, dic):
        """
         example for dic : 
         {
         'name': 'dent de fraise hélicoïdale de type 2',
         'tooth_id': 0,
         'storey_id': 0,
         
         'cut_face_thickness': 2.3E-2,
         'cut_face_nb_layers': 1,
         
         'dist_from_origin'      : 6.0D-3, # futur radiurs of the mill...
         'rayonBec' : 3.D-3,
         'longProlongAvant'    : 5.D-03,
         'longProlongApres'    : 0.0,
         'anglePointeOutil'    : 110.0, 'angleHelice' : -10.0,

          
         'nbPartiesFlancAvant' : 5, 'nbPartiesFlancApres' : 0, 'nbPartiesDisque' : 5,
         'seg_nb_slice_before':1, 'seg_nb_slice_after': 1, 'nb_slices_disk': 2,
         
         'nbCouchesLiaison'    : 1, 'nbSweep' : 1
         }
        """
        Tooth.__init__(self,dic)
        #1 : preparer les donnees pour pouvoir appliquer la methode classe insert
        # Construction des listes
        self.dic['seg_length_list'] = [dic['longProlongApres'],dic['longProlongAvant']]
        self.dic['seg_nb_elementary_tools_list'] = [dic['nbPartiesFlancApres'],dic['nbPartiesFlancAvant']]
        self.dic['seg_nb_slices_list'] = [dic['seg_nb_slice_after'],dic['seg_nb_slice_before']]
        
        self.dic['arc_angle_degrees_list'] = [180-dic['anglePointeOutil']]
        self.dic['arc_nb_elementary_tools_list'] = [dic['nbPartiesDisque']]
        self.dic['radius_list'] = [dic['rayonBec']]
        self.dic['arc_nb_slices_list'] = [dic['nb_slices_disk']]
        
        self.dic["mediatrice_seg_idx"]=1
        self.dic["dist_from_origin"] = dic["dist_from_origin"]

        
        self.nb_elementary_tools = dic['nbPartiesFlancAvant'] + dic['nbPartiesFlancApres'] + dic['nbPartiesDisque']
        ### rem. : self.nb_elementary_tools sera à priori calculé dans self.__generePartiesEtMaillagePlaquette__()
        #2 : On génère le maillage :
        self.__generePartiesEtMaillagePlaquette__()
        #3 : On retourne la face de coupe et on remonte la dent sur l'axe x :
        z_diff = self.dic['seg_length_list'][1]/2. +self.dic['radius_list'][0]
        for i in range (self.nb_elementary_tools):
        	for node in self.elementary_tools_list[i]['node']:
        	    node [2] = -node[2] + z_diff
        	self.elementary_tools_list[i]['pnt_cut_edge'][0][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][0][2] + z_diff
        	self.elementary_tools_list[i]['pnt_cut_edge'][1][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][1][2] + z_diff
        	self.elementary_tools_list[i]['pnt_in_cut_face'][2] = - self.elementary_tools_list[i]['pnt_in_cut_face'][2] + z_diff
        	
        
        #4 : Application de la methode l'hélicoidalisation 
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
        
if __name__ == "__main__":
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
    dico1_nouveau_1 = {   'name' : 'ma plaquette',
                          'tooth_id' : 0, 'storey_id': 0,
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 4},
                                   {'radius'     : 4.0e-3, 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 4},
                                   {'seg_length' : 5.0e-3,                      'nb_elementary_tools': 5},
                                   {'radius'     : 6.0e-3, 'angle_degrees': 30, 'nb_elementary_tools': 3, 'nb_slices': 3},
                                   {'seg_length' : 8.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx': 1, 'dist_from_origin':4.0e-3 },
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 3
         }
    dico1_nouveau_3 = {   'name' : 'ma plaquette',
                          'tooth_id' : 0, 'storey_id': 0,
             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 4},
                                   {'radius'     : 0., 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 1},
                                   {'seg_length' : 5.0e-3,                      'nb_elementary_tools': 5},
                                   {'radius'     : 0., 'angle_degrees': 30, 'nb_elementary_tools': 3},
                                   {'seg_length' : 8.0e-3,                      'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx': 1, 'dist_from_origin':4.0e-3 },
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2
         }
    dico1_nouveau_2 = {   'name' : 'ma plaquette',
                          'tooth_id' : 0, 'storey_id': 0,
             'cutting_edge_geom': [{'seg_length' : 0.,                      'nb_elementary_tools': 4, 'nb_slices': 4},
                                   {'radius'     : 2.8e-3, 'angle_degrees': 45, 'nb_elementary_tools': 4, 'nb_slices': 3},
                                   {'seg_length' : 0.,                      'nb_elementary_tools': 5}
                                                                     ],
             'insert_location': {'bissectrice_arc_idx': 0, 'dist_from_origin':4.0e-3 },
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 6
         }
         
    tooth_helico_type2_dic = {
         'name': 'dent de fraise hélicoïdale de type 2',
         'tooth_id': 0,
         'storey_id': 0,
         
         'cut_face_thickness': 2.3E-2,
         'cut_face_nb_layers': 3,
         
         'dist_from_origin'      : 6.0E-3, # futur radiurs of the mill...
         'rayonBec' : 3.E-3,
         'longProlongAvant'    : 5.E-03,
         'longProlongApres'    : 0.0,
         'anglePointeOutil'    : 110.0, 'angleHelice' : -10.0,

          
         'nbPartiesFlancAvant' : 5, 'nbPartiesFlancApres' : 0, 'nbPartiesDisque' : 5,
         'seg_nb_slice_before':1, 'seg_nb_slice_after': 1, 'nb_slices_disk': 2,
         
         'nbCouchesLiaison'    : 1, 'nbSweep' : 1
         }
    #plaquette = Insert(dicPlaquette1Segment)
    #plaquette = Insert(dicPlaquette1Arc)
    #plaquette = Insert(dicPlaquette3seg)
    #plaquette = Insert(dicPlaquetteEquerre)
    # plaquette = Insert(dico1_nouveau_1)
    
    dent_helico_type2 = ToothForHelicoidalMillType2(tooth_helico_type2_dic)
    #print plaquette.dic
    dent_helico_type2.showyou()