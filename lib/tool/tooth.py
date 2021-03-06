# -*- coding: Utf-8 -*-

# This file is part of the python package 'tool', itself part of nessy2m.
# 
# Copyright (C) 2010-2016
# Christophe GENGEMBRE (christophe.gengembre@ensam.eu)
# Philippe LORONG (philippe.lorong@ensam.eu)
# Amran/Lounes ILLOUL (amran.illoul@ensam.eu)
# Arts et Metiers ParisTech, Paris, France
#
# nessy2m is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nessy2m is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with nessy2m.  If not, see <http://www.gnu.org/licenses/>.
#
# Please report bugs of this package to christophe.gengembre@ensam.eu 

# --------------------------------------------------------------------------------------------------
# Christophe Gengembre
# 25 novembre 2014
# 
#
# 
# Les angles sont donnés en degres.
# Il sont convertis en Radian dès le constructeur
#
import math

import sys
import os
# tool_util
my_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(my_dir,'..','..','..','n2m','lib'))
# case_path = os.path.abspath(os.curdir)

import tool_util

import copy
import numpy as np
from frame_of_reference import frame_of_reference as FoR

CUTFACE_BLOC = 0
CLEARANCE_BLOC = 1

# ==================================================================================================
# 2 functions that compute the mesh.
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
def give_mesh_rect_patch(tri, dim1, dim2, offset=0):
    """
    Mesh of a rectangular area composed of (dim1+1)*(dim2+1) nodes stored in a one-dimensional array.
    Add the mesh to the array 'tri' (indexes in the nodes array of the triangles vertices  )
    
        *--*--*-- ...--*\
        *--*--*-- ...--* \
        ...               dim2+1 
        *--*--*-- ...--* /
        *--*--*-- ...--*/
        \_____dim1+1___/
    """
    # print("give_mesh --> Rectangle dim1 : %d, dim2 : %d"%(dim1, dim2))
    for j in range (dim2):    
            for i in range(dim1):
                tri.append([offset + j*(dim1+1)+i+1, offset + j*(dim1+1)+i,     offset + (j+1)*(dim1+1)+i ])
                tri.append([offset + j*(dim1+1)+i+1, offset + (j+1)*(dim1+1)+i, offset + (j+1)*(dim1+1)+i +1 ])
# --------------------------------------------------------------------------------------------------        
def give_mesh_rect_peak_patch(tri, dim1, dim2, offset=0):
    """
    Mesh of an area composed of (dim1+1)*(dim2+1) + 1 nodes stored in a one-dimensional array.
    The (dim1+1)*(dim2+1) first nodes is a rectangle. The last node gives dim1 triangles whith the last
    line of dim1+1 nodes.
    Add the mesh to the array 'tri'
    
        *--*--*-- ...--*\
        *--*--*-- ...--* \
        ...               dim2+1 
        *--*--*-- ...--* /
        *--*--*-- ...--*/
               *
        \_____dim1+1___/
    """
    # print("give_mesh --> Rectangle + 1 point dim1 : %d, dim2 : %d"%(dim1, dim2) )
    for j in range (dim2):    
        for i in range(dim1):
            tri.append([offset + j*(dim1+1)+i+1, offset + j*(dim1+1)+i,     offset + (j+1)*(dim1+1)+i ])
            tri.append([offset + j*(dim1+1)+i+1, offset + (j+1)*(dim1+1)+i, offset + (j+1)*(dim1+1)+i +1 ])
    for i in range(dim1):
        tri.append([offset+(dim1+1)*(dim2+1),offset+(dim1+1)*(dim2+1)-1-i, offset+(dim1+1)*(dim2+1)-2-i])
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class ToothInFrame:
# ==================================================================================================
    def __init__(self, **dic):
        self.tooth = dic['tth']
        self.frame = dic['frame']
        self.tooth_id = dic['tooth_id']
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_model:
# ==================================================================================================
    """
    Abstract class -  Mother class of every tooth.
    """
# --------------------------------------------------------------------------------------------------
    def __init__(self,  **dic):
        """
        Arguments attendus :
        name : optional argument. Name of the ToolModel 
        cut_face_thickness : Thickness of the cutting face of the Tooth
        cut_face_nb_layers : For the fineness of the meshing of the cutting face
        'mcr_rf_cl_name'
        'mcr_cv_cl_name'
        """
        self.dic = {}
        self.dic["name"]= dic["name"]
        
        #self.tooth_id = dic['tooth_id']
        #self.toolstep_id = dic['toolstep_id']
        
        self.cut_face_thickness = dic['cut_face_thickness']
        self.cut_face_nb_layers = dic['cut_face_nb_layers']
        self.mcr_rf_cl_name    = None if not dic.has_key('mcr_rf_cl_name') else dic ['mcr_rf_cl_name'] 
        self.mcr_cv_cl_name    = None if not dic.has_key('mcr_cv_cl_name') else dic ['mcr_cv_cl_name']
        self.nb_elementary_tools = 0 # Computed or given in subclasses
        self.elementary_tools_list = []
        self._has_clear_face = False
# --------------------------------------------------------------------------------------------------
    def has_clear_face(self):
        return self._has_clear_face
# --------------------------------------------------------------------------------------------------
    def compute_out_blocs (self):
        self.elem_tool_out_list = []
        elemtool_id  = 0
        for elem_tool in self.elementary_tools_list:
            elem_tool_cut = {}
            elem_tool_clear = {}
            ## cutting face :

            elem_tool_cut['type']            = 'rake_face'
            elem_tool_cut['node']            = elem_tool['node_cut_face'] # copy.deepcopy(elem_tool['node_cut_face']) # noeud
            elem_tool_cut['tri']             = elem_tool['tri_cut_face']  # copy.deepcopy(elem_tool['tri_cut_face']) # tri
            elem_tool_cut['pnt']             = elem_tool['pnt_cut_edge'] + [elem_tool['pnt_in_cut_face'],]  # : 3 point , les deux point de l'arrete et le point de la face. 
            elem_tool_cut['h_cut_max']       = elem_tool['h_cut_max']
            elem_tool_cut['mcr_cl_name']      = self.mcr_rf_cl_name# : liste nom lois de coupe, 1 par bloc dexel
            elem_tool_cut['elemtool_id']    = elemtool_id
            #elem_tool_cut['tooth_id']        = elem_tool['tooth_id']
            #elem_tool_cut['set_id']          = elem_tool['set_id']
            #elem_tool_cut['step_id']         = elem_tool['toolstep_id']
            #elem_tool_cut['rep_in_spindle']  = elem_tool['']# optionel
            #elem_tool_cut['id_node_dyn']     = elem_tool['']# optionel
            #elem_tool_cut['nb_rep']          = elem_tool['']# optionel
            self.elem_tool_out_list.append(elem_tool_cut)
            
            ## clear face
            if self.has_clear_face():
                elem_tool_clear['type']           = 'clear_vol'
                elem_tool_clear['node']           = elem_tool['node_clearance_bnd'] #copy.deepcopy(elem_tool['node_clearance_bnd'])# noeud
                elem_tool_clear['tri']            = elem_tool['tri_clearance_bnd']  #copy.deepcopy(elem_tool['tri_clearance_bnd'])# tri
                elem_tool_clear['pnt']            = [elem_tool['pnt_clearance_face'][i] for i in  [2,1,0]] #: 3 point , p1 point dans la face de talonnage, p1p2 dir U, p1p3 dir v, avec U^V normal sortante
                elem_tool_clear['mcr_cl_name']      = self.mcr_cv_cl_name# : liste nom lois de talonnage, 1 par bloc dexel
                elem_tool_clear['elemtool_id']    = elemtool_id
                #elem_tool_clear['tooth_id']       = elem_tool['tooth_id']
                #elem_tool_clear['set_id']         = elem_tool['set_id']
                #elem_tool_clear['step_id']        = elem_tool['toolstep_id']
                #elem_tool_clear['rep_in_spindle'] = elem_tool[]# optionel
                #elem_tool_clear['id_node_dyn']    = elem_tool[]# optionel
                #elem_tool_clear['nb_rep']         = elem_tool[]# optionel
                #
                # CGen-DONE-oct2015  - var interne no_clearface self.elem_tool_out_list.append(elem_tool_clear)
                #
            
                self.elem_tool_out_list.append(elem_tool_clear)
            elemtool_id+=1
