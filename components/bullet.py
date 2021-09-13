from utils.constants import Constants
from utils.common import Common

from arcade import Sprite
import math


class Bullet:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__x = x
        self.__y = y
        self.__angle = angle

        self.__sprite = Sprite('assets/sprites/bullet.png',
                               Constants.BULLET_SPRITE_SCALE)

        self.__vel_x = math.cos(self.__angle) * Constants.BULLET_SPEED
        self.__vel_y = math.sin(self.__angle) * Constants.BULLET_SPEED

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
        self.__x += self.__vel_x
        self.__y += self.__vel_y
        self.__handle_offscreen()

        self.__sprite.center_x = self.__x
        self.__sprite.center_y = self.__y

        # Add travel distance
        self.__distance_traveled += Constants.BULLET_SPEED

        # Delete bullet if traveled too much
        if self.__distance_traveled >= self.__max_distance:
            self.__deleted = True

    def __handle_offscreen(self) -> None:
        self.__x, self.__y = Common.handle_offscreen(
            self.__x, self.__y, self.__sprite)
