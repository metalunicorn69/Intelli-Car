import bge


class Cerveau():
    def __init__(self,parent): # parent est l'objet modele qui vous represente
        self.analyseur=Analyseur()
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.moi = self.participant.nom
        self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
        bge.c.actions.append([self.moi,"accelere",[]]) 
       
    def verifieenvironnement(self):
        viseur=self.modele.moi.asset.children["otoviseur"]
        obj=self.modele.moi.asset
        xx=obj.rayCast(viseur,obj,30.0,"")
        if xx[1]:
            bge.render.drawLine(obj.position,xx[1], (255,255,0))
            bge.c.actions.append([self.moi,"tournegauche",[]]) 


class Analyseur():
    def __init__(self):
        self.operations_recentes=[]


class AnalyseLaser():
    def __init__(self):
    	pass

class AnalyseImage():
	def __init__(self):
		pass

