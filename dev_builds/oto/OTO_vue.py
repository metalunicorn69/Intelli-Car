
import bgui
import bgui.bge_utils
import bge
import random
import os
os.chdir(bge.logic.expandPath('//'))


class SplashLayout(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)
        monnom,monip,self.own=data
        # ajout d'une image
        self.img = bgui.Image(self, 'splash.jpg', size=[.9, .7], pos=[.01, .3],
            options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)
        
        # ajout d'etiquette
        self.lbl = bgui.Label(self, text="Votre nom", pos=[0.1, 0.25],
            sub_theme='Large', options = bgui.BGUI_DEFAULT )
        self.lbl = bgui.Label(self, text="IP du serveur", pos=[0.1, 0.15],
            sub_theme='Large', options = bgui.BGUI_DEFAULT)
        self.lbl = bgui.Label(self, text="IP du client", pos=[0.1, 0.05],
            sub_theme='Large', options = bgui.BGUI_DEFAULT)

        # ajout de bouton
        self.btnserveur = bgui.FrameButton(self, text='Creer un serveur', size=[.25, .06], pos=[.6, .14],
            options = bgui.BGUI_DEFAULT)

        self.btnserveur.on_click = self.on_click_serveur
        
        # un autre bouton
        self.btnclient = bgui.FrameButton(self, text='Creer un client', size=[.25, .06], pos=[.6, .03],
            options = bgui.BGUI_DEFAULT)

        self.btnclient.on_click = self.on_click_client

        # ajout de champs de texte
        self.inNom = bgui.TextInput(self, text=monnom, size=[.4, .04], pos=[.3, 0.24],
            input_options = bgui.BGUI_INPUT_NONE, options = bgui.BGUI_DEFAULT)
        self.inNom.activate()
        
        # on aurait pu utiliser un Label (statique)
        self.inIPcreeServeur = bgui.TextInput(self, text=monip, size=[.4, .04], pos=[.3, 0.14],
            input_options = bgui.BGUI_INPUT_SELECT_ALL, options = bgui.BGUI_DEFAULT)
        self.inIPcreeServeur.frozen=1

        self.inIPconnecteClient= bgui.TextInput(self, text=monip, size=[.4, .04], pos=[.3, 0.04],
            options = bgui.BGUI_DEFAULT)
        
    def on_click_serveur(self, widget):
        bge.c.creeServeur()

    def on_click_client(self, widget):
        bge.c.inscritClient()

class LobbyLayout(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)
        monnom,monip,self.own=data
        # ajout d'une image
        self.img = bgui.Image(self, 'img.jpg', size=[.5, .4], pos=[.05, .5],
                            options = bgui.BGUI_DEFAULT)
        
        # ajout d'un listbox                    
        self.block=bgui.ListBox(self, items=['banane','pomme','orange','poire'],
                                size=[0.4, 0.6], pos=[0.6,0.3])
	
        # ajout d'etiquette
        self.lbl = bgui.Label(self, text="Liste des participants inscrits", pos=[0.6, 0.9],
            sub_theme='Large', options = bgui.BGUI_DEFAULT )
        # ajout de bouton
        self.btndemarre = bgui.FrameButton(self, text='Demarrer la simulation', size=[.25, .06], pos=[.6, .14],
            options = bgui.BGUI_DEFAULT)
        if bge.c.egoserveur!=1:
            self.btndemarre.frozen=1
            
        self.btndemarre.on_click = self.on_demarre_simulation
        
    def on_demarre_simulation(self, widget):
        bge.c.demarreSimulation()
        
class SimulLayout(bgui.bge_utils.Layout):
    def __init__(self, sys, data):
        super().__init__(sys, data)
        monnom,monip,self.own=data
        # ajout d'une image
        lisdir=os.listdir(bge.ppath+"images/")
        lisdir.sort()
        lisdir.reverse()
        img=lisdir.pop(0)
        nom=bge.ppath+"images/"+img
        print("IMAGEEEEE     ",nom)
        
        self.img = bgui.Image(self, nom, size=[.1, .1], pos=[.0, .0],
            options = bgui.BGUI_DEFAULT|bgui.BGUI_CACHE)
        #self.img = bgui.Image(self, nom, size=[.1, .1], pos=[.0, .0],
        #    options = bgui.BGUI_DEFAULT|bgui.BGUI_CENTERX|bgui.BGUI_CACHE)

        # ajout de bouton
        self.btnfermeimage = bgui.FrameButton(self, text='X', size=[.02, .02], pos=[.02, .02],
            options = bgui.BGUI_DEFAULT)

        self.btnfermeimage.on_click = self.on_click_fermeimage
        
        
    def on_click_fermeimage(self, widget):
        bge.c.hud=0
        bge.c.hudactif=0

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.splash=None
        self.lobby=None
        
    def afficheArtefact(self,j):
        for i in j:
            ass=j[i].asset
            a=j[i].auto
            if a.tourne:
                ass.applyRotation([0, 0, a.tourne], True)
                a.tourne=0
            if a.vitesse:
                ass.applyMovement([0,a.vitesse,0.0],True)
        if self.parent.hud:
            if self.parent.hudactif==0:
                print("In VUE PAS de HUD en faire un")
                self.parent.own['sys'].load_layout(None) # on supprime le dernier layout
                self.parent.own['sys'].load_layout(SimulLayout,[bge.c.monnom,bge.c.monip,bge.c.own]) # on place le lobby d'attente apres inscription
                self.parent.hudactif=1
            #else:
            #    print(" IN VUE HUD ACTIFFFFFFFFFFFF")
                
        else:
            if self.parent.hudactif:
                self.parent.own['sys'].load_layout(None) # on supprime le dernier layout
                self.parent.hudactif=0
                           
    def afficheListeparticipants(self,participants):
        b=bge.c.own['sys'].layout.block
        b.items=participants
        
    def trouveNom(self):
        nom=self.splash.inNom.text
        return nom
    
    def trouveIPServeur(self):
        ipserveur=self.splash.inIPconnecteClient.text
        return ipserveur
        
         