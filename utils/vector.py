from __future__ import annotations

from utils.constants import Constants

import math


class PositionalVector:
    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    def __add__(self, other: PositionalVector) -> PositionalVector | DirectionalVector:
        return PositionalVector(self.__x + other.x, self.__y + other.y)

    def handle_offscreen(self, sprite) -> None:
        # left to right
        if self.__x + sprite.width * .5 < 0:
            self.__x = Constants.WINDOW_WIDTH + sprite.width * .5

        # right to left
        elif self.__x - sprite.width * .5 > Constants.WINDOW_WIDTH:
            self.__x = -sprite.width * .5

        # bottom to top
        elif self.__y + sprite.height * .5 < 0:
            self.__y = Constants.WINDOW_HEIGHT + sprite.height * .5

        # top to bottom
        elif self.__y - sprite.height * .5 > Constants.WINDOW_HEIGHT:
            self.__y = -sprite.height * .5

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


class DirectionalVector:
    def __init__(self, mag: float, angle: float) -> None:
        self.__mag = mag
        self.__angle = angle
        self.__update_components()

    def __update_components(self) -> None:
        self.__x = math.cos(self.__angle) * self.__mag
        self.__y = math.sin(self.__angle) * self.__mag

    def lerp_mag(self, to: float, step: float) -> None:
        # Apply linear interpolation on magnitude
        self.__mag = (1 - step) * self.__mag + step * to
        self.__update_components()

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


class Vector:
    def distance(vect1: PositionalVector, vect2: PositionalVector) -> float:
        return math.sqrt(math.pow(vect2.x - vect1.x, 2) + math.pow(vect2.y - vect1.y, 2))

    def angle_between(vect1: PositionalVector, vect2: PositionalVector) -> float:
        angle = math.atan((vect2.y - vect1.y) / (vect2.x - vect1.x))

        if angle < 0:
            angle += math.pi

        return angle
