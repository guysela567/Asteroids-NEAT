from utils.vector import PositionalVector, DirectionalVector
from utils.constants import Constants

from arcade import Sprite
import math


class Bullet:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__pos = PositionalVector(x, y)
        self.__angle = angle

        self.__sprite = Sprite('assets/sprites/bullet.png',
                               Constants.BULLET_SPRITE_SCALE)

        self.__vel = DirectionalVector(Constants.BULLET_SPEED, self.__angle)
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
        self.__distance_traveled += Constants.BULLET_SPEED

        # Delete bullet if traveled too much
        if self.__distance_traveled >= self.__max_distance:
            self.__deleted = True
