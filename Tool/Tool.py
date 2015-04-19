# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 8 sept. 2014
# 
#
# 
# Les angles sont donnés en degres.
# Il sont convertis en Radian dès le constructeur
#

import math
import numpy as np

import bloc_util
import FrameOfReference as FoR
import Tooth
import Toolstep
# from Carbon.QuickDraw import frame
# from json import tool

class InconcistentDataError(Exception):
    pass
CUTFACE_BLOC = 0
CLEARANCE_BLOC = 1


# ==================================================================================================
class Tool:
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    __instance_counter__ = 0
    def __init__(self, **dic):
        
        self.elementary_tools_list = [] 
        self.benen_in_etl_dic = {'base_toolstep' : []}
        self.toolstep_dic = {}
        if dic.has_key('name'):
            self.name = dic['name']
        else:
            self.name = 'Tool_'+str(Tool.__instance_counter__)
        
        self.foref = FoR.FrameOfReference(name = 'for_' + self.name)
        
        toolstep0 = Toolstep.ToolstepModel()
        base_tsif = Toolstep.ToolstepInFrame(name = 'base_toolstep', toolstep = toolstep0, frame = None )
        self.toolstep_dic['base_toolstep'] = base_tsif
        self.__toolstep_id__ = 0
        Tool.__instance_counter__ += 1

