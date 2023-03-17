import serial.tools.list_ports
from utils.globals import *

class Serial:
  ser = None
  port = ''
  baudrate = 0
  isConnectedToPort = False
  
  def __init__(self) -> None:
    self.ser = None
    self.port = ''
    self.baudrate = 115200
    self.isConnectedToPort = False

  def setPort(self):
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
      port = ports[i]
      strPort = str(port)
      if "CP210x" in strPort:
        splitPort = strPort.split(" ")
        commPort = (splitPort[0])
    if commPort == 'None':
      self.port = 'COM5'
    else:
      self.port = commPort
    
  def setSerial(self, port, baudrate=115200):
    if port != '' and port != None:
      self.ser = serial.Serial(port=port, baudrate = baudrate or self.baudrate, timeout=0)
      self.isConnectedToPort = True
      print('Connected to ' + port)
    elif self.port != '' and self.port != None:
      self.ser = serial.Serial(port=port, baudrate = baudrate or self.baudrate, timeout=0)
      self.isConnectedToPort = True
      print('Connected to ' + self.port)
    else:
      print('Failed to initial serial. Please make sure that MCU was plugged in.')
  
  def getPort(self):
    return self.port
  
  def getSerial(self):
    return self.ser

  def write(self, data):
    self.ser.write(data)

  def read(self, bytesToRead):
    return self.ser.read(bytesToRead).decode("UTF-8")
  
  def inWaiting(self):
    return self.ser.inWaiting()
  
  def isComConnected(self):
    return self.isConnectedToPort