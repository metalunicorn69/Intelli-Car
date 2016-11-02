import bge
import reflexion

class Cerveau():
    def __init__(self,parent): # parent est l'objet modele qui vous represente
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.moi = self.participant.nom
        #self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
       
    def verifieenvironnement(self):
        viseur=self.modele.moi.asset.children["otoviseur"]
        obj=self.modele.moi.asset
        xx=obj.rayCast(viseur,obj,30.0,"")
        if xx[1]:
            bge.render.drawLine(obj.position,xx[1], (255,255,0))
            bge.c.actions.append([self.moi,"tournegauche",[]])

        # Tests
        bge.c.actions.append([self.moi,"accelere",[]]) 
        reflexion.analyseLaser.AnalyseLaser()
        
        



