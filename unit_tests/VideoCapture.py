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

  def save_img(self, path, img_name):

    try:    
      if img_name == "Cardbrd":
        img_name = "cardboard"

      img_name = img_name.lower()

      if img_name not in os.listdir(path):
        os.mkdir(path + "/" + img_name)

      # Keep iterating until a file name is available.
      i = 1
      filename = path + "/" + img_name + "/" + "LIVE_IMG_" + img_name  + str(i) + ".jpg"
      if self.ret:
        # Checks if filename already exists
        while os.path.exists(filename):
          i += 1
          filename = path + "/" + img_name + "/" + "LIVE_IMG_" + img_name  + str(i) + ".jpg"
        print(filename)
        cv2.imwrite(filename, self.frame)

    except NotADirectoryError:
      print(path)


  def __del__(self):
    """ Releases the camera when the program is closed """
    if self.is_running:
      self.is_running = False
    
    if self.capture.isOpened():
      self.capture.release()
