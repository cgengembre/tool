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
    def addTooth(self, tooth, frame, tsif_name ='base_toolstep' ):
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
            self.elementary_tools_list.append(dicPartie)
        idx_in_etl_end = len(self.elementary_tools_list)-1
        self.benen_in_etl_dic[tsif_name].append([idx_in_etl_begin, idx_in_etl_end])
        # Calculer arrete et maillage dans le repere canonique de la fraise et l'ajouter
        # dans la liste des parties
# --------------------------------------------------------------------------------------------------
    def addToolstep(self, name, toolstep, frame ):
        if self.benen_in_etl_dic.has_key(name):
            print name, " : attention - nom déjà choisi pour l'etage !!" 
        else:
            tsif = Toolstep.ToolstepInFrame(name = name, toolstep = toolstep, frame = frame)
            self.toolstep_dic[name] = tsif
            self.benen_in_etl_dic[name] = [[i+len(self.elementary_tools_list) for i in toolstep.idx_benen_in_etl_list[j]] for j in range(len(toolstep.idx_benen_in_etl_list))]
            for partie in toolstep.elementary_tools_list:
                dicPartie = {}
                dicPartie["tooth_id"] = partie['tooth_id']
                dicPartie['toolstep_id'] = name
                dicPartie["pnt_cut_edge"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_cut_edge"])
                dicPartie["pnt_in_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, [partie["pnt_in_cut_face"]])[0]
                dicPartie["h_cut_max"] = partie["h_cut_max"]
                dicPartie["node_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_cut_face"])
                dicPartie["tri_cut_face"] = partie["tri_cut_face"]
                # On ajoute le volume en dépouille, et les points de la face en dépouille :
                dicPartie["node_clearance_bnd"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_clearance_bnd"])
                dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
                dicPartie["pnt_clearance_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_clearance_face"])
            
                self.elementary_tools_list.append(dicPartie)
# --------------------------------------------------------------------------------------------------
    def draw(self):
        bloc_util.view_bloc(self.elementary_tools_list)
# --------------------------------------------------------------------------------------------------
    def write(self, file_name = None):
        if file_name == None :
            file_name = self.name + '.py'
        file_tool = open(file_name, 'w')
        file_tool.write("[")
        for etl in self.elementary_tools_list:
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
