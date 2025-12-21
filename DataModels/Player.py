
import pygame as pg
from pygame import Surface

from DataModels.GameObject import GameObject

class Player(GameObject):
    def __init__(self, width_position, height_position, player_width, player_height, color, border_radius):
       super().__init__(width_position, height_position, player_width, player_height, color , border_radius)
       self._border_radius = border_radius
       self._color = color


       #Instance:
       self.player_rect: pg.Rect = pg.Rect(width_position, height_position, player_width, player_height)

    def draw(self , window: Surface):
        pg.draw.rect(window, self._color, self.player_rect)