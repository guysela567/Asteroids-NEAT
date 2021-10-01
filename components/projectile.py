from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants

from arcade import Sprite
import numpy as np
import math


class Projectile:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__pos = PositionalVector(x, y)
        self.__angle = angle

        self.__sprite = Sprite('assets/sprites/projectile.png',
                               Constants.PROJECTILE_SPRITE_SCALE)

        self.__vel = DirectionalVector(
            Constants.PROJECTILE_SPEED, self.__angle)
        self.__sprite.angle = math.degrees(self.__angle) - 90

        self.__distance_traveled = 0
        self.__max_distance = 750
        self.__deleted = False

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @property
    def deleted(self) -> bool:
        return self.__deleted

    def delete(self) -> None:
        self.__deleted = True

    def update(self) -> None:
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__sprite)

        # Update sprite position
        self.__sprite.center_x = self.__pos.x
        self.__sprite.center_y = self.__pos.y

        # Add travel distance
        self.__distance_traveled += Constants.PROJECTILE_SPEED

        # Delete projectile if traveled too much
        if self.__distance_traveled >= self.__max_distance:
            self.__deleted = True

        # Fade out as more distance is traveled
        percentage = self.__distance_traveled / self.__max_distance
        self.__sprite.alpha = np.interp(percentage, [0, 1], [255, 0])