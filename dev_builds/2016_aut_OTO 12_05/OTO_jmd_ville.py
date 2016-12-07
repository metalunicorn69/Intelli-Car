
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
                nouveau.worldPosition=[k.posx,k.posy,-1.2] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                # change pas le z
                nws=nouveau.worldScale
                nouveau.worldScale=[k.scalex,k.scaley,nws[2]]
                
                ajouteur.object="batiment"
                for b in k.batisses:
                    ajouteur.instantAddObject() # on ajoute l'objet
                    nouveau=ajouteur.objectLastCreated
                    pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
                    nouveau.worldPosition=[b.posx,b.posy,-2] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                    nouveau.worldScale=[b.scalex,b.scaley,b.scalez]
                    
                # ajout pancarte
                
                typesPan={0:"affInfo",1:"affArret",2:"affAverti"}
                nbarbre=random.randrange(2)+2
                #coins=[[k.cadreBx1,k.cadreBy1,90],
                #       [k.cadreBx1,k.cadreBy2,0],
                #       [k.cadreBx2,k.cadreBy1,0],
                #       [k.cadreBx2,k.cadreBy2,90]]
                coins=[[k.cadreBx1+2,k.cadreBy1+1,90],
                       [k.cadreBx1+1,k.cadreBy2-1,0],
                       [k.cadreBx2-1,k.cadreBy1+1,0],
                       [k.cadreBx2-1,k.cadreBy2-1,90]]
                for a in coins:
                    pan=random.randrange(3)
                    ajouteur.object=typesPan[pan]
                    ajouteur.instantAddObject() # on ajoute l'objet
                    nouveau=ajouteur.objectLastCreated
                    nouveau.worldPosition=[a[0],a[1],1.1] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                    if a[2]:
                        nouveau.applyRotation([0, 0, math.radians(90)], True)
            
            print("EPAISSEUR",nws[2]) 
            for k in j.parcs:
                ajouteur.object="parc"
                ajouteur.instantAddObject() # on ajoute l'objet
                nouveau=ajouteur.objectLastCreated
                pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
                nouveau.worldPosition=[k.posx,k.posy,-1.2] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                nouveau.worldScale=[k.scalex,k.scaley,1]
                
                nbarbre=random.randrange(5)+5
                for a in range(nbarbre):
                    soua=random.randrange(2)
                    if soua:
                        ajouteur.object="sapin"
                    else:
                        ajouteur.object="arbre"
                    ajouteur.instantAddObject() # on ajoute l'objet
                    nouveau=ajouteur.objectLastCreated
                    pos=nouveau.worldPosition # on va chercher sa position actuel (pour preserver le y)
                    print
                    x=random.randrange(k.large-16)+k.cadreBx1+4
                    y=random.randrange(k.profond-16)+k.cadreBy1+4
                    nouveau.worldPosition=[x,y,-0.5] # replace nouveau (qui contient le dernier objet cree) au x (de lex), le y actuel, le z ==1
                    
                    gros=random.randrange(4)+2
                    haut=random.randrange(6)+2
                    nouveau.worldScale=[gros,gros,haut]
    
                
    return villes[0]
            
                    
   
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
        self.pancartes=[]
        
        self.posx=debx+(int(xl/2))
        self.posy=deby+(int(yl/2))
        
        self.cadreTx1=debx+3
        self.cadreTy1=deby+3
        self.cadreTx2=debx+xl-3
        self.cadreTy2=deby+yl-3
        
        self.cadreBx1=self.cadreTx1+5
        self.cadreBy1=self.cadreTy1+5
        self.cadreBx2=self.cadreTx2-5
        self.cadreBy2=self.cadreTy2-5
        
        self.Bxl=xl-8
        self.Byl=yl-8
        
        self.scalex=int(self.Bxl/8)
        self.scaley=int(self.Byl/8)
        
        #print("PATE debut ",debx,deby, "largeur ",xl,yl)
        
        #print("CADRET",self.cadreTx1,self.cadreTy1,self.cadreTx2,self.cadreTy2)
        #print("CADREB",self.cadreBx1,self.cadreBy1,self.cadreBx2,self.cadreBy2)
        self.batisses=[]
        nbbatisse=random.randrange(5)+1
        for i in range (nbbatisse):
            x=random.randrange(self.scalex-1)+1#*8
            y=random.randrange(self.scaley-1)+1#*8
            
            
            scalex=0
            scaley=0
            scalez=0
            
            while scalex==0:
                sc=random.randrange(int(self.scalex)-1)+1
                
                
                if (x-(sc/2) >= 0) and (x+(sc/2)< self.scalex):
                    scalex=sc
                    
            while scaley==0:
                sc=random.randrange(int(self.scaley)-1)+1
                if (y-(sc/2) >= 0) and (y+(sc/2)< self.scaley):
                    scaley=sc
            
            
            scalez=random.randrange(16)+2
            posx=(x*8)+self.cadreBx1
            posy=(y*8)+self.cadreBy1
            
            Bx1=posx-int((scalex*8)/2)
            By1=posy-int((scaley*8)/2)
            Bx2=posx+int((scalex*8)/2)
            By2=posy+int((scaley*8)/2)
            """
            if Bx1 < self.cadreBx1 or \
               Bx2 > self.cadreBx2 or \
               By1 < self.cadreBy1 or \
               By2 > self.cadreBy2:
                print("BATISSEcadre",Bx1,By1,Bx2,By2 )
                print("BATCADRE",self.cadreBx1,self.cadreBy1,self.cadreBx2,self.cadreBy2)
                print("BATISSE",posx,posy,scalex,scaley )
            """
            bat=Batisse(posx,posy,scalex,scaley,scalez)
            self.batisses.append(bat)
            
class Parc():
    def __init__(self,debx,deby,xl,yl,type=""):
        global qtebatiment
        self.pancartes=[]
        self.typesPan={0:"affInfo",1:"affArret",2:"affAverti"}
        self.large=xl
        self.profond=yl
        self.posx=debx+(int(xl/2))
        self.posy=deby+(int(yl/2))
        
        self.cadreTx1=debx+3
        self.cadreTy1=deby+3
        self.cadreTx2=debx+xl-3
        self.cadreTy2=deby+yl-3
        
        self.cadreBx1=self.cadreTx1+5
        self.cadreBy1=self.cadreTy1+5
        self.cadreBx2=self.cadreTx2-5
        self.cadreBy2=self.cadreTy2-5
        
        self.Bxl=xl-8
        self.Byl=yl-8
        
        self.scalex=int(self.Bxl/8)
        self.scaley=int(self.Byl/8)
        
            
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
        #print("quartiers ",self.x1,self.y1,self.x2,self.y2)
        self.pates=[]
        self.parcs=[]
        
        x=random.randrange(4)+2
        y=random.randrange(4)+2
        xl=int(xl/x)
        yl=int(yl/y)
        inity=deby
        for i in range (x):
            deby=inity
            for j in range(y):
                randparc=random.randrange(12)
                if randparc==1:
                    self.parcs.append(Parc(debx,deby,xl,yl))
                else:
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