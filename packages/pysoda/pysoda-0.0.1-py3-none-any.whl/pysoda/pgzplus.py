#import math
#from msilib.schema import Class
#from turtle import Screen
from msilib.schema import Class
import pgzrun
import pygame
#from pgzero import game, loaders
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor
from pgzero.runner import main
import sys
#import os
#import time
import pygame_gui
from pygame_gui.elements import *

full_screen = False
TITLE = "Soda"
ui = pygame_gui.UIManager((800, 600))

def gui():
  global ui 
  mod = sys.modules['__main__']
  ui = pygame_gui.UIManager((mod.WIDTH, mod.HEIGHT))
  
def fullscreen():
  global full_screen
  mod = sys.modules['__main__']
  mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT), pygame.FULLSCREEN)
  full_screen = True

def window():
  global full_screen
  mod = sys.modules['__main__']
  mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT))
  full_screen = False
  
def set_fullscreen(self,full):
  global full_screen
  global mod 
  if full:
    mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT), pygame.FULLSCREEN)
  else:
    mod.screen.surface = pygame.display.set_mode((mod.WIDTH, mod.HEIGHT), pygame.FULLSCREEN)
  full_screen = full

  
def mouse_off():
  pygame.mouse.set_visible(False)

def mouse_on():
  pygame.mouse.set_visible(True)
  
def set_mouse(self,show):
  if show:
    pygame.mouse.set_visible(True)
  else:
    pygame.mouse.set_visible(False)
  
def run():
  pgzrun.go()

  
class Actor(Actor):
  def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
    self._flip_x = False
    self._flip_y = False
    self._scale = 1
    self._mask = None
    self._animate_counter = 0
    self.fps = 5
    self.direction = 0
    super().__init__(image, pos, anchor, **kwargs)
    



    

    
    