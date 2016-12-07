class Decision():
    def __init__(self):
        self.forward    = 0
        self.stop       = 0
        self.turnRight  = 0
        self.turnLeft   = 0
        self.choixFinal = [0,0,0,0]
        
    def veriferChoix(self,choix):
        self.forward    = choix[0]
        self.stop       = choix[1]
        self.turnRight  = choix[2]
        self.turnLeft   = choix[3]
        
        if choix[0] == 1 and choix[1] == 1:
            self.forward = 0
            self.stop = 0
        
        if choix[2] == 1 and choix[3] == 1:
            self.turnRight = 0
            self.turnLeft = 0

    def getAction(self):       
        listeActions = []
        
        self.choixFinal[0] = self.forward
        self.choixFinal[1] = self.stop
        self.choixFinal[2] = self.turnRight
        self.choixFinal[3] = self.turnLeft
        choix = self.choixFinal
        
        if choix == [0,0,0,0]:
            pass #AUCUNE ACTION
        
        elif choix == [0,0,0,1]:
            listeActions.append(self.tournegauche())
        
        elif choix == [0,0,1,0]:
            listeActions.append(self.tournedroit())
        
        elif choix == [0,1,0,0]:
            listeActions.append(self.arrete())
        
        elif choix == [1,0,0,0]:
            listeActions.append(self.accelere())
        
        elif choix == [0,1,0,1]:
            listeActions.append(self.arrete())
            listeActions.append(self.tournegauche())
        
        elif choix == [0,1,1,0]:
            listeActions.append(self.arrete())
            listeActions.append(self.tournedroit())
        
        elif choix == [1,0,0,1]:
            listeActions.append(self.accelere())
            listeActions.append(self.tournegauche())
        
        elif choix == [1,0,1,0]:
            listeActions.append(self.accelere())
            listeActions.append(self.tournedroit())
 
        return listeActions
        
    #************************************************************************   
    def accelere(self):
        return "accelere"
    
    def tournegauche(self):
        return"tournegauche"
    
    def tournedroit(self):
        return"tournedroit"
    
    def arrete(self):
        return"arrete"
    