# --------------------------------------------------------------------------------------------------    
    def torsion_transformation(self):
        """apply a torsion transformation to the tooth self.
        
        Attention : To call this method, the fields
        self.radius, self.height, and  (self.helix_angle or self.torsion_angle) must be defined.
        Angles expressed in radians 
        """
        if hasattr(self, 'helix_angle'):
            self.torsion_angle = self.height*math.tan(self.helix_angle)/self.radius
        ## Transformation of the points of self.elementary_tools_list.
        for et in self.elementary_tools_list:
            # transformation de l'arrete, des nodes de face de coupe et de volume en dépouille, 
            # des point sur la cutface et sur la clearance face :
            liste_nodes = et['pnt_cut_edge'] + et['node_cut_face'] + [et['pnt_in_cut_face'],] 
            if et.has_key("node_clearance_bnd"): liste_nodes+= et['node_clearance_bnd'] + et['pnt_clearance_face']
            for node in liste_nodes:
                beta = node[2]*self.torsion_angle/self.height
                node[0], node[1] = node[0]*math.cos(beta) - node[1]*math.sin(beta), node[0]*math.sin(beta) + node[1]*math.cos(beta)
                # node[1] = node[0]*math.sin(beta) + node[1]*math.cos(beta)
            
    
    def __clearance_bnd_mesh_mng__(self):
        if not self.has_clear_face(): return 0
        for elem_tool in self.elementary_tools_list :
            initial_node_count = len (elem_tool['node_clearance_bnd'])
            tuplon_list = [[] for idx in range(initial_node_count)]
            for j in range(initial_node_count):
                for i in range(j+1, initial_node_count):
                    if elem_tool['node_clearance_bnd'][i]==elem_tool['node_clearance_bnd'][j]:
                        if len (tuplon_list[i]) == 0:
                            tuplon_list[i].append(-1)
                        if len (tuplon_list[j]) == 0 or len (tuplon_list[j]) > 0 and tuplon_list[j][0] != -1:
                            tuplon_list[j].append(i)
            # print('tuplon list : ', tuplon_list)
            for i in range(initial_node_count):
                if len(tuplon_list[i]) == 0 or tuplon_list[i][0] != -1 :
                    tuplon_list[i].append(i)
            # print('tuplon list 2: ', tuplon_list)
            i = 0
            while i < len (tuplon_list):
                while i < len (tuplon_list) and tuplon_list[i][0] == -1:
                    del tuplon_list[i]
                    del elem_tool['node_clearance_bnd'][i]
                i+=1
            old2new_list = [-1 for i in range(initial_node_count)]
            for j  in range (len(tuplon_list)):
                for i in tuplon_list[j]:
                    old2new_list[i]=j
                    
            for tri in elem_tool['tri_clearance_bnd']:
                for i in range(3):
                    tri[i]=old2new_list[tri[i]]
            # print('elem tool : %d nodes --> %d nodes'%(initial_node_count, len (elem_tool['node_clearance_bnd']) )
        
# --------------------------------------------------------------------------------------------------
    def draw(self):
        self.compute_out_blocs()
        out_d = './OUT/d_tooth'
        if not os.path.isdir(out_d): os.mkdir(out_d)
        
        # ********************
        # PhLo : 30/11/2016
        # Initial version:
        # # tool_util.draw_bloc(self.elem_tool_out_list, out_d) 
        # v3d_lf_name=tool_util.draw_bloc(self.elem_tool_out_list, out_d)
        # tool_util.v3d.show([v3d_lf_name],'rack face & clear vol')
        # New version:
        tool_util.draw_bloc(self.elem_tool_out_list, out_d)
        # ********************
    
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_insert(Tooth_model) :
# ==================================================================================================
    def __init__(self, **dic):
        """Tooth_insert constructor.
        {   
            # Mandatory data : 
            'name' : 'ma plaquette',
            'cutting_edge_geom': [
                {'seg_length' : 6.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 1},
                {'radius'     : 1.E-3, 'angle_degrees': 45, 'nb_elementary_tools': 3, 'nb_slices': 4}, # radius = 1.E-3
                {'seg_length' : 5.0e-3,                      'nb_elementary_tools': 5},
                {'radius'     : 2.0e-3, 'angle_degrees': 30, 'nb_elementary_tools': 3, 'nb_slices': 3},
                {'seg_length' : 8.0e-3,                      'nb_elementary_tools': 1, 'nb_slices': 4},
            ],
            'insert_location': {'mediatrice_seg_idx':0 , 'dist_from_origin':4.0e-3 }, #'bissectrice_arc_idx': 1
            'cut_face_thickness' : 3.E-3,
            'mcr_rf_cl_name' : 'mcl_rake_face'
            # optional data :
            'cut_face_nb_layers' : 2, # default: 1
            # Mandatory if clearance volume is given:
            'clearance_face_thickness' : 2.E-3,
            'clearance_face_angle_degrees' : 30.,
            'mcr_cv_cl_name' : 'mcl_rake_face'
            # Option for clearance volume :
            'clearance_face_nb_layers' : 2, # default: 1
        }
        An insert can contain as many segments as necessary.
        If it contain n segments it will contain n-1 arcs.
        """
        Tooth_model.__init__(self, **dic)
        # 0: Examnination of the coherence of the entries, defaults values
        needed_data = \
                dic.has_key('name') \
            and dic.has_key('cutting_edge_geom') \
            and dic.has_key('insert_location') \
            and dic.has_key('cut_face_thickness') \
            and dic.has_key('mcr_rf_cl_name')
        if not needed_data:
            raise Exception("Tooth_insert creation: one mandatory key is missing")            
        # optional data :
        if not dic.has_key('cut_face_nb_layers'): dic['cut_face_nb_layers'] = 1
        # clearance face data :
        # mandatory data if clearance volume is present
        clearance_vol = dic.has_key('clearance_face_thickness') \
                     or dic.has_key('clearance_face_angle_degrees') \
                     or dic.has_key('mcr_cv_cl_name') \
                     or dic.has_key('clearance_face_nb_layers')
        
        if clearance_vol : 
            needed_clear_data = dic.has_key('clearance_face_thickness') \
                            and dic.has_key('clearance_face_angle_degrees') \
                            and dic.has_key('mcr_cv_cl_name')
            if not needed_clear_data : 
                raise Exception("Tooth_insert creation: one mandatory key for clearance volume is missing")
            
            if not dic.has_key('clearance_face_nb_layers') : 
                dic['clearance_face_nb_layers'] = 1
        
        # 1
        if dic.has_key('clearance_face_thickness') and dic['clearance_face_thickness']:
            self._has_clear_face = True
            self.clearance_face_thickness = dic['clearance_face_thickness']
            self.clearance_face_nb_layers = dic['clearance_face_nb_layers']
            self.clearance_face_angle = math.radians(dic['clearance_face_angle_degrees'])        
        
        ## On compte le nombre d'elementary_tools :
        self.nb_elementary_tools = 0 # par prudence ...
        for ceg_dic in dic['cutting_edge_geom']:
            self.nb_elementary_tools += ceg_dic['nb_elementary_tools']

        # 2 : on transforme dic en une structure de données plus pratique pour l'algo :
        
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
            #for ceg_dic in dic['cutting_edge_geom']:
            #    print(ceg_dic)

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
        # Compute the points in plan (Op, zp, xp):
        # print(self.dic)
        self.__generePartiesEtMaillagePlaquette()
        # print('Elementary tools list : ',self.elementary_tools_list)
