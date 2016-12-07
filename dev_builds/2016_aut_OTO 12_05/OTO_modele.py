import random
import helper
import bge
import OTO_cerveau
import OTO_jmd_ville


class Auto():
    def __init__(self,parent,couleur):
        self.parent=parent
        self.x=0
        self.y=0
        self.z=0
        self.couleur=couleur
        self.etat=0
        self.vitesse=0
        self.acceleration=0.1
        self.direction=0
        self.max=20
        self.min=-0.2
        self.tourne=0
        self.actionsPossibles={"accelere":self.accelere,
                              "tournegauche":self.tournegauche,
                              "tournedroit":self.tournedroit,
                              "arrete":self.arrete}
        
    def tournegauche(self,a=None):
        self.tourne=-0.1
    def tournedroit(self,a=None):
        self.tourne=0.1
        
    def arrete(self,a=None):
        if self.vitesse>self.min:
            self.vitesse=self.vitesse-self.acceleration
        
    def accelere(self,a=None):
        if self.vitesse<self.max:
            self.vitesse=self.vitesse+self.acceleration
        
    def prochaineAction(self):
        if self.vitesse:
            self.y=self.y+self.vitesse

class Participant(): #_15 remplace participant par Participant pour conserver la majuscule au nom de classe
    def __init__(self,parent,nom,couleur):
        self.parent=parent
        self.cerveau=None
        self.actions={}
        self.nom=nom
        self.asset=None
        self.couleur=couleur
        self.auto=Auto(self,couleur)
        self.actions={"accelere":self.auto.accelere,
                     "tournegauche":self.auto.tournegauche,
                     "tournedroit":self.auto.tournedroit,
                     "arrete":self.auto.arrete}
        
    def prochaineAction(self):
        self.auto.prochaineAction()
    
    def evalueAction(self):
        pass

class Modele():
    id=0
    def nextId():
        Modele.id=Modele.id+1
        return Modele.id
    
    def __init__(self,parent):
        self.parent=parent
        self.rdseed=0
        self.participants={}
        self.piste=""
        self.actions=[]
        self.actionsAFaire={}
        
        scene = bge.logic.getCurrentScene()
        objets=scene.objects
        fond=objets["fond"]
        self.largeur,self.profondeur,haut=fond.worldScale
        self.ville=OTO_jmd_ville.creerVille(self.largeur,self.profondeur)
        
    def initSimulation(self,listeNomsparticipants):
        self.piste="premiere"
        couleurs=["red","blue","green","yellow","orange","purple","pink","lightblue"]
        n=0
        for j in listeNomsparticipants:
            e=Participant(self,j,couleurs[n]) # _15 corriger le nom de la classe pour Participant
            self.participants[j]=e
            if j==self.parent.monnom:
                self.moi=e
                e.cerveau=OTO_cerveau.Cerveau(self) # on ajoute un cerveau uniquement au participant qui correspond a moi
            n=n+1
    
    def prochaineAction(self,cadre):
        if cadre in self.actionsAFaire:
            for i in self.actionsAFaire[cadre]:
                self.participants[i[0]].actions[i[1]](i[2])
                """
                print("4- le modele distribue les actions au divers participants")
                print("4...- en executant l'action qui est identifie par i[1] le dico")
                print("4...- qui est dans l'attribut actions",i[0],i[1],i[2])
                print("NOTE: ici on applique immediatement cette action car elle consiste soit")
                print("NOTE... a changer la vitesse (accelere/arrete) soit l'angle de l'auto")
                print("NOTE... dans ce cas-ci faire la prochaine action (le prochain for en bas)")
                print("NOTE... c'est seulement changer la position de l'auto si sa vitesse est non-nul")
                """
            del self.actionsAFaire[cadre]
                
        for i in self.participants:
            self.participants[i].prochaineAction()
            
        for i in self.participants:
            self.participants[i].evalueAction()
            
        self.verifieenvironnement()
        
    def verifieenvironnement(self):
        self.moi.cerveau.verifieenvironnement()
        """
        viseur=self.moi.asset.children["otoviseur"]
        obj=self.moi.asset
        xx=obj.rayCast(viseur,obj,30.0,"")
        if xx[1]:
            bge.render.drawLine(obj.position,xx[1], (255,0,0))
        """