import bpy as b
import numpy as np
from scipy.spatial.transform import Rotation
from time import time,sleep
import json
import os

class Scene:
  def __init__(self):
    self.active_objs = dict()
    self.scene_path = ''
    self.timestep = 1/240.
    self.actions = list()
    
  def __del__(self):
    del self.active_objs
    pass

  def update(self):
    if not self.running: return

    if self.actions:
        fun,args = act = self.actions[0]
        fun(*args)
        self.actions.pop(0)

    for obj in self.active_objs.values():
      obj.update(self.timestep)