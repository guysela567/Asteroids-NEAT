from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants
from utils.sprite import Sprite

import math
from random import randint, uniform, random


class Asteroid:
    def __init__(self, x, y, angle: float = None, hits: int = 0) -> None:
        self.__pos = PositionalVector(x, y)
        self.__hits = hits

        self.__sprite = Sprite(
            f'assets/sprites/asteroid{randint(1, 3)}.png',
            Constants.ASTEROID_SPRITE_SCALE[self.__hits],
            self.__pos)

        # Get a random angle for direction
        self.__angle = uniform(0, math.pi * 2) if angle is None else angle

        # Set velocity vector in that angle
        self.__vel = DirectionalVector(
            Constants.ASTEROID_VELOCITY[self.__hits], self.__angle + math.pi)

        # Rotate sprite randomally (90n degrees to maintain hitbox)
        self.__sprite.angle = 90 * randint(0, 3)

        # TODO Add destruction vfx

    def update(self, delta_time: float) -> None:
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__sprite)

        # Update sprite position
        self.__sprite.pos = self.__pos

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
