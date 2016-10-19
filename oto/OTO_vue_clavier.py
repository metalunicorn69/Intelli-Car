import bge
import time
import os

def main():
    #Get current scene
    curScene = bge.logic.getCurrentScene()
    #Get current controller - vient de "Camera"
    obj=bge.logic.getCurrentController()
    
    # verifie clavier
    sensor=obj.sensors["Keyboard"]
    # un raccourci pour mon nom (participant local)
    moi=bge.c.monnom
    # verifie ce qui se passe et prepare l'action correspondante qui sera envoyee au serveur
    if sensor.positive : # keyDown
        for key,status in sensor.events:          
            print("---------touche encore",key,status) # sinon montrela touche enfoncee
            if key==112: # touche 'p'
                # Activate Forward!
                #ppath=bge.logic.expandPath("//")
                t=str(time.time())
                n=t.index(".")
                nom=t[:n]+"_"+t[n+1:]
                bge.render.makeScreenshot(bge.ppath+"images/"+nom)
            if key==146: # fleche haut
                print("1- a partir de 'OTO_vue_clavier', donc une action clavier du participant,")
                print("1... on place ce que cet event veut dire dans bge.c.actions",[moi,"accelere",[]])
                bge.c.actions.append([moi,"accelere",[]])
            elif key==144: # fleche bas
                bge.c.actions.append([moi,"arrete",[]])
            elif key==143: # fleche droit
                bge.c.actions.append([moi,"tournedroit",[]])
            elif key==145: # fleche gauche
                bge.c.actions.append([moi,"tournegauche",[]])
            elif key==49: # (barre des nombres) 1 
                curScene.active_camera=curScene.objects["camOto"]
            elif key==50: # (barre des nombres) 2 
                curScene.active_camera=curScene.objects["camVoldoiseau"]
            elif key==104: #  touche 'h' pour hud
                if bge.c.hud:
                    bge.c.hud=0
                else:
                    bge.c.hud=1     #curScene.active_camera=curScene.objects["camVoldoiseau"]
            elif key==108: #  touche 'l' pour clear screen (console)
                os.system("cls") # pour windows 
                #os.system("clear") # pour Linux ou iOS
            else:
                pass
            print("touche de jeu",key,status) # sinon montre la touche enfoncee
