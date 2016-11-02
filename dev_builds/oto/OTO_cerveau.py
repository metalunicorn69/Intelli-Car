import bge
import helper
import reflexion

class Cerveau():
    def __init__(self,parent): # parent est l'objet modele qui vous represente
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.moi = self.participant.nom
        self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
        self.angleVoiture = 0
       
    def verifieenvironnement(self):
        viseur=self.modele.moi.asset.children["otoviseur"]
        obj=self.modele.moi.asset
        xx=[]
        deg5toRad = 0.0872665 #variable contenant la valeur en radiant de 5 degree
    
        Ydebut = viseur.position.y;
        DistanceLaser = 60;
        self.angleVoiture = self.angleVoiture+self.auto.tourne


        x,y = helper.Helper.getAngledPoint(self.angleVoiture, DistanceLaser, obj.position.x, obj.position.y)

        DX = x-obj.position.x
        DY = y-obj.position.y

        viseur.position.x = x
        viseur.position.y = y



        for i in range(0,36):
            x,y = helper.Helper.getAngledPoint(self.angleVoiture+(i*deg5toRad), DistanceLaser, obj.position.x, obj.position.y)
            viseur.position.x = x
            viseur.position.y = y
            xx.append(obj.rayCast(viseur,obj,DistanceLaser,""))
            if xx[i][1]:
                bge.render.drawLine(obj.position,xx[i][1], (255,255,0))
                print("ray["+str(i)+"] distance : "+str(xx[i][1][1]))

        # Tests
        #bge.c.actions.append([self.moi,"accelere",[]]) 
        reflexion.analyseLaser.AnalyseLaser()
        
        



