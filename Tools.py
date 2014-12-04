# -*- coding: Utf-8 -*-
# Christophe Gengembre
# 8 sept. 2014
# 
#
# 
# Les angles sont donnés en degres.
# Il sont convertis en Radian dès le constructeur
#

import math
import numpy as np

import bloc_util
import FrameOfReference as fom
import Insert

class InconcistentDataError(Exception):
    pass
# ==================================================================================================
class Storey:
# ==================================================================================================
    def __init__(self, **dic):
        """
        structure de dic :
        {
            'name' : "nom de l'etage"
            'frame_dic' :  # dictionnaire en parametre du constructeur de fom.Frame
            
        }
        """
        self.name = dic['name']
        if dic.has_key('dic_frame'):
            self.frame = fom.Frame(**dic['frame_dic'])
        else :
            self.frame = None # dans ce cas le repere de l'étage et le repere canonique de fom
        self.tooth_list = []
        self.tooth_counter = 0
    
    def addTooth(self,**dic):
        """
        structure de dic attendue :
        {
            'tooth_class' : classe de la dent, ex :Insert.Insert
            'tooth_param' : dictionnaire attendu par le constructeur de la classe dic['tooth_class'] 
        }
        """
        tooth = dic['tooth_type'](**dic['tooth_param'])
        self.tooth_list.append(tooth)
        


# ==================================================================================================
class Mill:
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self,  dic):
        """
        clés attendues dans dic :
        nbParties         
        nbTranches        
        nbCouchesFaceCoupe
        nbCouchesLiaison
        nbDents
        """
        #self.name  = dic ["name"]
        self.nbParties          = dic["nbParties"] if dic.has_key("nbParties") else 5
        self.nbTranches         = dic["nbTranches"] if dic.has_key("nbTranches") else 1
        self.nbCouchesFaceCoupe = dic["nbCouchesFaceCoupe"] if dic.has_key("nbCouchesFaceCoupe") else 1
        self.nbCouchesLiaison   = dic["nbCouchesLiaison"] if dic.has_key("nbCouchesLiaison") else 1
        self.idNoeudMaitre      = dic["idNoeudMaitre"] if dic.has_key("idNoeudMaitre") else None
        self.nbDents            = dic["nbDents"] if dic.has_key("nbDents") else 1
        
        self.storey_list = []
        self.elementary_tools_list = []
        
# --------------------------------------------------------------------------------------------------
    def addTooth (self, dico_tooth, dico_frame):
        pass        
# --------------------------------------------------------------------------------------------------        
    def addTeethByRotation(self, nbPartiesModel):
        """
        genere face de coupe et maillage des autres dents par rotations des 
        points des parties et des nodes. 
        creer les dents manquantes 
        """
        listeAngles = []
        if self.nbDents > 1:
            listeAngles = [(i+1)*2 * math.pi /self.nbDents for i in range (self.nbDents-1)]
        tooth_id=0
        for alpha in listeAngles:
            tooth_id+=1
            cosAlpha = math.cos(alpha)
            sinAlpha = math.sin(alpha)
            # A : matrice de rotation.
            Anp = np.array([cosAlpha, -sinAlpha, 0, sinAlpha, cosAlpha, 0, 0,0,1]).reshape((3,3))
            # On parcourt les parties de la face de coupe de la dent 0 (tooth_id = 0)
            for idPartie in range (nbPartiesModel): ## self.nbParties
                
                dicoPartie = {}
                
                dicoPartie["tooth_id"] = tooth_id
               
                dicoPartie["pnt_cut_edge"] = []
                for point in self.partiesEtMaillageFaceDeCoupe[idPartie]["pnt_cut_edge"]:
                    Pnp = np.array(point)
                    nouvPoint = np.dot(Anp, Pnp).tolist()
                    dicoPartie["pnt_cut_edge"].append(nouvPoint)
                
                p3_tooth0 = self.partiesEtMaillageFaceDeCoupe[idPartie]["pnt_in_cut_face"]
                Pnp = np.array(p3_tooth0)
                nouvPoint = np.dot(Anp, Pnp).tolist()
                dicoPartie["pnt_in_cut_face"] = nouvPoint
                
                # Les points du maillage :
                dicoPartie["node"] = []
                for point in self.partiesEtMaillageFaceDeCoupe[idPartie]["node"]: 
                    Pnp = np.array(point)
                    nouvPoint = np.dot(Anp, Pnp).tolist()
                    dicoPartie["node"].append (nouvPoint)
                # Les triangles : on prend les meme que pour la dent 0
                dicoPartie["tri"]= self.partiesEtMaillageFaceDeCoupe[idPartie]["tri"]
                if isinstance (self, MonoblocMill):
                    dicoPartie["h_cut_max"] = 1.2*self.epaisseurFaceCoupe
                else :
                    dicoPartie["h_cut_max"] = self.partiesEtMaillageFaceDeCoupe[0]["h_cut_max"]
                self.partiesEtMaillageFaceDeCoupe.append (dicoPartie)
