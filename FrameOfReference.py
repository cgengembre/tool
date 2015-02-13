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

INSERT_FRAME_FOR_A_TURNERY_MACHIN = 1
INSERT_FRAME_AROUND_A_MILL = 2
# ==================================================================================================
class Frame:
# --------------------------------------------------------------------------------------------------
    def __init__(self, **dic):
        """
    	Structures possibles pour dic :
        --> clés communes à tous les types de reperes :
           "name"            : "nom du repere"
    	   "fatherFrameName" : "nom du repere pere"
    	   "frameType"       : <Id type frame>
        --> clés suivantes en fonction de dic["FrameType"]
    	A/ "frameType"   :
    	   ---------------
    	   "Origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "Vector1"     : [x1, y1, z1] # dans le fatherFrame
    	   "Vector12"    : [x12,y12,z12]# dans le fatherFrame
    	
    	B/ "frameType"   :
    	   ---------------
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "eulerAngles" : [Psi, Teta, Phi]
        
        C/ "frameType"   : INSERT_FRAME_FOR_A_TURNERY_MACHIN
           ---------------
    	   "origin"      : [xO, yO, zO] # dans le fatherFrame
    	   "rotAngles"   : [rotYfather, rotXfather, rotZfather]
    	   example : position plaquette de tour 
    	
    	D/ "frameType"          : INSERT_FRAME_AROUND_A_MILL
    	   -------------
    	   "axialAngleDegrees"  : alpha
    	   "radius"             : r
    	   "axialPosition"      : z
    	   "rotDegreAutourNormale" : rotYp
    	   "rotDegreAutourRadiale" : rotXp
    	   "rotDegreAutourAxiale"  : rotZp
    	   Example : position plaquettes de fraise
    	   
       	Le but du constructeur est de générer le vecteur translation et la matrice de
        rotation pour faire le changement de repère toujours de la meme manière
        """
        self.name             = dic["name"]
        self.fatherFrameName = dic["fatherFrameName"]
        self.frameType        = dic["frameType"]
        self.__computeRotationMatAndTanslationVect__(**dic)
        #self.name
        #self.FrameOfReference
        #self.FatherFrameName
        #self.rotMatrix
        #self.origin
# --------------------------------------------------------------------------------------------------
    def __computeRotationMatAndTanslationVect__(self,**dic):
        """
        Compute the matrix self.MatSelfToFather and the vector self.VectSelfToFather.
        Let P be a point expressed in self,
        [ self.npMatSelfToFather ].P + self.npVectSelfToFather expresses P in fatherFrame    
        """
        if dic["frameType"] == INSERT_FRAME_AROUND_A_MILL:
            alpha    = m.radians(dic["axialAngleDegrees"])
            radius   = dic["radius"]
            axialPos = dic["axialPosition"]
            rotXp    = m.radians(dic["rotDegreAutourRadiale"])
            rotYp    = m.radians(dic["rotDegreAutourNormale"])
            rotZp    = m.radians(dic["rotDegreAutourAxiale"])
            
            npMrotXp   = npRotAroundOxAxisMatrix (rotXp)
            npMrotYp   = npRotAroundOyAxisMatrix (rotYp)
            npMrotZp   = npRotAroundOzAxisMatrix (rotZp)
            npMrotAlpha= npRotAroundOzAxisMatrix (alpha)
            
            npMatSelfToFather = np.dot(npMrotXp,npMrotYp)
            npMatSelfToFather = np.dot(npMrotZp,npMatSelfToFather)
            npMatSelfToFather = np.dot(npMrotAlpha, npMatSelfToFather)
            self.npMatSelfToFather = npMatSelfToFather
            self.npVectSelfToFather = np.array([radius*m.cos(alpha), radius*m.sin(alpha), axialPos])
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
    def __init__(self, **dic):
        self.name = dic["name"]
        self.dic_frames = {"Canonical": None}
# --------------------------------------------------------------------------------------------------
    def create_frame(self, **dic):
        # Verifier que le père du repère ajouté existe bien dans le réferentiel
        # Ajouter le repère au dico des repères. Les clés sont les noms des repères
        if self.dic_frames.has_key(dic['fatherFrameName']):
            ## creer le frame :
            if self.dic_frames.has_key(dic['name']):
                # print self.dic_frames
                raise FrameError('Un frame de ce nom existe déjà')
            self.dic_frames[dic['name']] = Frame(**dic)
            self.dic_frames[dic['name']].fom = self
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
        name = self.dic_frames[name].fatherFrameName
        while name != 'Canonical':
            M = np.dot(self.dic_frames[name].npMatSelfToFather,M)
            T = np.dot(self.dic_frames[name].npMatSelfToFather,T) + self.dic_frames[name].npVectSelfToFather
            name = self.dic_frames[name].fatherFrameName
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
        if self.dic_frames[frameName].fatherFrameName == "Canonical":
            return _points_
        else:
            return self.givePointsInCanonicalFrameR(self.dic_frames[frameName].fatherFrameName ,_points_)
# --------------------------------------------------------------------------------------------------
# ==================================================================================================