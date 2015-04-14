# -*- coding: Utf-8 -*-
import FrameOfReference as FoR

import Tooth
CUTFACE_BLOC = 0
CLEARANCE_BLOC = 1

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
        
        self.foref = FoR.FrameOfReference()
        #self.name = dic['name']
        #if dic.has_key('dic_frame'):
        #    self.frame = FoR.Frame(**dic['frame_dic'])
        #else :
        #   self.frame = None # dans ce cas le repere de l'étage et le repere canonique de fom
        self.tif_list = []
        # CGen 19mars15 self.repeated_teeth_list = []
        #self.elementary_tools_obj = ElemToolList()
        #self.elementary_tools_list = self.elementary_tools_obj.elementary_tools_list
        self.elementary_tools_list = []
        self.idx_benen_in_etl_list = []
        self.__tooth_id__ = 0
        ToolstepModel.__instance_counter__ += 1 
        
# --------------------------------------------------------------------------------------------------
    def addTooth(self, tooth, frame, set_id = None):
        """
        In this method, frame must be a frame created in self.foref.
        If set_id == None : tooth is alone.
        Else : tooth belongs to a set of teeth identified by set_id. The user is guarant of the coherence
        of the sets of teeth in the toolstep.   
        """
        tif = Tooth.ToothInFrame(tooth = tooth, frame = frame, tooth_id= self.__tooth_id__)
        self.tif_list.append(tif)
        self.foref.computeRotMatAndTransVect(frame.name)
        idx_in_elt_begin = len(self.elementary_tools_list)
        
        for partie in tooth.elementary_tools_list:
            dicPartie = {}
            dicPartie["tooth_id"] = self.__tooth_id__
            dicPartie["set_id"] = set_id
            dicPartie["toolstep_id"] = self.name
            dicPartie["pnt_cut_edge"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_cut_edge"])# frame.givePointsInFatherFrame( partie["pnt_cut_edge"])
            dicPartie["pnt_in_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, [partie["pnt_in_cut_face"]])[0]
            dicPartie["h_cut_max"] = partie["h_cut_max"]
            dicPartie["node_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_cut_face"])
            dicPartie["tri_cut_face"] = partie["tri_cut_face"]
            # On ajoute le volume en dépouille, et les points de la face en dépouille :
            dicPartie["node_clearance_bnd"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_clearance_bnd"])
            dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
            dicPartie["pnt_clearance_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_clearance_face"])
            dicPartie["law_names"] = partie["law_names"]
            self.elementary_tools_list.append(dicPartie)
        idx_in_etl_end = len(self.elementary_tools_list)-1
        self.idx_benen_in_etl_list.append([idx_in_elt_begin, idx_in_etl_end])
        # CGen 19mars15 self.repeated_teeth_list.append(0)
        self.__tooth_id__+=1
        return self.__tooth_id__ - 1
# --------------------------------------------------------------------------------------------------
    def compute_out_blocs (self):
        self.elem_tool_cut_list = []
        self.elem_tool_clearance_list = []
        for elem_tool in self.elementary_tools_list:
            elem_tool_cut = {}
            elem_tool_clear = {}
            ## cutting face :

            elem_tool_cut['type']            = 'cute'
            elem_tool_cut['node']            = elem_tool['node_cut_face'] # noeud
            elem_tool_cut['tri']             = elem_tool['tri_cut_face'] # tri
            elem_tool_cut['pnt']             = elem_tool['pnt_cut_edge'] + [elem_tool['pnt_in_cut_face'],]  # : 3 point , les deux point de l'arrete et le point de la face. 
            elem_tool_cut['h_cut_max']       = elem_tool['h_cut_max']
            elem_tool_cut['law_names']       = elem_tool['law_names']# : liste nom lois de coupe, 1 par bloc dexel
            elem_tool_cut['tooth_id']        = elem_tool['tooth_id']
            elem_tool_cut['set_id']          = elem_tool['set_id']
            #elem_tool_cut['step_id']         = elem_tool['toolstep_id']
            #elem_tool_cut['rep_in_spindle']  = elem_tool['']# optionel
            #elem_tool_cut['id_node_dyn']     = elem_tool['']# optionel
            #elem_tool_cut['nb_rep']          = elem_tool['']# optionel
            self.elem_tool_cut_list.append(elem_tool_cut)
            
            ## clear face
            
            elem_tool_clear['type']           = 'clear'
            elem_tool_clear['node']           = elem_tool['node_clearance_bnd']# noeud
            elem_tool_clear['tri']            = elem_tool['tri_clearance_bnd']# tri
            elem_tool_clear['pnt']            = [elem_tool['pnt_clearance_face'][i] for i in  [2,1,0]] #: 3 point , p1 point dans la face de talonnage, p1p2 dir U, p1p3 dir v, avec U^V normal sortante
            elem_tool_clear['law_names']      = elem_tool['law_names']# : liste nom lois de talonnage, 1 par bloc dexel
            elem_tool_clear['tooth_id']       = elem_tool['tooth_id']
            elem_tool_clear['set_id']         = elem_tool['set_id']
            #elem_tool_clear['step_id']        = elem_tool['toolstep_id']
            #elem_tool_clear['rep_in_spindle'] = elem_tool[]# optionel
            #elem_tool_clear['id_node_dyn']    = elem_tool[]# optionel
            #elem_tool_clear['nb_rep']         = elem_tool[]# optionel
            self.elem_tool_clearance_list.append(elem_tool_clear)
 
# --------------------------------------------------------------------------------------------------
    def draw(self, bloc_type = CUTFACE_BLOC):
        self.compute_out_blocs()
            
        if bloc_type == CUTFACE_BLOC:
            bloc_util.view_bloc(self.elem_tool_cut_list, 'tool.lf')
        elif bloc_type == CLEARANCE_BLOC :
            bloc_util.view_bloc(self.elem_tool_clear_list, 'tool.lf')

        

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
