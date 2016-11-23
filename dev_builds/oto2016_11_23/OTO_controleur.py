"""
version 14

- Ajoute des batiments de diverse tailles sur la carte
- 

"""

# on importe toutes les librairies habituelles
import Pyro4    # reseau facile
import bge      # blender game engine
import bgui     # blender Graphic User Interface
import bgui.bge_utils # un utilitaire de BGUI qui fait un peu de magie (?)

import random   # pour les choses aleatoires
import os       # pas utilise dans ce module devrait etre enlever
import socket   # pour chercher l'adresse IP
from subprocess import Popen # pour lancer le serveur qui est une autre application python autonome (Popen est 'Process open')

import OTO_modele # notre modele (dans le sens MVC)
import OTO_vue # notre Vue, idem
import math

import OTO_jmd_ville

bge.ppath=bge.logic.expandPath("//")

# le controleur qui est genere par la derniere ligne- dans la fonction main qui est explicitement appelle au demarrage
# voir la paire sensor('demarre')/controller('python1') lie a la camera dans les logic bricks
class Controleur():
    def __init__(self):
        print("IN CONTROLEUR")
        self.cadre=0 # le no de cadre pour assurer la syncronisation avec les autres participants
        self.tempo=0 # insert a reconnaitre qu'on a lance le serveur et qu'on peut s'inscrire automatiquement sans cliquer sur inscription dans l'interface
                     # ne peut pas etre remplace par egoserveur car si cette variable test a vrai (1), l'inscription est effectuee et tempo remis a 0 pour ne pas reinscrire deux fois...
                     # NOTE le nom de variable est ici epouvantable, j'en conviens - devrait quelquechose comme 'autoInscription'
        self.egoserveur=0 # est-ce que je suis celui qui a demarre le serveur, a priori, non (0)
        self.actions=[]    # la liste de mes actions a envoyer au serveur pour qu'il les redistribue a tous les participants
        self.statut=0 # etat dans le quel je me trouve : 0 -> rien, 1 -> inscrit, 2 -> demarre, 3-> joue
        self.monip=self.trouveIP() # la fonction pour retoruner mon ip
        self.monnom=self.genereNom() # un generateur de nom pour faciliter le deboggage (comme ça il genere un nom quasi aleatoire et on peut demarrer plusieurs 'participants' sur une même machine pour tester)
        self.hud=0
        self.hudactif=0
        self.optionsdyn=[]
        self.modele=None # pas encore de modele
        self.vue=OTO_vue.Vue(self) # mais on cree la Vue
        
        cont=bge.logic.getCurrentController() # on procede a trouver l'objet qui tient le controle du jeu
        self.own = cont.owner # le proprietaire du controller courant (la camera en l'occurence)
        
        self.own['sys'] = bgui.bge_utils.System('../../themes/default') # cree un objet System qui contiendra le layout
                                                                        # et qui precise le theme des widgets (couleurs, font, etc)
        self.own['sys'].load_layout(OTO_vue.SplashLayout,[self.monnom,self.monip,self.own]) # on fournit au systeme cree avant une ref vers la classe de layout qu'on veut
        self.vue.splash=self.own['sys'].layout # on conserve une ref plus directe vers le layout pour y modifier le contenu initial au besoin (incrementer un nombre, deplacer une image etc)
        
        mouse = bge.logic.mouse # veut obtient la reference bge de la souris
        mouse.visible = True # on precise que le pointeur doit etre visible
                
    def trouveIP(self): # fonction pour trouver le IP en 'pignant' gmail
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # on cree un socket
        s.connect(("gmail.com",80))    # on envoie le ping
        monip=s.getsockname()[0] # on analyse la reponse qui contient l'IP en position 0 
        s.close() # ferme le socket
        return monip
    
    def genereNom(self):  # generateur de nouveau nom - accelere l'entree de nom pour les tests - parfois ça peut generer le meme nom mais c'est rare
        monnom="jmd_"+str(random.randrange(100))
        return monnom

    def creeServeur(self):
        pid = Popen(["C:\\Python34\\Python.exe", "./OTO_serveur.py"],shell=1).pid # on lance l'application serveur
        self.egoserveur=1 # on note que c'est soi qui, ayant demarre le serveur, aura le privilege de lancer la simulation
        self.tempo=1 # on change d'etat pour s'inscrire automatiquement 
                     # (parce que dans ce type de programme on prend pour acquis que celui qui prepare la simulation veut aussi y participer)


    # NOTE si on demarre le serveur, cette fonction est appellee pour nous (voir timer et variable tempo)
    #      ou par un clique sur le bouton 'Creerunclient' du layout
    def inscritClient(self):
        ipserveur=self.vue.trouveIPServeur() # lire le IP dans le champ du layout
        ad="PYRO:controleurServeur@"+ipserveur+":54440" # construire la chaine de connection
        self.serveur=Pyro4.core.Proxy(ad) # se connecter au serveur
        
        nom=self.vue.trouveNom() # noter notre nom
        if nom:
            self.monnom=nom
        
        rep=self.serveur.inscritClient(self.monnom)    # on averti le serveur de nous inscrire
        
        self.own['sys'].load_layout(None) # on supprime le dernier layout
        self.own['sys'].load_layout(OTO_vue.LobbyLayout,[bge.c.monnom,bge.c.monip,bge.c.own]) # on place le lobby d'attente apres inscription
        self.statut=1 # statut 1 == attente de lancement de partie
    
    def demarreSimulation(self): # reponse du bouton de lancement de simulation (pour celui qui a parti le serveur seulement)
        rep=self.serveur.demarreSimulation() 
        if rep==1:
            self.statut=3 # il change son statut pour lui permettre d'initer la simulation, les autres sont en 1 (attente) - voir timer.py
    
    def initierSimulation(self,rep):  # initalisation locale de la simulation, creation du modele, generation des assets et suppression du layout de lobby
        if rep[1][0][0]=="demarreSimulation":
            self.statut=2  # statut de simulation en cours
            self.modele=OTO_modele.Modele(self) # on cree le modele
            self.modele.initSimulation(rep[1][0][1]) # on initialise certains attributs
            self.genereAssets(self.modele.participants) # on genere les obejts 3D charghes de les representer
            # Options dynamiques
            print("Mes Options dynamiques ",self.optionsdyn)
            self.own['sys'].load_layout(None) # on enleve le layout e lobby (NOTE on pourrait ici inserer un lobby de jeu au besoin)
        #self.creerVille()
        #OTO_jmd_ville.creerVille()
    """   
    def creerVille(self):
        scene = bge.logic.getCurrentScene()
        objets=scene.objects
        cam=objets["createur"] # notre camera
        ajouteur = cam.actuators['ajoutObjet']
        ajouteur.object="batiment"
        print("MON OBJET",ajouteur.object)
        for i in range(100):
            ajouteur.instantAddObject() # on ajoute l'objet
            nouveau=ajouteur.objectLastCreated
            pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
            x=random.randrange(400)-200
            y=random.randrange(400)-200
            nouveau.worldPosition=[x,y,0] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
            x,y,z=nouveau.worldScale
            #print("SCALE ",x,y,z)
            rz=random.randrange(10)/5
            nouveau.worldScale=[x*2,y,z+(z*rz)]
            print("Nouveau ",nouveau.worldOrientation)
            rrot=random.randrange(2)
            if rrot:
                nouveau.applyRotation([0, 0, math.radians(90)], True)
                print("Nouveau change ",nouveau.worldOrientation)
    """    
        
    def genereAssets(self,participants):
        scene = bge.logic.getCurrentScene()
        objets=scene.objects
        createur=objets["createur"] # un objet sur la scene s'appelle createur
        cam=objets["camOto"] # notre camera
        ajouteur = createur.actuators['ajoutObjet'] # le empty 'createur' a une brick actuator de type objet qui s'appelle ajoutObjet
        lex=0
        #print("1 ",objets)
        # ici on va trier les noms des participants qu'ils s'alignent tous dasn le meme ordre sur les diverses machines
        if len(participants.keys())>1:
            j=list(participants.keys())
            j.sort()
        else:
            j=participants
        # pour tous ces participants nous allons ajouter un objet 3D
        ajouteur.object="oto"
        for i in j:
            ajouteur.instantAddObject() # on ajoute l'objet
            nouveau=ajouteur.objectLastCreated
            #print("Nouvel objet ",nouveau.name,nouveau.children)
            pos=nouveau.position # on va chercher sa position actuel (pour preserver le y)
            nouveau.position=[lex,pos[1],1] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
            x=random.randrange(100)/100
            y=random.randrange(100)/100
            nouveau.color=[1,x,y,True] # inutilise - finalement les couleurs sont attribuees dans le modele
            participants[i].asset=nouveau # on place le nouveau dasn l'asset du participant courant i
            participants[i].auto.x=lex # on modifie les proprietes de position de l'Auto dans le modele ici, le x
            participants[i].auto.y=pos[1] # ici le y
            participants[i].auto.direction=nouveau.localOrientation.to_euler() # on note l'angle actuel de l'objet dans le modele
            print("ANGLE DE L'AUTO ", participants[i].auto.direction,math.degrees(participants[i].auto.direction[2]))
            #self.Eu_rad(
            if i==self.monnom: # si le participant pour lequel on vient de creer un objet 3D est 'moi' c'est a dire mon char pas celui des autres participants
                cam.setParent(nouveau, False,True) # alors on parente la camera a cette auto pour la suivre dans ses deplacements
            lex=lex+2 # on incremente le x pour tasser le prochain char sur la ligne de depart
            
    def Eu_rad(self,eu):  # eu in degrees
        eu_x,eu_y,eu_z = eu[0],eu[1],eu[2]
        eu_x = math.radians(eu_x)
        eu_y = math.radians(eu_y)
        eu_z = math.radians(eu_z)
        eu_rad = Mathutils.Euler(eu_x,eu_y,eu_z)
        return eu_rad
        
    def prochaintour(self): # la boucle de jeu principale, qui sera apelle par la fonction bouclejeu du timer
        if self.serveur: # s'il existe un serveur
            self.cadre=self.cadre+1 # increment du compteur de cadre
            self.modele.prochaineAction(self.cadre)    # mise a jour du modele
            self.vue.afficheArtefact(self.modele.participants) # mise a jour de la vue
            if self.actions: # si on a des actions a partager 
                rep=self.serveur.faitAction([self.monnom,self.cadre,self.actions]) # on les envoie 
                """
                print("2 - dans la boucle prochaintour du controleur (dans OTO_controleur.py")
                print("2... on envoie au serveur la variable du controleur self.actions")
                print("2... avec mon nom et mon cadre",[self.monnom,self.cadre,self.actions])
                print("2... NOTE:le serveur va placer cet action dans le dico representant chaque participant")
                print("2... NOTE... pour que tous les participants recoivent cette information")
                """
            else:
                rep=self.serveur.faitAction([self.monnom,self.cadre,0]) # sinon on envoie rien au serveur on ne fait que le pigner 
                                                                        # (HTTP requiert une requete du client pour envoyer une reponse)
            self.actions=[] # on s'assure que les actions a`envoyer sont maintenant supprimer (on ne veut pas les envoyer 2 fois)
            if rep[0]: # si le premier element de reponse n'est pas vide
                """
                print("3- reponse du serveur ",rep)
                print("3... s'il y a qqchose dans rep[0], c'est qu'on a une action a mettre dans le modele")
                print("3... traite l'element 2 en le(s) placants dans le dico self.modele.actionsAFaire")
                print("3... voici rep[2]",rep[2])
                """
                for i in rep[2]:   # pour chaque action a faire (rep[2] est dictionnaire d'actions en provenance des participants
                                   # dont les cles sont les cadres durant lesquels ses actions devront etre effectuees
                    if i not in self.modele.actionsAFaire.keys(): # si la cle i n'existe pas
                        self.modele.actionsAFaire[i]=[] #faire une entree dans le dictonnaire
                    for k in rep[2][i]: # pour toutes les actions lies a une cle du dictionnaire d'actions recu
                        self.modele.actionsAFaire[i].append(k) # ajouter cet action au dictionnaire sous l'entree dont la cle correspond a i
            if rep[1]=="attend": # si jamais rep[0] est vide MAIS que rep[1] == 'attend', on veut alors patienter
                self.cadre=self.cadre-1  # donc on revient au cadre initial
        else:
            print("Aucun serveur connu")
  
        
def main(): # la fonction appellee explicitement par le premier sensor 'Always' attache a la camera - c'est elle qui part le bal!!!
    bge.c=Controleur()