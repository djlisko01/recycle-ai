#---------Imports
import cv2
import os
import time
#---------End of imports

class VideoCapture:
  

  def __init__(self, width=224, height=224, capture_src = 0, fps=30) -> None:
    """This Creates a Video Capture Object, which will set up the camera
     with a height, width and capture rate (in fps) """
    # Open the video source
    self.capture = cv2.VideoCapture(capture_src)
    self.is_running = True

    # Camera Attributes
    self.width=width
    self.height=height
    self.fps = fps

    # Default Start values
    self.ret = False
    self.frame = None

  def get_frame(self):
    """ This will return the frame and if boolean of weather there's an image or not """
    self.process()
    return self.ret, self.frame

  
  def process(self):

    """ Processes a live feed if the camera is running """

    if self.is_running:
      # Capture the video frame
      ret, frame = self.capture.read()

      if ret:
        frame = cv2.resize(frame, (self.width, self.height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      
      else:
        print("[Video Capture Failed] stream end")
        self.is_running = False
      
      self.ret = ret
      self.frame = frame
      time.sleep(1/self.fps)

  def __del__(self):
    """ Releases the camera when the program is closed """
    if self.is_running:
      self.is_running = False
    
    if self.capture.isOpened():
      self.capture.release()
