
import pygame as pg
from pygame import Surface

from DataModels.GameObject import GameObject

class Platforms(GameObject) :
    def __init__(self, platform_x, platform_y, platform_width, platform_height, color, platform_border_radius ):
        super().__init__(platform_x, platform_y, platform_width, platform_height, color ,platform_border_radius)
        self._border_radius = platform_border_radius
        self._color = color

        # Instance:
        self.platform_rect: pg.Rect = pg.Rect(platform_x, platform_y, platform_width, platform_height)

    def draw(self, window: Surface):
        pg.draw.rect(window, self._color, self.platform_rect)