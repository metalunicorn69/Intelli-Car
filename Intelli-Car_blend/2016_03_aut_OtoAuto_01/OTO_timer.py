import bgui
import bgui.bge_utils
import bge
import OTO_vue

def boucleattente():
    rep=bge.c.serveur.faitAction([bge.c.monnom,0,0])
    if rep[0]:
        print("Recu ORDRE de DEMARRER")
        bge.c.own['sys'].load_layout(None)
        bge.c.initierSimulation(rep[2])
    elif rep[0]==0:
        bge.c.vue.afficheListeparticipants(rep[2])
    
def initiejeu():
    rep=bge.c.serveur.faitAction([bge.c.monnom,0,0])
    if rep[0]==1:
        print("Initie jeu",rep)
        bge.c.initierSimulation(rep[2])
        bouclejeu()
    else:
        print("On a commence, la!")

def bouclejeu():
    bge.c.prochaintour()
    
def mainloop():    
    if bge.c.tempo:
        bge.c.tempo=0
        bge.c.inscritClient()
    else:
        bge.c.own['sys'].run()
        
    if bge.c.statut==1:
        boucleattente()
        
    elif bge.c.statut==2:
        bouclejeu()
        
    elif bge.c.statut==3:
        initiejeu()
    