# --------------------------------------------------------------------------------------------------
    def showyou(self):
        #print self.partiesEtMaillageFaceDeCoupe
        bloc_util.view_bloc(self.partiesEtMaillageFaceDeCoupe)
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class WithInsertsMill (Mill):
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self, dic):
        """
        Fraise à plaquettes de base : composee de self.nbDents plaquettes identiques.
        On définit une plaquette et calcule ses aretes faces de coupe et maillage. 
        Ensuite, on calcule les autres dents par rotation.
        structure de dic attendue : (en plus des cles de la classe de base Mill)
        'insert': dic de la classe Insert
        'frameInsert' : dic de la classe Frame.
        """
        Mill.__init__(self, dic)
        self.millFom = fom.FrameOfReference(dic)
        self.listInserts = []
        self.__toothId__ = 0
        self.partiesEtMaillageFaceDeCoupe = []
        self.__computeTeeth__(dic)
# --------------------------------------------------------------------------------------------------
    def __computeTeeth__(self, dic):
        self.__addInsert__(dic['insert'], dic['insertFrame'])
        self.__addInsertByRotation__(len(self.partiesEtMaillageFaceDeCoupe))
# --------------------------------------------------------------------------------------------------
    def __addInsert__(self, dicInsert, dicFrame):
        insert = Insert.Insert(dicInsert)
        frame = fom.Frame(dicFrame)
        self.millFom.add(frame)
        # calculer les points de la plaquette dans le repere canonique de la fraise
        # insert.partiesEtMaillageFaceDeCoupe est la liste des parties de la plaquette ajoutée
        dicPartie = {}
        dicPartie["tooth_id"] = self.__toothId__
        print insert.elementary_tools_list
        for partie in insert.elementary_tools_list:
            dicPartie = {}
            dicPartie["tooth_id"] = self.__toothId__
            dicPartie["pnt_cut_edge"] = self.millFom.givePointsInCanonicalFrame(frame.name, partie["pnt_cut_edge"])
            dicPartie["pnt_in_cut_face"] = self.millFom.givePointsInCanonicalFrame(frame.name, [partie["pnt_in_cut_face"]])[0]
            dicPartie["h_cut_max"] = partie["h_cut_max"]
            dicPartie["node"] = self.millFom.givePointsInCanonicalFrame(frame.name, partie["node"])
            dicPartie["tri"] = partie["tri"]
            self.partiesEtMaillageFaceDeCoupe.append(dicPartie)
        print self.partiesEtMaillageFaceDeCoupe
        self.__toothId__+=1
# --------------------------------------------------------------------------------------------------
    def __addInsertByRotation__(self, nbParties):
        self.addTeethByRotation(nbParties)
# --------------------------------------------------------------------------------------------------        
# ==================================================================================================
class MonoblocMill(Mill):
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self,  dic):
        Mill.__init__(self, dic)

        self.nbDents            = dic["nbDents"] if dic.has_key("nbDents") else 2
        self.diametreFraise     = dic["diametreFraise"] if dic.has_key("diametreFraise") else 6.0E-3
        self.angleAxialInitial  = math.radians(dic["angleAxialInitial"]) if dic.has_key("angleAxialInitial") else 0.0
        self.angleHelice        = math.radians(dic["angleHelice"]) if dic.has_key("angleHelice") else 0.0
        self.loiDeCoupe         = dic["loiDeCoupe"]          if dic.has_key("loiDeCoupe")         else ["Loi1","Loi2","Loi3"]
        self.epaisseurFaceCoupe = dic["epaisseurFaceCoupe"]  if dic.has_key("epaisseurFaceCoupe") else 0.5e-3
        
        
        self.rayonFraise = self.diametreFraise/2
        self.partiesEtMaillageFaceDeCoupe = []
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class MonoblocMillType1(MonoblocMill):
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self, dic):
        """
        Documentation : Fraise cylindrique hélicoïdale
        """
        MonoblocMill.__init__(self, dic)

        self.longueurSuivantAxe = dic["longueurSuivantAxe"] if dic.has_key("longueurSuivantAxe") else 10.0e-3
        self.deltaBetaDegres    = dic["deltaBetaDegres"]    if dic.has_key("deltaBetaDegres")    else math.radians(1000.0)
        self.epaisseurFaceCoupe = dic["epaisseurFaceCoupe"] if dic.has_key("epaisseurFaceCoupe") else 0.5e-3
        self.nbSweep            = dic["nbSweep"]            if dic.has_key("nbSweep")            else 1

        self.angleHelice        = - math.atan(self.deltaBetaDegres*self.diametreFraise*0.5/self.longueurSuivantAxe)
        ###
        ### liste de dictionnaires : 
        ### chaque element a la structure suivante : 
        ###   { 
        ###     "partie" : [p1,p2,p3], 
        ###     "maillagePoints":[[x,y,z],["],...],
        ###     "maillageTiangles":[[i1,i2,i3],["],...]
        ###   }
        
        self.__generePartiesEtMaillageDent0__()
        self.addTeethByRotation()
