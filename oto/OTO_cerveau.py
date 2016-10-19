import bge


class Cerveau():
    def __init__(self,parent): # parent est l'objet modele qui vous represente
        self.analyseur=Analyseur()
        self.modele = parent # Référence au modele qui vous represente
        self.participant=self.modele.moi # Référence au participant qui vous represente
        self.auto = self.participant.auto # Référence a l'auto du participant qui vous represente
       
       

class Analyseur():
    def __init__(self):
        self.operations_recentes=[]


class AnalyseLaser():
    def __init__(self):
    	pass

class AnalyseImage():
	def __init__(self):
		pass