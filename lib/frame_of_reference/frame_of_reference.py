# -*- coding: Utf-8 -*-

# This file is part of the python package 'tool', itself part of nessy2m.
# 
# Copyright (C) 2010-2016
# Christophe GENGEMBRE (christophe.gengembre@ensam.eu)
# Philippe LORONG (philippe.lorong@ensam.eu)
# Amran/Lounes ILLOUL (amran.illoul@ensam.eu)
# Arts et Metiers ParisTech, Paris, France
#
# nessy2m is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nessy2m is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with nessy2m.  If not, see <http://www.gnu.org/licenses/>.
#
# Please report bugs of this package to christophe.gengembre@ensam.eu 

# --------------------------------------------------------------------------------------------------
# Fr            | En
# référenciel   | frame of reference
# repère        | frame
# Plaquuette    | insert

import math  as m
import numpy as np

class FrameError(Exception):
    pass


# --------------------------------------------------------------------------------------------------
def npRotAroundOxAxisMatrix(angle):
    sin_angle = m.sin(angle)
    cos_angle = m.cos(angle)
    return np.array([1.,0.,0., 0, cos_angle, - sin_angle, 0., sin_angle, cos_angle]).reshape(3,3)
# --------------------------------------------------------------------------------------------------
def npRotAroundOyAxisMatrix(angle):
    sin_angle = m.sin(angle)
    cos_angle = m.cos(angle)
    return np.array([cos_angle, 0., sin_angle, 0.,1.,0., - sin_angle, 0., cos_angle]).reshape(3,3)
# --------------------------------------------------------------------------------------------------
def npRotAroundOzAxisMatrix(angle):
    sin_angle = m.sin(angle)
    cos_angle = m.cos(angle)
    return np.array([cos_angle, - sin_angle, 0., sin_angle, cos_angle,0.,0., 0, 1. ]).reshape(3,3)
# --------------------------------------------------------------------------------------------------
def vector_norm (vect):
    """ return the euclidian norm of vect
    """
    return m.sqrt (reduce (lambda a, b : a+b, [x**2 for x in vect]))
# --------------------------------------------------------------------------------------------------
def normalize (vect):
    """ return a new vector that is collinear to vect, and whose norm is 1. 
    """
    the_norm = vector_norm(vect)
    return map(lambda a: a/the_norm, vect)
# --------------------------------------------------------------------------------------------------
# -- Integers used to define frame types --
FRAME_CARTESIAN_V1V12   = 0   # DONE
FRAME_CYLINDRICAL_V1V12 = 1   # DONE
FRAME_SPHERICAL_V1V12   = 2   
FRAME_CYLINDRICAL_NRA   = 3   # DONE
FRAME_CYLINDRICAL_EULER = 4
# ----------------------------------------
EPSILON = .1E-7
# ==================================================================================================
class Frame:
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
        """ Frame class constructor
        --> Common keys needed for every way to define a frame :
           
           "name"              : "name for the frame"
    	   "father_frame_name" : "name of the father frame"
    	   "frame_type"        : <type frame id>
    	   
        --> Other needed keys depend on the value of dic["frame_type"] :

    	---------------
    	if dic["frame_type"] == FRAME_CARTESIAN_V1V12 then needed keys are :
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "vector1"     : [x1, y1, z1] # dans le fatherFrame
    	   "vector12"    : [x12,y12,z12]# dans le fatherFrame
    	---------------
    	if dic["frame_type"] == FRAME_CYLINDRICAL_V1V12 then needed keys are :    	   
    	   "origin"      : [radius, teta, zO] # dans le fatherFrame
    	   "vector1"     : [u1_r, u1_teta, u1_z] # dans le fatherFrame
    	   "vector12"    : [u12_r, u12_teta, u12_z]# dans le fatherFrame
    	---------------
    	if dic["frame_type"] == FRAME_CYLINDRICAL_NRA then needed keys are :    	
    	   "origin"      : [radius, teta_degrees, zO] # dans le fatherFrame
    	   "nra"         : [normal_angle_degrees, radial_angle_degrees, axial_angle_degrees]
    	---------------
    	[TODO] if dic["frame_type"] == FRAME_SPHERICAL_V1V12 then needed keys are :    	
           "origin"      : [radius, teta, phi] # dans le fatherFrame
    	   "vector1"     : [u1_r, u1_teta, u1_phi] # dans le fatherFrame
    	   "vector12"    : [u12_r, u12_teta, u12_phi]# dans le fatherFrame
    	---------------
    	[TODO] if dic["frame_type"] == FRAME_CARTESIAN_EULER then needed keys are :        
    	   "origin"       : [xO, yO, zO] # dans le fatherFrame
    	   "euler_angles" : [Psi, Teta, Phi]
    	---------------
    	[TODO] if dic["frame_type"] == FRAME_CARTESIAN_NRA then needed keys are :        
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "nra"         : [normal_angle_degrees, radial_angle_degrees, axial_angle_degrees]
    	   example : position plaquette de tour 
    	---------------
        
        The constructor compute translation vector and rotation matrix expressed in
       	cartesian coordinates so that the change of reference is always done in the same manner.
        """
        self.name              = dic["name"]
        self.father_frame_name = dic["father_frame_name"]
        self.frame_type        = dic["frame_type"]
        self.__computeRotationMatAndTanslationVect__(**dic)
        #self.name
        #self.FrameOfReference
        #self.father_frame_name
        #self.rotMatrix
        #self.origin
