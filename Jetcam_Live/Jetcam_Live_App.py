#---------Imports
from ast import mod
from importlib.util import module_for_loader
from tkinter import *
from VideoCapture import VideoCapture
from PIL import Image, ImageTk
import PIL
from threading import Thread
from LiveGraphs import LivePVals
from random import random
from Predictor import RecyclePredict
from os.path import exists
import torch
import os
#---------End of imports

RECYCLE_TYPE = ["Cardbrd", "Glass", "Metal", "Paper", "Plastic", "Trash"]

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
    
    # Create the window
    self.window = Tk()
    self.window.title("Jetcam Live")
    self.camera_src = camera_src

    ################################ Frames ###################################

    self.main_frame = Frame(self.window, padx=5 ,pady=5)
    self.video_frame = Frame(self.main_frame, pady=10, padx=10)
    self.graph_frame = Frame(self.main_frame, padx= 10)

    ############################### Create Camera Object #########################
    
    self.camera = VideoCapture(capture_src=camera_src)

    # Instatiate with no image
    self.image = None
    self.photo = None
    self.isConverted = False
    ############################### Canvases #####################################
    # Canvas for Live Camera
    self.canvas_img = Canvas(self.video_frame, width=self.camera.width, height=self.camera.height)
    self.canvas_img.pack()

    # # # Canvas for Graph
    # self.canvas_graph = PvalueGraph(x_values=RECYCLE_TYPE, y_values= [self.i for x in range(len(RECYCLE_TYPE))])
    # self.canvas_graph.show_plot(self.graph_frame)
    self.live_graph = LivePVals(RECYCLE_TYPE)
    canvas = self.live_graph.create_graph_canvas(self.graph_frame)
    canvas.get_tk_widget().pack()
    ############################### Buttons ######################################
    
    # Start and Stop Buttons Camera
    self.btn_start = Button(self.main_frame, text="Start Camera", command=self.start_camera)
    self.btn_stop = Button(self.main_frame, text="Stop Camera", command=self.stop_camera)

    # Capture Images Based on Recycling Category
    self.btn_cardboard = Button(self.main_frame, text="Cardboard")
    self.btn_paper = Button(self.main_frame, text="Paper")
    self.btn_plastic = Button(self.main_frame, text="Plastic")
    self.btn_metal = Button(self.main_frame, text="Metal")
    self.btn_glass = Button(self.main_frame, text="Glass")
    self.btn_trash = Button(self.main_frame, text="Trash")

   
    ############################### Grid Layout #################################

    self.main_frame.grid(column=0, row=0)
    self.video_frame.grid(column=0, row=0, columnspan=3, rowspan=2)
    self.graph_frame.grid(column=3, row =0, columnspan=6, rowspan=2)


    # Start and Stop Grid Location
    self.btn_start.grid(column=1, row=3)
    self.btn_stop.grid(column=2, row=3)

    # Recycle Button Categories
    self.btn_cardboard.grid(column=3, row=3)
    self.btn_paper.grid(column=4, row=3)
    self.btn_plastic.grid(column=5, row=3)
    self.btn_metal.grid(column=6, row=3)
    self.btn_glass.grid(column=7, row=3)
    self.btn_trash.grid(column=8, row=3)

    # Set Delay
    self.delay = self.camera.fps

    # Run Update Frame on Live a Thread
    camera_thrd = Thread(target=self.update_frame)
    camera_thrd.start()
    predict_thrd = Thread(target=self.update_predictions)
    predict_thrd.start()

    # This will replot the the graph every 200 ms
    ani = self.live_graph.run_animation()
    self.window.mainloop()

 ############################### Functions ###################################

  def update_frame(self):
    ret, frame = self.camera.get_frame()

    if ret:
      self.image = Image.fromarray(frame)
      self.photo = ImageTk.PhotoImage(image=self.image)
      self.isConverted = True

      self.canvas_img.create_image(0, 0, image=self.photo, anchor="nw")


      # # This is to generate random live y_vals for now
      # self.live_graph.y_vals = [random() for i in range(len(RECYCLE_TYPE))]
     
      if self.camera.is_running:
        self.window.after(self.delay, self.update_frame)

  def update_predictions(self):
    
    if self.isConverted:
      self.image = self.model.preprocess_image(self.image)
      probs = self.model.get_probabilities(self.image)
      prediction = self.model.get_prediction()
      print("Probs")
      print(probs)
      print("Prediction:")
      print(prediction)
      
    self.isConverted = False

    if self.camera.is_running:
      self.window.after(self.delay + 100, self.update_predictions)

        
  def start_camera (self):
    if not self.camera.is_running:
      self.camera.is_running = True
      # Thread(target=self.update_frame).start()
     
  def stop_camera(self):
    if  self.camera.is_running:
      self.camera.is_running = False

path = "/home/cs5500/recycle-ai-neu/data/resnet18_recycle_train.pth"

App(trained_file_path=path)
os._exit(0)