
import bge
import random
import math

def creerVille():
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
        #print("Nouveau ",nouveau.worldOrientation)
        rrot=random.randrange(2)
        if rrot:
            nouveau.applyRotation([0, 0, math.radians(90)], True)
            #print("Nouveau change ",nouveau.worldOrientation)