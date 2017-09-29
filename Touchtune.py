
import time
from collections import deque
import os 

touchsleeptime = 0.5

def UpdatePenHeight():
    # adjust at current posotion 
    DEV1.config_pendown = 12000
    DEV1.config_penup = 14500
    DEV1.config_penrate = 750
    DEV1.configPenUpDown()
    
    looppendown = 20
    
    adjustdone = False
    time.sleep(2)
    rc, result = DEV1.UIGetObjectByText("Touchtune")
    if rc == AT_SUCCESS:
        DEV1.KeyPressByAlias(u"back, back")
        time.sleep(touchsleeptime) 
        DEV1.KeyPressByAlias(u"home, home")
        DEV1.RunApplication(u"Touchtune", u"")
        time.sleep(1)
    
    while(looppendown > 0 ) : 
        looppendown -= 1 
        
        try:
            DEV1.PenDown()
            time.sleep(touchsleeptime)
            DEV1.PenUp()
            time.sleep(touchsleeptime)
            coordi_x = float(DEV1.UIGetObjectByName(u"coordi_x")[1].Text)
            coordi_y = float(DEV1.UIGetObjectByName(u"coordi_y")[1].Text)
            print("**** %s, %s" %(coordi_x, coordi_y))
            if coordi_x >= 0 :
                DEV1.config_pendown -= 400
                DEV1.config_penup -= 400
                DEV1.configPenUpDown()
                adjustdone = True
                break
        except:
            DEV1.config_pendown -= 200
            DEV1.config_penup -= 200
            DEV1.configPenUpDown()
            continue
    if adjustdone == True:
        print("Pen Height was adjusted")
    else:
        print("Pen Height was not configured")
    return adjustdone
        
    
def UpdateRateXY(dq):
    if len(dq) != 2 : 
        print("Not length of Deque == 2 ")
        exit()
    
    PhoneRes0_X, PhoneRes0_Y, AxiDraw0_X, AxiDraw0_Y = dq[0]
    PhoneRes1_X, PhoneRes1_Y, AxiDraw1_X, AxiDraw1_Y = dq[1]
    
    # in case of too closed too point
    if abs(PhoneRes0_X - PhoneRes1_X) < 4 or abs(PhoneRes0_Y - PhoneRes1_Y) < 5 : 
        print("too closed points")
        return
    
    rateX = float(AxiDraw1_X - AxiDraw0_X ) / float( PhoneRes1_X - PhoneRes0_X )
    rateY = float(AxiDraw1_Y - AxiDraw0_Y ) / float( PhoneRes1_Y - PhoneRes0_Y )
    
    DEV1.rateX = rateX
    DEV1.rateY = rateY
    
    print("coordiante Ratex, RateY: %s, %s" %(rateX, rateY))
    
listcurrpoint = []
def saveCurrentPosition():
    global listcurrpoint
    loop = 30
    while(loop>0) : 
        try:
            loop -= 1 
            listcurrpoint = []
            DEV1.PenClick()
            time.sleep(0.5)
            coordi_x = DEV1.UIGetObjectByName(u"coordi_x")
            coordi_y = DEV1.UIGetObjectByName(u"coordi_y")
            listcurrpoint.append(float(coordi_x[1].Text))
            listcurrpoint.append(float(coordi_y[1].Text))
            print("current position : %s,%s"%(listcurrpoint[0],listcurrpoint[1] ))
            break
        except:
            print("can't read coord_x or coordi_y")
            time.sleep(0.5)
            rc, result = DEV1.UIGetObjectByText("Touchtune")
            if rc == AT_SUCCESS:
                DEV1.KeyPressByAlias(u"back, back")
                time.sleep(touchsleeptime) 
                DEV1.KeyPressByAlias(u"home, home")
                DEV1.RunApplication(u"Touchtune", u"")
                time.sleep(1)
                
            continue
    
