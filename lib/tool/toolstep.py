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

import os

from frame_of_reference import frame_of_reference as FoR

import tooth
CUTFACE_BLOC = 0
CLEARANCE_BLOC = 1

import sys
import os
my_dir=os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(my_dir,'..','..','..','n2m','lib'))
import tool_util

# ==================================================================================================
class ToolstepModel:
# ==================================================================================================
    __instance_counter__ = 0
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
        """Constructor of ToolstepModel.
        
        Madatory key for dic :
        'name' : The name the user give
        
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
        self.__set_counter__ = 0
        self.__set_id_dic__ = {}
        ToolstepModel.__instance_counter__ += 1 
        
        
# --------------------------------------------------------------------------------------------------
    def addTooth(self, tth, frame, set_id = None):
        """Add the tooth tth to the toolstep self. The position in self is defined by the frame. 
        
        In this method, frame must be a frame created in self.foref.
        If set_id == None : tooth is alone.
        Else : tooth belongs to a set of teeth identified by set_id. The user is guarant of the coherence
        of the sets of teeth in the toolstep.   
        """
        tif = tooth.ToothInFrame(tth = tth, frame = frame, tooth_id= self.__tooth_id__)
        self.tif_list.append(tif)
        self.foref.computeRotMatAndTransVect(frame.name)
        idx_in_elt_begin = len(self.elementary_tools_list)
        # Numerotation des ensembles de dents
        set_idx = 0 
        if set_id :
            if self.__set_id_dic__.has_key(set_id) :
                set_idx = self.__set_id_dic__[set_id]
            else :
                self.__set_id_dic__[set_id] = self.__set_counter__
                set_idx = self.__set_counter__
                self.__set_counter__+=1
        else :
            set_idx = self.__set_counter__
            self.__set_counter__+=1
            
            
            
        for partie in tth.elementary_tools_list:
            dicPartie = {}
            dicPartie["tooth_id"] = self.__tooth_id__
            dicPartie["set_id"] = set_idx
            dicPartie["toolstep_id"] = self.name
            dicPartie["pnt_cut_edge"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_cut_edge"])# frame.givePointsInFatherFrame( partie["pnt_cut_edge"])
            dicPartie["pnt_in_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, [partie["pnt_in_cut_face"]])[0]
            dicPartie["h_cut_max"] = partie["h_cut_max"]
            dicPartie["node_cut_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_cut_face"])
            dicPartie["tri_cut_face"] = partie["tri_cut_face"]
            dicPartie["mcr_rf_cl_name"] = partie["mcr_rf_cl_name"]
            # On ajoute le volume en dépouille, et les points de la face en dépouille :
            if tth.has_clear_face():
                dicPartie["node_clearance_bnd"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["node_clearance_bnd"])
                dicPartie["tri_clearance_bnd"] = partie["tri_clearance_bnd"]
                dicPartie["pnt_clearance_face"] = self.foref.givePointsInCanonicalFrame(frame.name, partie["pnt_clearance_face"])
                dicPartie["mcr_cv_cl_name"] = partie["mcr_cv_cl_name"]
                
            self.elementary_tools_list.append(dicPartie)
        idx_in_etl_end = len(self.elementary_tools_list)-1
        self.idx_benen_in_etl_list.append([idx_in_elt_begin, idx_in_etl_end])
        # CGen 19mars15 self.repeated_teeth_list.append(0)
        self.__tooth_id__+=1
        return self.__tooth_id__ - 1
# --------------------------------------------------------------------------------------------------
    def compute_out_blocs (self):
        self.elem_tool_out_list = []
        elem_tool_id = 0
        for elem_tool in self.elementary_tools_list:
            elem_tool_cut = {}
            elem_tool_clear = {}
            ## cutting face :

            elem_tool_cut['type']            = 'rake_face'
            elem_tool_cut['node']            = elem_tool['node_cut_face'] # noeud
            elem_tool_cut['tri']             = elem_tool['tri_cut_face'] # tri
            elem_tool_cut['pnt']             = elem_tool['pnt_cut_edge'] + [elem_tool['pnt_in_cut_face'],]  # : 3 point , les deux point de l'arrete et le point de la face. 
            elem_tool_cut['h_cut_max']       = elem_tool['h_cut_max']
            elem_tool_cut['mcr_cl_name']       = elem_tool['mcr_rf_cl_name']# : liste nom lois de coupe, 1 par bloc dexel
            elem_tool_cut['tooth_id']        = elem_tool['tooth_id']
            elem_tool_cut['set_id']          = elem_tool['set_id']
            elem_tool_cut['elemtool_id']     =  elem_tool_id

            #elem_tool_cut['step_id']         = elem_tool['toolstep_id']
            #elem_tool_cut['rep_in_spindle']  = elem_tool['']# optionel
            #elem_tool_cut['id_node_dyn']     = elem_tool['']# optionel
            #elem_tool_cut['nb_rep']          = elem_tool['']# optionel
            self.elem_tool_out_list.append(elem_tool_cut)
            
            ## clear face
            if elem_tool.get('mcr_cv_cl_name'):
                elem_tool_clear['type']           = 'clear_vol'
                elem_tool_clear['node']           = elem_tool['node_clearance_bnd']# noeud
                elem_tool_clear['tri']            = elem_tool['tri_clearance_bnd']# tri
                elem_tool_clear['pnt']            = [elem_tool['pnt_clearance_face'][i] for i in  [2,1,0]] #: 3 point , p1 point dans la face de talonnage, p1p2 dir U, p1p3 dir v, avec U^V normal sortante
                elem_tool_clear['mcr_cl_name']      = elem_tool['mcr_cv_cl_name']# : liste nom lois de talonnage, 1 par bloc dexel
                elem_tool_clear['tooth_id']       = elem_tool['tooth_id']
                elem_tool_clear['set_id']         = elem_tool['set_id']
                elem_tool_clear['elemtool_id']      =  elem_tool_id
                
                self.elem_tool_out_list.append(elem_tool_clear)

            #elem_tool_clear['step_id']        = elem_tool['toolstep_id']
            #elem_tool_clear['rep_in_spindle'] = elem_tool[]# optionel
            #elem_tool_clear['id_node_dyn']    = elem_tool[]# optionel
            #elem_tool_clear['nb_rep']         = elem_tool[]# optionel
            #
            # CGen-DONE-oct2015  - var interne no_clearface  self.elem_tool_out_list.append(elem_tool_clear)
            #
            
            elem_tool_id+=1
 
# --------------------------------------------------------------------------------------------------
    def draw(self):
        self.compute_out_blocs()
        out_d = './OUT/d_toolstep'
        if not os.path.isdir(out_d): os.mkdir(out_d)
        
        #tooth.tool_util.draw_bloc(self.elem_tool_out_list, out_d)
	v3d_lf_name=tool_util.draw_bloc(self.elem_tool_out_list, out_d)
    	tool_util.v3d.show([v3d_lf_name],'rack face & clear vol')

        

# ==================================================================================================
class ToolstepInFrame:
# ==================================================================================================
    """Internal class : used to add a toolstep to a tool.

    When you add a toolstep to a tool, a ToolstepInFrame is created and added to the tool.
    """
    def __init__(self, **dic):
        """ToolstepInFrame constructor.
        
        Mandatory keys for dic :
        {
            'name'    : "name for the toolstep"
            'frame'   : a frame to position the toolstep in the tool
            'toolstep': the toolstep
            'id'      : id to identify the toolstep in the tool.  
        }
        """
        self.name = dic['name']
        self.toolstep = dic ['toolstep']
        self.frame = dic ['frame']
        self.tsif_id = dic['id']
