import outils.vision

class Reflexion():
    def __init__(self):
        pass
    
    def analyseVision(self):
        result = [0,0,0,0]
        vision = vision.Vision() #instancier
        image = vision.getScreen() #prendre le screenshot et le charger en objet PIL
        imageBoW = vision.convertirBoW(image) #convertion en noir et blanc

        if vision.routeEnFace(image) is True:
            result[0] = 1
        else:
            result[1] = 1

        if vision.rueADroite is True:
            result[2] = 1

        if vision.rueAGauche is True:
            result[3] = 1

        print(result)
        return result 
    def analyseMapping(self):
        #Example: Le mapping en deduit que chaque action est possible sauf stop
        result = [1,0,1,1]
        return result
    
    def analyseLasers(self):
        #Example: Les lasers en deduisent que chaque action est possible sauf turnLeft
        result = [1,1,1,0]
        return result
    
        #Resultat attendu: forward, turnRight
    def analyseGlobale(self):
        v = self.analyseVision()
        m = self.analyseMapping()
        l = self.analyseLasers()
        numeroChoix = [] 
        
        for i in range (0,4):
        #INDEX 0 forward    #INDEX 2 turnRight
        #INDEX 1 stop       #INDEX 3 turnLeft
        
            if v[i]==1 and m[i]==1 and l[i]==1 :
                numeroChoix.append(1)
            else:
                numeroChoix.append(0)
      
        return numeroChoix