# --------------------------------------------------------------------------------------------------
    def __generePartiesEtMaillageArc(self, idxArc, current_point, current_angle, next_point, next_angle):
        dicoPartie = {}
        # print("__generePartiesEtMaillageArc  -  idxArc = %d\n"%(idxArc))
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
            firstIdxElemTool = len (self.elementary_tools_list)

            #   Arête :
            cur_point_local = [current_point[0], current_point[1]]
            cur_angle_local = current_angle
            deltaAlpha = alpha/nbPartiesArc
            sliceAngle = deltaAlpha/nbSlices
            for k in range (nbPartiesArc):
                dicoPartie = {}
                p1 = list(cur_point_local) 
                p2 = [rayon*math.cos (cur_angle_local + deltaAlpha) + centreArc[0], rayon*math.sin (cur_angle_local + deltaAlpha) + centreArc[1]]
                if self.cut_face_thickness > rayon :
                    p3 = [(centreArc[0]+p1[0]+p2[0])/3.,(centreArc[1]+p1[1]+p2[1])/3.]
                else : ## TODO Calculer le barycentre des 4 points ....
                    xi = self.cut_face_thickness/rayon
                    p1e = [xi*p1[0]+(1.-xi)*centreArc[0],xi*p1[1]+(1.-xi)*centreArc[1]]
                    p2e = [xi*p2[0]+(1.-xi)*centreArc[0],xi*p2[1]+(1.-xi)*centreArc[1]]
                    p3 = [(p1e[0]+p2e[0]+p1[0]+p2[0])/4.,(p1e[1]+p2e[1]+p1[1]+p2[1])/4.]
                dicoPartie["tooth_id"] = 0
                dicoPartie["pnt_cut_edge"] = [ [p2[1], 0., p2[0]],[p1[1], 0., p1[0]]]
                dicoPartie["pnt_in_cut_face"] = [p3[1], 0., p3[0]]
                dicoPartie["h_cut_max"] = .8*e
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
                
                dicoPartie['mcr_rf_cl_name'] = self.mcr_rf_cl_name
                dicoPartie['mcr_cv_cl_name'] = self.mcr_cv_cl_name    
                self.elementary_tools_list.append (dicoPartie)
                cur_point_local[0],cur_point_local[1] = p2[0], p2[1]
                cur_angle_local = cur_angle_local + deltaAlpha
            next_angle[0] = current_angle + alpha
            next_point[0],next_point[1] = p2[0], p2[1]
                        
            lastIdxElemTool = len (self.elementary_tools_list)

            self.__genereVolumeDepouilleArc([centreArc[1],0,centreArc[0]], rayon, current_angle, deltaAlpha, sliceAngle, nbSlices, nbCouchesReel, firstIdxElemTool, lastIdxElemTool)
            self.__clearance_bnd_mesh_mng__()
        else:
            next_point[0],next_point[1] = current_point[0], current_point[1]
            next_angle[0] = current_angle + alpha
# --------------------------------------------------------------------------------------------------        
    def __genereVolumeDepouilleArc (self, center, radius, current_angle, et_angle, 
                                    slice_angle, nb_slices, cutf_nb_layers,  
                                    firstIdx, lastIdx):
        
        if not (self.has_clear_face()) : return None
                
        truncated_cone = self.clearance_face_angle < math.atan(radius/self.clearance_face_thickness)
        coef = math.tan(self.clearance_face_angle) * self.clearance_face_thickness / radius
        
        delta_clearance_face_thickness = self.clearance_face_thickness/self.clearance_face_nb_layers
        
        # ********************
        # PhLo : 05/03/17
        # Initial version: Pb if self.clearance_face_angle == 0.
        # l_limit_on_clearance_face = max(0.,(radius - self.cut_face_thickness)/math.sin(self.clearance_face_angle))
        # l_max_on_clearance_face = radius/math.sin(self.clearance_face_angle)
        # New version:
        if truncated_cone : 
            l_max_on_clearance_face = (1.+1e-6) * self.clearance_face_thickness
        else : 
            l_max_on_clearance_face = radius/math.sin(self.clearance_face_angle)
        
        if radius - self.cut_face_thickness > 0. : 
            if self.clearance_face_angle < math.atan((radius - self.cut_face_thickness)/self.clearance_face_thickness) : 
                l_limit_on_clearance_face = (1.+1e-6) * self.clearance_face_thickness
            else : 
                l_limit_on_clearance_face = (radius - self.cut_face_thickness)/math.sin(self.clearance_face_angle)
        else : 
            l_limit_on_clearance_face = 0.0
            
        # ********************
        
        
        # print("limit : %f, max : %f"%(l_limit_on_clearance_face,l_max_on_clearance_face) )
        
        for k in range(firstIdx, lastIdx):
            back_peak = False
            bottom_peak = False
            elem_tool_dic =  self.elementary_tools_list[k]
            elem_tool_dic['node_clearance_bnd'] = []
            elem_tool_dic['tri_clearance_bnd'] = []
            
            # ********************
            # PhLo : 30/11/2016
            # Initial version:
            #elem_tool_dic['pnt_clearance_face'] = copy.deepcopy(elem_tool_dic['pnt_cut_edge']) + \
            #    [[center[0],  
            #      radius*math.cos(self.clearance_face_angle)/math.sin(self.clearance_face_angle), 
            #      center[2]],]
            # New version: 05/03/17
            cut_edge_middle = [0.5*elem_tool_dic['pnt_cut_edge'][0][idx]+0.5*elem_tool_dic['pnt_cut_edge'][1][idx] for idx in range(3)]

            y_length = 0.99 * min( delta_clearance_face_thickness, l_max_on_clearance_face)
            coef = y_length * math.tan(self.clearance_face_angle) / radius
            
            radial_dir_0 = [ (center[idx]-elem_tool_dic['pnt_cut_edge'][1][idx]) for idx in range(3) ]
            pnt_0 = [ elem_tool_dic['pnt_cut_edge'][1][0] + coef * radial_dir_0[0],
                      elem_tool_dic['pnt_cut_edge'][1][1] + y_length,
                      elem_tool_dic['pnt_cut_edge'][1][2] + coef * radial_dir_0[2] ]
            radial_dir_1 = [ (center[idx]-elem_tool_dic['pnt_cut_edge'][01][idx]) for idx in range(3) ]
            pnt_1 = [ elem_tool_dic['pnt_cut_edge'][0][0] + coef * radial_dir_1[0],
                      elem_tool_dic['pnt_cut_edge'][0][1] + y_length,
                      elem_tool_dic['pnt_cut_edge'][0][2] + coef * radial_dir_1[2] ]
            #pnt_axe = [center[0], radius*math.cos(self.clearance_face_angle)/math.sin(self.clearance_face_angle), center[2] ]
            #pnt_0 = [0.5*elem_tool_dic['pnt_cut_edge'][1][idx]+0.5*pnt_axe[idx] for idx in range(3)]
            #pnt_1 = [0.5*elem_tool_dic['pnt_cut_edge'][0][idx]+0.5*pnt_axe[idx] for idx in range(3)]
            
            elem_tool_dic['pnt_clearance_face'] = [pnt_0]+[pnt_1]+[cut_edge_middle]
            # ********************
            
            # compute the points :
            curr_et_angle = current_angle + (k - firstIdx)*et_angle
            
            clearance_layers_points_list = []
            
            idx_first_peaked_clearance_face_layer = -1
            for j in range(self.clearance_face_nb_layers+1):
                clearance_layer_points = []
                local_num_slice = 0
                # print('clearance layer nuum : %d'%(j,) )
                
                if j*delta_clearance_face_thickness < l_max_on_clearance_face:
                    if j*delta_clearance_face_thickness < l_limit_on_clearance_face:
                        for node in elem_tool_dic['node_cut_face']:
                            point = [node [0] - math.sin(curr_et_angle+local_num_slice*slice_angle) * j*delta_clearance_face_thickness * math.sin(self.clearance_face_angle),\
                                     j*delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
                                     node[2] - math.cos(curr_et_angle+local_num_slice*slice_angle)* j*delta_clearance_face_thickness* math.sin(self.clearance_face_angle)]
                            clearance_layer_points.append(point) 
                            local_num_slice+=1
                            if local_num_slice == nb_slices+1: 
                                local_num_slice = 0
                                    
                    else :    # Le secteur de disque contient le centre :
                        
                        if not back_peak:
                        
                            back_peak = True
                            idx_first_peaked_clearance_face_layer = j
                        hauteur_sous_cutface = j*delta_clearance_face_thickness * math.cos(self.clearance_face_angle)
                        # print('cutf_nb_layers : %d'%(cutf_nb_layers,) )
                        if cutf_nb_layers == 0: cutf_nb_layers = 1
                        for l in range(cutf_nb_layers):
                            xi  = float(l) /cutf_nb_layers
                            for s in range (nb_slices+1):
                                point = [(1-xi)*(elem_tool_dic['node_cut_face'][s][0]- math.sin(curr_et_angle+s*slice_angle) * j*delta_clearance_face_thickness * math.sin(self.clearance_face_angle))+xi*center[0],
                                         hauteur_sous_cutface,
                                         (1-xi)*(elem_tool_dic['node_cut_face'][s][2]- math.cos(curr_et_angle+s*slice_angle) * j*delta_clearance_face_thickness * math.sin(self.clearance_face_angle))+ xi*center[2]]
                                clearance_layer_points.append(point)
                        clearance_layer_points.append([center[0],\
                                                           j*delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
                                                          center[2]]) 
                            #cut_face_arc_num_layers+=1
                else : 
                    # print("hauteur max depacee")
                    clearance_layer_points.append([center[0],  radius*math.cos(self.clearance_face_angle)/math.sin(self.clearance_face_angle), center[2]])
                    clearance_layers_points_list.append(clearance_layer_points)
                    bottom_peak = True
                    back_peak = True
                    if idx_first_peaked_clearance_face_layer == -1: idx_first_peaked_clearance_face_layer = j 
                    break
                clearance_layers_points_list.append(clearance_layer_points)
            
            actual_clearance_face_nb_layers = len(clearance_layers_points_list)-1
            # nodes and mesh of the clearance volume :
            offset = 0
            
            # --> The clearance face :
            
            
            for j in range(actual_clearance_face_nb_layers):
                elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[j][0:nb_slices+1]
            if len(clearance_layers_points_list[-1]) == 1 :
                
                elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[-1][0])
                give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, actual_clearance_face_nb_layers-1, offset)
                offset = (nb_slices+1) * actual_clearance_face_nb_layers +1  
            else :
                 
                elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[actual_clearance_face_nb_layers][0:nb_slices+1]
                give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, actual_clearance_face_nb_layers, offset)
                offset = (nb_slices+1) * (self.clearance_face_nb_layers+1) 
            
            # ********************
            # PhLo : 30/11/2016
            # Initial version:
            ## Compute a point in the clearance face : the average of the points.
            #sum_pnt_in_clear_face = reduce (lambda a,b:  [a[i]+b[i] for i in range(3)],  elem_tool_dic['node_clearance_bnd'])
            #elem_tool_dic['pnt_clearance_face'][2] = [sum_pnt_in_clear_face[i]/len (elem_tool_dic['node_clearance_bnd']) for i in range (3)]
            # New version:
            #   Inutile selon moi car déjà calculé ...
            # ********************
            
            # --> The face below :
            if len(clearance_layers_points_list[-1]) != 1 :
                # print("On passe ....")
                elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[-1]
                if back_peak :
            
                    give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, cutf_nb_layers-1, offset)
                else :
                    give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, cutf_nb_layers, offset)
                offset += len (clearance_layers_points_list[-1])
            
            # print("ici ici")
            
            ## --> The rear face (optional face)
            # print("Face arriere")
            if back_peak:
                # print('idx_first_peaked_clearance_face_layer =', idx_first_peaked_clearance_face_layer)
                if idx_first_peaked_clearance_face_layer != 0:
                    for j in range(idx_first_peaked_clearance_face_layer):
                        elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[j][-nb_slices-1:]
                    elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[idx_first_peaked_clearance_face_layer][-1])
                    # print("back peak - mesh peak")
                    give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, idx_first_peaked_clearance_face_layer-1, offset)
                    offset+=(nb_slices+1)*(idx_first_peaked_clearance_face_layer)+1
            else :

                for j in range(actual_clearance_face_nb_layers+1):
                    elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[j][-nb_slices-1:]
                # print("back no peak - mesh rect")
                give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, actual_clearance_face_nb_layers, offset)
                offset += (actual_clearance_face_nb_layers+1) * (nb_slices+1)    

            
            # --> Les couvercles :
            if bottom_peak:
                for j in range(actual_clearance_face_nb_layers):
                    elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][i*(nb_slices+1)] for i in range(cutf_nb_layers+1) ]
                elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[-1][0])
                give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers-1, offset)
                offset+=actual_clearance_face_nb_layers*(cutf_nb_layers+1)+1
                for j in range(actual_clearance_face_nb_layers):
                    elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(cutf_nb_layers) ]
                    elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[j][-1])####
                elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[-1][0])
                give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers-1, offset)
                
               
            else:
                # couvercle 1 :
                if idx_first_peaked_clearance_face_layer == 0 :
                    for j in range(actual_clearance_face_nb_layers+1):
                        elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][i*(nb_slices+1)] for i in range(cutf_nb_layers+1) ] 
                    give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers, offset)
                    offset+=(actual_clearance_face_nb_layers+1)*(cutf_nb_layers+1)
                else :
                    for j in range(actual_clearance_face_nb_layers+1):
                        elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][i*(nb_slices+1)] for i in range(cutf_nb_layers+1) ] 
                    give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers, offset)
                    offset+=(actual_clearance_face_nb_layers+1)*(cutf_nb_layers+1)
                
                # couvercle 2 :
                if idx_first_peaked_clearance_face_layer == 0 :
                    
                    for j in range(actual_clearance_face_nb_layers+1):
                        if back_peak :
                            elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(cutf_nb_layers) ]
                            elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[j][-1])
                        else :
                            elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(cutf_nb_layers+2) ] 
                    give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers, offset)
                    #offset+=(actual_clearance_face_nb_layers+1)*(cutf_nb_layers+2)
                else :
                    for j in range(actual_clearance_face_nb_layers+1):
                        if back_peak :
                            elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(cutf_nb_layers) ]
                            elem_tool_dic['node_clearance_bnd'].append(clearance_layers_points_list[j][-1])
                        else :
                            elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(cutf_nb_layers+1) ]
                    give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], cutf_nb_layers, actual_clearance_face_nb_layers, offset)
                    #offset+=(actual_clearance_face_nb_layers+1)*(cutf_nb_layers+1)
            offset = len(elem_tool_dic['node_clearance_bnd'])
                
            # --> on ferme avec la face de coupe :
            elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[0]
            if back_peak and idx_first_peaked_clearance_face_layer == 0:
                give_mesh_rect_peak_patch(elem_tool_dic['tri_clearance_bnd'],   nb_slices, cutf_nb_layers - 1, offset)
            else :
                give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'],   nb_slices, cutf_nb_layers, offset)
        
                    
            ## """
