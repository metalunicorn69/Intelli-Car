import bge


class Cerveau():
    def __init__(self,parent): # parent est l'objet participant qui vous represente
        self.analyseur=Analyseur()
        
class Analyseur():
    def __init__(self):
        self.operations_recentes=[]

