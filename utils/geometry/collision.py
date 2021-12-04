from __future__ import annotations

from utils.vector import PositionalVector

import random


class SpriteDimensions:
    dimensions = {}

class Hitbox:
    def __init__(self, pos: PositionalVector, component: str, scale: float):
        self.__pos, self.__scale = pos, scale

        dimensions = SpriteDimensions.dimensions[component]
        self.__index = random.randint(0, len(dimensions) - 1)

        w, h = SpriteDimensions.dimensions[component][self.__index]
        self.__width, self.__height = int(w * scale), int(h * scale)

    def collides(self, other: Hitbox) -> bool:
        # Rectangular collision check
        return self.__pos.x - self.__width * .5 < other.pos.x + other.width * .5 \
            and self.__pos.x + self.__width * .5 > other.pos.x - other.width * .5 \
            and self.__pos.y - self.__height * .5 < other.pos.y + other.height * .5 \
            and self.__pos.y + self.__height * .5 > other.pos.y - other.height * .5

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
    def pos(self) -> PositionalVector:
        return self.__pos
    
    @property
    def scale(self) -> float:
        return self.__scale

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__pos = pos

    @scale.setter
    def scale(self, scale: float) -> None:
        self.__scale = scale