# -*- coding: utf-8 -*-

import time
from datetime import datetime
import sys
sys.path.append(".\\\\Test Scenarios")
import Touchtune

listmodename = [u"쉬프트",u"언어 변경", u"쉬프트",u"언어 변경", u"쉬프트",  u"숫자 및 기호", u"쉬프트", u"문자" , u"쉬프트"]
def touchingCharAtSoftkeypad(char):
    nRetryCount = 0
    while(nRetryCount < 16 ) :
        rc = DEV1.UIClickByText(char, 0, UITarget.SoftKeyPad)
        if rc == AT_SUCCESS : 
            break
        else:
            if char == "0" : 
                rc = DEV1.UIClickByText("0+", 0, UITarget.SoftKeyPad)
                if rc == AT_SUCCESS : 
                    break
                
            # change input mode and try again .
            indexmode = (nRetryCount ) % (len(listmodename))
            nRetryCount += 1
            
            print(listmodename[indexmode])
            rc1, result = DEV1.UIGetObjectByDescription(listmodename[indexmode], 0, UITarget.SoftKeyPad )
            
            if rc1 == AT_SUCCESS : 
                x, y = result.GetCenterCoords()
                DEV1.TouchScreen(x, y)
                time.sleep(0.2)
                continue  
    return rc



def touchingStringAtSoftkeypad(str):
    for char in str :
        if char == u" " : 
            DEV1.UIClickByDescription(u"띄어쓰기", 0, UITarget.SoftKeyPad)
            continue
        
        rc = touchingCharAtSoftkeypad(char)
            
        
        
def TestMain():
    
    #Touchtune.TestMain()
    
    DEV1.KeyPressByAlias(u"home, home")
    
    
    looptotal = 150
    
    while(looptotal > 0 ) :
        
        DEV1.UIClickByText(u"Chrome")  
        nRetryCount = 5
        coordiScreenUp = (int(DEV1.MainScreen.Width / 2),  400 ) 
        coordiScreenDown = (int(DEV1.MainScreen.Width / 2), DEV1.MainScreen.Height - 400 )
        while(nRetryCount > 0 ) : 
            #scroll up 
            DEV1.UIDrag(coordiScreenDown[0], coordiScreenDown[1], coordiScreenUp[0], coordiScreenUp[1], 1)
            DEV1.UIDrag(coordiScreenDown[0], coordiScreenDown[1], coordiScreenUp[0], coordiScreenUp[1], 1)
              
            # scroll down
            DEV1.UIDrag(coordiScreenUp[0], coordiScreenUp[1], coordiScreenDown[0], coordiScreenDown[1], 1)
            DEV1.UIDrag(coordiScreenUp[0], coordiScreenUp[1], coordiScreenDown[0], coordiScreenDown[1], 1)
            nRetryCount -= 1 
    
    
        DEV1.KeyPressByAlias(u"home, home")
        time.sleep(2)
        
                
        
        listcontact = [
            [u"loj dddd aatya", u"12323450202"],
            [u"ccc jkfudj plpl", u"08023454455"],
            [u"ddd YYYY lml", u"12344448483"],
            [u"bhygf LLL piou", u"08033334455"],
            [u"lkol PPP po9o", u"12312125656"]
            ]
        
        DEV1.UIClickByText(u"주소록")  
        time.sleep(0.5)
        
        for contact in listcontact : 
            DEV1.UIClickByName("add_contact_button")                  
            time.sleep(0.5)
            
            DEV1.UIClickByHint(u"이름")
            time.sleep(0.5)
            
            touchingStringAtSoftkeypad(contact[0])
            
            
            DEV1.UIClickByHint(u"전화번호")
            time.sleep(0.5)
            
            touchingStringAtSoftkeypad(contact[1])
            
            DEV1.UIClickByText(u"저장")  
            time.sleep(0.5)
            
            DEV1.UIClickByDescription(u"상위 폴더로")
            time.sleep(0.5)
        
        # 전체 지우기
        
        DEV1.UIClickByDescription(u"옵션 더보기")
        time.sleep(0.5)
        
        DEV1.UIClickByText(u"삭제")  
        time.sleep(0.5)
        
        DEV1.UIClickByName("all_selectable_button")                  
        time.sleep(0.5)
         
        DEV1.UIClickByText(u"삭제")  
        time.sleep(0.5)
        
        DEV1.UIClickByText(u"삭제")  
        time.sleep(0.5) 
        
        
        DEV1.KeyPressByAlias(u"home, home")
        time.sleep(2)
    
        for j in range(2) : 
            # 사진 촬영.    
            for i  in range(2) : 
                #DEV1.RunApplication(u"카메라", u"")
                DEV1.UIClickByText(u"카메라")  
                time.sleep(3)
             
                DEV1.UIClickByName("shutter_bottom_comp_type")                  
                time.sleep(3)
                 
                DEV1.UIClickByName("shutter_bottom_comp_type")
                time.sleep(3)
             
                DEV1.UIClickByName("back_button")
                time.sleep(3)
                
            # 사진 지우기
            # 캘러리 기동
            DEV1.UIClickByText(u"갤러리") 
            time.sleep(3)
            # 맨 위 카메라 선택
            DEV1.UIClickByText(u"카메라")
            time.sleep(3)
            #삭제 선택
            DEV1.UIClickByDescription(u"삭제")
            time.sleep(3)
            # 모두 삭제 체크박스선택 
            DEV1.UIClickByText(u"모두 선택")
            time.sleep(3)
            # 삭제 글자 선택
            DEV1.UIClickByText(u"삭제")
            time.sleep(3)
            # 다시 확인
            DEV1.UIClickByText(u"삭제")
            time.sleep(3)
            
            DEV1.KeyPressByAlias(u"back, back")
            time.sleep(3)
                
    
        
        
        # 동영상 촬영.    
    #     for i  in range(1) : 
    #         #DEV1.RunApplication(u"카메라", u"")
    #         DEV1.UIClickByText(u"카메라")  
    #         time.sleep(3)
    #     
    #         DEV1.UIClickByName("shutter_top_comp")                  
    #         time.sleep(3)
    #         
    #         DEV1.UIClickByName("shutter_top_comp")
    #         time.sleep(3)
    #     
    #         DEV1.UIClickByName("back_button")
    #         time.sleep(3)
        
        looptotal -= 1 
		#print("looptotal : %s"%looptotal)
    
    
    result = DEV1.KeyPressByAlias(u"home, home")
    

    System.Finish(result, "message")
    exit()

