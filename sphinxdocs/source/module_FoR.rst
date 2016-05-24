################################################################################
Module frame_of_reference
################################################################################
*This section is under construction*

Note :  This module is imported as FoR in the tool_maker script.

This module defines 2 classes : 

    * class FrameOfReference
    * class Frame

The class FrameOfReference defines a frame of reference in which you can create frames to position objects. So you will always create a frame inside a frame of reference instance. To do that, please use the create_frame() method of the FrameOfReference class.

To create a new frame of reference (instance of the FrameOfReference class) you can write : 

::

    my_foref = frame_of_reference.FrameOfReference(name = 'a name')

*Note : when you create a tool or a toolstep, a new frame of reference is automaticaly created (field ``foref``). So every toolstep and every tool has his own frame of reference*

Every frame of reference has its canonical frame. In addition, you can create inside it other frames. 

Every frame is identified by a ``name`` (see below). The ``name`` of the canonical frame is : ``"Canonical"``.

To create a new frame inside a frame of reference, you must use its ``create_frame()`` method with the following named parameters (**CGen** very importtant): 

    * ``name`` : string. The name of the frame. It must be uniq in the frame of reference.
    * ``father_frame_name`` : string. The name of the frame in which you define the new frame. The frame whose name is father_frame_name must exit.
    * ``frame_type``: integer defined in the module frame_of_reference. The value of this parameter determine the way to define the positioning of the new frame with respect to the father frame.
    
    So, next parameters depends on  the value of frame_type :
        
        * If ``frame_type`` is ``frame_of_reference.FRAME_CYLINDRICAL_NRA``, the position of the new frame is defined by :
        
            * ``origin`` : translation of the origin of the father frame expressed by 3 cylindrical coordinates given as a python list [:math:`r`, :math:`\alpha`, :math:`z`] 
            * ``nra`` : orientation of the son basis defined by 3 successive rotations given as a list [rotation around :math:`\overrightarrow{e}_\theta\ `, rotation around :math:`\overrightarrow{e}_r\ `, rotation around :math:`\overrightarrow{z}_F`] expressed in degrees.
            
            On the figure below is depicted an exemple of the positioning of a Son frame  :math:`R_S=(O_S,\overrightarrow{x}_S,\overrightarrow{y}_S,\overrightarrow{z}_S)` with respect to a Father frame :math:`R_F=(O_F,\overrightarrow{x}_F,\overrightarrow{y}_F,\overrightarrow{z}_F)`.
            
            .. image:: fig/FoR_positioning.png
                :align: center
                :width: 13 cm
            
        * If ``frame_type`` is ``frame_of_reference.FRAME_CYLINDRICAL_V1V12``, the position of the new frame is defined by :

            * ``origin`` : translation of the origin of the father frame expressed by 3 cylindrical coordinates given as a python list [:math:`r`, :math:`\alpha`, :math:`z`]
            * ``vector1`` and ``vector12`` : 2 vectors given as python lists,  expressed in cylindrical coordinates, defining the orientation of the son basis.
        
        * If ``frame_type`` is ``frame_of_reference.FRAME_CARTESIAN_V1V12``, the position of the new frame is defined by
        
            * ``origin`` : translation of the origin of the father frame expressed by 3 cartesian coordinates given as a python list [:math:`x`, :math:`y`, :math:`z`]
            * ``vector1`` and ``vector12`` : 2 vectors given as python lists,  expressed in cartesian coordinates, defining the orientation of the son basis.


    
