from utils.geometry.vector import PositionVector, DirectionVector
from utils.geometry.collision import Hitbox
from utils.constants import Constants

import math


class Projectile:
    '''Physical component for a single projectile
    :param x: X coordinate of the projectile's position
    :param y: Y coordinate of the projectile's position
    :param angle: direction angle of the projectile, measured in radians
    '''

    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__pos = PositionVector(x, y)
        self.__angle = angle

        self.__hitbox = Hitbox(self.__pos, 'projectile', Constants.PROJECTILE_SPRITE_SCALE)

        self.__vel = DirectionVector(Constants.PROJECTILE_SPEED, self.__angle + math.pi)

        self.__distance_traveled = 0
        self.__max_distance = Constants.WINDOW_DIAGONAL * .5
        self.__deleted = False

    def delete(self) -> None:
        '''Deletes this projectile, as it is "dead"'''
        self.__deleted = True

    def update(self) -> None:
        '''Updates the projectile'''
        self.__pos += self.__vel
        self.__pos.handle_offscreen(self.__hitbox)

        self.__hitbox.pos = self.__pos  # Update sprite position
        self.__distance_traveled += Constants.PROJECTILE_SPEED  # Add travel distance

        # Delete projectile if traveled too much
        if self.__distance_traveled >= self.__max_distance:
            self.__deleted = True

    @property
    def hitbox(self) -> Hitbox:
        return self.__hitbox

    @property
    def deleted(self) -> bool:
        return self.__deleted

    @property
    def angle(self) -> float:
        return -(int(math.degrees(self.__angle)) - 90) % 360

    @property
    def alpha(self) -> int:
        return int(255 * (1 - self.__distance_traveled / self.__max_distance))
