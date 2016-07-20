from SelectaBakeOut import SelectaBakeOut
from datetime import datetime
from time import sleep
import time
import sys

selCom = SelectaBakeOut("/dev/ttyUSB0")
fileNameInit = "logFile"
targetTemperature = 55

if len(sys.argv)==3:
    filenNameInit = sys.argv[1]
    targetTemperature = int(sys.argv[2])
else:
    fileNameInit = raw_input("Enter Log File Name: ")
    targetTemperature = input("Enter target Temperature: ")


incrementStepList = [12]
minimumTemperature = 30
secondsInAMinute = 60
secondsInAnHour = 3600
currentTemperature = selCom.getCurrentTemperature()

print "Initial Temperature is:", currentTemperature, "\t and the introduced target temperature is: ", targetTemperature

selCom.getSelectaStatus()
selCom.setSelectaTemperatureOn()

for incrementStep in incrementStepList:
    if selCom.getSelectaStatus() != "STPT":
        selCom.setSelectaTemperatureOn()
    fileName = "step" + str(incrementStep) + fileNameInit
    print "Openning Log File Named: "+ fileName
    logFile = open(fileName,"w")
    selCom.setProgrammedTemperature(minimumTemperature)
    while(currentTemperature > minimumTemperature):
        currentTemperature = selCom.getCurrentTemperature()
        sleep(60.0)
        print "I'm cooling down to ", str(minimumTemperature), " degrees, now I'm at ", currentTemperature, " degrees, too hot still!"

    print "Temperature is equal or below the minimum, let's ramp it up now dude!"

    while currentTemperature < targetTemperature:
        secondsPast = time.time()
        nextTemperature = currentTemperature + incrementStep
        selCom.setProgrammedTemperature(int(nextTemperature))
        while secondsPast + secondsInAMinute > time.time():
            fileLine = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t"+str(selCom.getProgrammedTemperature())+"\t"+str(selCom.getCurrentTemperature())+"\n"
            print(fileLine)
            logFile.write(fileLine)
            sleep(1.0)
            currentTemperature = selCom.getCurrentTemperature()
            print "Current Temperature is: ", currentTemperature
    
    print "Temperature is now equal target"
    selCom.setProgrammedTemperature(targetTemperature)
    
    while secondsPast + (secondsInAnHour * 2) > time.time():
        secondsPast = time.time()
        fileLine = datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\t"+str(selCom.getProgrammedTemperature())+"\t"+str(selCom.getCurrentTemperature())+"\n"
        print(fileLine)
        logFile.write(fileLine)
        sleep(60.0)
        currentTemperature = selCom.getCurrentTemperature()
     
     
    print "Two hours went by, now I'm done!"
    selCom.setProgrammedTemperature(minimumTemperature)        
    
    print "Closing Log File"
    logFile.close()

print "Finishing the whole script now, took a while, right?"
selCom.closeCommunication()