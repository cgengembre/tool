# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 25 novembre 2014
# 
#
# 
# Les angles sont donnés en degres.
# Il sont convertis en Radian dès le constructeur
#

import bloc_util


class Tooth:
    def __init__(self, dic):
        self.dic = {}
        self.dic["name"]= dic["name"]
        
        self.tooth_id = dic['tooth_id']
        self.storey_id = dic['storey_id']
        
        self.dic['cut_face_thickness'] = dic['cut_face_thickness']
        self.dic['cut_face_nb_layers'] = dic['cut_face_nb_layers']
        
        self.nb_elementary_tools = 0 # Computed or given in subclasses
        self.elementary_tools_list = []
    def showyou(self):
        bloc_util.view_bloc(self.elementary_tools_list)


class ToothForHelicoidalMillType1(Tooth):
    pass
class ToothForHelicoidalMillTore(Tooth):
    pass