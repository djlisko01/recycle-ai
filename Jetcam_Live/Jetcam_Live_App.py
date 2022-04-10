from concurrent.futures import thread
from tkinter import *
from tkinter import ttk
import cv2
from VideoCapture import VideoCapture
from PIL import Image, ImageTk
from threading import Thread
from LiveGraphs import LivePVals
from matplotlib.animation import FuncAnimation
from random import random
from matplotlib.animation import FuncAnimation


RECYCLE_TYPE = ["Cardboard", "Plastic", "Paper", "Glass", "Garbage", "Metal"]
class App:

  def __init__(self, camera_src = 0) -> None:
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

    threads = []
    # Run Update Frame on Live a Thread
    camera_thrd = Thread(target=self.update_frame)
    camera_thrd.start()


    ani = self.live_graph.run_animation()
    self.window.mainloop()

 ############################### Functions ###################################

  def update_frame(self):
    ret, frame = self.camera.get_frame()

    if ret:
      self.image = Image.fromarray(frame)

      self.photo = ImageTk.PhotoImage(image=self.image)
      self.canvas_img.create_image(0, 0, image=self.photo, anchor="nw")

      if self.camera.is_running:

        #ToDo -> Add image processing.
        self.live_graph.y_vals = [random() for i in range(len(RECYCLE_TYPE))]
        self.window.after(self.delay, self.update_frame)

  def start_camera (self):

    if not self.camera.is_running:
      self.camera.is_running = True
      Thread(target=self.update_frame).start()
     

  def stop_camera(self):
    if  self.camera.is_running:
      self.camera.is_running = False


App()