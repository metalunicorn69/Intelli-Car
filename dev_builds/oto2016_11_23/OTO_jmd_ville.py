
import bge
import random
import math

qtebatiment=0

def creerVille(largeur,profondeur):
    print("DEBUT DE VILLE")
    villes=[]
    for i in range(1):
        villes.append(Ville(largeur,profondeur))
    scene = bge.logic.getCurrentScene()
    objets=scene.objects
    cam=objets["createur"] # empty
    ajouteur = cam.actuators['ajoutObjet']
    ajouteur.object="batiment"
    print("MON OBJET",ajouteur.object)
    for i in villes:
        for j in i.quartiers:
            for k in j.pates:
                ajouteur.object="trottoir"
                ajouteur.instantAddObject() # on ajoute l'objet
                nouveau=ajouteur.objectLastCreated
                pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
                
                nouveau.worldPosition=[k.posx,k.posy,0] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                
                nouveau.worldScale=[k.scalex,k.scaley,1]
                
                ajouteur.object="batiment"
                for b in k.batisses:
                    ajouteur.instantAddObject() # on ajoute l'objet
                    nouveau=ajouteur.objectLastCreated
                    pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
                    
                    nouveau.worldPosition=[b.posx,b.posy,0] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                    
                    nouveau.worldScale=[b.scalex,b.scaley,b.scalez]
                    
                    #rrot=random.randrange(2)
                    #if rrot:
                    #    nouveau.applyRotation([0, 0, math.radians(90)], True)
                    #    
                    #    ddir=nouveau.localOrientation.to_euler() # on note l'angle actuel de l'objet dans le modele
                     
   
class Batisse():
    def __init__(self,posx,posy,sx,sy,sz):
        self.posx=posx
        self.posy=posy
        self.scalex=sx
        self.scaley=sy
        self.scalez=sz

class Pate():
    def __init__(self,debx,deby,xl,yl,type=""):
        global qtebatiment
        self.posx=debx+(int(xl/2))
        self.posy=deby+(int(yl/2))
        
        self.cadreTx1=debx+3
        self.cadreTy1=deby+3
        self.cadreTx2=debx+xl-3
        self.cadreTy2=deby+yl-3
        
        self.cadreBx1=self.cadreTx1+1
        self.cadreBy1=self.cadreTy1+1
        self.cadreBx2=self.cadreTx2-1
        self.cadreBy2=self.cadreTy2-1
        
        self.Bxl=xl-8
        self.Byl=yl-8
        
        self.scalex=int(self.Bxl/8)
        self.scaley=int(self.Byl/8)
        
        self.batisses=[]
        nbbatisse=random.randrange(5)+1
        
        for i in range (nbbatisse):
            x=random.randrange(self.scalex-2)+1#*8
            y=random.randrange(self.scaley-2)+1#*8
            scalex=0
            scaley=0
            scalez=0
            while scalex==0:
                sc=random.randrange(4)+2
                if (x-(int(sc/2)) >= 0) and (x+(int(sc/2))< self.scalex):
                    scalex=sc
                    
            while scaley==0:
                sc=random.randrange(4)+2
                if (y-(int(sc/2)) >= 0) and (y+(int(sc/2))< self.scaley):
                    scaley=sc
            
            scalez=random.randrange(16)+2
            posx=(x*8)+self.cadreBx1
            posy=(y*8)+self.cadreBy1
            
            print("BATISSE",self.scalex,self.scaley,x,y,"ET",scalex,scaley,posx,posy)
            
            bat=Batisse(posx,posy,scalex,scaley,scalez)
            self.batisses.append(bat)
            
            
class Pate1():
    def __init__(self,debx,deby,xl,yl,type=""):
        global qtebatiment
        self.posx=debx+(int(xl/2))
        self.posy=deby+(int(yl/2))
        self.scalex=int(xl/8)
        self.scaley=int(yl/8)
        self.batisses=[]
        xplace=int((xl-32)/16)
        yplace=int((yl-32)/16)
        
        nbbatisse=random.randrange(5)+1
        for i in range (nbbatisse):
            x=random.randrange(xplace)
            y=random.randrange(yplace)
            posx=(x*16)+16+debx
            posy=(y*16)+16+deby
            scalx=random.randrange(8)+1
            scaly=random.randrange(8)+1
            scalz=random.randrange(16)+2
            bat=Batisse(posx,posy,scalx,scaly,scalz)
            self.batisses.append(bat)
            #print("            BATISSE ",posx,posy,scalx,scaly,scalz)
            qtebatiment +=1
            
            
        
        
class Quartier():
    def __init__(self,debx,deby,xl,yl,type=""):
        self.x1=debx
        self.y1=deby
        self.x2=debx+xl
        self.y2=deby+yl
        print("quartiers ",self.x1,self.y1,self.x2,self.y2)
        self.pates=[]
        
        x=random.randrange(4)+2
        y=random.randrange(4)+2
        xl=int(xl/x)
        yl=int(yl/y)
        inity=deby
        for i in range (x):
            deby=inity
            for j in range(y):
                self.pates.append(Pate(debx,deby,xl,yl))
                deby =deby+yl
                #print("        PATE ",debx,deby,xl,yl)
            debx=debx+xl
        
class Ville():
    def __init__(self,largeur,profondeur):
        global qtebatiment
        self.quartiers=[]
        x=random.randrange(4)+4
        y=random.randrange(4)+4
        xl=int(largeur/x)
        yl=int(profondeur/y)
        debx=int((largeur/2)*-1)
        deby=int((profondeur/2)*-1)
        initdeby=deby
        for i in range (x):
            deby=initdeby
            for j in range(y):
                self.quartiers.append(Quartier(debx,deby,xl,yl))
                deby =deby+yl
                #print("    QUARTIER ",debx,deby,xl,yl)
            debx=debx+xl
        print("FIN DE VILLE ",qtebatiment)