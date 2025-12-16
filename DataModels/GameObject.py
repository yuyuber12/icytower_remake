from abc import ABC
import pygame as pg


class GameObject(ABC):
    def __init__(self, width_position, height_position, player_width, player_height, color , border_radius):
        self._width_position = width_position
        self._height_position = height_position
        self._player_width = player_width
        self._player_height = player_height
        self._color = color
        self._border_radius = border_radius

#border radius trouble