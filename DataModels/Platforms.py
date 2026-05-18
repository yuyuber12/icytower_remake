
import pygame as pg
from pygame import Surface

from DataModels.GameObject import GameObject


# Represent a single platform object that can be drawn on the game screen.
class Platforms(GameObject):
    # Initialize platform geometry, color, and pygame rectangle.
    def __init__(self, platform_x, platform_y, platform_width, platform_height, color, platform_border_radius):
        super().__init__(platform_x, platform_y, platform_width,
                         platform_height, color, platform_border_radius)
        self._border_radius = platform_border_radius
        self._color = color

        # Create a concrete rectangle used for collision and rendering.
        self.platform_rect: pg.Rect = pg.Rect(
            platform_x, platform_y, platform_width, platform_height)

    # Draw the platform on the given surface.
    def draw(self, window: Surface):
        pg.draw.rect(window, self._color, self.platform_rect)
