from __future__ import annotations
from ctypes import Union

from utils.constants import Constants

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.geometry.collision import Hitbox

import math


class PositionVector:
    '''Algebraic vector used for positions
    :param x: The X component of the position vector
    :param y: The Y component of the position vector
    '''

    def __init__(self, x: float = 0, y: float = 0):
        self.__x = x
        self.__y = y

    def __add__(self, other: PositionVector | DirectionVector) -> PositionVector:
        return PositionVector(self.__x + other.x, self.__y + other.y)

    def __sub__(self, other: PositionVector | DirectionVector) -> PositionVector:
        return PositionVector(self.__x - other.x, self.__y - other.y)

    def __mul__(self, other: PositionVector | DirectionVector) -> PositionVector:
        return PositionVector(self.__x * other.x, self.__y * other.y)

    def __iter__(self) -> iter:
        return iter((self.__x, self.__y))

    def handle_offscreen(self, sprite: Hitbox = None) -> None:
        '''Loops the vector through the edges of the screen if it is offscreen
        :param sprite: The hitbox for the looped sprite
        '''

        width = sprite.width if sprite else 0
        height = sprite.height if sprite else 0

        # left to right
        if self.__x + width * .5 < 0:
            self.__x = Constants.WINDOW_WIDTH + width * .5

        # right to left
        elif self.__x - width * .5 > Constants.WINDOW_WIDTH:
            self.__x = -width * .5

        # bottom to top
        elif self.__y + height * .5 < 0:
            self.__y = Constants.WINDOW_HEIGHT + height * .5

        # top to bottom
        elif self.__y - height * .5 > Constants.WINDOW_HEIGHT:
            self.__y = -height * .5

    def distance(self, other: PositionVector) -> float:
        '''Returns the distance between this postion and a given position
        :param other: given position to calculate distance from
        '''

        if self is None or other is None:
            return 0
            
        return math.sqrt(math.pow(other.x - self.x, 2) + math.pow(other.y - self.y, 2))

    def angle_between(self, other: PositionVector) -> float:
        '''Returns the angle between this postion and a given position
        :param other: given position to calculate angle with
        '''

        return math.atan((other.y - self.y) / (other.x - self.x))

    def copy(self) -> PositionVector:
        '''Returns a copy of this vector'''
        return PositionVector(self.__x, self.__y)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

class DirectionVector:
    '''Geometric vector used for directions
    :param mag: magnitude of the vector
    :param angle: angle of the vector, measured in radians
    '''

    def __init__(self, mag: float, angle: float) -> None:
        self.__mag = mag
        self.__angle = angle
        self.__update_components()

    def __iter__(self) -> iter:
        return iter((self.__x, self.__y))

    def __update_components(self) -> None:
        '''Updates the X and Y algebraic components of the vector'''
        self.__x = math.cos(self.__angle) * self.__mag
        self.__y = math.sin(self.__angle) * self.__mag

    def lerp_mag(self, to: float, step: float) -> None:
        '''Applies linear interpolation on the magnitude
        :param to: target magnitude
        :param step: step of the interpolation
        '''

        self.__mag = (1 - step) * self.__mag + step * to
        self.__update_components()

    def dot(self, other: PositionVector | DirectionVector) -> float:
        '''Returns the dot product of this vector with a given vector
        :param other: second vector.
        '''

        return self.__x * other.x + self.__y * other.y

    def normalized(self) -> DirectionVector:
        '''Returns the vector after normalization, does not apply to original vector'''
        return DirectionVector(1, self.__angle)

    def copy(self) -> DirectionVector:
        '''Returns a copy of this vector'''
        return DirectionVector(self.__mag, self.__angle)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def mag(self) -> float:
        return self.__mag

    @property
    def angle(self) -> float:
        return self.__angle

    @mag.setter
    def mag(self, mag: float) -> None:
        self.__mag = mag
        self.__update_components()

    @angle.setter
    def angle(self, angle: float) -> None:
        self.__angle = angle
        self.__update_components()
