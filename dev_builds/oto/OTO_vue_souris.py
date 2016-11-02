
import bge
#import time
import bgui

#lg=bge.logic
#rd=bge.render

#rd.showMouse(1)


def mainSouris():
    obj=bge.logic.getCurrentController()
    
    
    if obj.sensors["Mouse"].positive and obj.sensors["Mouse1"].positive:
        pass
        #print(obj.sensors)
        #print("OK",obj.sensors["Mouse"].hitPosition,obj.sensors["Mouse"].hitObject)