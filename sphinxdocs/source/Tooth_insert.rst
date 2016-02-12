################################################################
Tool with insert teeth
################################################################

A frame :math:`(O_P,\overrightarrow{x}_P,\overrightarrow{y}_P,\overrightarrow{z}_P)` is associated to each insert.
The location of the cutting edge is defined inside the plane :math:`(O_P,\overrightarrow{z}_P,\overrightarrow{x}_P)` (that implies that the cutting edge remains inside a plane !).

Cutting egde geometry
*********************************
    
    * the cutting edge of an insert tooth is a continuous chain alternating straight segments and circular arcs (see figure bellow),
    * this chain always begin with a segment,
    * the length a one or more segments may be null, and so may be the radius of the arcs,
    * entities are numbered counter clockwise.

.. image:: fig/PlaquettesPlanes.png
    :align: center
    :width: 13 cm


Cutting edge positioning 
****************************************
    
    * the position of the chain with respect to the axis  :math:`(0_P,\overrightarrow{x}_P)` is defined as being:
    
        * the perpendicular bisector of a segment of the chain, this segment is defined by its index (value associated to the dictionary key ``mediatrice_seg_idx``), the point :math:`P` is then the intersection between :math:`(0_P,\overrightarrow{x}_P)` and this segment,
        * OR the bisector of a the circular arc of the chain, this arc is defined by its index (value associated to the dictionary key ``bissectrice_arc_idx``), the point :math:`P` is then the centre of the circular arc, 
    
    * the position of point :math:`P` inside the plane :math:`(O_P,\overrightarrow{z}_P,\overrightarrow{x}_P)` is defined by:
        
        * :math:`\overrightarrow{O_PP} = L \overrightarrow{x}_P`, where :math:`L` is an algebraic length defined by the value associated to the dictionary key ``dist_from_origin``.

Example of a "complex" insert tooth:

.. image:: fig/ExemplePlqt_3_seg.png
    :align: center
    :width: 13 cm


Script example
*********************************

.. literalinclude:: script/Test_insert_mill.py
    
Obtained tool:

.. image:: fig/Tool_insert.png
    :align: center
    :width: 10 cm

