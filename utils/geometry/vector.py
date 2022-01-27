from __future__ import annotations

from utils.constants import Constants

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from utils.geometry.collision import Hitbox

import math


class PositionVector:
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
        if self is None or other is None:
            return 0
            
        return math.sqrt(math.pow(other.x - self.x, 2) + math.pow(other.y - self.y, 2))

    def angle_between(self, other: PositionVector) -> float:
        return math.atan((other.y - self.y) / (other.x - self.x))

    def copy(self) -> PositionVector:
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
    def __init__(self, mag: float, angle: float) -> None:
        self.__mag = mag
        self.__angle = angle
        self.__update_components()

    def __iter__(self) -> iter:
        return iter((self.__x, self.__y))

    def __update_components(self) -> None:
        self.__x = math.cos(self.__angle) * self.__mag
        self.__y = math.sin(self.__angle) * self.__mag

    def lerp_mag(self, to: float, step: float) -> None:
        # Apply linear interpolation on magnitude
        self.__mag = (1 - step) * self.__mag + step * to
        self.__update_components()

    def normalized(self) -> None:
        return DirectionVector(self.__x / self.__mag, self.__y / self.__mag)

    def copy(self) -> DirectionVector:
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
