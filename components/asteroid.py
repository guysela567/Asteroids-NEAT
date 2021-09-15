from utils.constants import Constants
from utils.common import Common

import math
from arcade import Sprite
from random import randint, uniform


class Asteroid:
    def __init__(self, x, y, angle: float = None, hits: int = 0) -> None:
        self.__x = x
        self.__y = y
        self.__hits = hits

        self.__sprite = Sprite(
            f'assets/sprites/asteroid{randint(1, 3)}.png',
            Constants.ASTEROID_SPRITE_SCALE[self.__hits])

        self.__angle = uniform(0, math.pi * 2) if angle is None else angle
        self.__vel = Constants.ASTEROID_VELOCITY[self.__hits]

        self.__vel_x = math.cos(self.__angle) * self.__vel
        self.__vel_y = math.sin(self.__angle) * self.__vel

        self.__sprite.center_x = self.__x
        self.__sprite.center_y = self.__y

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def hits(self) -> float:
        return self.__hits

    def update(self, delta_time: float) -> None:
        self.__x += self.__vel_x
        self.__y += self.__vel_y
        self.__handle_offscreen()

        self.__sprite.center_x = self.__x
        self.__sprite.center_y = self.__y

    def __handle_offscreen(self) -> bool:
        self.__x, self.__y = Common.handle_offscreen(
            self.__x, self.__y, self.__sprite)
