import bge
import helper
import random

class Laser():
    def __init__(self,parent):
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.moi = self.participant.nom
        self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
        self.angleVoiture = 0
        self.deg5toRad = 0.0872665
      
    def calculeAngle(self, laser1, laser2):
        return ((laser1 * self.deg5toRad + laser2 * self.deg5toRad) / 2)

    def scan(self):
        viseur=self.modele.moi.asset.children["otoviseur"]
        obj=self.modele.moi.asset
        xx=[]
        noLaserOuverture = None   #Premier laser qui ne détecte rien (Ouverture)
        noLaserFermeture = None   #Dernier laser qui ne détecte rien (Fermeture)
        listeAng = []   #Une liste des angles possibles

        Ydebut = viseur.position.y;
        DistanceLaser = 60;
        self.angleVoiture = self.angleVoiture+self.auto.tourne


        x,y = helper.Helper.getAngledPoint(self.angleVoiture, DistanceLaser, obj.position.x, obj.position.y)

        DX = x-obj.position.x
        DY = y-obj.position.y

        viseur.position.x = x
        viseur.position.y = y



        for i in range(0,36):
            x,y = helper.Helper.getAngledPoint(self.angleVoiture+(i*self.deg5toRad), DistanceLaser, obj.position.x, obj.position.y)
            viseur.position.x = x
            viseur.position.y = y
            xx.append(obj.rayCast(viseur,obj,DistanceLaser,""))
            if xx[i][1]:
                bge.render.drawLine(obj.position,xx[i][1], (255,255,0))
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
                listeAng.append(self.calculeAngle(noLaserOuverture, noLaserFermeture))
                print("--- SUPPRIME PASSAGE ---")
                noLaserOuverture = None
                noLaserFermeture = None

        print("--- LES ANGLES ---")
        for i in listeAng:
            print(i)

        if listeAng:
            angleChoisi = random.sample(listeAng, 1)
            print("--- ANLE CHOISI ---")
            print(angleChoisi)

# Tests
        #bge.c.actions.append([self.moi,"accelere",[]]) 
        #reflexion.analyseLaser.AnalyseLaser()
        print("--- RECOMMENCE ---")