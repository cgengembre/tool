# -*- coding: Utf-8 -*-

import Tooth
# ==================================================================================================
class ToolstepModel:
# ==================================================================================================
    __instance_counter__ = 0
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
        """
        
        """
        
        if dic.has_key('name'):
            self.name = dic['name']
        else:
            self.name = 'Toolstep_'+str(ToolstepModel.__instance_counter__)
        
        #self.name = dic['name']
        #if dic.has_key('dic_frame'):
        #    self.frame = FoR.Frame(**dic['frame_dic'])
        #else :
        #   self.frame = None # dans ce cas le repere de l'étage et le repere canonique de fom
        self.tif_list = []
        self.repeated_teeth_list = []
        #self.elementary_tools_obj = ElemToolList()
        #self.elementary_tools_list = self.elementary_tools_obj.elementary_tools_list
        self.elementary_tools_list = []
        self.range_in_etl_list = []
        self.__tooth_id__ = 0
        ToolstepModel.__instance_counter__ += 1 
# --------------------------------------------------------------------------------------------------
    def addTooth(self, tooth, frame):
        """
        """
        tif = Tooth.ToothInFrame(tooth = tooth, frame = frame, tooth_id= self.__tooth_id__)
        self.tif_list.append(tif)
        idx_in_elt_begin = len(self.elementary_tools_list)
        for partie in tooth.elementary_tools_list:
            dicPartie = {}
            dicPartie["tooth_id"] = self.__tooth_id__
            dicPartie["pnt_cut_edge"] = frame.givePointsInFatherFrame( partie["pnt_cut_edge"])
            dicPartie["pnt_in_cut_face"] = frame.givePointsInFatherFrame( [partie["pnt_in_cut_face"]])[0]
            dicPartie["h_cut_max"] = partie["h_cut_max"]
            dicPartie["node_cut_face"] = frame.givePointsInFatherFrame( partie["node_cut_face"])
            dicPartie["tri_cut_face"] = partie["tri_cut_face"]
            # On ajoute le volume en dépouille, et les points de la face en dépouille :
            dicPartie["node_clearance_bnd"] = frame.givePointsInFatherFrame(partie["node_clearance_bnd"])
            dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
            dicPartie["pnt_clearance_face"] = frame.givePointsInFatherFrame(partie["pnt_clearance_face"])
            self.elementary_tools_list.append(dicPartie)
        idx_in_etl_end = len(self.elementary_tools_list)-1
        self.range_in_etl_list.append([idx_in_elt_begin, idx_in_etl_end])
        self.repeated_teeth_list.append(0)
        self.__tooth_id__+=1
# --------------------------------------------------------------------------------------------------
    def draw(self):
        bloc_util.view_bloc(self.elementary_tools_list)

# ==================================================================================================
class ToolstepInFrame:
# ==================================================================================================
    def __init__(self, **dic):
        """
        structure de dic :
        {
            'name'  : "nom de l'etage"
            'frame' : le repere pour placer l'étage dans un outil
            'toolstep': l'étage  
        }
        """
        self.name = dic['name']
        self.toolstep = dic ['toolstep']
        self.frame = dic ['frame']
