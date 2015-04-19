
import sys
import random

sys.path.append('/Users/gengembre/nessy2/mesh/util_mesh')

import v3d
import Mesh_IO

def view_bloc(Bloc,v3d_lf_name='bloc.lf'):
    
    
    lf_file=open(v3d_lf_name,'w')

    I=0
    for bloc in Bloc:
        
        node=bloc['node']
        tri=bloc['tri']
        pnt=bloc['pnt']
        
        if bloc['type'] == 'clear' :
            
            zz = 0
            for p in pnt:
                file_name=Mesh_IO.OUT_PNT_V3D(p,(0,1,0),10,'pnt_clearance_face_'+str(zz)+'_'+str(I))
                zz+=1
                lf_file.write(file_name+'\n')
            color=(random.random(),random.random(),random.random(),0.5) #0.5)
            file_name=Mesh_IO.OUT_TRI_V3D([[item for sl in node for item in sl],\
                                           [item for sl in tri for item in sl]],\
                                           (color,(1,1,0)),'node_tri_clear'+str(I),False)
            lf_file.write(file_name+'\n')
       
        elif bloc['type'] == 'cut' :
            pass
            file_name=Mesh_IO.OUT_SEG_V3D([[item for sl in pnt[0:1]  for item in sl],[]],(0,0,1),4,1,'pnt_'+str(I),1)
            lf_file.write(file_name+'\n')
            
            file_name=Mesh_IO.OUT_PNT_V3D(node,(0,1,0),10,'pnt_cut_face_'+str(I))
            lf_file.write(file_name+'\n')


            color=(random.random(),random.random(),random.random(),0.5) #0.5)
            file_name=Mesh_IO.OUT_TRI_V3D([[item for sl in node for item in sl],\
                                           [item for sl in tri for item in sl]],\
                                           (color,(1,1,0)),'node_tri_cut'+str(I),False)
            lf_file.write(file_name+'\n')
        
        
        
            
        I+=1
    
    lf_file.close()

    v3d.show([v3d_lf_name])