# --------------------------------------------------------------------------------------------------
    def addToolstep(self, toolstep, frame, name = "default" ):
        if name == "default" :
            name = toolstep.name + str (self.__toolstep_id__)
        if self.benen_in_etl_dic.has_key(name):
            print name, " : attention - nom déjà choisi pour l'etage !!" 
        else:
            tsif = Toolstep.ToolstepInFrame(name = name, toolstep = toolstep, frame = frame)
            self.toolstep_dic[name] = tsif
            self.benen_in_etl_dic[name] = [[i+len(self.elementary_tools_list) for i in toolstep.idx_benen_in_etl_list[j]] for j in range(len(toolstep.idx_benen_in_etl_list))]
            for partie in toolstep.elementary_tools_list:
                dicPartie = {}
                dicPartie["tooth_id"] = partie['tooth_id']
                dicPartie["set_id"] = partie['set_id']
                dicPartie['toolstep_id'] = self.__toolstep_id__
                dicPartie["pnt_cut_edge"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_cut_edge"])
                dicPartie["pnt_in_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, [partie["pnt_in_cut_face"]])[0]
                dicPartie["h_cut_max"] = partie["h_cut_max"]
                dicPartie["node_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_cut_face"])
                dicPartie["tri_cut_face"] = partie["tri_cut_face"]
                # On ajoute le volume en dépouille, et les points de la face en dépouille :
                dicPartie["node_clearance_bnd"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_clearance_bnd"])
                dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
                dicPartie["pnt_clearance_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_clearance_face"]) 
                dicPartie["generic_cut_law"] = partie["generic_cut_law"]
                dicPartie["generic_clear_law"] = partie["generic_clear_law"]
            
                self.elementary_tools_list.append(dicPartie)
        self.__toolstep_id__+=1
# --------------------------------------------------------------------------------------------------        
    def addTooth(self, tooth, frame, set_id = None , tsif_name ='base_toolstep' ):
        tooth_id = self.toolstep_dic[tsif_name].toolstep.addTooth(tooth, frame)#,self.toolstep_dic[sif_name].toolstep.__tooth_id__)
        # self.foref.add(frame)
        # calculer les points de la dent dans le repere canonique de la fraise
        # insert.elementary_tools_list est la liste des parties de la plaquette ajoutée
        # print tooth.elementary_tools_list
        idx_in_etl_begin = len(self.elementary_tools_list)
        begin_in_toolstep = self.toolstep_dic[tsif_name].toolstep.idx_benen_in_etl_list[tooth_id][0]
        end_in_toolstep = self.toolstep_dic[tsif_name].toolstep.idx_benen_in_etl_list[tooth_id][1]
        for partie in self.toolstep_dic[tsif_name].toolstep.elementary_tools_list[begin_in_toolstep:end_in_toolstep+1]:
            dicPartie = {}
            
            dicPartie["tooth_id"] = tooth_id
            dicPartie["toolstep_id"] = tsif_name
            dicPartie["set_id"] = set_id
            if self.toolstep_dic[tsif_name].frame : # != None:
                toolstep_frame = self.toolstep_dic[tsif_name].frame
                dicPartie["pnt_cut_edge"] = self.foref.givePointsInCanonicalFrame(toolstep_frame.name, partie["pnt_cut_edge"])
                dicPartie["pnt_in_cut_face"] = self.foref.givePointsInCanonicalFrame(toolstep_frame.name, [partie["pnt_in_cut_face"]])[0]
                dicPartie["h_cut_max"] = partie["h_cut_max"]
                dicPartie["node_cut_face"] = self.foref.givePointsInCanonicalFrame(toolstep_frame.name, partie["node_cut_face"])
                dicPartie["tri_cut_face"] = partie["tri_cut_face"]
                # On ajoute le volume en dépouille, et les points de la face en dépouille :
                dicPartie["node_clearance_bnd"] = self.foref.givePointsInCanonicalFrame(toolstep_frame.name, partie["node_clearance_bnd"])
                dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
                dicPartie["pnt_clearance_face"] = self.foref.givePointsInCanonicalFrame(toolstep_frame.name, partie["pnt_clearance_face"])
            else :
                dicPartie["pnt_cut_edge"] =   partie["pnt_cut_edge"]
                dicPartie["pnt_in_cut_face"] =   partie["pnt_in_cut_face"]
                dicPartie["h_cut_max"] = partie["h_cut_max"]
                dicPartie["node_cut_face"] =   partie["node_cut_face"]
                dicPartie["tri_cut_face"] = partie["tri_cut_face"]
                # On ajoute le volume en dépouille, et les points de la face en dépouille :
                dicPartie["node_clearance_bnd"] =   partie["node_clearance_bnd"]
                dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
                dicPartie["pnt_clearance_face"] =   partie["pnt_clearance_face"]
            dicPartie['generic_cut_law'] = tooth.generic_cut_law
            dicPartie['generic_clear_law'] = tooth.generic_clear_law
            self.elementary_tools_list.append(dicPartie)
        idx_in_etl_end = len(self.elementary_tools_list)-1
        self.benen_in_etl_dic[tsif_name].append([idx_in_etl_begin, idx_in_etl_end])
        # Calculer arrete et maillage dans le repere canonique de la fraise et l'ajouter
        # dans la liste des parties
# --------------------------------------------------------------------------------------------------
    def draw(self, bloc_type = CUTFACE_BLOC):
        self.compute_out_blocs() 
        bloc_util.view_bloc(self.elem_tool_out_list, 'tool.lf')
        
# --------------------------------------------------------------------------------------------------
    def compute_out_blocs (self):
        self.elem_tool_out_list = []
        elemtool_id = 0
        for elem_tool in self.elementary_tools_list:
            elem_tool_cut = {}
            elem_tool_clear = {}
            ## cutting face :

            elem_tool_cut['type']            = 'cut'
            elem_tool_cut['node']            = elem_tool['node_cut_face'] # noeud
            elem_tool_cut['tri']             = elem_tool['tri_cut_face'] # tri
            elem_tool_cut['pnt']             = elem_tool['pnt_cut_edge'] + [elem_tool['pnt_in_cut_face'],]  # : 3 point , les deux point de l'arrete et le point de la face. 
            elem_tool_cut['h_cut_max']       = elem_tool['h_cut_max']
            elem_tool_cut['generic_cut_law']      = elem_tool['generic_cut_law']# : liste nom lois de coupe, 1 par bloc dexel
            elem_tool_cut['tooth_id']        = elem_tool['tooth_id']
            elem_tool_cut['set_id']          = elem_tool['set_id']
            elem_tool_cut['step_id']         = elem_tool['toolstep_id']
            elem_tool_cut['elemtool_id']     = elemtool_id


            #elem_tool_cut['rep_in_spindle']  = elem_tool['']# optionel
            #elem_tool_cut['id_node_dyn']     = elem_tool['']# optionel
            #elem_tool_cut['nb_rep']          = elem_tool['']# optionel
            self.elem_tool_out_list.append(elem_tool_cut)
            
            ## clear face
            
            elem_tool_clear['type']           = 'clear'
            elem_tool_clear['node']           = elem_tool['node_clearance_bnd']# noeud
            elem_tool_clear['tri']            = elem_tool['tri_clearance_bnd']# tri
            elem_tool_clear['pnt']            = [elem_tool['pnt_clearance_face'][i] for i in  [2,1,0]] #: 3 point , p1 point dans la face de talonnage, p1p2 dir U, p1p3 dir v, avec U^V normal sortante
            elem_tool_clear['generic_clear_law']      = elem_tool['generic_clear_law']# : liste nom lois de talonnage, 1 par bloc dexel
            elem_tool_clear['tooth_id']       = elem_tool['tooth_id']
            elem_tool_clear['set_id']         = elem_tool['set_id']
            elem_tool_clear['step_id']        = elem_tool['toolstep_id']
            elem_tool_cut['elemtool_id']      = elemtool_id
            #elem_tool_clear['rep_in_spindle'] = elem_tool[]# optionel
            #elem_tool_clear['id_node_dyn']    = elem_tool[]# optionel
            #elem_tool_clear['nb_rep']         = elem_tool[]# optionel
            self.elem_tool_out_list.append(elem_tool_clear)
            elemtool_id += 1
            
# --------------------------------------------------------------------------------------------------
    def write(self,  file_name = None):
        # Construction de la liste OUT à partir de self.elementary_tools_list
        self.compute_out_blocs()    
        
        if file_name == None :
            file_name = self.name + '.py'
        file_tool = open(file_name, 'w')
        file_tool.write("tool_def = [")
        for etl in self.elem_tool_out_list:
            file_tool.write ('{\n')
            for k in etl.keys():
                if isinstance(etl[k], str):
                    file_tool.write("'"+k+"' : "+"'"+str(etl[k])+"'")
                else:
                    file_tool.write("'"+k+"' : "+str(etl[k]))
                file_tool.write(',\n')
            file_tool.write("},\n")
        file_tool.write("]")
        file_tool.close()
# --------------------------------------------------------------------------------------------------                
# ==================================================================================================