def TestMain():
    global listcurrpoint
    
    dirconfig = u"C:\\eclipse\\Axidraw_conf"
    try:
        os.mkdir(dirconfig)
    except :
        pass
    
    
    System.Debug(os.getcwd())
    
    ScreenWidth = DEV1.MainScreen.Width
    ScreenHeight = DEV1.MainScreen.Height    
    x = 0
    y = 1 
    
    # below is for x-y alignment
    ScreenSpace = 300
    p0 = [0 + ScreenSpace, 0 + ScreenSpace ]
    p1 = [ScreenWidth - ScreenSpace, 0 + ScreenSpace ]
    p2 = [ScreenWidth - ScreenSpace, ScreenHeight - ScreenSpace ]
    p3 = [0 + ScreenSpace, ScreenHeight - ScreenSpace ]
    pointcenter = {0:int(ScreenWidth/2), 1:int(ScreenHeight/2)}    

    DEV1.KeyPressByAlias(u"home, home")
    
    DEV1.RunApplication(u"Touchtune", u"")
    
    rc, result = DEV1.UIGetObjectByText("Touchtune")
    if rc == AT_SUCCESS:
        DEV1.KeyPressByAlias(u"back, back")
        time.sleep(touchsleeptime) 
        DEV1.KeyPressByAlias(u"home, home")
        DEV1.RunApplication(u"Touchtune", u"")
        
    
    # determine if pen is on screen and adjust the pen height    
    dq = deque([[0,0,],[0,400],[0,-800] ])

    while(len(dq) > 0 ):
        DEV1.RunApplication(u"Touchtune", u"")
        p = dq.popleft()
        DEV1.TouchScreenEx(TOUCH_MOVEBY, p[0], p[1] , 500)
        
        adjustdone = UpdatePenHeight()
        if adjustdone == True : 
            break       
         
    if adjustdone == False : 
        print("can't adjust pen height")
        exit()      
          
    print("pendown = %s" % DEV1.config_pendown)
    print("penup = %s" % DEV1.config_penup)
     
    
    # first, set the default screen resolution rate 
    DEV1.rateX = -3.5
    DEV1.rateY = -3.5
    
    dequeRateXY = deque()
    dequeZ = deque()
    
    #add current point to dequeRateXY
    saveCurrentPosition()
    dequeRateXY.append( listcurrpoint + DEV1.listpos[:])
    
    #add screen center point to dequeRateXY
    print("At center Point, updateXY and UpdatePenHeight")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, pointcenter[0] - listcurrpoint[0], pointcenter[1] - listcurrpoint[1] , 500)
    UpdatePenHeight()
    dequeZ.append([DEV1.config_pendown, DEV1.config_penup])
    saveCurrentPosition()
    
    dequeRateXY.append( listcurrpoint + DEV1.listpos[:])
    UpdateRateXY(dequeRateXY)
    

    
    
    # move to p0 and  measure the height.
    print("move to p0 and  updateXY and UpdatePenHeight")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p0[x] - listcurrpoint[0], p0[y] - listcurrpoint[1] , 500)
    UpdatePenHeight()
    dequeZ.append([DEV1.config_pendown, DEV1.config_penup])
    saveCurrentPosition()
    
    print("updateXY at p0")
    while(1):
        DEV1.TouchScreenEx(TOUCH_MOVEBY, p0[x] - listcurrpoint[0], p0[y] - listcurrpoint[1] , 500)
        saveCurrentPosition()
    
        if (abs(p0[x] - listcurrpoint[0] < 5 ) and (p0[y] - listcurrpoint[1])< 5 ):
            break
        
    dequeRateXY.append( listcurrpoint + DEV1.listpos[:])
    dequeRateXY.popleft()
    UpdateRateXY(dequeRateXY)

    

    # move to p2    
    print("move to p2 and     updateXY and UpdatePenHeight")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p2[x] - listcurrpoint[0], p2[y] - listcurrpoint[1] , 500)
    UpdatePenHeight()
    dequeZ.append([DEV1.config_pendown, DEV1.config_penup])
    saveCurrentPosition()
    
    ## second touch and get the coordinate    
    print("updateXY at p2")
    while(1):
        DEV1.TouchScreenEx(TOUCH_MOVEBY, p2[x] - listcurrpoint[0], p2[y] - listcurrpoint[1] , 500)
        saveCurrentPosition()
    
        if (abs(p2[x] - listcurrpoint[0]) < 5 ) and (abs(p2[y] - listcurrpoint[1])< 5 ):
            break
 
    dequeRateXY.append( listcurrpoint + DEV1.listpos[:])
    dequeRateXY.popleft()
    UpdateRateXY(dequeRateXY)
    
    # move to p1 and     UpdatePenHeight
    print("move to p1 and     updateXY and UpdatePenHeight")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p1[x] - listcurrpoint[0], p1[y] - listcurrpoint[1] , 500)
    UpdatePenHeight()
    dequeZ.append([DEV1.config_pendown, DEV1.config_penup])
    saveCurrentPosition()
    
    # move to p3 and     UpdatePenHeight
    print("move to p3 and     updateXY and UpdatePenHeight")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p3[x] - listcurrpoint[0], p3[y] - listcurrpoint[1] , 500)
    UpdatePenHeight()
    dequeZ.append([DEV1.config_pendown, DEV1.config_penup])
    saveCurrentPosition()
    
    # at here, finish the pendown value, and must to set the value
    # because the next touchscreen command should be done.
    
    print(dequeZ)
    listz = sorted(dequeZ, key=lambda lista: lista[0] )
    
    DEV1.config_pendown = listz[0][0]
    DEV1.config_penup = listz[0][1]
    DEV1.configPenUpDown()
    
        
    # to set up the DEV1.listpos exactly, listcurrpoint * rate should not be  zero 
    # so we move to p1 point.
    print("set current position")
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p2[x] - listcurrpoint[0], p2[y] - listcurrpoint[1] , 500)
    saveCurrentPosition()
    DEV1.listpos = [DEV1.rateX * listcurrpoint[0], DEV1.rateY * listcurrpoint[1] ] 
    time.sleep(touchsleeptime) 
    
    # set the axidraw origin
    DEV1.TouchScreen(0, 0)
    DEV1.AxiReset()
    
    # after reset, configure the pendown value again.
    
    DEV1.config_pendown = listz[0][0]
    DEV1.config_penup = listz[0][1]
    DEV1.configPenUpDown()
    
    print("pendown = %s" % DEV1.config_pendown)
    print("penup = %s" % DEV1.config_penup)
    

    
    listPhoneRes = [ScreenWidth, ScreenHeight ]
    
    # screen touch at the 4 corner     
    time.sleep(touchsleeptime) 
    DEV1.TouchScreen(listPhoneRes[0], 0)
    
    time.sleep(touchsleeptime) 
    DEV1.TouchScreen(listPhoneRes[0], listPhoneRes[1])
    
    time.sleep(touchsleeptime) 
    DEV1.TouchScreen(0, listPhoneRes[1])
    
    time.sleep(touchsleeptime) 
    DEV1.TouchScreen(0, 0)
    
    # check the screen alignment to Axidraw .

    
    DEV1.TouchScreen(p0[x], p0[y])
    saveCurrentPosition()
    
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p0[x] - listcurrpoint[0], p0[y] - listcurrpoint[1] , 500)
    saveCurrentPosition()
    m0 = listcurrpoint
    
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p1[x] - listcurrpoint[0], p1[y] - listcurrpoint[1] , 500)
    saveCurrentPosition()
    m1 = listcurrpoint
    
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p2[x] - listcurrpoint[0], p2[y] - listcurrpoint[1] , 500)
    saveCurrentPosition()
    m2 = listcurrpoint
    
    DEV1.TouchScreenEx(TOUCH_MOVEBY, p3[x] - listcurrpoint[0], p3[y] - listcurrpoint[1] , 500)
    saveCurrentPosition()
    m3 = listcurrpoint
    
    diffy = min (abs(p0[y] - p1[y]), abs(p3[y] - p2[y]))
    diffx = min (abs(p0[x] - p3[x]), abs(p1[x] - p2[x]))
    
    print("Algnment diffx:%s, diffy:%s"%(diffx,diffy ))
    
    
    print("screen width,height : %s, %s" %(listPhoneRes[0], listPhoneRes[1]))
    print("screen center is    : %s, %s" %(int(listPhoneRes[0]/2), int(listPhoneRes[1]/2)))

    ## close this application 
    DEV1.UIClickByName(u"coordi_x")
    time.sleep(touchsleeptime) 
    DEV1.KeyPressByAlias(u"back, back")
    time.sleep(touchsleeptime) 
    DEV1.KeyPressByAlias(u"home, home")
    
    ## save a configuration file 
    filenameconfig = dirconfig + u"\\" + DEV1.GetDeviceShellId()[1] + u".conf"
    dictconf = {}
    try:
        fconf = open(filenameconfig)
        for line in fconf :
            key,values = line.strip().split("=") 
            if len(key) == 0 : 
                continue
            listvalues = values.split(",")
            if len(listvalues) >= 2 :
                dictconf[key.strip()] = [int(aa) for aa in values.split(",")]
            else:
                dictconf[key.strip()] = int(listvalues[0])
        fconf.close()
    except: 
        print("can't open a config file :%s" % filenameconfig )
        pass

    
    listAxiRes = [ int( ScreenWidth * DEV1.rateX),  int(ScreenHeight * DEV1.rateY ) ]
    
    dictconf["listAxiRes"] = listAxiRes
    dictconf["config_pendown"] = DEV1.config_pendown
    dictconf["config_penup"] = DEV1.config_penup
    dictconf["config_penrate"] = DEV1.config_penrate
    
    fconf = open(filenameconfig, "w")
    for key_value in dictconf.items() : 
        key, value = key_value 
        if type(value) == list : 
            fconf.write("%s=%s,%s\n"%(key, value[0], value[1]))
        else:
            fconf.write("%s=%s\n"%(key, value))
    fconf.close()

