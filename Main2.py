# -*- coding: Utf-8 -*-
# Christophe Gengembre - Test de la classe dent en slices
# TODO : Renomer le fichier en TestToothSliced.py ...


from Tool import Tool, Toolstep, Tooth
import FrameOfReference as FoR


from os import chdir



angles = [0,10, 90, 100, 180, 190, 270, 280  ]

outil = Tool.Tool(name = 'sliced_tooth_tool1')

# construction du dico à partir du fichier modelFraise.gtool

# eventuellement : chdir('/Users/gengembre/NessyCGen/tools')

data_file_tool = open ('modelFraise.gtool', 'r')

first_line = data_file_tool.readline()
nb_data_slice = int (first_line)

from_data_dic_list = []
data_keys = ['z','x','y','gamma','L_gamma','alpha1','L1','alpha2','L2']
for i in range (nb_data_slice):
    
    from_data_line = data_file_tool.readline()
    splitted_line = from_data_line.split()
    from_data_dic = {}
    i = 0
    for cle in data_keys:
        from_data_dic [cle] = float(splitted_line[i])
        i+=1
    from_data_dic_list.append(from_data_dic)
    

print 'nombre de slices dans donnees : ', nb_data_slice

"""
'cut_face_thickness' : 1.2E-3
        'cut_face_nb_layers' : 1
        'nb_slices_per_elt': 1
        --> Clés propres à ToothForMonoblocMillType3
        'nb_elementary_tools' : 50
        'cutting_edge_geom' : [{'z': 2.0E-2, 'x': 3.0E-2 , 'y': 1.0E-2 , 'gamma':60 ,'L_gamma': 1.3E-2,'alpha1': 10 ,'L1':1.E-2 ,'alpha2': 30,'L2':0.7E-2 },
                               {'z': 4.0E-2, 'x': 3.4E-2 , 'y': 1.4E-2 , 'gamma':60 ,'L_gamma': 1.3E-2,'alpha1': 10 ,'L1':1.E-2 ,'alpha2': 30,'L2':0.7E-2 },
                               ...
                              ]
"""
dent = Tooth.ToothSliced(name = 'dent en slices', 
                         cut_face_thickness= 1.2E-3, 
                         cut_face_nb_layers = 1, 
                         clearance_face1_nb_layers = 1,
                         clearance_face2_nb_layers = 1,
                         nb_slices_per_elt = 5,
                         nb_elementary_tools = 4,
                         cutting_edge_geom = from_data_dic_list)

dent.draw()