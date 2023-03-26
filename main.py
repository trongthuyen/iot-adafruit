from datetime import datetime
import time
from utils.configs import *
import utils.globals as g
from Controllers.SerialController import SerialController
from Controllers.AIOController import AIOController

def main():
  RootSerial = SerialController()
  RootSerial.subscribe()
  
  feeds = [
    FEED_INTENSITY,
    FEED_LED,
    FEED_TEMP,
    FEED_ACK
  ]
  
  RootAIO = AIOController(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY, feeds=feeds, serial=RootSerial)
  
  isRead = 500
  timeResend = 0
  numOfResend = 0
  isSleep = False
  timeSleep = 0
  numOfSleep = 0
  
  RootAIO.client.on_connect = RootAIO.connect
  RootAIO.client.on_disconnect = RootAIO.disconnected
  RootAIO.client.on_message = RootAIO.message
  RootAIO.client.on_subscribe = RootAIO.subscribe
  RootAIO.client.connect()
  RootAIO.client.loop_background()
    
  while True:
    if RootAIO.serial.isComConnected():
      if isRead == 0 and g.lastSendOk:
        if RootAIO.serial.readSerial():
          RootAIO.publishData(RootAIO.serial.getData(), False)
          isRead = g.TIME_TO_READ
          g.lastSendOk = False
          RootAIO.serial.setSavedData(RootAIO.serial.getData())
          RootAIO.serial.setData('')
          timeResend = g.TIME_TO_RESEND
          numOfResend = 0
          numOfSleep = 0
        else:
          if RootAIO.serial.getReRead() == 0:
            RootAIO.serial.setIsGetData(True)

      # resend after g.TIME_TO_RESEND (ms)
      if not g.lastSendOk and timeResend == 0 and not isSleep:
        timeResend = g.TIME_TO_RESEND
        RootAIO.publishData(RootAIO.serial.getSavedData(), True)
        numOfResend += 1
        print("Resend " + str(RootAIO.serial.getSavedData()) + " =+= " + str(numOfResend) + " times")
          
      # after resend g.MAX_NUM_OF_RESEND times, change system to sleep g.TIME_SLEEP (ms)
      # stop resending
      if not g.lastSendOk and numOfResend >= g.MAX_NUM_OF_RESEND:
        isSleep = True
        timeSleep = g.TIME_SLEEP
        numOfResend = 0
        print(str(g.MAX_NUM_OF_RESEND) + " times resend failed. Stop resending!")
      
      # after sleep g.TIME_SLEEP (ms), countinue resend again
      if not g.lastSendOk and timeSleep == 0 and isSleep:
        isSleep = False
        numOfSleep += 1
        timeResend = 0
      
      # after sleep g.MAX_NUM_OF_SLEEP (ms), skip resend data, begin change to send new data
      if not g.lastSendOk and numOfSleep >= g.MAX_NUM_OF_SLEEP:
        g.lastSendOk = True
        timeSleep = 0
        timeResend = 0
        isSleep = False
        numOfResend = 0
        numOfSleep = 0
        RootAIO.serial.setSavedData("")
        print("Send data failed. Skip data this time!")
      
      if isRead > 0:
        isRead -= 1
      if timeResend > 0:
        timeResend -= 1
      if timeSleep > 0:
        timeSleep -= 1
      if RootAIO.serial.getReRead() > 0:
        RootAIO.serial.setReRead(RootAIO.serial.getReRead() - 1)
      time.sleep(0.001)
    else:
      print("None serial port !!!")


if __name__ == "__main__":
  main()
