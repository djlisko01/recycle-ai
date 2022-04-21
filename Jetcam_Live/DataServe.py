import json
from wsgiref.util import request_uri
from importlib_metadata import pass_none
from numpy import index_exp
import requests
import os

class DataServe:

  RECYCLE_KEY = {"Cardbrd": "field1", "Glass": "field2", "Metal": "field3", "Paper": "field4", "Plastic": "field5", "Trash": "field6"}

  def __init__(self) -> None:
    self.data = None
    self.url = None
    self.dir = None

  
  def PostThingSpeak(self, prediction, index):
    """ Sends Prediction to Thingspeak"""
    print(self.RECYCLE_KEY[prediction])
    url_update =  f"https://api.thingspeak.com/update?api_key=AM4R84IBHPIZNFLY&{self.RECYCLE_KEY[prediction]}=1"
    url_exe_cmnd = f"https://api.thingspeak.com/talkbacks/45743/commands.json?api_key=3MXD0NIV0W0VDVYM&command_string={index}"
    requests.post(url_update)
    requests.post(url_exe_cmnd)
    print("Sent to thingspeak...")


# if __name__ == "__main__":
# #   test = "Cardbrd"
#   data_server = DataServe()

#   for i in range(6):
#     data_server.PostThingSpeak("Glass", i)