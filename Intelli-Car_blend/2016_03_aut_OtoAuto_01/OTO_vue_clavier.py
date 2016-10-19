import bge

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
            if key==112:
                # Activate Forward!

                ppath=bge.logic.expandPath("//")
                bge.render.makeScreenshot(ppath+"/image2")
                print("PHOTO ", ppath+"/image2")
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
            elif key==49:
                curScene.active_camera=curScene.objects["Camera"]
            elif key==50:
                curScene.active_camera=curScene.objects["Camera_haut"]
            else:
                print("touche de jeu",key,status) # sinon montre la touche enfoncee
