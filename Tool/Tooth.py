# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 25 novembre 2014
# 
#
# 
# Les angles sont donnés en degres.
# Il sont convertis en Radian dès le constructeur
#
import math
import bloc_util
        
# ==================================================================================================
class ToothInFrame:
# ==================================================================================================
    def __init__(self, **dic):
        self.tooth = dic['tooth']
        self.frame = dic['frame']
        self.tooth_id = dic['tooth_id']

# ==================================================================================================
class ToothModel:
# ==================================================================================================
    """
    Classe abstraite mère de toutes les dents. Attentions aux dents de la mer !
    """
# --------------------------------------------------------------------------------------------------
    def __init__(self,  **dic):
        """
        Arguments attendus :
        name : optional argument. Name of the ToolModel 
        cut_face_thickness : Thickness of the cutting face of the Tooth
        cut_face_nb_layers : For the fineness of the meshing of the cutting face
        """
        self.dic = {}
        self.dic["name"]= dic["name"]
        
        #self.tooth_id = dic['tooth_id']
        #self.toolstep_id = dic['toolstep_id']
        
        self.cut_face_thickness = dic['cut_face_thickness']
        self.cut_face_nb_layers = dic['cut_face_nb_layers']
        
        
        self.nb_elementary_tools = 0 # Computed or given in subclasses
        self.elementary_tools_list = []    
# --------------------------------------------------------------------------------------------------    
    def torsion_transformation(self):
        """
        Attention : To call this method, attributes 
        self.radius, self.height, and self.helix_angle or self.torsion_angle must be defined. 
        """
        if hasattr(self, 'helix_angle'):
            self.torsion_angle = self.height*math.tan(self.helix_angle)/self.radius
        ## Transformation des points de self.elementary_tools_list.
        for et in self.elementary_tools_list:
            # transformation de l'arrete, des nodes de face de coute et de volume en dépouille, des point sur la cutface et sur la clearance face :
            for node in et['pnt_cut_edge'] + et['node_cut_face']+et['node_clearance_bnd'] + [et['pnt_in_cut_face'], et['pnt_in_clearance_bnd']]:
                beta = node[2]*self.torsion_angle/self.height
                radius = node[0]
                node[0] = radius*math.cos(beta)
                node[1] = radius*math.sin(beta)
            
    def give_mesh_rect_patch(self, tri, dim1, dim2, offset=0):
        """
        Maillage d'une zone rectangulaire de dim1*dim2 points rangés dans un tableau unidimensionel.   
        Ajoute le maillage (indices dans le tableau de nodes des sommets des triangles) au tableau tri
        
            *--*--*-- ...--*\
            *--*--*-- ...--* \
            ...               dim2 
            *--*--*-- ...--* /
            *--*--*-- ...--*/
            \_____dim1_____/
        """
        for j in range (dim2):    
                for i in range(dim1):
                    tri.append([offset + j*(dim1+1)+i+1, offset + j*(dim1+1)+i,     offset + (j+1)*(dim1+1)+i ])
                    tri.append([offset + j*(dim1+1)+i+1, offset + (j+1)*(dim1+1)+i, offset + (j+1)*(dim1+1)+i +1 ])
            
        
