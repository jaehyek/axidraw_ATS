# -*- coding: utf-8 -*- 

from ATS.ETA2ClientPlugin.ETA2ClientPlugin import ETA2ClientPlugin
import ebb_motion
import os
import time

class ClientPlugin(ETA2ClientPlugin):
    def __init__(self, client, index, context):
        ETA2ClientPlugin.__init__(self, client, index, context) 
        COMPort = System.GetScenarioParameter("COMPort", "")
        System.Debug( "COMPort : "  + COMPort )
        self.ebb = ebb_motion.EBB(COMPort)
        self.ebb.sendEnableMotors(1)
        self.listpos = self.ebb.getStepPosition(False)
        System.Debug(("Axidraw current pos : %s %s" % (self.listpos[0], self.listpos[1] )))
        self.listAxiRes = [100,100]
        self.listPhoneRes = [100,100]
        
        self.config_penup = 14500
        self.config_pendown = 12000
        self.config_penrate = 750
        self.listAxiRes = [-5500, -11000]
        
        dirconfig = u"C:\\eclipse\\Axidraw_conf"
        filenameconfig = dirconfig + u"\\" + self.GetDeviceShellId()[1] + u".conf"
        try:
            
            fconf = open(filenameconfig)
            for line in fconf :
                key,values = line.strip().split("=") 
                if len(key) == 0 : 
                    continue
                listvalues = values.split(",")
                if len(listvalues) >= 2 :
                    self.__dict__[key.strip()] = [int(aa) for aa in values.split(",")]
                else:
                    self.__dict__[key.strip()] = int(listvalues[0])
        except: 
            System.Debug("can't open a config file :%s" % filenameconfig )
            pass
        
        self.configPenUpDown()
        self.listPhoneRes = [self.MainScreen.Width, self.MainScreen.Height]
        
        System.Debug( self.listAxiRes )
        System.Debug( self.listPhoneRes )
        
        self.rateX = float(self.listAxiRes[0])/float(self.listPhoneRes[0])
        self.rateY = float(self.listAxiRes[1])/float(self.listPhoneRes[1])
        System.Debug("coordiante Ratex, RateY: %s, %s" %(self.rateX, self.rateY))
        System.Debug("Pen Height, low: %s, height:%s" %(self.config_pendown, self.config_penup))

    def configPenUpDown(self):
        self.ebb.configServo(4, self.config_pendown)
        self.ebb.configServo(5, self.config_penup)
        self.ebb.configServo(11, self.config_penrate) 
        self.ebb.configServo(12, self.config_penrate)
        
    def PenDown(self):
        self.ebb.getReady()
        self.ebb.sendPenDown()
        
    def PenUp(self):
        self.ebb.getReady()
        self.ebb.sendPenUp( ) 
        
    def PenClick(self):
        self.PenDown()
        time.sleep(0.1)
        self.PenUp()    
        
    def setXYSpeedLimit(self, speedlimitpersec):  
        self.ebb.setXYSpeedLimit(speedlimitpersec)  
    
    def setZSpeedLimit(self, config_penrate):  
        self.ebb.configServo(11, self.config_penrate) 
        self.ebb.configServo(12, self.config_penrate)          

    def TouchScreen(self, x, y):
        System.Debug(u"STARTED DEVx.TouchScreen()")
        #print("Touch coordi : %s, %s" %(x, y))
        self.ebb.sendPenUp( )
        self.ebb.getReady()
        self.ebb.doABMove(int(x*self.rateX-self.listpos[0]), int(y*self.rateY-self.listpos[1]))
        self.PenClick()
        self.ebb.getReady()
        self.listpos = self.ebb.getStepPosition(False)
        System.Debug(u"FINISHED DEVx.TouchScreen()")
        
    def TouchScreenEx(self,action, x, y, milidelay):
        System.Debug(u"STARTED DEVx.TouchScreenEx()")
        #print("Touch coordi : %s, %s" %(x, y))
        if action == TOUCH_MOVETO : 
            self.ebb.getReady()
            self.ebb.doABMove(int(x*self.rateX-self.listpos[0]), int(y*self.rateY-self.listpos[1]))
        elif action == TOUCH_MOVEBY:
            self.ebb.getReady()
            self.ebb.doABMove(int(x*self.rateX), int(y*self.rateY))
        elif action == TOUCH_CLICK : 
            self.ebb.sendPenUp( )
            self.ebb.getReady()
            self.ebb.doABMove(int(x*self.rateX-self.listpos[0]), int(y*self.rateY-self.listpos[1]))
            self.PenClick()
        elif action == TOUCH_DBLCLICK : 
            self.TouchScreenDouble(x, y, 200)
        elif action == TOUCH_DOWN : 
            self.ebb.getReady()
            self.ebb.doABMove(int(x*self.rateX), int(y*self.rateY))
            self.PenDown()
        elif action == TOUCH_UP :
            self.ebb.getReady()
            self.ebb.doABMove(int(x*self.rateX), int(y*self.rateY)) 
            self.PenUp()
        else : 
            print('cant operation for action')
            exit(0)
            
        self.ebb.getReady()
        time.sleep(float(milidelay)/float(1000))
        self.listpos = self.ebb.getStepPosition(False)
        System.Debug(u"FINISHED DEVx.TouchScreenEx()")
        
    
    def TouchScreenDouble(self, x, y, milidelay):
        System.Debug(u"STARTED DEVx.TouchScreenDouble()")
        #print("Touch coordi : %s, %s" %(x, y))
        
        self.ebb.sendPenUp( )
        self.ebb.getReady()
        self.ebb.doABMove(int(x*self.rateX-self.listpos[0]), int(y*self.rateY-self.listpos[1]))
        
        self.ebb.getReady()
        self.ebb.sendPenDown( )
        self.ebb.getReady()
        self.ebb.sendPenUp( ) 
        
        time.sleep(float(milidelay)/1000)     
        
        self.ebb.sendPenDown( )
        self.ebb.getReady()
        self.ebb.sendPenUp( )
           
        self.listpos = self.ebb.getStepPosition(False)
        
        
        '''
        self.ebb.sendPenUp( )
        self.ebb.getReady()
        self.ebb.doABMove(int(x*self.rateX-self.listpos[0]), int(y*self.rateY-self.listpos[1]))
        
        self.ebb.getReady()
        self.ebb.sendPenDown( )
        #time.sleep(float(0.05))
        self.ebb.getReady()
        self.ebb.sendPenUp( ) s
        
        time.sleep(float(milidelay)/1000)     
        
        self.ebb.sendPenDown( )
        #time.sleep(float(0.05))
        self.ebb.getReady()
        self.ebb.sendPenUp( )
           
        
        self.listpos = self.ebb.getStepPosition(False)    
        '''
        
        System.Debug(u"FINISHED DEVx.TouchScreenDouble()")

        
    def UIClickByName(self, objName, occurrence=0,uiTarget=UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByName()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIGetObjectByName(objName, uiTarget, occurrence)
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1 
        if rc != AT_SUCCESS : 
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByName()")
        return rc
 
    def UIClickByText(self, findText, occurrence = 0, uiTarget = UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByText()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIGetObjectByText(findText, occurrence, uiTarget )
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1
        if rc != AT_SUCCESS : 
            System.Debug(u"FINISHED DEVx.UIClickByText()")
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByText()")
        return rc
    
    def UIClickByDescription(self,description, occurrence = 0, uiTarget = UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByDescription()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIGetObjectByDescription(description, occurrence, uiTarget )
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1
        if rc != AT_SUCCESS : 
            System.Debug(u"FINISHED DEVx.UIClickByDescription()")
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByDescription()")
        return rc
    
    def UIClickByFieldValue(self, fieldName, fieldValue, occurrence = 0, target = UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByFieldValue()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIClickByFieldValue(fieldName, fieldValue, occurrence, uiTarget )
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1
        if rc != AT_SUCCESS : 
            System.Debug(u"FINISHED DEVx.UIClickByFieldValue()")
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByFieldValue()")
        return rc
    
    def UIClickByHint(self, hint, occurrence = 0, uiTarget = UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByHint()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIGetObjectByHint(hint, occurrence, uiTarget )
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1
        if rc != AT_SUCCESS : 
            System.Debug(u"FINISHED DEVx.UIClickByHint()")
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByHint()")
        return rc
    
    def UIClickByTypeIndex(self, objType, index, uiTarget = UITarget.TopWindow):
        System.Debug(u"STARTED DEVx.UIClickByTypeIndex()")
        nRetryCount = 2
        while( nRetryCount > 0 ) : 
            rc, result = self.UIGetObjectByTypeIndex(objType, index, uiTarget )
            if rc == AT_SUCCESS:
                break
            else:
                time.sleep(0.2)
                nRetryCount -= 1
        if rc != AT_SUCCESS : 
            System.Debug(u"FINISHED DEVx.UIClickByTypeIndex()")
            return rc
        x, y = result.GetCenterCoords()
        self.TouchScreen(x, y)
        System.Debug(u"FINISHED DEVx.UIClickByTypeIndex()")
        return rc    
    
    def UIDrag(self, xFrom, yFrom, xTo, yTo, steps) : 
        System.Debug(u"STARTED DEVx.UIDrag()")
        self.PenUp()
        self.ebb.doABMove(int(xFrom*self.rateX-self.listpos[0]), int(yFrom*self.rateY-self.listpos[1]))
        self.PenDown()
        self.listpos = self.ebb.getStepPosition(False)
        self.ebb.doABMove(int(xTo*self.rateX-self.listpos[0]), int(yTo*self.rateY-self.listpos[1]))
        self.PenUp()
        self.listpos = self.ebb.getStepPosition(False)
        System.Debug(u"FINISHED DEVx.UIDrag()")
        
    def AxiReset(self):
        self.ebb.getReset()
        self.listpos = self.ebb.getStepPosition(False)
