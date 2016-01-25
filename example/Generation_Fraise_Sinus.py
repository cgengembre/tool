
import numpy as np

nbParties = 100
nbSection = nbParties + 1

Z_0 = 0.0
Z_D = 5.e-3
n_Z = 5.0
d_Z = Z_D / nbParties

R_0   = 5.0e-3  # Rayon de depart
R_D   = 0.0e-3  # Variation de rayon sur la hauteur
R_mod = 0.0e-3  # Modulation de rayon
R_n   = 1       # Nombre de modulations sur la hauteur
R_e   = 0.0     # Dephasage

d_R = R_D / nbParties

# Angles en radians 
dr    = 2 * np.pi / 180.
T_0   =  0.0       # Angle initial
T_D   =  5.0 * dr  # Variation d'angle sur la hauteur
T_mod =  2.0 * dr  # Modulation d'angle
T_n   =  3         # Nombre de mdoulations sur la hauteur 
T_e   = 0.0        # Dephasage

d_T = T_D / nbParties

w = 2.0 * np.pi / nbParties

f1=open('FraiseSinus.gtooth','w')

f1.write(str(nbSection)+'\n')

for iSec in range(nbSection) :
    
    i_m = iSec
    
    Z_m = Z_0 + i_m * d_Z
    
    R_m = R_0 + i_m * d_R + R_mod * np.sin(i_m*w * R_n + R_e )
    
    T_m = T_0 + i_m * d_T + T_mod * np.sin(i_m*w * T_n + T_e )
    
    x_m = R_m * np.cos(T_m)

    y_m = R_m * np.sin(T_m)
    
    suite = '  0.0  2.e-3  5.0  1.e-3  10. 2.e-3 \n' 
    
    f1.write(str(Z_m)+'  '+str(x_m)+'  '+str(y_m) + suite)
    
f1.close()
    