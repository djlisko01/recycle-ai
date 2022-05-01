#---------Imports
from tkinter import *
from VideoCapture import VideoCapture
from PIL import Image, ImageTk
from threading import Thread
from LiveGraphs import LivePVals
from random import random
from Predictor import RecyclePredict
from os.path import exists
import time
import os
import DataServe
import numpy
#---------End of imports

RECYCLE_TYPE = ["Cardbrd", "Glass", "Metal", "Paper", "Plastic", "Trash"]
IMG_SAVE_PATH = "../data/camera_pictures"

class App:
  """ This will run an application that provides a live video feed, 
  a graph with real time probability predictions and the prediction for recycling waste. 
  This also allows adminstrators to take a snap shot of a miscategorized item, which can be used
  to furhter improve predicitons.
  """
  def __init__(self, trained_file_path, camera_src = 0) -> None:

    ################################ Load the Trained Dataset #########################

    self.model = RecyclePredict()

    if exists(trained_file_path):

      self.model.prep_model(RECYCLE_TYPE) # Loads the ResNet that the model was trained on
      self.model.load_trained_model(trained_file_path) # Loads the trained Model

      # Running this does a test prediction before loading the full application.
      # The first predicition takes ~ 2 mins, but then drastically speeds up to about 0.05 seconds per prediction.
      self.model.test_predict()

    else:
      print("Trained File Path doesn't exist...")
      print("Quiting Program")
      os._exit(0)
    

    ###################### Create Window and Check Camera Source ##################

    # Create the window
    self.window = Tk()
    self.window.title("Jetcam Live")
    self.camera_src = camera_src

    self.temp_y = [0 for i in range(len(RECYCLE_TYPE))]

    ################################ Frames ######################################

    self.video_frame = Frame(self.window, pady=10, padx=10, bg="#6c757d")
    self.graph_frame = Frame(self.window, pady=20, padx= 10,  bg="#6c757d")
    self.btn_frame_save = Frame(self.graph_frame, pady=10,  bg="#6c757d")
 
    ############################### Create Camera Object #########################
    
    self.camera = VideoCapture(capture_src=camera_src)

    # Instatiate with no image
    self.image = None
    self.photo = None
    self.isConverted = False
    
    ############################### Canvases #####################################
    # Canvas for Live Camera
  
    self.canvas_img = Canvas(self.video_frame, width=self.camera.width, height=self.camera.height)
    self.canvas_img.pack(fill="both", expand=True)

    # Canvas for Graph
    # self.canvas_graph = PvalueGraph(x_values=RECYCLE_TYPE, y_values= [self.i for x in range(len(RECYCLE_TYPE))])
    # self.canvas_graph.show_plot(self.graph_frame)
    self.live_graph = LivePVals(RECYCLE_TYPE)
    canvas = self.live_graph.create_graph_canvas(self.graph_frame)
    # canvas.get_tk_widget().grid(column=0, row=0, columnspan=6)
    canvas.get_tk_widget().pack(fill="both", expand=True)


    ############################### Buttons ######################################
    
    # Start and Stop Buttons Camera
    self.make_pred_btn = Button(self.video_frame, text="Make Prediction", command=self.send_prediction, font="Times 10 bold")
    self.make_pred_btn.pack(pady=10, fill="both")
  
    # # Capture Images Based on Recycling Category
    def save_buttons(col_i = 0, row_i=1):
      for item in RECYCLE_TYPE:
  
        self.photo_save_btn = Button(self.btn_frame_save, text = item, 
            command= lambda x = item: Thread(self.save_images(x)).start(), font="Times 10 bold")
        self.photo_save_btn.grid(column=col_i, row=row_i, pady=10, padx=5)
        col_i += 1

    save_buttons()

    ############################### Grid Layout #################################

    # self.main_frame.grid(column=0, row=0)
    self.video_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky="NSEW")
    self.graph_frame.grid(column=3, row =0, columnspan=len(RECYCLE_TYPE), rowspan=2, sticky="NSEW")
    
    # Add the save buttons below the graph
    self.btn_frame_save.pack()

    # This will adjust the size of the frames -> causing the graph/image to resize in response.
    self.window.rowconfigure(0, weight=1)
    self.window.rowconfigure(1, weight=1)
    self.window.columnconfigure(0, weight=1)
    self.window.columnconfigure(3, weight=1)


    # Set Delay
    self.delay = self.camera.fps

    ############################### Threading #################################

    # Run Update Frame on Live a Thread
    camera_thrd = Thread(target=self.update_frame)
    camera_thrd.start()
    predict_thrd = Thread(target=self.update_predictions)
    predict_thrd.start()

    # This will replot the the graph every 200 ms
    ani = self.live_graph.run_animation()
    self.window.bind("<Return>", self.send_prediction)
    self.window.mainloop()

 ############################### Functions ###################################

  def update_frame(self):
    ret, frame = self.camera.get_frame()

    if ret:
      self.image = Image.fromarray(frame) # Convert Numpy Array to PIL image

      width = self.canvas_img.winfo_width()
      height = self.canvas_img.winfo_height()

      self.image = self.image.resize((width, height))
      
      self.photo = ImageTk.PhotoImage(image=self.image) 
      self.isConverted = True

      self.canvas_img.create_image(0, 0, image=self.photo, anchor="nw")
      self.temp_y = [random() for x in range(len(RECYCLE_TYPE))]

      if not self.camera.is_running:
        time.sleep(3)
        self.camera.is_running = True
    
      self.window.after(self.delay, self.update_frame)

  def update_predictions(self):
    
    if self.isConverted:
      # self.live_graph.y_vals = self.temp_y
      # self.pred_i = numpy.argmax(self.temp_y)
      # prediction  = RECYCLE_TYPE[self.pred_i]
      # print(prediction)
      self.image = self.model.preprocess_image(self.image)
      probs = self.model.get_probabilities(self.image)
      self.pred_i = self.model.get_prediction()
      print("Probs")
      self.live_graph.y_vals = probs
      print("Prediction:")
      prediction = RECYCLE_TYPE[self.pred_i]
      print(prediction)

    self.isConverted = False
    self.window.after(self.delay + 100, self.update_predictions)

  def save_images(self, item):
    self.camera.save_img(IMG_SAVE_PATH, item)
    time.sleep(2)

  def send_prediction (self, e=None):
    if self.camera.is_running:
      self.camera.is_running = False

      # Send Prediciton to thingspeak
      prediction = RECYCLE_TYPE[self.pred_i]
      data_send = DataServe.DataServe()
      data_send.PostThingSpeak(prediction, self.pred_i)
      print("Prediction Sent:", prediction)

# Original Path:
# path = "/home/cs5500/recycle-ai-neu/data/resnet18_recycle_train.pth"

# New Larger Dataset:
path = "../data/resnet18_recycle_train_2022-04-23.pth"

if __name__ == "__main__":
  App(trained_file_path=path)
  os._exit(0)