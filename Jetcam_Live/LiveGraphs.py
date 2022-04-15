#---------Imports
from random import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports


class LivePVals:
  """ This is a class object for generating a live graph animation"""
  def __init__(self, x_vals) -> None:
      self.figure = plt.Figure(figsize = (4, 2), dpi = 100)
      self.ax = self.figure.add_subplot(111)
      self.x_vals = x_vals 
      self.y_vals = [0 for x in range(len(x_vals))]   # x-array
      

  def animate(self, i):
      """ Used to create the bar graph """
      # update the data
      # self.y_vals = [random() for i in range(len(self.x_vals))]
      self.ax.cla()
      self.ax.axis(ymin=0, ymax=1)
      return self.ax.bar(self.x_vals, self.y_vals)

  def run_animation(self):
    # Calls animate method every 200 intervals (200 ms)
    return animation.FuncAnimation(self.figure, self.animate, interval=200, blit=True)


  def create_graph_canvas(self, parent_frame):
    """ Draws the graph on Tk canvas. """
    return FigureCanvasTkAgg(self.figure, master=parent_frame)
