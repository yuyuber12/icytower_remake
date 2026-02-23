
import pygame as pg
from pygame import Surface

from DataModels.GameObject import GameObject


# Represent the player entity and its drawable collision rectangle.
class Player(GameObject):
    # Initialize player geometry, style, and rectangle state.
    def __init__(self, width_position, height_position, player_width, player_height, color, border_radius):
        super().__init__(width_position, height_position,
                         player_width, player_height, color, border_radius)
        self._border_radius = border_radius
        self._color = color

        # Create a concrete rectangle used for movement and rendering.
        self.player_rect: pg.Rect = pg.Rect(
            width_position, height_position, player_width, player_height)

    # Draw the player on the target surface.
    def draw(self, window: Surface):
        pg.draw.rect(window, self._color, self.player_rect)
