import sys
from Adafruit_IO import MQTTClient
from utils.configs import *
import utils.globals as g

class AIOController:
  feeds = []
  client = None
  ADAFRUIT_IO_USERNAME = ""
  ADAFRUIT_IO_KEY = ""
  serial = None
  
  def __init__(self, username, key, feeds, serial) -> None:
    self.feeds = feeds
    self.ADAFRUIT_IO_USERNAME = username
    self.ADAFRUIT_IO_KEY = key
    self.client = MQTTClient(username=username, key=key)
    self.serial = serial
  
  def connect(self, client):
    for feed in self.feeds:
      client.subscribe(feed)
      print(f'Connected to {feed}')
  
  def subscribe(self, client, userdata, mid, granted_qos):
    print("Subscribed successful!")
  
  def disconnected(self, client):
    print("Disconnected from Adafruit IO!")
    sys.exit(1)

  def message(self, client, feed_id, payload):
    g.lastSendOk = True
    if feed_id == FEED_TEMP or feed_id == FEED_INTENSITY:
      print(feed_id + " received ACK: " + payload)
    elif feed_id == FEED_LED:
      print("!L:"+payload+"#")
      self.serial.writeSerial("!L:"+ payload + "#")

  def publishData(self, data, flagSendAgain):
    data = data.replace(g.START_CHAR, "")
    data = data.replace(g.END_CHAR, "")
    splitData = data.split(";")
    for i in range(1, len(splitData)):
      splitData[i] = splitData[i].split(":")
    if not flagSendAgain:
      print("Publish new: STT:" + str(data))

    for element in splitData:
      if len(element) > 1:
        separate = element.find(g.SEPARATE)
        if separate != -1:
          if element[0] == "T":
            self.client.publish(FEED_TEMP, element[separate + 1 :])
            # print("T", element[1])
          if element[0] == "I":
            self.client.publish(FEED_INTENSITY, element[separate + 1 :])
            print(element[separate + 1 :])
          if element[0] == "L":
            self.client.publish(FEED_LED, element[separate + 1 :])
            # print("T", element[1])
