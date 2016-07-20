import serial
from time import sleep

class SelectaBakeOut:
    "Selecta's bake out oven interface for RS232 communications"
    
    def __init__(self, deviceLabel):
        
        self._port = serial.Serial(deviceLabel, 
                     baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.SEVENBITS,
                     writeTimeout = 0,
                     timeout = 10,
                     rtscts=False,
                     dsrdtr=False,
                     xonxoff=False)   
        
        if self._port.isOpen():
            print "\nPort is Open, that's a start, right? \n"
        else:
            print "\nPor isn't Open, nothing good is expected, get home and cry, bitch! \n"      
     
    def setSelectaOn(self):
        instruction = "#01RUN"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta is ON now, YAY! \n"
        else:
            print "Could NOT set Selecta ON, NAY! \n"

    def setSelectaOff(self):
        instruction = "#01STOP"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta is OFF now, YAY! \n"
        else:
            print "Could NOT set Selecta OFF, NAY! \n"   
    
    def setSelectaTemperatureOn(self):
        instruction = "#01RUNT"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta Temperature is ON now, YAY! \n"
        else:
            print "Could NOT set Selecta Temperature ON, NAY! \n"
    
    def setSelectaPressureOn(self):
        instruction = "#01RUNP"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta Pressure is ON now, YAY! \n"
        else:
            print "Could NOT set Selecta Pressure ON, NAY! \n"
            
    def setSelectaTemperatureOff(self):
        instruction = "#01STOPT"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta Temperature is OFF now, YAY! \n"
        else:
            print "Could NOT set Selecta Temperature OFF, NAY! \n"
    
    def setSelectaPressureOff(self):
        instruction = "#01STOPP"
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Selecta Pressure is OFF now, YAY! \n"
        else:
            print "Could NOT set Selecta Pressure OFF, NAY! \n"
            
    def getSelectaStatus(self):
        instruction = "#01RUN?"
        instruction = self._instructionExchange(instruction)
        cmd = instruction[3:7]
        if cmd == "STPT":
            print "Selecta Temperature is STOPPED \n"
        elif cmd == "STPP":
            print "Selecta Pressure is STOPPED \n"
        elif cmd == "RUNT":
            print "Selecta Temperature is RUNNING \n"
        elif cmd == "RUNP":
            print "Selecta Pressure is RUNNING \n"
        elif cmd == "ALAR":
            print "Selecta is in ALARM Status OMG! \n"
        elif cmd == "STBY":
            print "Selecta is in STANDBY time \n"
        return cmd
    
    def getCurrentTemperature(self):
        instruction = "#01PVT?"
        instruction = self._instructionExchange(instruction)
        return float(instruction[4:7])
        
    def getProgrammedTemperature(self):
        instruction = "#01SVT?"
        instruction = self._instructionExchange(instruction)
        return float(instruction[4:7])
    
    def setProgrammedTemperature(self, temperature):
        instruction = "#01SVT +"+str(temperature).zfill(3)
        instruction = self._instructionExchange(instruction)
        if instruction[3:5]=="OK":
            print "Programming Temperature went just FINE \n"
        else:
            print "Something WRONG with Programming Temperature \n"
    
    def _lrcCalculation(self, inputString):
        num = 0
        for ch in inputString:
            num += ord(ch)
        d = 0xFF - int(hex(num)[-2:],16) + 1
        outputString  = hex(d)[-2:]
        return outputString
    
    def _sendMessage(self, message):
        #print "Sent message is: ", message
        self._port.write(message)
    
    def _receiveMessage(self):
        message = self._port.readline()
        #print "Received message is: ", message
        return message
    
    def _instructionExchange(self, instruction):
        instruction = instruction + self._lrcCalculation(instruction) + "\r\n"
        self._sendMessage(instruction)
        instruction = self._receiveMessage()
        return instruction
        
    def closeCommunication(self):
        self._port.close()
        print "Closing communications, leamme alone now, was about that time! \n"
        
            
        
if __name__ == '__main__':
    
	        
    selCom = SelectaBakeOut("/dev/ttyUSB0")
    
    selCom.getSelectaStatus()

    #targetTemperature = input("Type target temperature: ")
    
    #selCom.setProgrammedTemperature(targetTemperature)

    print "CURRENT TEMPERATURE: ", selCom.getCurrentTemperature(),"\n"
    
    print "CURRENT PROGRAMMED TEMPERATURE: ", selCom.getProgrammedTemperature(),"\n"
    
    selCom.setSelectaTemperatureOff()
    
    selCom.closeCommunication()
    
