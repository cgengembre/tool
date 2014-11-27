##
##  Tooth : common parameters for every tooth :
##



##
## Data entry - Dictionaries. 
##
dicInsert = {      
            'name'               : 'ma plaquette',
            'cutting_edge_geom'  : [{'seg_length' : 6.0e-3,                      'nb_elementary_tool': 4, 'nb_slices': 4},
                                    {'radius'     : 1.0e-3, 'angle_degrees': 45, 'nb_elementary_tool': 3, 'nb_slices': 4},
                                    {'seg_length' : 5.0e-3,                      'nb_elementary_tool': 5},
                                    {'radius'     : 2.0e-3, 'angle_degrees': 30, 'nb_elementary_tool': 3, 'nb_slices': 3},
                                    {'seg_length' : 8.0e-3,                      'nb_elementary_tool': 4, 'nb_slices': 1},
                                   ],
            'insert_location'    : {'bissectrice_arc_idx': 1, 'dist_from_origin':4.0e-3 },
            'cut_face_thickness' : 3.E-3,
            'cut_face_nb_layers' : 2
            }

dicInsertFrame = {
                 "name"                  : "repere plaquette ",
                 "fatherFrameName"       : "Canonical",
                 "frameType"             : Fom.INSERT_FRAME_AROUND_A_MILL,
                 "axialAngleDegrees"     : 90.,
                 "radius"                : 20.0E-3,
                 "axialPosition"         : 5.0E-3,
                 "rotDegreAutourNormale" : 0.,
                 "rotDegreAutourRadiale" : -20.,
                 "rotDegreAutourAxiale"  : 0.
                 }
    	   
dicFraisePlaquettes = {
                      "name"        : "fraisePlaquette",
                      "insert"      : dicInsert, #dicPlaquetteEquerre,
                      "insertFrame" : dicInsertFrame,
                      "nbDents"     : 8
                      }

## -------------------------------------------------------------------------------------------------
## API for Mill Object.
## -------------------------------------------------------------------------------------------------

# A tooth : a contiguous subset of MyTool.ET_list 
## Teeth list : index ranges for MyTool_ET_list :
                    #/----------teeth list------\
MyMill.Teeth_list = [[range(b,e), range(b,e), ...], #\
                     [range(b,e), range(b,e), ...], # | Storey list
                     ...]                          #/

MyMill.Teeth_dic = {'storey1': { 'tooth1': range(start,stop), 'teethSet' : [range (start, stop),range (start, stop),...], ...},
                    'storey2': ...
                   }
                   
MyMill.addInsert(dicoInsert) # return a tooth_id.
MyMill.addTeethByRotation (nbTeeth = 2, storey_id, tooth_id )



## -------------------------------------------------------------------------------------------------
## Public result when you create a mill :
## -------------------------------------------------------------------------------------------------
## Elementary tool list : a list of dictionaries :
## f = float, i = integer
MyMill.ET_list =[
                {
                 'pnt_cut_edge'   : [ [f, f, f], [f, f, f] ],
                 'pnt_in_cut_face': [f, f, f],
                 'node'           : [ [f, f, f], [f, f, f],...],
                 'tri'            : [ [i,i,i], [i,i,i], ...],                   
                 'h_cut_max'      : f
                 'cut_law_names'  : ['cut law 1 name', 'cut law 2 name', 'cut law 3 name'],
                 'tooth_id'       : i,
                 'storey_id'      : i
                },
                { idem },
                { idem },
                 ...
                ]






fraise_avec_plaquettes  = Tools.WithInsertsMill(dicFraisePlaquettes)
fraise_avec_plaquettes.showyou()


