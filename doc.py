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
                 "frameType"             : Fom.FRAME_CYLINDRIC_NRA,
                 "axialAngleDegrees"     : 90.,
                 "radius"                : 20.0E-3,
                 "axialPosition"         : 5.0E-3,
                 "rotDegreAutourNormale" : 0.,
                 "rotDegreAutourRadiale" : -20.,
                 "rotDegreAutourAxiale"  : 0.
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
                   



## -------------------------------------------------------------------------------------------------
## Public result when you create a tool :
## -------------------------------------------------------------------------------------------------
## Elementary tool list : a list of dictionaries :
## f = float, i = integer
MyMill.elementary_tools_list =[
                {
                 'pnt_cut_edge'   : [ [f, f, f], [f, f, f] ],
                 'pnt_in_cut_face': [f, f, f],
                 'node_cut_face'  : [ [f, f, f], [f, f, f],...],
                 'tri_cut_face'   : [ [i,i,i], [i,i,i], ...],                   
                 
                 'pnt_clearance_face' : [ [f, f, f], [f, f, f], [f, f, f] ],
                 'node_clearance_bnd' :[ [f, f, f], [f, f, f], ... ],
                 'tri_clearance_bnd'  : [ [i,i,i], [i,i,i], ...],
                 
                 'h_cut_max'      : f
                 'cut_law_names'  : ['cut law 1 name', 'cut law 2 name', 'cut law 3 name'],
                 'tooth_id'       : i,
                 'toolstep_id'      : 'bla'
                 
                },
                { idem },
                { idem },
                 ...
                ]
MyMill.toolstep_dic = {'base_toolstep' : a_toolstep_in_frame, ... }
                a_toolstep_in_frame.name =  'base_toolstep'
                a_toolstep_in_frame.toolstep =  <ToolstepModel>
                a_toolstep_in_frame.toolstep =  <Frame>
MyMill.benen_in_etl_dic = {'base_toolstep' : [idx_in_etl_begin, idx_in_etl_end], ...}

MyMill.foref = <FrameOfReference>


def addToolstep(self, name, toolstep, frame )
def addTooth(self, tooth, frame, tsif_name ='base_toolstep' )
def draw(self)
def write(self, file_name = None)
# -------------------------------------------------------------------------------------------------
# ToolstepModel
# -------------------------------------------------------------------------------------------------
MyToolstepModel.foref = FoR.FrameOfReference()
MyToolstepModel.elementary_tools_list = [{elmt_dic}, {elmt_dic}, ...]
MyToolstepModel.idx_benen_in_etl_list = [[idx_in_etl_begin,idx_in_etl_end], ...]
MyToolstepModel.name

def addTooth(self, tooth, frame):
def draw(self):
# -------------------------------------------------------------------------------------------------
# ToolstepInFrame
# -------------------------------------------------------------------------------------------------
MyToolstepInFrame.toolstep
MyToolstepInFrame.frame
MyToolstepInFrame.name

# ==================================================================================================
class ToothModel:
# ==================================================================================================
def torsion_transformation(self)
def give_mesh_rect_patch(self, tri, dim1, dim2, offset=0)
def give_mesh_rect_peak_patch(self, tri, dim1, dim2, offset=0)









