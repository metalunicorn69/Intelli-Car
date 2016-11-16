import bge
import helper

class Laser():
    def __init__(self,parent):
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.moi = self.participant.nom
        self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
        self.angleVoiture = 0
    
    def scan(self):
        viseur=self.modele.moi.asset.children["otoviseur"]
        obj=self.modele.moi.asset
        xx=[]
        deg5toRad = 0.34#0.0872665 variable contenant la valeur en radiant de 5 degree
        Ydebut = viseur.position.y;
        DistanceLaser = 10#60;
        self.angleVoiture = self.angleVoiture+self.auto.tourne
        x,y = helper.Helper.getAngledPoint(self.angleVoiture, DistanceLaser, obj.position.x, obj.position.y)
        DX = x-obj.position.x
        DY = y-obj.position.y
        viseur.position.x = x
        viseur.position.y = y

        for i in range(0,10):#(0,36):
            x,y = helper.Helper.getAngledPoint(self.angleVoiture+(i*deg5toRad), DistanceLaser, obj.position.x, obj.position.y)
            viseur.position.x = x
            viseur.position.y = y
            xx.append(obj.rayCast(viseur,obj,DistanceLaser,""))
            if xx[i][1]:
                bge.render.drawLine(obj.position,xx[i][1], (255,255,0))
                bge.c.actions.append([self.moi,"tournegauche",[]])
                #print("ray["+str(i)+"] distance : "+str(xx[i][1][1]))

        #REGARDE LISTE DE LASERS ET ANALYSE OÙ SONT LES PASSAGES
        noLaserOuverture = None   #Premier laser qui ne détecte rien (Ouverture)
        noLaserFermeture = None   #Dernier laser qui ne détecte rien (Fermeture)
        for idx, laser in enumerate(xx):   #Enumeration des lasers (idx = Index)
            if idx == 0 and laser[1] is None:   #Si le premier laser est null, début d'ouverture
                noLaserOuverture = idx
            elif laser[1] is None and noLaserOuverture == None: #Si le laser détecte rien, prend laser d'avant (début d'ouverture)
                noLaserOuverture = idx-1
            elif (laser[1] is not None or idx == len(xx)-1) and noLaserOuverture != None:   #Si le laser détecte quelque chose après début d'ouverture, fin d'ouverture
                noLaserFermeture = idx
                #FONCTION POUR CALCULER ANGLE
                #if noLaserFermeture - noLaserOuverture > 2:
                #    print(calculeAngle(noLaserOuverture,noLaserFermeture))
                print(noLaserOuverture)
                print(noLaserFermeture)
                print("--- SUPPRIME PASSAGE ---")
                noLaserOuverture = None
                noLaserFermeture = None