# --------------------------------------------------------------------------------------------------
    def __generePartiesEtMaillageDent0__(self):
        alpha = self.angleAxialInitial
        beta  = self.deltaBetaDegres
        r     = self.diametreFraise / 2.
        L     = self.longueurSuivantAxe
        nb    = self.nbParties
        e     = self.epaisseurFaceCoupe
        
        theta = alpha
        z = 0.
        for i in range (nb):
            # Calcul des aretes de coupe :
            dicoPartie = {}
            next_theta = alpha + (i+1)*beta/nb
            next_z =  (i+1)*L/nb
            theta3 = theta + 0.5*beta/nb
            z3     = z + 0.5*L/nb
        
            p1 = [r* math.cos (theta), r* math.sin (theta), z ]
            p2 = [r* math.cos (next_theta), r* math.sin (next_theta), next_z ]
            p3 = [(r-e)* math.cos (theta3), (r-e)* math.sin (theta3), z3]
            
            dicoPartie["tooth_id"] = 0
            dicoPartie["pnt_cut_edge"] = [p1, p2]
            dicoPartie["pnt_in_cut_face"] = p3
            dicoPartie["h_cut_max"] = 1.2*e
            dicoPartie["node"] = []
            dicoPartie["tri"] = []
            # Calcul du maillage de la partie :
            # D'abord les points (les nodes)
            for jp in range (self.nbCouchesFaceCoupe+1):
                rm = r - jp*e/self.nbCouchesFaceCoupe
                for ip in range (self.nbTranches+1):
                    thetam = theta + ip*(next_theta - theta)/self.nbTranches
                    zm     = z + ip*(next_z -z)/self.nbTranches
                    
                    pm = [rm* math.cos (thetam), rm* math.sin (thetam), zm]
                    
                    dicoPartie["node"].append(pm)
            # ensuite les triangles (liste de tripplets indicant les 
            # indices des nodes dans le tableau des nodes)
            for jp in range (self.nbCouchesFaceCoupe):
                for ip in range (self.nbTranches):
                    idsommet1 = ip + jp*(self.nbTranches+1)
                    idsommet2 = ip + jp*(self.nbTranches+1)+1
                    idsommet3 = ip + (jp+1)*(self.nbTranches+1)
                    dicoPartie["tri"].append([idsommet1,idsommet2,idsommet3])
                    idsommet1 = idsommet3
                    idsommet3 = idsommet3+1   
                    dicoPartie["tri"].append([idsommet1,idsommet2,idsommet3])
            
            dicoPartie["cutlaw_names"] = ["LC_mat1","LC2_mat2","LC3_mat3"]
            self.partiesEtMaillageFaceDeCoupe.append(dicoPartie)
            theta = next_theta
            z = next_z
# --------------------------------------------------------------------------------------------------
# ==================================================================================================
class ToreMonoblocMill(MonoblocMill):
# ==================================================================================================
# --------------------------------------------------------------------------------------------------
    def __init__(self,  dic) :
        MonoblocMill.__init__(self, dic)


        self.angleSecteurCoupe  = math.radians(dic["angleSecteurCoupe"]) if dic.has_key("angleSecteurCoupe")  else math.pi
        self.angleDebutSecteur  = math.radians(dic["angleDebutSecteur"]) if dic.has_key("angleDebutSecteur")  else 0.
        self.rayonTore          = dic["rayonTore"]         if dic.has_key("rayonTore")  else None
                                         # rayonTore == None => fraise boule,
                                         # 0<rayonTore<diametreFraise/2 => fraise torique.
                       
        
        self.partiesEtMaillageFaceDeCoupe = []
        ###
        ### liste de dictionnaires : 
        ### chaque element a la structure suivante : 
        ###   { 
        ###     "partie" : [p1,p2,p3], 
        ###     "maillagePoints":[[x,y,z],["],...],
        ###     "maillageTiangles":[[i1,i2,i3],["],...]
        ###   }
        
        self.__generePartiesEtMaillageDent0__()
        self.addTeethByRotation()