# --------------------------------------------------------------------------------------------------
    def __computeRotationMatAndTanslationVect__(self,**dic):
        """
        Compute the matrix self.MatSelfToFather and the vector self.VectSelfToFather.
        Let P be a point expressed in self,
        [ self.npMatSelfToFather ].P + self.npVectSelfToFather expresses P in fatherFrame    
        """
        if dic["frame_type"] == FRAME_CYLINDRICAL_NRA:
            # waited dic :  
            # "origin"        : [radius, teta_degrees, zO] # dans le fatherFrame
            # "nra" : [normal_angle_degrees, radial_angle_degrees, axial_angle_degrees]

            radius   = dic["origin"][0]
            alpha    = m.radians(dic["origin"][1])
            axialPos = dic["origin"][2]
            rotYp    = m.radians(dic["nra"][0])
            rotXp    = m.radians(dic["nra"][1])
            rotZp    = m.radians(dic["nra"][2])
            
            npMrotXp   = npRotAroundOxAxisMatrix (rotXp) # e_radial (Radial)
            npMrotYp   = npRotAroundOyAxisMatrix (rotYp) # e_teta   (Normal)
            npMrotZp   = npRotAroundOzAxisMatrix (rotZp) # e_z      (Axial)
            npMrotAlpha= npRotAroundOzAxisMatrix (alpha)
            
            npMatSelfToFather = np.dot(npMrotXp,npMrotYp)
            npMatSelfToFather = np.dot(npMrotZp,npMatSelfToFather)
            npMatSelfToFather = np.dot(npMrotAlpha, npMatSelfToFather)
            self.npMatSelfToFather = npMatSelfToFather
            self.npVectSelfToFather = np.array([radius*m.cos(alpha), radius*m.sin(alpha), axialPos])
        
        elif dic['frame_type'] == FRAME_CARTESIAN_V1V12:
            ## waited dic :  
            # "origin"      : [xO, yO, zO] # dans le fatherFrame
    	    # "vector1"     : [x1, y1, z1] # dans le fatherFrame
    	    # "vector12"    : [x12,y12,z12]# dans le fatherFrame
    	    self.npVectSelfToFather = np.array(dic['origin'])
    	    # Compute the matrix : 
    	    # 1: normalize vector1 and vector12 
    	    # produit scalaire : np.dot(a,b). produit vectoriel : np.cross(a,b)
    	    # Norme d'un vecteur : math.sqrt (reduce (lambda a, b : a+b, [x**2 for x in vect]))
    	    u1 = normalize(dic['vector1'])
    	    u12 = normalize(dic['vector12'])
    	    
    	    np_u1, np_u12 = np.array(u1), np.array(u12) 
    	    if np.linalg.norm(np_u1 - np_u12) < EPSILON*np.linalg.norm(self.npVectSelfToFather):
    	        raise FrameError('u1 and u12 vectors seems to be colinear !')
    	    
    	    w = np.cross(np_u1, np_u12)
    	    u = np.array(u1)
    	    v = np.cross (w, u)
    	    self.npMatSelfToFather = np.concatenate ((u,v,w)).reshape(3,3).transpose()
    	    
    	    
    	elif dic['frame_type'] == FRAME_CYLINDRICAL_V1V12:
            ## waited dic :  
            # "origin"      : [radius, teta, zO] # dans le fatherFrame
    	    # "vector1"     : [u1_r, u1_teta, u1_z] # dans le fatherFrame
    	    # "vector12"    : [u12_r, u12_teta, u12_z]# dans le fatherFrame
    	    # 1.: Compute translation vector:
    	    radius = dic['origin'][0]
    	    teta = m.radians(dic['origin'][1])
    	    zO = dic['origin'][2]
    	    self.npVectSelfToFather = np.array([radius*m.cos(teta), radius*m.sin(teta), zO])
    	    # 2.: Compute rotation matrix:
    	    u1_r, u1_teta, u1_z = dic['vector1'][0],dic['vector1'][1],dic['vector1'][2]
    	    u1 = normalize([u1_r*m.cos(teta)-u1_teta*m.sin(teta), u1_r*m.sin(teta)+u1_teta*m.cos(teta), u1_z])
    	    u12_r, u12_teta, u12_z = dic['vector12'][0],dic['vector12'][1],dic['vector12'][2]
    	    u12 = normalize([u12_r*m.cos(teta)-u12_teta*m.sin(teta), u12_r*m.sin(teta)+u12_teta*m.cos(teta), u12_z])
    	    
    	    np_u1, np_u12 = np.array(u1), np.array(u12) 
    	    if np.linalg.norm(np_u1 - np_u12) < EPSILON*np.linalg.norm(self.npVectSelfToFather):
    	        raise FrameError('u1 and u12 vectors seems to be colinear !')
    	    
    	    w = np.cross(np_u1, np_u12)
    	    u = np.array(u1)
    	    v = np.cross (w, u)
    	    self.npMatSelfToFather = np.concatenate ((u,v,w)).reshape(3,3).transpose()
    	    

    	elif dic['frame_type'] == FRAME_SPHERICAL_V1V12:
            ## waited dic :  
            # "origin"      : [radius, teta, phi] # dans le fatherFrame
    	    # "vector1"     : [u1_r, u1_teta, u1_phi] # dans le fatherFrame
    	    # "vector12"    : [u12_r, u12_teta, u12_phi]# dans le fatherFrame
            raise FrameError("frame_type FRAME_SPHERICAL_V1V12 not yet implemented")
            
        else :
            raise FrameError("frame_type not yet implemented")
