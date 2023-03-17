from Models.Serial import Serial
from utils.globals import *

class SerialController:
  serial = None
  isGet = True
  data = ''
  savedData = ''
  reRead = 0
  
  def __init__(self) -> None:
    self.serial = Serial()
    self.isGet = True
    self.data = ''
    self.savedData = ''
    self.reRead = 300
  
  def subscribe(self):
    self.serial.setPort()
    self.serial.setSerial(self.serial.getPort())
  
  def publish(self, data):
    pass
  
  def isComConnected(self):
    return self.serial.isConnectedToPort

  def writeSerial(self, message):
    self.serial.write(message.encode())

  def readSerial(self):
    if self.isGet == True:
      # self.serial.write(GOT_MSG.encode())
      self.isGet = False
      self.reRead = TIME_TO_RE_READ_SERIAL
    bytesToRead = self.serial.inWaiting()
    message = self.serial.read(bytesToRead)
    
    if message:
      print(f'MCU recieved: {message}')
      
    start = message.find(START_CHAR)
    end = message.find(END_CHAR)
    if start == -1 or end == -1:
      return False
    self.data = message[start : end + 1]
    # while end < ( bytesToRead - 1):
    #   bytesToRead -= end
    #   message = message[end + 1 :]
    #   start = message.find(START_CHAR)
    #   end = message.find(END_CHAR)
    #   self.data += message[start : end + 1]
    message = ''
    self.isGet = True
    return True

  def getData(self):
    return self.data

  def getSavedData(self):
    return self.savedData
  
  def setSavedData(self, data):
    self.savedData = data
  
  def setData(self, data):
    self.data = data

  def setIsGetData(self, isGet):
    self.isGet = isGet
  
  def isGetData(self):
    return self.isGet
  
  def getReRead(self):
    return self.reRead
  
  def setReRead(self, timeToReRead):
    self.reRead = timeToReRead