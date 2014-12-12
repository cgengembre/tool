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


class ToothModel:
    """
    Classe abstraite, mère de toutes les dents. Attentions aux dents de la mer !
    """
    def __init__(self, dic):
        self.dic = {}
        self.dic["name"]= dic["name"]
        
        self.tooth_id = dic['tooth_id']
        self.storey_id = dic['storey_id']
        
        self.dic['cut_face_thickness'] = dic['cut_face_thickness']
        self.dic['cut_face_nb_layers'] = dic['cut_face_nb_layers']
        
        
        self.nb_elementary_tools = 0 # Computed or given in subclasses
        self.elementary_tools_list = []    
    
    def torsion_transformation(self):
        """
        Attention : Pour appeler cette méthode, les attributs 
        self.radius, self.height, et self.helix_angle ou self.torsion_angle doivent exister. 
        """
        if hasattr(self, 'helix_angle'):
            self.torsion_angle = self.height*math.tan(self.helix_angle)/self.radius
        ## Transformation des points de self.elementary_tools_list.
        for et in self.elementary_tools_list:
            # transformation des nodes
            for node in et['node']:
                beta = node[2]*self.torsion_angle/self.height
                radius = node[0]
                node[0] = radius*math.cos(beta)
                node[1] = radius*math.sin(beta)
            # transformation de l'arrête :
            for pnt in et['pnt_cut_edge']:
                beta = pnt[2]*self.torsion_angle/self.height
                radius = pnt[0]
                pnt[0] = radius*math.cos(beta)
                pnt[1] = radius*math.sin(beta)
            # Transformation du point sur la cut_face :
            beta = et['pnt_in_cut_face'][2]*self.torsion_angle/self.height
            radius = et['pnt_in_cut_face'][0]
            et['pnt_in_cut_face'][0] = radius*math.cos(beta)
            et['pnt_in_cut_face'][1] = radius*math.sin(beta)

    def showyou(self):
        bloc_util.view_bloc(self.elementary_tools_list)


class ToothForHelicoidalMillType1(ToothModel):
    pass
class ToothForHelicoidalMillTore(ToothModel):
    pass