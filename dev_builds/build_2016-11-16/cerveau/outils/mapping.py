import bge
import helper

class Mapping():
    def __init__(self,parent):
        self.modele = parent # Référence au modele qui vous represente
    
    def maptest(self):
        print("MAPPING!")