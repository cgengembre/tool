# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 30 sept. 2014
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


FRAME_CARTESIAN_V1V12 = 0
FRAME_CARTESIAN_EULER = 1
FRAME_CARTESIAN_NRA   = 2
FRAME_CYLINDRIC_NRA   = 3 # FRAME_CYLINDRIC_NRA
# ==================================================================================================
class Frame:
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
        """
    	Structures possibles pour dic :
        --> clés communes à tous les types de reperes :
           "name"              : "nom du repere"
    	   "father_frame_name" : "nom du repere pere"
    	   "frame_type"        : <Id type frame>
        --> clés suivantes en fonction de dic["frame_type"]
    	A/ "frame_type"   : FRAME_CARTESIAN_V1V12
    	   ---------------
    	   "Origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "Vector1"     : [x1, y1, z1] # dans le fatherFrame
    	   "Vector12"    : [x12,y12,z12]# dans le fatherFrame
    	
    	B/ "frame_type"  : FRAME_CARTESIAN_EULER
    	   ---------------
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "eulerAngles" : [Psi, Teta, Phi]
        
        C/ "frame_type"  : FRAME_CARTESIAN_NRA # INSERT_FRAME_FOR_A_TURNERY_MACHIN
           ---------------
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "rotAngles"   : [rotYfather, rotXfather, rotZfather]
    	   example : position plaquette de tour 
    	
    	D/ "frame_type"         : FRAME_CYLINDRIC_NRA
    	   -------------
    	   "axial_angle_degrees": alpha
    	   "radius"             : r
    	   "axial_position"     : z
    	   "rot_normal_degrees" : rotYp
    	   "rot_radial_degrees" : rotXp
    	   "rot_axial_degrees"  : rotZp
    	   Example : position plaquettes de fraise
    	   
       	Le but du constructeur est de générer le vecteur translation et la matrice de
        rotation pour faire le changement de repère toujours de la meme manière
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
        if dic["frame_type"] == FRAME_CYLINDRIC_NRA:
            alpha    = m.radians(dic["axial_angle_degrees"])
            radius   = dic["radius"]
            axialPos = dic["axial_position"]
            rotXp    = m.radians(dic["rot_radial_degrees"])
            rotYp    = m.radians(dic["rot_normal_degrees"])
            rotZp    = m.radians(dic["rot_axial_degrees"])
            
            npMrotXp   = npRotAroundOxAxisMatrix (rotXp)
            npMrotYp   = npRotAroundOyAxisMatrix (rotYp)
            npMrotZp   = npRotAroundOzAxisMatrix (rotZp)
            npMrotAlpha= npRotAroundOzAxisMatrix (alpha)
            
            npMatSelfToFather = np.dot(npMrotXp,npMrotYp)
            npMatSelfToFather = np.dot(npMrotZp,npMatSelfToFather)
            npMatSelfToFather = np.dot(npMrotAlpha, npMatSelfToFather)
            self.npMatSelfToFather = npMatSelfToFather
            self.npVectSelfToFather = np.array([radius*m.cos(alpha), radius*m.sin(alpha), axialPos])
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
        # Verifier que le père du repère ajouté existe bien dans le réferentiel
        # Ajouter le repère au dico des repères. Les clés sont les noms des repères
        if self.dic_frames.has_key(dic['father_frame_name']):
            ## creer le frame :
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