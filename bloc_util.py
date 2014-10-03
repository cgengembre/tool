
import sys
import random

sys.path.append('./mesh')

import v3d
import Mesh_IO

def view_bloc(Bloc):
    
    v3d_lf_name='bloc.lf'
    lf_file=open(v3d_lf_name,'w')

    I=0
    for bloc in Bloc:
        
        node=bloc['node']
        tri=bloc['tri']
        pnt_cut_edge=bloc['pnt_cut_edge']
        pnt_in_cut_face=bloc['pnt_in_cut_face']

        file_name=Mesh_IO.OUT_PNT_V3D(pnt_in_cut_face,(1,0,0),10,'pnt_in_cut_face_'+str(I))
        lf_file.write(file_name+'\n')

        file_name=Mesh_IO.OUT_SEG_V3D([[item for sl in pnt_cut_edge  for item in sl],[]],(0,0,1),4,1,'pnt_cut_edge_'+str(I),1)
        lf_file.write(file_name+'\n')

        color=(random.random(),random.random(),random.random(),0.5)
        file_name=Mesh_IO.OUT_TRI_V3D([[item for sl in node for item in sl],\
                                       [item for sl in tri for item in sl]],\
                                       (color,(1,1,0)),'node_tri_'+str(I),False)
        lf_file.write(file_name+'\n')
        
        I+=1
    
    lf_file.close()

    v3d.show(v3d_lf_name)
