################################################################################
Module ``FoR``
################################################################################
* This section is under construction *
This module define 2 classes : 

    * class FrameOfReference
    * class Frame

The class FrameOfReference defines a frame of reference in which you can create frames to position objects. So you will always create a frame inside a frame of reference instance. To do that, please use the create_frame() method of the class FrameOfReference.


On the figure below is depicted an exemple of the positioning of a Son frame of reference :math:`R_S=(O_S,\overrightarrow{x}_S,\overrightarrow{y}_S,\overrightarrow{z}_S)` with respect to a Father frame of reference 
:math:`R_F=(O_F,\overrightarrow{x}_F,\overrightarrow{y}_F,\overrightarrow{z}_F)`.

The way used for this positioning is:

    * Positioning of :math:`O_S`: usage of a cylindrical coordinate system, with the 3 coordinates :math:`r`, :math:`\alpha` and :math:`z.`
    * Orientation of the basis :math:`(\overrightarrow{x}_S,\overrightarrow{y}_S,\overrightarrow{z}_S)`: this orientation is defined by 3 successive rotations, 
    
        * *i)* a rotation around :math:`\overrightarrow{e}_\theta\ ` (``rot_normal_degrees``), 
        * *ii)* a rotation around :math:`\overrightarrow{e}_r\ ` (``rot_radial_degrees``), 
        * *iii)* a rotation around :math:`\overrightarrow{z}_F` (``rot_axial_degrees``). 


.. image:: fig/FoR_positioning.png
    :align: center
    :width: 13 cm

Many other ways are possible in order to define the positioning of a frame with respect to an other frame but only the previous way is used for all the given examples.