# --------------------------------------------------------------------------------------------------
    def draw(self):
        bloc_util.view_bloc(self.elementary_tools_list)
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class ToothInsert(ToothModel) :
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
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
             
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 2,
             'clearance_face_thickness' : 2.E-3,
             'clearance_face_nb_layers' : 2,

             'cutting_edge_geom': [{'seg_length' : 6.0e-3,                'nb_elementary_tools': 4, 'nb_slices': 1}, # même nbSlices pour chaque el. tool
                                   {'angle_degrees': 45, 'radius':1.0e-3, 'nb_elementary_tools': 4, 'nb_slices': 3},
                                   {'seg_length' : 5.0e-3,                'nb_elementary_tools': 5, 'nb_slices': 4},
                                   {'angle_degrees': 30, 'radius':2.0e-3, 'nb_elementary_tools': 4                }, # valeur par defaut : nb_slices = 1
                                   ...
                                   {'seg_length' : 8.0e-3,                'nb_elementary_tools': 4, 'nb_slices': 1},
                                  ],
             'insert_location': {'bissectrice_arc_idx'|'mediatrice_seg_idx': 2, 'dist_from_origin':4.0e-3 }
         }
         On pourra en théorie mettre autant de segment que l'on veut. 
         S'il y a n segments il y aura n-1 arcs.
        """
        ToothModel.__init__(self, **dic) 
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
        e  = self.cut_face_thickness
        centreArc = [current_point[0] - rayon * math.cos(current_angle), \
                     current_point[1] - rayon * math.sin(current_angle)] # dans (Op,zp,xp)
        
        nbCouches = self.cut_face_nb_layers
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
                dicoPartie["node_cut_face"] = []
                dicoPartie["tri_cut_face"] = []
                #   maillage :
                mesh_point = cur_point_local
                mesh_angle = cur_angle_local
                # Dans un premier temps, les triangles ont ttous pour sommet le centre de l'arc 
                # Les points :
                # dicoPartie["node_cut_face"].append([mesh_point[1],0,mesh_point[0]])
                nbCouchesReel = nbCouches
                for j in range (nbCouches+1):
                    distanceCentre = rayon - j*epCouche
                    if distanceCentre > 0:
                        for i in range(nbSlices+1):
                            mesh_point = [distanceCentre*math.cos (mesh_angle + i*sliceAngle) + centreArc[0], \
                                          distanceCentre*math.sin (mesh_angle + i*sliceAngle) + centreArc[1]]
                            dicoPartie["node_cut_face"].append([mesh_point[1],0,mesh_point[0]])
                    else:
                        dicoPartie["node_cut_face"].append([centreArc[1],0,centreArc[0]])
                        nbCouchesReel = j-1
                        break
                # Les triangles :
                for j in  range (nbCouchesReel):
                    for i in range (nbSlices):
                        idxSommet1 = j*(nbSlices+1)+i
                        idxSommet2 = idxSommet1 + 1
                        idxSommet3 = idxSommet1 + nbSlices+1
                        dicoPartie["tri_cut_face"].append([idxSommet1,idxSommet2,idxSommet3])
                        idxSommet1 = idxSommet3
                        idxSommet2 = idxSommet2
                        idxSommet3 = idxSommet1 + 1
                        dicoPartie["tri_cut_face"].append([idxSommet1,idxSommet2,idxSommet3])
                if nbCouchesReel < nbCouches:
                    for i in range (nbSlices):
                        idxSommet1 = nbCouchesReel*(nbSlices+1)+i
                        idxSommet2 = idxSommet1+1
                        idxSommet3 = (nbCouchesReel+1)*(nbSlices+1)
                        dicoPartie["tri_cut_face"].append([idxSommet1,idxSommet2,idxSommet3])
                    
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
            nbCouchesFaceDeCoupe = self.cut_face_nb_layers
            e = self.cut_face_thickness
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
                dicoPartie["node_cut_face"] = []
                dicoPartie["tri_cut_face"] = []
                # Maillage :
            
                # Les points :

                for j in range (nbCouchesFaceDeCoupe+1):
                    # on décale de j couches :
                    mesh_point_dep = [p1[0]-j*deltaEpaisseur*math.cos(current_angle), \
                                      p1[1]-j*deltaEpaisseur*math.sin(current_angle) ]
                    dicoPartie["node_cut_face"].append([mesh_point_dep[1], 0., mesh_point_dep[0]])
                    for i in range(nbSlices):
                        next_mesh_point = [mesh_point_dep[0] - (i+1)*deltaLongET*math.cos(current_angle - math.pi/2), \
                                           mesh_point_dep[1] - (i+1)*deltaLongET*math.sin(current_angle - math.pi/2)]
                        dicoPartie["node_cut_face"].append([next_mesh_point[1], 0., next_mesh_point[0]])
                # Les triangles =
                for j in range (nbCouchesFaceDeCoupe):
                    for i in range (nbSlices):
                        idxSommet1 = j*(nbSlices+1)+i
                        idxSommet2 = idxSommet1 + 1
                        idxSommet3 = idxSommet1 + nbSlices+1
                        dicoPartie["tri_cut_face"].append([idxSommet1,idxSommet2,idxSommet3])
                        idxSommet1 = idxSommet3
                        idxSommet2 = idxSommet2
                        idxSommet3 = idxSommet1 + 1
                        dicoPartie["tri_cut_face"].append([idxSommet1,idxSommet2,idxSommet3])
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
        e = self.cut_face_thickness
        nbCouchesFaceDeCoupe = self.cut_face_nb_layers
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

class ToothForHelicoidalMillType2(ToothInsert):
    def __init__(self, dic):
        """
         example for dic : 
         {
         'name': 'dent de fraise hélicoïdale de type 2',
         
         'cut_face_thickness': 2.3E-2,
         'cut_face_nb_layers': 1,
         
         'dist_from_origin'      : 6.0D-3, # futur radiurs of the mill...
         'rayonBec' : 3.D-3,
         'longProlongAvant'    : 5.D-03,
         'longProlongApres'    : 0.0,
         'anglePointeOutil'    : 110.0, 'angleHelice' : -10.0,

          
         'nbPartiesFlancAvant' : 5, 'nbPartiesFlancApres' : 0, 'nbPartiesDisque' : 5,
         'seg_nb_slice_before':1, 'seg_nb_slice_after': 1, 'arc_nb_slices': 2,
         
         'nbCouchesLiaison'    : 1, 'nbSweep' : 1
         }
        """
        ToothModel.__init__(self,dic)
        #1 : preparer les donnees pour pouvoir appliquer la methode classe insert
        # Construction des listes
        self.dic['seg_length_list'] = [dic['longProlongApres'],dic['longProlongAvant']]
        self.dic['seg_nb_elementary_tools_list'] = [dic['nbPartiesFlancApres'],dic['nbPartiesFlancAvant']]
        self.dic['seg_nb_slices_list'] = [dic['seg_nb_slice_after'],dic['seg_nb_slice_before']]
        
        self.dic['arc_angle_degrees_list'] = [180-dic['anglePointeOutil']]
        self.dic['arc_nb_elementary_tools_list'] = [dic['nbPartiesDisque']]
        self.dic['radius_list'] = [dic['rayonBec']]
        self.dic['arc_nb_slices_list'] = [dic['arc_nb_slices']]
        
        self.dic["mediatrice_seg_idx"]=1
        self.dic["dist_from_origin"] = dic["dist_from_origin"]

        
        self.nb_elementary_tools = dic['nbPartiesFlancAvant'] + dic['nbPartiesFlancApres'] + dic['nbPartiesDisque']
        ### rem. : self.nb_elementary_tools sera à priori calculé dans self.__generePartiesEtMaillagePlaquette__()
        #2 : On génère le maillage :
        self.__generePartiesEtMaillagePlaquette__()
        #3 : On retourne la face de coupe et on remonte la dent sur l'axe x :
        z_diff = self.dic['seg_length_list'][1]/2. +self.dic['radius_list'][0]
        for i in range (self.nb_elementary_tools):
            for node in self.elementary_tools_list[i]['node_cut_face']:
                node [2] = -node[2] + z_diff
            self.elementary_tools_list[i]['pnt_cut_edge'][0][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][0][2] + z_diff
            self.elementary_tools_list[i]['pnt_cut_edge'][1][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][1][2] + z_diff
            self.elementary_tools_list[i]['pnt_in_cut_face'][2] = - self.elementary_tools_list[i]['pnt_in_cut_face'][2] + z_diff
            
        
        #4 : Application de la methode l'hélicoidalisation 
        # self.radius, self.height, et self.helix_angle ou self.torsion_angle doivent exister.
        self.radius = self.dic['dist_from_origin']
        self.helix_angle = dic['angleHelice']
        self.height = dic['rayonBec']+dic['longProlongAvant']
        self.torsion_transformation()
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class ToothSliced(ToothModel):
# ==================================================================================================
    def __init__(self, **dic):
        """
        structure de dic attendue :
        --> Clés héritées de ToothModel:
        'name' : 'name for th tooth' # Optional
        'cut_face_thickness' : 1.2E-3
        'cut_face_nb_layers' : 1
        'clearance_face1_nb_layers' : 1  # clearance face 1 defined by alpha1 and L1
        'clearance_face2_nb_layers' : 1  # clearance face 2 defined by alpha2 and L2
        'nb_slices_per_elt': 1
        --> Clés propres à ToothForMonoblocMillType3
        'nb_elementary_tools' : 50
        'cutting_edge_geom' : [{'z': 2.0E-2, 'x': 3.0E-2 , 'y': 1.0E-2 , 'gamma':60 ,'L_gamma': 1.3E-2,'alpha1': 10 ,'L1':1.E-2 ,'alpha2': 30,'L2':0.7E-2 },
                               {'z': 4.0E-2, 'x': 3.4E-2 , 'y': 1.4E-2 , 'gamma':60 ,'L_gamma': 1.3E-2,'alpha1': 10 ,'L1':1.E-2 ,'alpha2': 30,'L2':0.7E-2 },
                               ...
                              ]
        """
        ToothModel.__init__(self, **dic)
        self.cutting_edge_geom = dic['cutting_edge_geom']
        self.nb_elementary_tools = dic['nb_elementary_tools']
        self.nb_slices_per_elt = dic['nb_slices_per_elt']
        self.clearance_face1_nb_layers = dic['clearance_face1_nb_layers']
        self.clearance_face2_nb_layers = dic['clearance_face2_nb_layers']
        ## Calcule des arrête et du maillage :
        # Initialisation - premier plan :
        current_point = [self.cutting_edge_geom[0][coord] for coord in ['x','y','z']]
        first_z = current_point [2]
        last_z  = self.cutting_edge_geom[-1]['z']
        delta_z_et = (last_z - first_z)/self.nb_elementary_tools
        delta_z_slice_et = delta_z_et/self.nb_slices_per_elt
        epsilon = 1.E-7 * (last_z - first_z)/len(self.cutting_edge_geom)
        
        # 1 : interpolation des data en fonction des elem_tools et des slices pour le maillage
        # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
        cutting_edge_geom_interpolated = []
        cutting_edge_geom_interpolated.append(self.cutting_edge_geom[0])
        idx_tool_geom = 0 
        for k in range (self.nb_elementary_tools):
            curr_z_et = first_z + (k)*delta_z_et
            for j in range (self.nb_slices_per_elt):
                next_z_slices = curr_z_et + (j+1)*delta_z_slice_et
                while self.cutting_edge_geom[idx_tool_geom]['z'] + epsilon < next_z_slices:
                    idx_tool_geom+=1
                # A ce stade, self.cutting_edge_geom[idx_tool_geom-1]['z'] < next_z_slices <= epsilon + self.cutting_edge_geom[idx_tool_geom]['z'] 
                xi = (next_z_slices - self.cutting_edge_geom[idx_tool_geom-1]['z'])/ \
                    (self.cutting_edge_geom[idx_tool_geom]['z'] - self.cutting_edge_geom[idx_tool_geom -1]['z'])
                # calcul des coef. 
                dic_slice_geom = {key : (1- xi)*self.cutting_edge_geom[idx_tool_geom-1][key] + xi*self.cutting_edge_geom[idx_tool_geom][key] \
                                   for key in self.cutting_edge_geom[idx_tool_geom].keys()}
                cutting_edge_geom_interpolated.append(dic_slice_geom)
        # petit print pour controle ... à supprimer par la suite :
        for i in range(len(cutting_edge_geom_interpolated)): print i, ' : ', cutting_edge_geom_interpolated[i]
        
        # 2 : Calcul des points
        # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
        elem_tools_slices_points_list = [] # tableau de self.nb_elementary_tools tableaux de slices
        idx_in_interp_list = 0
        for k in range (self.nb_elementary_tools):
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            slices_points_list = []
            idx_in_interp_list-=1
            for j in range (self.nb_slices_per_elt+1):
                idx_in_interp_list+=1
                slice_geom_dic = cutting_edge_geom_interpolated[idx_in_interp_list]
                slices_points = [] # les points d'un slice dans un meme plan.
            
                ## calcul de l'angle util à partir de gamma :
                gamma = math.radians(slice_geom_dic['gamma'])
                radius = math.sqrt(slice_geom_dic['x']**2 + slice_geom_dic['y']**2)
                rho =  math.acos(slice_geom_dic['x']/radius)
                gamma_util = math.pi -(rho - gamma)
                increment_l_gamma = slice_geom_dic['L_gamma'] /self.cut_face_nb_layers
                
                alpha1_util = gamma_util - math.pi/2  + math.radians(slice_geom_dic['alpha1'])
                increment_l_alpha1 = slice_geom_dic['L1']/self.clearance_face1_nb_layers
                
                alpha2_util = gamma_util - math.pi/2  + math.radians(slice_geom_dic['alpha2'])
                increment_l_alpha2 = slice_geom_dic['L2']/self.clearance_face2_nb_layers
                
                
                # première face en depouille
                cut_edge_point = [slice_geom_dic[coord] for coord in ['x','y','z']]
                for i in range(self.clearance_face1_nb_layers+1):
                    first_point_curr = [cut_edge_point[0]+i*increment_l_alpha1*math.cos(alpha1_util), \
                                       cut_edge_point[1]+i*increment_l_alpha1*math.sin(alpha1_util), \
                                       cut_edge_point[2]]
                    slices_points.append(first_point_curr)
                    for h in range(self.cut_face_nb_layers):
                        slices_points.append([first_point_curr[0]+(h+1)*increment_l_gamma*math.cos(gamma_util), \
                                       first_point_curr[1]+(h+1)*increment_l_gamma*math.sin(gamma_util), \
                                       slice_geom_dic['z']])
                # deuxième face en depouille
                first_point = [cut_edge_point[0]+slice_geom_dic['L1']*math.cos(alpha1_util), \
                               cut_edge_point[1]+slice_geom_dic['L1']*math.sin(alpha1_util), \
                               cut_edge_point[2]]
                for i in range(self.clearance_face2_nb_layers):
                    first_point_curr = [first_point[0]+(i+1)*increment_l_alpha2*math.cos(alpha2_util), \
                                        first_point[1]+(i+1)*increment_l_alpha2*math.sin(alpha2_util), \
                                        cut_edge_point[2]]
                    slices_points.append(first_point_curr)
                    for h in range(self.cut_face_nb_layers):
                        slices_points.append([first_point_curr[0]+(h+1)*increment_l_gamma*math.cos(gamma_util), \
                                       first_point_curr[1]+(h+1)*increment_l_gamma*math.sin(gamma_util), \
                                       slice_geom_dic['z']])
                  
                ###
                
                slices_points_list.append(slices_points)
            elem_tools_slices_points_list.append(slices_points_list)
            ###
        # for i in range(self.nb_elementary_tools): print i, ' : ', elem_tools_slices_points_list[i]
        
        # 3 : arrêtes, nodes et maillages :
        # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨ 
        # self.elementary_tools_list
        # Face de coupe :
        for k in range (self.nb_elementary_tools):
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            elem_tool = {}
            ## revoir suite
            elem_tool ['pnt_cut_edge'] = [elem_tools_slices_points_list[k][0][0], elem_tools_slices_points_list[k][self.nb_slices_per_elt][0]]
            elem_tool ['pnt_in_cut_face'] = [(elem_tools_slices_points_list[k][0][self.cut_face_nb_layers][idx]+elem_tools_slices_points_list[k][self.nb_slices_per_elt][self.cut_face_nb_layers][idx])/2. for idx in [0,1,2]]
            elem_tool ['node_cut_face'] = []
            elem_tool['tri_cut_face'] = []
            
            
            
            for j in range (self.nb_slices_per_elt+1):
                elem_tool['node_cut_face']+=elem_tools_slices_points_list[k][j][0:self.cut_face_nb_layers+1]
            self.give_mesh_rect_patch( tri = elem_tool['tri_cut_face'], dim1 = self.cut_face_nb_layers, dim2 = self.nb_slices_per_elt)
            #for j in range (self.nb_slices_per_elt):    
            #    for i in range(self.cut_face_nb_layers):
            #        elem_tool['tri_cut_face'].append([j*(self.cut_face_nb_layers+1)+i+1, j*(self.cut_face_nb_layers+1)+i,     (j+1)*(self.cut_face_nb_layers+1)+i ])
            #        elem_tool['tri_cut_face'].append([j*(self.cut_face_nb_layers+1)+i+1, (j+1)*(self.cut_face_nb_layers+1)+i, (j+1)*(self.cut_face_nb_layers+1)+i +1 ])
            self.elementary_tools_list.append(elem_tool)
        print "Nombre d'outils elementaires  : ", len(self.elementary_tools_list)
        for tool_elementaire in self.elementary_tools_list : print tool_elementaire
        
        # Volume en dépouille :
        
        # Faces en dépouilles
        for k in range (self.nb_elementary_tools):
            
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            elem_tool = self.elementary_tools_list[k]
            elem_tool['node_clearance_bnd'] = []
            elem_tool['tri_clearance_bnd'] = []
            elem_tool['pnt_in_clearance_face'] = [((elem_tools_slices_points_list[k][0][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)][idx]) + \
                                                   (elem_tools_slices_points_list[k][self.nb_slices_per_elt][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)][idx]))/2. for idx in [0,1,2]]
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=[elem_tools_slices_points_list[k][j][i*(self.cut_face_nb_layers+1)] for i in range(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)]
            self.give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, dim2 = self.nb_slices_per_elt)
            
             
        print 'self.elementary_tools_list : ', self.elementary_tools_list
        # Faces opposées 
        for k in range (self.nb_elementary_tools):
            
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            elem_tool = self.elementary_tools_list[k]
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=[elem_tools_slices_points_list[k][j][(i+1)*(self.cut_face_nb_layers+1)-1] for i in range(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)]
            self.give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, dim2 = self.nb_slices_per_elt, \
                                   offset=(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        
        print 'self.elementary_tools_list After : ', self.elementary_tools_list
        
        # Face arriere :
        for k in range (self.nb_elementary_tools):
            elem_tool = self.elementary_tools_list[k]
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][j][-self.cut_face_nb_layers-1:]
            self.give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.cut_face_nb_layers, dim2 = self.nb_slices_per_elt, \
                                   offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        # Face dessous et face dessus :
        for k in range (self.nb_elementary_tools):
            elem_tool = self.elementary_tools_list[k]
            elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][0]
            elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][self.nb_slices_per_elt]
            self.give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.cut_face_nb_layers, dim2 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, \
                                   offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)+(self.cut_face_nb_layers+1)*(self.nb_slices_per_elt+1))
            self.give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], \
                                       dim1 = self.cut_face_nb_layers, \
                                       dim2 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, \
                                       offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1) + \
                                              (self.cut_face_nb_layers+1)*(self.nb_slices_per_elt+1) + \
                                              (self.cut_face_nb_layers+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        
# ==================================================================================================
class ToothForHelicoidalMillType1(ToothInsert):
    def __init__(self, **dic):
        """
        waited params : 
        {
        'radius' : 1.6E-3
         
        
        """
        # 1: transformation des données pour être géré commme une plaquette. 
# --------------------------------------------------------------------------------------------------
    def __generePartiesEtMaillageDent0__(self):
        alpha = self.angleAxialInitial
        beta  = self.deltaBetaDegres
        r     = self.diametreFraise / 2.
        L     = self.longueurSuivantAxe
        nb    = self.nbParties
        e     = self.epaisseurFaceCoupe
        
        theta = alpha
        z = 0.
        for i in range (nb):
            # Calcul des aretes de coupe :
            dicoPartie = {}
            next_theta = alpha + (i+1)*beta/nb
            next_z =  (i+1)*L/nb
            theta3 = theta + 0.5*beta/nb
            z3     = z + 0.5*L/nb
        
            p1 = [r* math.cos (theta), r* math.sin (theta), z ]
            p2 = [r* math.cos (next_theta), r* math.sin (next_theta), next_z ]
            p3 = [(r-e)* math.cos (theta3), (r-e)* math.sin (theta3), z3]
            
            dicoPartie["tooth_id"] = 0
            dicoPartie["pnt_cut_edge"] = [p1, p2]
            dicoPartie["pnt_in_cut_face"] = p3
            dicoPartie["h_cut_max"] = 1.2*e
            dicoPartie["node_cut_face"] = []
            dicoPartie["tri_cut_face"] = []
            # Calcul du maillage de la partie :
            # D'abord les points (les nodes)
            for jp in range (self.nbCouchesFaceCoupe+1):
                rm = r - jp*e/self.nbCouchesFaceCoupe
                for ip in range (self.nbTranches+1):
                    thetam = theta + ip*(next_theta - theta)/self.nbTranches
                    zm     = z + ip*(next_z -z)/self.nbTranches
                    
                    pm = [rm* math.cos (thetam), rm* math.sin (thetam), zm]
                    
                    dicoPartie["node_cut_face"].append(pm)
            # ensuite les triangles (liste de tripplets indicant les 
            # indices des nodes dans le tableau des nodes)
            for jp in range (self.nbCouchesFaceCoupe):
                for ip in range (self.nbTranches):
                    idsommet1 = ip + jp*(self.nbTranches+1)
                    idsommet2 = ip + jp*(self.nbTranches+1)+1
                    idsommet3 = ip + (jp+1)*(self.nbTranches+1)
                    dicoPartie["tri_cut_face"].append([idsommet1,idsommet2,idsommet3])
                    idsommet1 = idsommet3
                    idsommet3 = idsommet3+1   
                    dicoPartie["tri_cut_face"].append([idsommet1,idsommet2,idsommet3])
            
            dicoPartie["cutlaw_names"] = ["LC_mat1","LC2_mat2","LC3_mat3"]
            self.elementary_tools_list.append(dicoPartie)
            theta = next_theta
            z = next_z
# --------------------------------------------------------------------------------------------------

    pass
# ==================================================================================================
class ToothForHelicoidalMillTore(ToothModel):
    pass
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
    dicInsertModel1 = {   'name' : 'ma plaquette',
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
    dicInsertModel3 = {   'name' : 'ma plaquette',
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
    dicInsertModel2 = {   'name' : 'ma plaquette',
                          'tooth_id' : 0, 'storey_id': 0,
             'cutting_edge_geom': [{'seg_length' : 0.,                      'nb_elementary_tools': 4, 'nb_slices': 4},
                                   {'radius'     : 2.8e-3, 'angle_degrees': 45, 'nb_elementary_tools': 4, 'nb_slices': 3},
                                   {'seg_length' : 0.,                      'nb_elementary_tools': 5}
                                                                     ],
             'insert_location': {'bissectrice_arc_idx': 0, 'dist_from_origin':4.0e-3 },
             'cut_face_thickness' : 3.E-3,
             'cut_face_nb_layers' : 6
         }
         
    dicToothHelicoType2 = {
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
         'seg_nb_slice_before':1, 'seg_nb_slice_after': 1, 'arc_nb_slices': 2,
         
         'nbCouchesLiaison'    : 1, 'nbSweep' : 1
         }
    #plaquette = Insert(dicPlaquette1Segment)
    #plaquette = Insert(dicPlaquette1Arc)
    #plaquette = Insert(dicPlaquette3seg)
    #plaquette = Insert(dicPlaquetteEquerre)
    # plaquette = Insert(dicInsertModel1)
    
    dent_helico_type2 = ToothForHelicoidalMillType2(dicToothHelicoType2)
    #print plaquette.dic
    dent_helico_type2.draw()