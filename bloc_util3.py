
import sys
import random

sys.path.append('/Users/gengembre/nessy2/mesh/util_mesh')

import v3d
import Mesh_IO

def view_bloc(Bloc,v3d_lf_name='bloc.lf'):
    
    
    lf_file=open(v3d_lf_name,'w')

    I=0
    for bloc in Bloc:
        
        if bloc['type'] == 'cut':
            node_cut_face=bloc['node']
            tri_cut_face=bloc['tri']
            pnt_cut_edge=bloc['pnt'][0:2]
            pnt_in_cut_face=bloc['pnt'][2]
        
        if bloc['type'] == 'clear':
            node_clearance_bnd = bloc['node']
            tri_clearance_bnd  = bloc['tri']
            pnt_clearance_face = bloc['pnt']

        file_name=Mesh_IO.OUT_PNT_V3D(pnt_in_cut_face,(1,0,0),10,'pnt_in_cut_face_'+str(I))
        lf_file.write(file_name+'\n')

        file_name=Mesh_IO.OUT_SEG_V3D([[item for sl in pnt_cut_edge  for item in sl],[]],(0,0,1),4,1,'pnt_cut_edge_'+str(I),1)
        lf_file.write(file_name+'\n')

        color=(random.random(),random.random(),random.random(),0.5) #0.5)
        file_name=Mesh_IO.OUT_TRI_V3D([[item for sl in node_cut_face for item in sl],\
                                       [item for sl in tri_cut_face for item in sl]],\
                                       (color,(1,1,0)),'node_tri_cut_face_'+str(I),False)
        lf_file.write(file_name+'\n')
        
        if bloc['type'] == 'clear':
            #file_name=Mesh_IO.OUT_PNT_V3D(pnt_clearance_face,(0,0,1),10,'pnt_clearance_face_'+str(I))
            #lf_file.write(file_name+'\n')
            
            color=(random.random(),random.random(),random.random(),1.) #0.5)
            file_name=Mesh_IO.OUT_TRI_V3D([[item for sl in node_clearance_bnd for item in sl],\
                                           [item for sl in tri_clearance_bnd for item in sl]],\
                                           (color,(1,1,0)),'node_tri_clearance_bnd_'+str(I),False)
            lf_file.write(file_name+'\n')
            
            zz= 0
            for node in pnt_clearance_face:
                file_name=Mesh_IO.OUT_PNT_V3D(node,(0,1,0),10,'pnt_clearance_face_%d_'%(zz,)+str(I))
                zz+=1
                lf_file.write(file_name+'\n')
            
 
            
        I+=1
    
    lf_file.close()

    v3d.show([v3d_lf_name])
