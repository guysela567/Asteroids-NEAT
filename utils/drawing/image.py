from __future__ import annotations

import pygame as pg
from functools import lru_cache


class Image:
    '''The Image class wraps on the pygame.Surface class
    and is used for loading, manipulating and and drawing images
    :param image: path to the image file or the Surface obhect of the image
    '''

    def __init__(self, image: str | pg.Surface) -> None:
        base_image = image if isinstance(image, pg.Surface) else pg.image.load(image) # Load image
        self.__surface = base_image.convert_alpha() # The surface used for viewing

    @staticmethod
    @lru_cache(maxsize=1000)
    def resize(image: Image, width: int, height: int, smooth: bool = True) -> Image:
        '''Returns a resized version of the given image
        :param image: original image to be resized
        :param width: new width of the image
        :param height: new height of the image
        :param smooth: whether or not to use pygame's smoothscaling feature'''

        if smooth:
            new_surf = pg.transform.smoothscale(image.surface, (width, height)).convert_alpha()
        else:
            new_surf = pg.transform.scale(image.surface, (width, height)).convert_alpha()

        return Image(new_surf)

    @staticmethod
    @lru_cache(maxsize=1000)
    def rotate(image: Image, angle: int) -> Image:
        '''Returns a rotated version of the given image
        :param image: original image to be rotated
        :param angle: the angle to rotate by, measured in degrees'''

        new_surf = pg.transform.rotate(image.surface, angle)
        return Image(new_surf)

    @staticmethod
    def load_by_scale(image_path: str, scale: float) -> Image:
        '''Loads an resizes an image from a given path and scale
        :param image_path: path to image file
        :param scale: the scale of the loaded image'''

        original = Image(image_path)
        size = tuple(int(d * scale) for d in original.size)
        return Image.resize(original, *size, smooth=False)

    def get_rect(self, point: tuple[float, float]) -> tuple[int, int, int, int]:
        '''Returns the rectangle vertecies of the image in respect to center point
        :param point: the center of the rectangle'''
        return self.__surface.get_rect(center=point)

    @property
    def surface(self) -> pg.Surface:
        return self.__surface

    @property
    def size(self) -> tuple[int, int]:
        return self.__surface.get_size()
    
    @property
    def alpha(self) -> float:
        return self.__surface.get_alpha()

    @alpha.setter
    def alpha(self, alpha: int) -> None:
        self.__surface.set_alpha(alpha)