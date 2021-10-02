from __future__ import annotations

from utils.vector import PositionalVector

import pygame as pg
from utils.drawing import Context

from typing import Tuple


class Sprite:
    def __init__(self, image_path: str, scale: float, pos: PositionalVector):
        self.__pos = pos.to_tuple()

        # Save original image to maintain it's quality
        image = Context.load_image(image_path)
        self.__width, self.__height = map(lambda x: int(x * scale), image.get_size())
        self.__original_image = Context.resize_image(image, self.__width, self.__height)

        self.__image = self.__original_image.copy()
        self.__rect = self.__image.get_rect()
        self.__rect.center = self.__pos

        self.__angle = 0

    def collides(self, other: Sprite) -> bool:
        # Rectangular collision check
        return self.__pos[0] - self.__width * .5 < other.pos[0] + other.width * .5 \
            and self.__pos[0] + self.__width * .5 > other.pos[0] - other.width * .5 \
            and self.__pos[1] - self.__height * .5 < other.pos[1] + other.height * .5 \
            and self.__pos[1] + self.__height * .5 > other.pos[1] - other.height * .5

    @property
    def angle(self) -> float:
        return self.__angle

    @angle.setter
    def angle(self, angle: float) -> None:
        self.__angle = -angle  # Convert from anti-clockwize to clockwize

        # Rotate original image to prevent big changes in image quality
        self.__image = Context.rotate_image(self.__original_image, self.__angle)

        self.__rect = self.__image.get_rect()  # Update position rectangle
        self.__rect.center = self.__pos  # Keep previous center point

    @property
    def image(self) -> pg.Surface:
        return self.__image

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def pos(self) -> Tuple[float, float]:
        return self.__pos

    @property
    def rect(self) -> pg.Rect:
        return self.__rect

    @property
    def alpha(self) -> float:
        return self.__image.get_alpha()

    @alpha.setter
    def alpha(self, alpha: float) -> None:
        self.__image.set_alpha(alpha)

    @pos.setter
    def pos(self, pos: PositionalVector) -> None:
        self.__pos = pos.to_tuple()
        self.__rect.center = self.__pos