# --------------------------------------------------------------------------------------------------
    def givePointsInFatherFrame(self, points):

        pointsInFatherFrame = []
        for p in points:
            npPoint = np.array(p)
            npPoint = np.dot(self.npMatSelfToFather, npPoint)
            npPoint += self.npVectSelfToFather
            pointsInFatherFrame.append(npPoint.tolist())
        return pointsInFatherFrame
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class FrameOfReference:
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    __instance_counter__ = 0

    def __init__(self, **dic):
        if dic.has_key("name"):
            self.name = dic["name"]+'_'+str(FrameOfReference.__instance_counter__)
        else:
            self.name = "FoRef_"+str(FrameOfReference.__instance_counter__)
            
        self.dic_frames = {"Canonical": None}
        FrameOfReference.__instance_counter__ +=1
# --------------------------------------------------------------------------------------------------
    def create_frame(self, **dic):
        # Ensure that the created frame father exists in this frame of reference
        # Add the created frame to the frames dictionary whose keys are frames mames.
        if self.dic_frames.has_key(dic['father_frame_name']):
            ## frame creation :
            if self.dic_frames.has_key(dic['name']):
                # print self.dic_frames
                raise FrameError('Un frame de ce nom existe déjà')
            self.dic_frames[dic['name']] = Frame(**dic)
            self.dic_frames[dic['name']].foref = self
        else: raise FrameError("Pere inexistant")
        return self.dic_frames[dic['name']]
# --------------------------------------------------------------------------------------------------
    def computeRotMatAndTransVect(self, frameName):
        """
        compute self.dic_frames[frameName].npMatRot2Canonical (say M) and 
                self.dic_frames[frameName].npVectTrans2Canonical (say T).
        Let P be a point expressed in the frame named frameName, 
        M.P + T expresses P in Canonical frame.
        """
        name = frameName
        M = self.dic_frames[name].npMatSelfToFather
        T = self.dic_frames[name].npVectSelfToFather
        name = self.dic_frames[name].father_frame_name
        while name != 'Canonical':
            M = np.dot(self.dic_frames[name].npMatSelfToFather,M)
            T = np.dot(self.dic_frames[name].npMatSelfToFather,T) + self.dic_frames[name].npVectSelfToFather
            name = self.dic_frames[name].father_frame_name
        self.dic_frames[frameName].npMatRot2Canonical = M
        self.dic_frames[frameName].npVectTrans2Canonical = T
# --------------------------------------------------------------------------------------------------
    def givePointsInCanonicalFrame(self, frameName, points):
        if hasattr(self.dic_frames[frameName], 'npMatRot2Canonical'):
            ret_points = []
            for p in points:
                npPoint = np.array(p)
                npPointInCan = np.dot(self.dic_frames[frameName].npMatRot2Canonical,npPoint) + self.dic_frames[frameName].npVectTrans2Canonical
                ret_points.append (npPointInCan.tolist())
            return ret_points
        else:
            return self.givePointsInCanonicalFrameR(frameName, points)
# --------------------------------------------------------------------------------------------------
    def givePointsInCanonicalFrameR(self, frameName, points):
        """
        Recurcive version.
        points are given in the frame whose name is frameName. 
        return points coordinates expressed in Canonical Frame.
        """
        # print '<CGen> givePointsInCanonicalFrame()'
        # print type(self.dic_frames[frameName])
        # print type(points)
        _points_ = Frame.givePointsInFatherFrame(self.dic_frames[frameName], points)
        #_points_ = self.dic_frames[frameName].givePointsInFatherFrame(points)
        if self.dic_frames[frameName].father_frame_name == "Canonical":
            return _points_
        else:
            return self.givePointsInCanonicalFrameR(self.dic_frames[frameName].father_frame_name ,_points_)
# --------------------------------------------------------------------------------------------------
# ==================================================================================================