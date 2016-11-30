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
        self.timer   = int(round(time.time() * 1000))
        
    def getTime(self):
        ret = int(round(time.time() * 1000))-self.timer
        self.timer = int(round(time.time() * 1000))
        return ret;

    def verifieenvironnement(self):
        # OBSERVATIONS
        print("|||||||||||||||||| temps avant tout: " + str(self.getTime()))
        self.laser.scan()
        print("|||||||||||||||||| laser: " + str(self.getTime()))
        self.mapping.maptest()
        print("|||||||||||||||||| temps map: " + str(self.getTime()))
        self.vision.traitementImage()
        print("|||||||||||||||||| temps image: " + str(self.getTime()) + "\n")
        


        # REFLEXION
        self.ref.analyseLasers()
        self.ref.analyseMapping()
        self.ref.analyseVision()

        # DECISION
        #print(self.returnAction())

    def returnAction(self):
        choix = self.ref.analyseGlobale()
        self.dec.veriferChoix(choix)
        action = self.dec.getAction()
        return action

       
        
