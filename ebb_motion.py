# -*- coding: utf-8 -*- 
# ebb_motion.py
# Motion control utilities for EiBotBoard
# https://github.com/evil-mad/plotink
# 
# Intended to provide some common interfaces that can be used by 
# EggBot, WaterColorBot, AxiDraw, and similar machines.
#
# Version 0.6, Dated April 2, 2016.
#
#
# The MIT License (MIT)
# 
# Copyright (c) 2016 Evil Mad Scientist Laboratories
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
For the reference of EBB command set, visit to http://evil-mad.github.io/EggBot/ebb.html
"""

from __future__ import print_function
import ebb_serial
import time

class EBB():
    def __init__(self, strPort=""):
        self.port = ebb_serial.openPort(strPort)
        if self.port == None : 
            print("Try to open port again")
            self.port = ebb_serial.openPort("")
        if self.port != None:
            print("Comport opened...")
        self.sleeptime_pen = 0.1
        self.speedlimit = float(12000)/float(1000)    # 20000 steps/500ms


    def __del__(self):
        ebb_serial.closePort(self.port)

    def version(self):
        return "0.6"    # Version number for this document

    def getEBBVersion(self):
        return ebb_serial.query(self.port, "V\r")
    # EBBv13_and_above EB Firmware Version 2.5.1
    
    def setXYSpeedLimit(self, speedlimitpersec):
        if 2 < speedlimitpersec < 24900 : 
            self.speedlimit = float(speedlimitpersec) / float(1000)
        else:
            print("speed valid speed is 2 <speed<24900 ")


    def getReset(self):
        return ebb_serial.command(self.port, "R\r")


    def getReady(self):
        if (self.port is not None):
            nRetryCount = 0
            while(nRetryCount < 100) :
                liststatus = ebb_serial.query( self.port, 'QM\r').strip().split(",")
                if liststatus[0] == "QM" and any([int(aa)for aa in liststatus[1:]]) == False:
                    return
                else:
                    time.sleep(0.1)
                    nRetryCount += 1
            print("getReady time-out")


    def getStepPosition(self, getnow=True):
        if getnow == False:
            self.getReady()
        if (self.port is not None):
            nRetryCount = 0
            while(nRetryCount < 100) :
                try:
                    liststatus = ebb_serial.query(self.port, "QS\r").split(",")
                    liststatus = [int(aa)for aa in liststatus]
                    if len(liststatus) == 2 :
                        return [(liststatus[0]+liststatus[1])//2, (liststatus[0]-liststatus[1])//2]
                except:
                    pass
                nRetryCount += 1

    def doTimedPause(self,  nPause ):
        self.getReady()
        if (self.port is not None):
            while ( nPause > 0 ):
                if ( nPause > 750 ):
                    td = int( 750 )
                else:
                    td = nPause
                    if ( td < 1 ):
                        td = int( 1 ) # don't allow zero-time moves
                ebb_serial.command( self.port, 'SM,' + str( td ) + ',0,0\r')
                nPause -= td

    def sendEnableMotors( self, Res=1 ):
        self.getReady()
        if (Res < 0):
            Res = 0
        if (Res > 5):
            Res = 5
        if (self.port is not None):
            ebb_serial.command( self.port, 'EM,' + str(Res) + ',' + str(Res) + '\r' )
            # 0: Disable motor 1
            # 1: Enable motor 1, set both motors to 1/16 step mode (default resolution upon reset)
            # 2: Enable motor 1, set both motors to 1/8 step mode
            # 3: Enable motor 1, set both motors to 1/4 step mode
            # 4: Enable motor 1, set both motors to 1/2 step mode
            # 5: Enable motor 1, set both motors to full step mode

    def sendDisableMotors( self ):
        self.getReady()
        if (self.port is not None):
            ebb_serial.command( self.port, 'EM,0,0\r')

    def QueryPRGButton( self ):
        self.getReady()
        if (self.port is not None):
            return ebb_serial.query( self.port, 'QB\r' )

    def TogglePen( self ):
        if (self.port is not None):
            ebb_serial.command( self.port, 'TP\r')
            time.sleep(self.sleeptime_pen)


    def sendPenDown( self ):
        if (self.port is not None):
            strOutput = 'SP,1' + '\r'
            ebb_serial.command( self.port, strOutput)
            time.sleep(self.sleeptime_pen)

        # Command: SP,value[,duration[,portBpin]]<CR>
        # value is either 0 or 1, indicating to raise or lower the pen.
        # duration (optional) is an integer from 1 to 65535, which gives a delay in milliseconds.
        # portBpin (optional) is an integer from 0 through 7.

        # When a value of 1 is used, : the servo_min ("SC,4") value as the 'Pen up position'
        # When a value of 0 is used, : the servo_max ("SC,5") value as the 'Pen down position'.

    def sendPenUp( self ):
        if (self.port is not None):
            strOutput = 'SP,0' + '\r'
            ebb_serial.command( self.port, strOutput)
            time.sleep(self.sleeptime_pen)

    def doXYAccelMove( self, deltaX, deltaY, vInitial=10000, vFinal=10000 ):
        self.getReady()
        # Move X/Y axes as: "AM,<initial_velocity>,<final_velocity>,<axis1>,<axis2><CR>"
        # Typically, this is wired up such that axis 1 is the Y axis and axis 2 is the X axis of motion.
        # On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
        # Note that minimum move duration is 5 ms.
        # Important: Requires firmware version 2.4 or higher.
        if (self.port is not None):
            strOutput = ','.join( ['AM', str( vInitial ), str( vFinal ), str( deltaX ), str( deltaY )] ) + '\r'
            ebb_serial.command( self.port, strOutput)

    def doXYMove( self, deltaX, deltaY, duration=500 ):
        self.getReady()
        # Move X/Y axes as: "SM,<move_duration>,<axis1>,<axis2><CR>"
        # Typically, this is wired up such that axis 1 is the Y axis and axis 2 is the X axis of motion.
        # On EggBot, Axis 1 is the "pen" motor, and Axis 2 is the "egg" motor.
        if (self.port is not None):
            strOutput = ','.join( ['SM', str( duration ), str( deltaY ), str( deltaX )] ) + '\r'
            ebb_serial.command( self.port, strOutput)

        # "SM"  Stepper Move
        # Command: SM,duration,axis1[,axis2]<CR>
        # duration is an integer in the range from 1 to 16777215, giving time in milliseconds.
        # axis1 and axis2 are integers, each in the range from -16777215 to 16777215, giving movement distance in steps.
        # If both axis1 and axis2 are zero, then a delay of duration ms is executed.
        # The minimum speed at which the EBB can generate steps for each motor is 1.31 steps/second.
        # The maximum speed is 25,000 steps/second


    def doABMove( self, deltaA, deltaB, duration=500 ):
        #print("delta : %s, %s"%(deltaA, deltaB))
        #check the speed limit .
        timeA = abs(int(float(deltaA + deltaB)/float(self.speedlimit)))
        timeB = abs(int(float(deltaA - deltaB)/float(self.speedlimit)))
        timemax = max(timeA, timeB)
        if timemax == 0 :
            return 
        
        # Issue command to move A/B axes as: "XM,<move_duration>,<axisA>,<axisB><CR>"
        # Then, <Axis1> moves by <AxisA> + <AxisB>, and <Axis2> as <AxisA> - <AxisB>
        if (self.port is not None):
            strOutput = ','.join( ['XM', str( timemax ), str( deltaA ), str( deltaB )] ) + '\r'
            self.getReady()
            ebb_serial.command( self.port, strOutput)

    def configServo(self, value1, value2):
        if ((0 < value1 < 255) == False ) :
            print("value1 is invalid ")
            return
        if ((0< value2 < 65535) == False ) :
            print("value2 is invalid ")
            return

        self.getReady()
        if (self.port is not None):
            strOutput = ','.join(['SC', str(value1), str(value2)]) + '\r'
            ebb_serial.command(self.port, strOutput)

