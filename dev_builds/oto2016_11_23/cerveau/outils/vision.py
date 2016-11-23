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

    def getScreen(self):
        prendreScreenshot("temp")
        image = Image.open("images")

    
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