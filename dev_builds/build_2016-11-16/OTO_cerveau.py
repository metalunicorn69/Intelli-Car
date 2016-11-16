from cerveau.outils.lasers import *
from cerveau.outils.mapping import *
from cerveau.outils.vision import *
from cerveau.reflexion import *
from cerveau.decision import *

class Cerveau():
    def __init__(self,parent): # parent est l'objet modele qui vous represente
        self.laser 	 = Laser(parent)
        self.mapping = Mapping(parent)
        self.vision  = Vision(parent)
        self.ref 	 = Reflexion()
        self.dec 	 = Decision()
        
    def verifieenvironnement(self):
        # OBSERVATIONS
        self.laser.scan()
        self.mapping.maptest()
        self.vision.traitementImage()

        # REFLEXION
        self.ref.analyseLasers()
        self.ref.analyseMapping()
        self.ref.analyseVision()

        # DECISION
        print(self.returnAction())

    def returnAction(self):
        choix = self.ref.analyseGlobale()
        self.dec.veriferChoix(choix)
        action = self.dec.getAction()
        return action
       
        
