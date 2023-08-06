
import pygame_gui
from pygame_gui.elements import *
import sys


def gui():
  global ui 
  mod = sys.modules['__main__']
  ui = pygame_gui.UIManager((mod.WIDTH, mod.HEIGHT))
  return ui