# --------------------------------------------------------------------------------------------------               
    def __generePartiesEtMaillageSegment(self, idxSeg, current_point, current_angle, next_point):
        

        longSeg = self.dic["seg_length_list"][idxSeg]
        firstIdxElemTool = len (self.elementary_tools_list)
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
                dicoPartie["pnt_cut_edge"] = [[p2[1], 0., p2[0]],[p1[1], 0., p1[0]]]
                dicoPartie["pnt_in_cut_face"] = [p3[1], 0., p3[0]]
                dicoPartie["h_cut_max"] = .8*e
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
                dicoPartie['mcr_rf_cl_name'] = self.mcr_rf_cl_name
                dicoPartie['mcr_cv_cl_name'] = self.mcr_cv_cl_name
                self.elementary_tools_list.append (dicoPartie)
                cur_point_local = p2
            next_point[0],next_point[1] = p2[0], p2[1]
            lastIdxElemTools = len(self.elementary_tools_list)

            self.__genereVolumeDepouilleSegment(current_angle, nbSlices, firstIdxElemTool, lastIdxElemTools)
            self.__clearance_bnd_mesh_mng__()
        else:
            next_point[0],next_point[1] = current_point[0], current_point[1]
        
        
# --------------------------------------------------------------------------------------------------
    def __genereVolumeDepouilleSegment(self, current_angle, nb_slices, 
                                       firstIdx, lastIdx):
        
        if not (self.has_clear_face()) : return None
        
        delta_clearance_face_thickness = self.clearance_face_thickness/self.clearance_face_nb_layers
        for k in range(firstIdx, lastIdx):
            elem_tool_dic =  self.elementary_tools_list[k]
            elem_tool_dic['node_clearance_bnd'] = []
            elem_tool_dic['tri_clearance_bnd'] = []
            
            cut_edge_middle = [0.5*elem_tool_dic['pnt_cut_edge'][0][idx]+0.5*elem_tool_dic['pnt_cut_edge'][1][idx] for idx in range(3)]
            # ********************
            # PhLo : 30/11/2016
            # Initial version:
            #elem_tool_dic['pnt_clearance_face'] =copy.deepcopy(elem_tool_dic['pnt_cut_edge']) + \
            #       [[cut_edge_middle [0] - math.sin(current_angle) * delta_clearance_face_thickness * math.sin(self.clearance_face_angle),\
            #         delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
            #         cut_edge_middle[2] - math.cos(current_angle)* delta_clearance_face_thickness* math.sin(self.clearance_face_angle)],]
            # New version:
            pnt_0 = [elem_tool_dic['pnt_cut_edge'][1][0] - math.sin(current_angle) * delta_clearance_face_thickness * math.sin(self.clearance_face_angle),\
                     delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
                     elem_tool_dic['pnt_cut_edge'][1][2] - math.cos(current_angle)* delta_clearance_face_thickness* math.sin(self.clearance_face_angle)]
            pnt_1 = [elem_tool_dic['pnt_cut_edge'][0][0] - math.sin(current_angle) * delta_clearance_face_thickness * math.sin(self.clearance_face_angle),\
                     delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
                     elem_tool_dic['pnt_cut_edge'][0][2] - math.cos(current_angle)* delta_clearance_face_thickness* math.sin(self.clearance_face_angle)]
            elem_tool_dic['pnt_clearance_face'] = [pnt_0]+[pnt_1]+[cut_edge_middle]
            # ********************
            
            # 1: calcul des points :
            clearance_layers_points_list = []
            for j in range(self.clearance_face_nb_layers+1):
                clearance_layer_points = []
                for node in elem_tool_dic['node_cut_face']:
                    point = [node [0] - math.sin(current_angle) * j*delta_clearance_face_thickness * math.sin(self.clearance_face_angle),\
                             j*delta_clearance_face_thickness * math.cos(self.clearance_face_angle),\
                             node[2] - math.cos(current_angle)* j*delta_clearance_face_thickness* math.sin(self.clearance_face_angle)]
                    clearance_layer_points.append(point) 
                clearance_layers_points_list.append(clearance_layer_points)
            # Calcul des nodes et maillage :
            # --> face en depouille :
            for j in range(self.clearance_face_nb_layers+1):
                elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[j][0:nb_slices+1]
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, self.clearance_face_nb_layers)
            offset = (nb_slices+1) * (self.clearance_face_nb_layers+1) 
            # --> face arriere
            for j in range(self.clearance_face_nb_layers+1):
                elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[j][-nb_slices-1:]
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, self.clearance_face_nb_layers, offset)
            offset = 2*offset
            # --> face en dessous
            elem_tool_dic['node_clearance_bnd']+=clearance_layers_points_list[self.clearance_face_nb_layers]
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, self.cut_face_nb_layers, offset)
            offset += (nb_slices+1)*(self.cut_face_nb_layers+1) 
            # --> faces des côtés (faces adjassantes à un autre elem_tool)
            for j in range(self.clearance_face_nb_layers+1):
                elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][i*(nb_slices+1)] for i in range(self.cut_face_nb_layers+1) ]
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], self.cut_face_nb_layers, self.clearance_face_nb_layers, offset)
            offset += (self.clearance_face_nb_layers+1)*(self.cut_face_nb_layers+1)
            for j in range(self.clearance_face_nb_layers+1):
                elem_tool_dic['node_clearance_bnd']+=[clearance_layers_points_list[j][(i+1)*(nb_slices+1)-1] for i in range(self.cut_face_nb_layers+1) ]
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], self.cut_face_nb_layers, self.clearance_face_nb_layers, offset)
            offset = len(elem_tool_dic['node_clearance_bnd'])
            # --> face de coupe pour fermer le volume
            elem_tool_dic['node_clearance_bnd']+=copy.deepcopy(elem_tool_dic['node_cut_face'])
            give_mesh_rect_patch(elem_tool_dic['tri_clearance_bnd'], nb_slices, self.cut_face_nb_layers, offset)
