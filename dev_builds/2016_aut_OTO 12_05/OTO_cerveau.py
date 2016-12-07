import bge


class Cerveau():
    def __init__(self,parent): # parent est l'objet participant qui vous represente
        self.parent=parent
        self.analyseur=Analyseur()
        
    def verifieenvironnement(self):
        # C'EST ICI QUE VOUS INTERVENEZ
        #ceci est juste pour voir qqch
        viseur=self.parent.moi.asset.children["otoviseur"]
        obj=self.parent.moi.asset
        xx=obj.rayCast(viseur,obj,30.0,"")
        if xx[1]:
            bge.render.drawLine(obj.position,xx[1], (255,0,0))
        
        
class Analyseur():
    def __init__(self):
        self.operations_recentes=[]

