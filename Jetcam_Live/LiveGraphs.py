#---------Imports
from random import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#---------End of imports


class LivePVals:
  def __init__(self, x_vals) -> None:
      self.figure = plt.Figure(figsize = (4, 2), dpi = 100)
      self.ax = self.figure.add_subplot(111)
      self.x_vals = x_vals 
      self.y_vals = 0     # x-array
      

  def animate(self, i):
      # update the data
      # self.y_vals = [random() for i in range(len(self.x_vals))]
      self.ax.cla()
      self.ax.axis(ymin=0, ymax=1)
      return self.ax.bar(self.x_vals, self.y_vals)

  def run_animation(self):
    return animation.FuncAnimation(self.figure, self.animate, interval=200, blit=True)


  def create_graph_canvas(self, parent_frame):
    return FigureCanvasTkAgg(self.figure, master=parent_frame)