# --------------------------------------------------------------------------------------------------

    def __calculPremierPointEtAngle(self, pointEtAngle):
        if self.dic.has_key("bissectrice_arc_idx"):
            idxArc = self.dic["bissectrice_arc_idx"]
            idxSeg = idxArc
            
            alpha = math.radians (self.dic["arc_angle_degrees_list"][idxArc])
            
            rayon = self.dic["radius_list"][idxArc]
            centreArc = [0., self.dic["dist_from_origin"]] # dans (Op,zp,xp)
            
            current_angle = (math.pi+alpha)/2
            current_point = [rayon*math.cos (current_angle) + centreArc[0], rayon*math.sin (current_angle) + centreArc[1]]
        else : ##  self.dic doit avoir la clef "mediatrice_seg_idx"
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
            current_point[0] += longSeg * math.cos(current_angle-math.pi/2.)
            current_point[1] += longSeg * math.sin(current_angle-math.pi/2.)
            
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
    def __generePartiesEtMaillagePlaquette(self):
        # On effectue  tous les calculs dans le repère (Op,zp,xp).
        # On ajoute yp lors de la creation des dictionnaires à passer en entrée de donnnées.
        self.elementary_tools_list = []
        e = self.cut_face_thickness
        nbCouchesFaceDeCoupe = self.cut_face_nb_layers
        pointEtAngle = [0.,0.,0.] # contiendra [z,x, alpha]
        current_point = [0.,0.]
        self.__calculPremierPointEtAngle(pointEtAngle)
        current_point[0], current_point[1], current_angle = pointEtAngle[0],pointEtAngle[1],pointEtAngle[2]  
        
        idxSeg = 0
        idxArc = 0
        
        next_point = [0.,0.]
        next_angle = [0.]
        while idxArc < len (self.dic["radius_list"]):
            ### Section segment
            self.__generePartiesEtMaillageSegment(idxSeg, current_point, current_angle, next_point)
            current_point = next_point
            
            ### Section arc :
            self.__generePartiesEtMaillageArc(idxArc, current_point, current_angle, next_point, next_angle)
            ### Section Segment : 
            current_point = next_point
            current_angle = next_angle[0]
            idxArc += 1
            idxSeg += 1
        ### derniere section segment :    
        self.__generePartiesEtMaillageSegment(idxSeg, current_point, current_angle, next_point)
        
        #print('<CGen> self.elementary_tools_list :')
        #for ddd in self.elementary_tools_list:
        #    print(ddd)
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_toroidal_mill(Tooth_insert):
# ==================================================================================================
    def __init__(self, **dic):
        """
        
        
        waited params : 
            # Mandatory data : 
            'name'                    : 'toothMonoblocTyp1', ##
            'dist_from_origin'        : 6.0D-3, ## futur radiurs of the mill...
            'tool_tip_radius'         : 3.D-3,
            'tool_tip_angle_degrees'  : 110.0,
            'lenght_before'           : 5.D-03,
            'lenght_after'            : 0.0,
            'seg_nb_elem_tool_before' : 5, 
            'seg_nb_elem_tool_after'  : 0, 
            'arc_nb_elem_tool'        : 5,
            'cut_face_thickness'      : 1.E-3, ##
            'mcr_rf_cl_name'          : "MCL1",
            # optional data :
            'helix_angle_degrees'     : -10.0, # defaut: 0.
            'cut_face_nb_layers'      : 2, # default: 1 ##
            'seg_nb_slice_before'     : 1,  # default: 1       
            'seg_nb_slice_after'      : 1, # default: 1
            'arc_nb_slices'           : 2, # default: 1   
        
            # mandatory data if clearance volume is present
            'clearance_face_angle_degrees' : 5.,
            'clearance_face_thickness'     : 0.5E-3,
            'mcr_cv_cl_name'               : "MCV1",
            # optional data if clearance volume is present
            'clearance_face_nb_layers'     : 1, # default: 1
        """
        # 0: Examnination of the coherence of the entries, defaults values
        # Medatory data : 
        needed_data = \
                dic.has_key('name') \
                and dic.has_key('dist_from_origin') \
                and dic.has_key('tool_tip_radius') \
                and dic.has_key('tool_tip_angle_degrees') \
                and dic.has_key('lenght_before') \
                and dic.has_key('lenght_after') \
                and dic.has_key('seg_nb_elem_tool_before') \
                and dic.has_key('seg_nb_elem_tool_after') \
                and dic.has_key('arc_nb_elem_tool') \
                and dic.has_key('cut_face_thickness') \
                and dic.has_key('mcr_rf_cl_name')
        if not needed_data:
            raise Exception("Tooth_toroidal_mill creation: one mandatory key is missing")
        # Optional data :
        if not dic.has_key('helix_angle_degrees'): dic['helix_angle_degrees'] = 0.
        if not dic.has_key('cut_face_nb_layers') : dic['cut_face_nb_layers' ] = 1
        if not dic.has_key('seg_nb_slice_before'): dic['seg_nb_slice_before'] = 1
        if not dic.has_key('seg_nb_slice_after') : dic['seg_nb_slice_after' ] = 1
        if not dic.has_key('arc_nb_slices')      : dic['arc_nb_slices'      ] = 1
        # mandatory data if clearance volume is present
        clearance_vol = dic.has_key('clearance_face_thickness') \
                     or dic.has_key('clearance_face_angle_degrees') \
                     or dic.has_key('mcr_cv_cl_name') \
                     or dic.has_key('clearance_face_nb_layers')
        
        if clearance_vol : 
            needed_clear_data = dic.has_key('clearance_face_thickness') \
                            and dic.has_key('clearance_face_angle_degrees') \
                            and dic.has_key('mcr_cv_cl_name')
            if not needed_clear_data : 
                raise Exception("Tooth_toroidal_mill creation: one mandatory key for clearance volume is missing")
            
            if not dic.has_key('clearance_face_nb_layers') : 
                dic['clearance_face_nb_layers'] = 1
        
        # 1: On construit le dictionnaire passé à la classe mere :
        params = {   
             'name' : dic ['name'],
             'mcr_rf_cl_name' : dic['mcr_rf_cl_name'], 
             'mcr_cv_cl_name' : dic.get('mcr_cv_cl_name'), 
             
             'cut_face_thickness' : dic['cut_face_thickness'],
             'cut_face_nb_layers' : dic['cut_face_nb_layers'],
             'clearance_face_thickness' : dic.get('clearance_face_thickness'),
             'clearance_face_nb_layers' : dic.get('clearance_face_nb_layers'),
             'clearance_face_angle_degrees' :dic.get('clearance_face_angle_degrees'),

             'cutting_edge_geom': [ # même nbSlices pour chaque el. tool
                                   {'seg_length' : dic['lenght_before'],'nb_elementary_tools': dic['seg_nb_elem_tool_before'], 'nb_slices': dic['seg_nb_slice_before']},
                                   {'angle_degrees': 180-dic['tool_tip_angle_degrees'], 'radius':dic['tool_tip_radius'], 'nb_elementary_tools': dic['arc_nb_elem_tool'], 'nb_slices': dic['arc_nb_slices']},
                                   {'seg_length' : dic['lenght_after'],'nb_elementary_tools': dic['seg_nb_elem_tool_after'], 'nb_slices': dic['seg_nb_slice_after']},
                                   
                                  ],
             'insert_location': {'mediatrice_seg_idx': 0, 'dist_from_origin':dic['dist_from_origin'] }
         }
        # 2 : Appel du constructeur de la classe mère sur les params :
        Tooth_insert.__init__(self,**params)
        #1 : preparer les donnees pour pouvoir appliquer la methode classe insert
        # Construction des listes
        """
        self.dic['seg_length_list'] = [dic['lenght_after'],dic['lenght_before']]
        self.dic['seg_nb_elementary_tools_list'] = [dic['seg_nb_elem_tool_after'],dic['seg_nb_elem_tool_before']]
        self.dic['seg_nb_slices_list'] = [dic['seg_nb_slice_after'],dic['seg_nb_slice_before']]
        
        self.dic['arc_angle_degrees_list'] = [180-dic['tool_tip_angle_degrees']]
        self.dic['arc_nb_elementary_tools_list'] = [dic['arc_nb_elem_tool']]
        self.dic['radius_list'] = [dic['tool_tip_radius']]
        self.dic['arc_nb_slices_list'] = [dic['arc_nb_slices']]
        
        self.dic["mediatrice_seg_idx"]=1
        self.dic["dist_from_origin"] = dic["dist_from_origin"]

        
        self.nb_elementary_tools = dic['seg_nb_elem_tool_before'] + dic['seg_nb_elem_tool_after'] + dic['arc_nb_elem_tool']
        ### rem. : self.nb_elementary_tools sera à priori calculé dans self.__generePartiesEtMaillagePlaquette__()
        #2 : On génère le maillage :
        self.__generePartiesEtMaillagePlaquette__()
        """
        #3 : On retourne la face de coupe et on remonte la dent sur l'axe x :
        z_diff = self.dic['seg_length_list'][1]/2. +self.dic['radius_list'][0]
        
        for elem_tool in self.elementary_tools_list:
            liste_cles = ['node_cut_face','pnt_cut_edge']
            if self.has_clear_face():
                liste_cles+=['node_clearance_bnd','pnt_clearance_face']
            for key in liste_cles:
                 
                for node in elem_tool[key]:
                    node[2] += z_diff
                    #node[1]= -node[1]
            elem_tool['pnt_in_cut_face'][2] += z_diff
        
        #for i in range (self.nb_elementary_tools):
        #    for node in self.elementary_tools_list[i]['node_cut_face']:
        #        node [2] = -node[2] + z_diff
        #    self.elementary_tools_list[i]['pnt_cut_edge'][0][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][0][2] + z_diff
        #    self.elementary_tools_list[i]['pnt_cut_edge'][1][2] = - self.elementary_tools_list[i]['pnt_cut_edge'][1][2] + z_diff
        #    self.elementary_tools_list[i]['pnt_in_cut_face'][2] = - self.elementary_tools_list[i]['pnt_in_cut_face'][2] + z_diff
            
        
        #4 : Application de la methode l'hélicoidalisation 
        # self.radius, self.height, et self.helix_angle ou self.torsion_angle doivent exister.
        self.radius = self.dic['dist_from_origin']
        self.helix_angle = math.radians(dic['helix_angle_degrees'])
        self.height = dic['tool_tip_radius']+dic['lenght_before']
        self.torsion_transformation()
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_cylindrical_mill(Tooth_insert):
# ==================================================================================================
    def __init__(self, **dic):
        """
        waited params : 
            # Mandatory data : 
            name = 'toothMonoblocTyp1',
            radius                   = 3.6E-3,
            cut_face_thickness       = 1.E-3,
            height                   = 2.E-3,
            nb_elementary_tools      = 3,
            mcr_rf_cl_name = "MCL1",
            # optional data :
            torsion_angle_degrees    = 20.# default: 0.0
            cut_face_nb_layers       = 2, # default: 1
            nb_slices                = 4, # default: 1
            # mandatory data if clearance volume is present
            clearance_face_angle_degrees = 5.,
            clearance_face_thickness = 0.5E-3,
            mcr_cv_cl_name = "MCV1",
            # optional data if clearance volume is present
            clearance_face_nb_layers = 1, # default: 1
        """
        # 0: Examnination of the coherence of the entries, defaults values
        needed_data = dic.has_key('name') \
                    and dic.has_key('radius') \
                    and dic.has_key('cut_face_thickness') \
                    and dic.has_key('height') \
                    and dic.has_key('nb_elementary_tools') \
                    and dic.has_key('mcr_rf_cl_name')
        if not needed_data:
            raise Exception("Tooth_cylindrical_mill creation: one mandatory key is missing")
        # Default values
        if not dic.has_key('torsion_angle_degrees') : 
            dic['torsion_angle_degrees'] = 0.0
        if not dic.has_key('cut_face_nb_layers') : 
            dic['cut_face_nb_layers'] = 1        
        if not dic.has_key('nb_slices') : 
            dic['nb_slices'] = 1
        
        clearance_vol = dic.has_key('clearance_face_thickness') \
                     or dic.has_key('clearance_face_angle_degrees') \
                     or dic.has_key('mcr_cv_cl_name') \
                     or dic.has_key('clearance_face_nb_layers')
        
        if clearance_vol : 
            needed_clear_data = dic.has_key('clearance_face_thickness') \
                            and dic.has_key('clearance_face_angle_degrees') \
                            and dic.has_key('mcr_cv_cl_name')
            if not needed_clear_data : 
                raise Exception("Tooth_cylindrical_mill creation: one mandatory key for clearance volume is missing")
            
            if not dic.has_key('clearance_face_nb_layers') : 
                dic['clearance_face_nb_layers'] = 1




                    
        self.torsion_angle = math.radians(dic['torsion_angle_degrees'])
        self.height = dic['height']
        # 1: transformation des données pour être géré commme une plaquette. 
        params = {}
        params['name'] = dic['name']
        params['cut_face_thickness'] = dic['cut_face_thickness']
        params['cut_face_nb_layers'] = dic['cut_face_nb_layers']
        params['clearance_face_thickness'] = dic.get('clearance_face_thickness')
        params['clearance_face_nb_layers'] = dic.get('clearance_face_nb_layers')
        params['clearance_face_angle_degrees'] = dic.get('clearance_face_angle_degrees')
        params['mcr_rf_cl_name']  = dic ['mcr_rf_cl_name']
        params['mcr_cv_cl_name'] = dic.get('mcr_cv_cl_name')
        
        params['cutting_edge_geom'] = [{'seg_length' : dic['height'], \
                                        'nb_elementary_tools': dic['nb_elementary_tools'], \
                                        'nb_slices':  dic['nb_slices']},]
        params['insert_location'] ={'mediatrice_seg_idx' : 0, 'dist_from_origin': dic['radius']}
        
        
        # 2: Appel du contructeur de la classe mère :
        Tooth_insert.__init__(self, **params) 
        # 3: deplacement des points pour que la dent soit posée sur le plan (O,x,y)
        
        for elem_tool in self.elementary_tools_list:
            liste_cles = ['node_cut_face','pnt_cut_edge']
            if self.has_clear_face(): liste_cles+=['node_clearance_bnd','pnt_clearance_face']
            for key in liste_cles:
                 
                for node in elem_tool[key]:
                    node[2]+=dic['height']/2.
                    #node[1]= -node[1]
            elem_tool['pnt_in_cut_face'][2] += dic['height']/2.
            
        # 4: application de la torsion transformation. 
        self.torsion_transformation()
                
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_ball_mill(Tooth_insert):
# ==================================================================================================
    def __init__(self, **dic):
        """
        waited params : 
        {
        # Mandatory data : 
        'name' : 'ball_mill_tooth',
        'radius' : 4.E-3,
        'init_angle_degrees' : 5. ,
        'cutting_angle_degrees' : 160., 
        'cut_face_thickness' : 0.80E-3,
        'nb_elementary_tools': 20,  
        'mcr_rf_cl_name' : 'mcl_rake_face',
        # optional data :
        'helix_angle_degrees': 20., # default: 0.0
        'cut_face_nb_layers' : 2,   # default: 1
        'nb_slices'          : 3,   # default: 1       
        # mandatory data if clearance volume is present
        'mcr_cv_cl_name' : 'mcl_clear_face',
        'clearance_face_thickness' : 1.5E-3,
        'clearance_face_angle_degrees' : 1.20,
        # optional data
        'clearance_face_nb_layers' : 2 # default: 1
        #
        }
        """
        
        # 0: Examnination of the coherence of the entries, defaults values
        
        needed_data = dic.has_key('name') \
                  and dic.has_key('radius') \
                  and dic.has_key('init_angle_degrees') \
                  and dic.has_key('cutting_angle_degrees') \
                  and dic.has_key('cut_face_thickness') \
                  and dic.has_key('nb_elementary_tools') \
                  and dic.has_key('mcr_rf_cl_name')
        if not needed_data:
            raise Exception("Tooth_ball_mill creation: one mandatory key is missing")
        
        # Default values
        if not dic.has_key('helix_angle_degrees') : 
            dic['helix_angle_degrees'] = 0.0
        if not dic.has_key('cut_face_nb_layers') : 
            dic['cut_face_nb_layers'] = 1        
        if not dic.has_key('nb_slices') : 
            dic['nb_slices'] = 1
        
        clearance_vol = dic.has_key('clearance_face_thickness') \
                     or dic.has_key('clearance_face_angle_degrees') \
                     or dic.has_key('mcr_cv_cl_name') \
                     or dic.has_key('clearance_face_nb_layers')
        
        if clearance_vol : 
            needed_clear_data = dic.has_key('clearance_face_thickness') \
                            and dic.has_key('clearance_face_angle_degrees') \
                            and dic.has_key('mcr_cv_cl_name')
            if not needed_clear_data : 
                raise Exception("Tooth_ball_mill creation: one mandatory key for clearance volume is missing")
            
            if not dic.has_key('clearance_face_nb_layers') : 
                dic['clearance_face_nb_layers'] = 1
                        
        
        # 1: transformation des données pour être géré commme une plaquette. 
        params = {}
        params['name'] = dic['name']
        params['cut_face_thickness'] = dic['cut_face_thickness']
        params['cut_face_nb_layers'] = dic['cut_face_nb_layers']
        params['mcr_rf_cl_name']  = dic ['mcr_rf_cl_name']
        if clearance_vol :
            params['clearance_face_thickness'] = dic.get('clearance_face_thickness')
            params['clearance_face_nb_layers'] = dic.get('clearance_face_nb_layers')
            params['clearance_face_angle_degrees'] = dic.get('clearance_face_angle_degrees')
            params['mcr_cv_cl_name'] = dic.get('mcr_cv_cl_name')
        
            
        ## TODO : Controler que radius > cut_face_thickness + debordement volume en depouille /!\
        params['radius'] = dic['radius']
        
        params['cutting_edge_geom'] = [{'seg_length' : 0., \
                                        'nb_elementary_tools': 1, \
                                        'nb_slices':  dic['nb_slices']},\
                                       {'angle_degrees': dic['cutting_angle_degrees'], 'radius':dic['radius'],\
                                        'nb_elementary_tools': dic['nb_elementary_tools'], 'nb_slices': dic['nb_slices']}, \
                                       {'seg_length' :0.,                'nb_elementary_tools': 5, 'nb_slices': 2}] 
        params['insert_location'] ={'bissectrice_arc_idx' : 0, 'dist_from_origin': 0.}
        # 2: Appel du contructeur de la classe mère :
        Tooth_insert.__init__(self, **params)
        
        self.helix_angle = np.radians(dic['helix_angle_degrees'])
        self.radius = dic['radius']
        cutting_angle_degrees = np.radians(dic['cutting_angle_degrees'])
        init_angle_degrees  = np.radians(dic['init_angle_degrees'])
        self.height = self.radius*(np.sin(cutting_angle_degrees+init_angle_degrees-np.pi/2) - np.sin(init_angle_degrees-np.pi/2))

        # 3: Rotation  d'axe y pour se caler sur l'init_angle_degrees et 
        # deplacement des points pour que la dent soit posée sur le plan (O,x,y):
        
        for elem_tool in self.elementary_tools_list:
            liste_cles = ['node_cut_face','pnt_cut_edge']
            if self.has_clear_face(): liste_cles+=['node_clearance_bnd','pnt_clearance_face']
            for key in liste_cles:                 
                for node in elem_tool[key]:
                    ## DONE : incerer ici la rotation d'axe y.
                    np_node = np.array(node)
                    np_rot_matrix = FoR.npRotAroundOyAxisMatrix(np.pi/2.-np.radians(dic['cutting_angle_degrees']/2. + dic['init_angle_degrees']))
                    np_rot_node = np.dot(np_rot_matrix,np_node)
                    node[0] = np_rot_node[0]
                    node[1] = np_rot_node[1]
                    node[2] = np_rot_node[2]
                    node[2]+=dic['radius']
                    #node[1]= -node[1]
            np_node = np.array(elem_tool['pnt_in_cut_face'])
            np_rot_matrix = FoR.npRotAroundOyAxisMatrix(np.pi/2.-np.radians(dic['cutting_angle_degrees']/2. + dic['init_angle_degrees']))
            np_rot_node = np.dot(np_rot_matrix,np_node)
            elem_tool['pnt_in_cut_face'][0] = np_rot_node[0]
            elem_tool['pnt_in_cut_face'][1] = np_rot_node[1]
            elem_tool['pnt_in_cut_face'][2] = np_rot_node[2]
            elem_tool['pnt_in_cut_face'][2]+=dic['radius']
            
        # 5: application de l'angle de torsion 
        self.torsion_transformation()
        
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class Tooth_sliced(Tooth_model):
# ==================================================================================================
    def __init__(self, **dic):
        """
        parameters        
        # Mandatory data :    
        name                      = 'ball_mill_tooth',
        cutting_edge_geom         = file_gtooth,
        nb_elementary_tools       = 4,
        nb_slices_per_elt         = 5,
        clearance_face1_nb_layers = 1,
        clearance_face2_nb_layers = 1,
        mcr_rf_cl_name            = 'mcl_cut_face', 
        cut_face_thickness        = 1.E-3,
        # Optional data :
        cut_face_nb_layers = 1, # default: 1
        mcr_cv_cl_name = 'mcl_clear_face'  # if not specified, clearance volume is
                                           # not generated
        """
        # 0: Examnination of the coherence of the entries, defaults values
        # 0.1: Mandatory data :
        needed_data = dic.has_key('name') \
                 and  dic.has_key('cutting_edge_geom') \
                 and  dic.has_key('nb_elementary_tools') \
                 and  dic.has_key('nb_slices_per_elt') \
                 and  dic.has_key('clearance_face1_nb_layers') \
                 and  dic.has_key('clearance_face2_nb_layers') \
                 and  dic.has_key('mcr_rf_cl_name') \
                 and  dic.has_key('cut_face_thickness')
        if not needed_data:
            raise Exception("Tooth_sliced creation: one mandatory key is missing")
        
        if not dic.has_key('cut_face_nb_layers'): dic['cut_face_nb_layers'] = 1
        # 1: Call the constructor of the mother class
        Tooth_model.__init__(self, **dic)
        if self.mcr_cv_cl_name: self._has_clear_face = True
        
        
            
            
        self.nb_elementary_tools = dic['nb_elementary_tools']
        self.nb_slices_per_elt = dic['nb_slices_per_elt']
        self.clearance_face1_nb_layers = dic['clearance_face1_nb_layers']
        self.clearance_face2_nb_layers = dic['clearance_face2_nb_layers']

        ## Import of the sliced tooth data and dictionary creation :
        file_name_gtooth = dic['cutting_edge_geom']
        print("reading gtooth file : " + file_name_gtooth) 
        #file_name_gtooth = os.path.join(case_path,file_name_gtooth)
        data_file_tooth = open (file_name_gtooth, 'r')
        first_line = data_file_tooth.readline()
        nb_data_slice = int (first_line)
        print(' number of slices: '+ str(nb_data_slice) )
        from_data_dic_list = []
        data_keys = ['z','x','y','gamma','L_gamma','alpha1','L1','alpha2','L2']
        for i in range (nb_data_slice):       
            from_data_line = data_file_tooth.readline()
            splitted_line = from_data_line.split()
            from_data_dic = {}
            i = 0
            for cle in data_keys:
                from_data_dic [cle] = float(splitted_line[i])
                i+=1
            from_data_dic_list.append(from_data_dic)
        self.cutting_edge_geom = from_data_dic_list

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
        # for i in range(len(cutting_edge_geom_interpolated)): print i, ' : ', cutting_edge_geom_interpolated[i]
        
        # 2 : Calcul des points
        # ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨
        hcut_max = 0
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
                hcut_max = max(hcut_max,slice_geom_dic['L_gamma'] )
                ## calcul de l'angle util à partir de gamma :
                gamma = math.radians(slice_geom_dic['gamma'])
                radius = math.sqrt(slice_geom_dic['x']**2 + slice_geom_dic['y']**2)
                rho =  math.acos(slice_geom_dic['x']/radius)
                gamma_util = rho + math.pi - gamma
                increment_l_gamma = slice_geom_dic['L_gamma'] /self.cut_face_nb_layers
                
                #alpha1_util = gamma_util - math.pi/2  + math.radians(slice_geom_dic['alpha1'])
                alpha1_util = rho + math.pi/2  + math.radians(slice_geom_dic['alpha1'])
                increment_l_alpha1 = slice_geom_dic['L1']/self.clearance_face1_nb_layers
                
                #alpha2_util = gamma_util - math.pi/2  + math.radians(slice_geom_dic['alpha2'])
                alpha2_util = rho + math.pi/2  + math.radians(slice_geom_dic['alpha2'])
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
            elem_tool['h_cut_max'] = hcut_max
            
            
            
            for j in range (self.nb_slices_per_elt+1):
                elem_tool['node_cut_face']+=elem_tools_slices_points_list[k][j][0:self.cut_face_nb_layers+1]
            give_mesh_rect_patch( tri = elem_tool['tri_cut_face'], dim1 = self.cut_face_nb_layers, dim2 = self.nb_slices_per_elt)
            #for j in range (self.nb_slices_per_elt):    
            #    for i in range(self.cut_face_nb_layers):
            #        elem_tool['tri_cut_face'].append([j*(self.cut_face_nb_layers+1)+i+1, j*(self.cut_face_nb_layers+1)+i,     (j+1)*(self.cut_face_nb_layers+1)+i ])
            #        elem_tool['tri_cut_face'].append([j*(self.cut_face_nb_layers+1)+i+1, (j+1)*(self.cut_face_nb_layers+1)+i, (j+1)*(self.cut_face_nb_layers+1)+i +1 ])
            elem_tool['mcr_rf_cl_name'] = self.mcr_rf_cl_name
            elem_tool['mcr_cv_cl_name'] = self.mcr_cv_cl_name
            self.elementary_tools_list.append(elem_tool)
        #print("Nombre d'outils elementaires  : ", len(self.elementary_tools_list) )
        #for tool_elementaire in self.elementary_tools_list : print(tool_elementaire)
        
        # Volume en dépouille :
        
        # Faces en dépouilles
        for k in range (self.nb_elementary_tools):
            
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            elem_tool = self.elementary_tools_list[k]
            elem_tool['node_clearance_bnd'] = []
            elem_tool['tri_clearance_bnd'] = []
            
            # ********************
            # PhLo : 30/11/2016
            # Initial version:
            #elem_tool['pnt_clearance_face'] =elem_tool['pnt_cut_edge'] + \
            #                  [[( (elem_tools_slices_points_list[k][0][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)][idx]) \
            #                    + (elem_tools_slices_points_list[k][self.nb_slices_per_elt][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)][idx]) )/2. for idx in [0,1,2]],]
            # New version:
            cut_edge_middle = [0.5*elem_tool['pnt_cut_edge'][0][idx]+0.5*elem_tool['pnt_cut_edge'][1][idx] for idx in range(3)]
            pnt_0 = elem_tools_slices_points_list[k][self.nb_slices_per_elt][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)]
            pnt_1 = elem_tools_slices_points_list[k][0][self.clearance_face1_nb_layers*(self.cut_face_nb_layers+1)]
            elem_tool['pnt_clearance_face'] = [pnt_0]+[pnt_1]+[cut_edge_middle]
            # ********************
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=[elem_tools_slices_points_list[k][j][i*(self.cut_face_nb_layers+1)] for i in range(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)]
            give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, dim2 = self.nb_slices_per_elt)
            
             
        # print('self.elementary_tools_list : ', self.elementary_tools_list)
        # Faces opposées 
        for k in range (self.nb_elementary_tools):
            
            #j_max = self.nb_slices_per_elt if k < self.nb_elementary_tools-1 else self.nb_slices_per_elt+1
            elem_tool = self.elementary_tools_list[k]
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=[elem_tools_slices_points_list[k][j][(i+1)*(self.cut_face_nb_layers+1)-1] for i in range(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)]
            give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, dim2 = self.nb_slices_per_elt, \
                                   offset=(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        
        # print('self.elementary_tools_list After : ', self.elementary_tools_list)
        
        # Face arriere :
        for k in range (self.nb_elementary_tools):
            elem_tool = self.elementary_tools_list[k]
            for j in range(self.nb_slices_per_elt+1):
                elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][j][-self.cut_face_nb_layers-1:]
            give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.cut_face_nb_layers, dim2 = self.nb_slices_per_elt, \
                                   offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        # Face dessous et face dessus :
        for k in range (self.nb_elementary_tools):
            elem_tool = self.elementary_tools_list[k]
            elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][0]
            elem_tool['node_clearance_bnd']+=elem_tools_slices_points_list[k][self.nb_slices_per_elt]
            give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], dim1 = self.cut_face_nb_layers, dim2 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, \
                                   offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1)+(self.cut_face_nb_layers+1)*(self.nb_slices_per_elt+1))
            give_mesh_rect_patch( tri = elem_tool['tri_clearance_bnd'], \
                                       dim1 = self.cut_face_nb_layers, \
                                       dim2 = self.clearance_face1_nb_layers+self.clearance_face2_nb_layers, \
                                       offset=2*(self.nb_slices_per_elt+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1) + \
                                              (self.cut_face_nb_layers+1)*(self.nb_slices_per_elt+1) + \
                                              (self.cut_face_nb_layers+1)*(self.clearance_face1_nb_layers+self.clearance_face2_nb_layers+1))
        
        # On ajoute la face de coupe pour fermer le volume en dépouille :
        for k in range (self.nb_elementary_tools):
            elem_tool = self.elementary_tools_list[k]
            offset = len(elem_tool['node_clearance_bnd'])
            elem_tool['node_clearance_bnd']+=elem_tool['node_cut_face']
            give_mesh_rect_patch(tri = elem_tool['tri_clearance_bnd'], dim1 = self.cut_face_nb_layers, dim2 = self.nb_slices_per_elt, offset = offset)
        self.__clearance_bnd_mesh_mng__()
# --------------------------------------------------------------------------------------------------
# ==================================================================================================


if __name__ == "__main__":
    """
    TODO : test
    """
    print("TODO : a test that test every thing ...")
