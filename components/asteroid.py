from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants

import math
from arcade import Sprite
from random import randint, uniform


class Asteroid:
    def __init__(self, x, y, angle: float = None, hits: int = 0) -> None:
        self.__pos = PositionalVector(x, y)
        self.__hits = hits

        self.__sprite = Sprite(
            f'assets/sprites/asteroid{randint(1, 3)}.png',
            Constants.ASTEROID_SPRITE_SCALE[self.__hits])

        self.__angle = uniform(0, math.pi * 2) if angle is None else angle
        self.__vel = DirectionalVector(
            Constants.ASTEROID_VELOCITY[self.__hits], self.__angle)

        self.__sprite.center_x = self.__pos.x
        self.__sprite.center_y = self.__pos.y

        # TODO Add destruction vfx

    def update(self, delta_time: float) -> None:
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__sprite)

        self.__sprite.center_x = self.__pos.x
        self.__sprite.center_y = self.__pos.y

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @property
    def x(self) -> float:
        return self.__pos.x

    @property
    def y(self) -> float:
        return self.__pos.y

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def hits(self) -> float:
        return self.__hits