# --------------------------------------------------------------------------------------------------
    def __prepareDonnees__(self):
        self.angleDebut = - math.pi/2. + self.angleDebutSecteur
        self.angleFin   = self.angleDebut + self.angleSecteurCoupe
        self.deltaAngle = self.angleSecteurCoupe / self.nbParties
        self.rayonCourbure = 0
        if self.rayonTore :
            self.rayonCourbure = self.rayonTore
        else : 
            self.rayonCourbure = self.diametreFraise/2

        #
        # Controle des données : verifier que : 
        # -> self.rayonCourbure - self.rayonCourbure * cos (self.angleDebut) < self.rayonFraise 
        # et
        # -> self.rayonCourbure - self.rayonCourbure * cos (self.angleFin) < self.rayonFraise 
        #
        if  self.rayonCourbure - self.rayonCourbure * math.cos (self.angleDebut) > self.rayonFraise \
           or self.rayonCourbure - self.rayonCourbure * math.cos (self.angleFin) > self.rayonFraise :
            raise InconcistentDataError("rayonCourbure et rayonFraise incohérents !")
            
        
# --------------------------------------------------------------------------------------------------
    def __generePartiesEtMaillageDent0__(self):
        self.__prepareDonnees__()
        alpha = self.angleAxialInitial
        r     = self.diametreFraise / 2.
        nb    = self.nbParties
        e     = self.epaisseurFaceCoupe
        rc    = self.rayonCourbure
        
        # Calcul des coordonnées cylindriques du premier point de la première arrête.
        betav  = self.angleDebut  # secteur de coupe.
        # Coordonnées cylidriques du premier point :
        zv = rc+rc*math.sin(betav)
        rv = self.rayonFraise - (rc - rc*math.cos(betav))
        thetav = zv * math.tan(self.angleHelice)/self.rayonFraise
        for i in range (nb):
            # Calcul des aretes de coupe :
            dicoPartie = {}
            next_betav = betav + self.deltaAngle
            #calcule du 2e point de l'arrête :
            next_zv = rc+rc*math.sin(next_betav)
            next_rv = self.rayonFraise - (rc - rc*math.cos(next_betav))
            next_thetav = next_zv * math.tan(self.angleHelice)/self.rayonFraise
            # Calcul du point dans face de coupe :
            p3_betav = betav+self.deltaAngle/2.
            p3_rcv   = rc-e
            p3_zv = rc+p3_rcv*math.sin(p3_betav)
            p3_rv = self.rayonFraise - rc + p3_rcv*math.cos(p3_betav)
            p3_thetav = p3_zv * math.tan(self.angleHelice)/self.rayonFraise
            
            
            
            p1 = [rv* math.cos (thetav), rv* math.sin (thetav), zv ]
            p2 = [next_rv* math.cos (next_thetav), next_rv* math.sin (next_thetav), next_zv ]
            p3 = [p3_rv* math.cos (p3_thetav), p3_rv* math.sin (p3_thetav), p3_zv]
            
            dicoPartie["tooth_id"] = 0
            dicoPartie["pnt_cut_edge"] = [p1, p2]
            dicoPartie["pnt_in_cut_face"] = p3
            dicoPartie["h_cut_max"] = 1.2*e
            dicoPartie["node"] = []
            dicoPartie["tri"] = []
            # Calcul du maillage de la partie :
            # D'abord les points (les nodes)
            for jp in range (self.nbCouchesFaceCoupe+1):
                rc_mv = rc - jp*e/self.nbCouchesFaceCoupe
                for ip in range (self.nbTranches+1):
                    beta_mv = betav + ip*(next_betav - betav)/self.nbTranches
                    # les 3 coordonnees en cylindrique :
                    z_mv = rc+(rc_mv)*math.sin(beta_mv)
                    r_mv = self.rayonFraise - rc + rc_mv*math.cos(beta_mv)
                    theta_mv = z_mv * math.tan(self.angleHelice)/self.rayonFraise
                                        
                    pm = [r_mv* math.cos (theta_mv), r_mv* math.sin (theta_mv), z_mv]
                    
                    dicoPartie["node"].append(pm)

            # ensuite les triangles (liste de tripplets indiquant les 
            # indices des nodes dans le tableau des nodes)
            for jp in range (self.nbCouchesFaceCoupe):
                for ip in range (self.nbTranches):
                    idsommet1 = ip + jp*(self.nbTranches+1)
                    idsommet2 = ip + jp*(self.nbTranches+1)+1
                    idsommet3 = ip + (jp+1)*(self.nbTranches+1)
                    dicoPartie["tri"].append([idsommet1,idsommet2,idsommet3])
                    idsommet1 = idsommet3
                    idsommet3 = idsommet3+1   
                    dicoPartie["tri"].append([idsommet1,idsommet2,idsommet3])
         
            dicoPartie["cutlaw_names"] = ["LC_mat1","LC2_mat2","LC3_mat3"]
            self.partiesEtMaillageFaceDeCoupe.append(dicoPartie)
            
            betav  = next_betav
            # Coordonnées cylidriques du premier point :
            zv = next_zv
            rv = next_rv
            thetav = next_thetav
# --------------------------------------------------------------------------------------------------
