from PIL import Image, ImageFilter
import bge
import math
import time

class Vision():

    def __init__(self,parent):
        self.modele = parent # Référence au modele qui vous represente
    
    def traitementImage(self):
        print("analyseImage!")

    #prend UN screenshot
    def prendreScreenshot(self, nom):
        bge.render.makeScreenshot(bge.ppath+"images/"+nom)

    #prend un screenshot, le nomme temp, et va le chargen en objet PIL
    #retourne le screenshot sous forme d'object PIL
    def getScreen(self):
        prendreScreenshot("temp")
        image = Image.open("images/temp")
        return image

    #retourne true si une rue à droite est détectée
    #A utiliser avec une image monochrome! pas RGB!
    def rueADroite(image):
        avantNoir = False
        entreNoir = False
        apresNoir = False
        width, height = image.size
        ligneDroite = (width-2, 0, width-1, height-2)
        image = image.crop(ligneDroite)

        for i in range(height-2):
            pixel = image.getpixel((0, i))
            if pixel < 20:
                avantNoir = True
            if avantNoir is True:
                if pixel == 255:
                    entreNoir = True
            if avantNoir is True and entreNoir is True:
                if pixel < 20:
                    apresNoir = True

        return avantNoir and entreNoir and apresNoir

    #retourne True s'il y a un virage à gauche possible
    #a utiliser avec des images monochromes! pas RGB!
    def rueAGauche(image):
        avantNoir = False
        entreNoir = False
        apresNoir = False
        width, height = image.size
        ligneGauche = (0, 0, 1, height-2)
        image = image.crop(ligneGauche)

        for i in range(height-2):
            pixel = image.getpixel((0, i))
            if pixel < 20:
                avantNoir = True
            if avantNoir is True:
                if pixel == 255:
                    entreNoir = True
            if avantNoir is True and entreNoir is True:
                if pixel < 20:
                    apresNoir = True

        return avantNoir and entreNoir and apresNoir

    def convertirBoW(image):
        imageBoW = Image.new('L', image.size) #cree une nouvelle image grayscale
        imageBoW.paste(image) #colle le contenu de l'image rgb
        imageBoW = imageBoW.point(lambda x: 0 if x<50 else 255, '1') #converti en noir OU blanc
        return imageBoW #retourne l'objet PIL monochrome


    
    # Retourne une string clarifiant la section de l'image en HORIZ_VERTI ex : CG_C (Centre Gauche en Horizontal et Centre Vertical)
    def trouverSection(image,x,y):
        width, height = img.size
        baseX = width/5
        baseY = height/3
        result = []

        # Trouver section Horizontal 
        for i in range(0,5):
            if x < baseX*(i+1) and x >= baseX*i:
                #0 : Gauche
                #1 : Centre-Gauche
                #2 : Centre
                #3 : Centre-Droit
                #4 : Droit
                result.append(i)

        # Trouver section Vertical
        for i in range(0,3):
            if y < baseY*(i+1) and y >= baseY*i:
                #0 : Haut
                #1 : Centre
                #2 : Bas
                result.append(i)
            return result

    # Append les points Y, en relation avec un X initial, qui ont un changement de couleur dans une liste
    def changementDeCouleurVertical(image,x):
        width, height = image.size
        derniereCouleur = image.getpixel((x,0))
        result=[]

        for i in range(0,height):
                if not is_similar(derniereCouleur, image.getpixel((x,i)), 5): # Si la derniere couleur est differente de la nouvelle
                    result.append(i)

                derniereCouleur = image.getpixel((x,i))
            

        return result

        # Append les points X, en relation avec un Y initial, qui ont un changement de couleur dans une liste
    def changementCouleurHorizontal(image,y):
        width, height = image.size
        derniereCouleur = image.getpixel((0,y))
        result=[]

        for i in range(0,width):
                if not isCouleursSimilaires(derniereCouleur, image.getpixel((i,y)), 5): # Si la derniere couleur est differente de la nouvelle
                    result.append(i)

                derniereCouleur = image.getpixel((i,y))
            

        return result

    # Cree matrice avec points qui definit un rectangle
    def defRect(image):
        width, height = image.size
        arrayRect = []
        for i in range(0,width,5):
            arrayVertical = changementDeCouleurVertical(image,i)
            tuple_rgb = (255,0,0) ## TUPLE COULEUR ROUGE POUR FEEDBACK VISUEL
            arrayTmp = []
            if(arrayVertical[len(arrayVertical)-1]-arrayVertical[0] > 10): # Si premiere position - derniere position est plus petite que 10 px, reconait en tant que rectangle
                tuple_position = (i, arrayVertical[0]) ## TEST POUR FEEDBACK VISUEL
                image.putpixel(tuple_position, tuple_rgb) ## TEST POUR FEEDBACK VISUEL
                arrayTmp.append(arrayVertical[0])

            tuple_position = (i, arrayVertical[len(arrayVertical)-1]) ## TEST POUR FEEDBACK VISUEL
            image.putpixel(tuple_position, tuple_rgb) ## TEST POUR FEEDBACK VISUEL
            arrayTmp.append(arrayVertical[len(arrayVertical)-1])
            arrayRect.append(arrayTmp)

        image.save('out.png') ## TEST POUR FEEDBACK VISUEL
        #image.show() ## TEST POUR FEEDBACK VISUEL

        return arrayRect

    def trouvePancarte(image):
        width, height = image.size
        partieDroite = image.crop(width/2, 0, width, height)
        partieDroite.show()

    def isCouleursSimilaires(pixelA, pixelB, threshold):
        r1,g1,b1 = pixelA
        r2,g2,b2 = pixelB
        result = False

        if abs(r1-r2) <= threshold:
            if abs(g1-g2) <= threshold:
                if abs(b1-b2) <= threshold:
                    result = True

        return result

    def getCouleurString(pixel): ######################################################## A TESTER
        r,g,b = pixel
        couleur = "gris"

        # Rouge
        if r > g and r > b and b is g:
            couleur = "rouge"

        # Jaune
        elif g > r and b > r:
            couleur = "jaune"

        # Rose
        elif r > b and b > g:
            couleur = "rose"

        # Vert
        elif g > r and g > b and r is b:
            couleur = "vert"

        # Aqua
        elif b > g and g > r:
            couleur = "aqua"

        # Bleu
        elif b > r and b > r and r is g:
            couleur = "bleu"

        # Blanc
        elif r > 200 and g > 200 and b > 200:
            couleur = "blanc"

        return couleur

# Cree matrice avec points qui definit un rectangle
    def dessiner(image):
        width, height = image.size
        arrayRect = []

        for i in range(0,width,1):
            arrayVertical = changementCouleurVertical(image,i)
            tuple_rgb = (0,0,255) ## TUPLE COULEUR ROUGE POUR FEEDBACK VISUEL
            
            for j in enumerate(arrayVertical):
                tuplePosition = (i,j[1])
                image.putpixel(tuplePosition,tuple_rgb)

        for i in range(0,height,1):
            arrayVertical = changementCouleurHorizontal(image,i)
            tuple_rgb = (0,0,255) ## TUPLE COULEUR ROUGE POUR FEEDBACK VISUEL
            
            for j in enumerate(arrayVertical):
                tuplePosition = (j[1],i)
                image.putpixel(tuplePosition,tuple_rgb)

        #image.save('out.png') ## TEST POUR FEEDBACK VISUEL
        image.show() ## TEST POUR FEEDBACK VISUEL

        return arrayRect