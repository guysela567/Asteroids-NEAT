from __future__ import annotations

from utils.geometry.vector import PositionVector

import random


class SpriteDimensions:
    '''This class is used to store the dimensions of each sprite in the game'''
    dimensions = {}

class Hitbox:
    '''The hitbox class is responsible for collision detection of the different sprites
    :param pos: position of the sprite
    :param component: name of the sprite
    :param scale: the scale of the sprite in respect to the original image size'''

    def __init__(self, pos: PositionVector, component: str, scale: float):
        self.__pos, self.__scale = pos, scale

        dimensions = SpriteDimensions.dimensions[component]
        self.__index = random.randint(0, len(dimensions) - 1)

        w, h = SpriteDimensions.dimensions[component][self.__index]
        self.__width, self.__height = int(w * scale), int(h * scale)

    def collides(self, other: Hitbox) -> bool:
        '''Returns wether this hitbox collides with the given hitbox
        via rectangular collision check
        :param other: the other hitbox to check collision with'''
        
        # Rectangular collision check
        return self.__pos.x - self.__width * .5 < other.pos.x + other.width * .5 \
            and self.__pos.x + self.__width * .5 > other.pos.x - other.width * .5 \
            and self.__pos.y - self.__height * .5 < other.pos.y + other.height * .5 \
            and self.__pos.y + self.__height * .5 > other.pos.y - other.height * .5

    @property
    def rect_verts(self) -> list[tuple[float, float]]:
        return [
            # Top left
            (self.__pos.x - self.__width * .5, self.__pos.y - self.__height * .5),
            # Top right
            (self.__pos.x + self.__width * .5, self.__pos.y - self.__height * .5),
            # Bottom right
            (self.__pos.x + self.__width * .5, self.__pos.y + self.__height * .5),
            # Bottom left
            (self.__pos.x - self.__width * .5, self.__pos.y + self.__height * .5),
        ]

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def index(self) -> int:
        return self.__index

    @property
    def pos(self) -> PositionVector:
        return self.__pos
    
    @property
    def scale(self) -> float:
        return self.__scale

    @pos.setter
    def pos(self, pos: PositionVector) -> None:
        self.__pos = pos

    @scale.setter
    def scale(self, scale: float) -> None:
        self.__scale = scale