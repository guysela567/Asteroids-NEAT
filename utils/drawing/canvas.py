import pygame as pg


class Canvas:
    '''The Canvas class resembels the HTML canvas and is used as base
    surface for drawing. This class is based on the pygame.Surface class
    :param width: the width of the canvas
    :param height: the height of the canvas
    '''

    def __init__(self, width: int, height: int) -> None:
        self.__display = pg.Surface((width, height)).convert()
        self.__width = width
        self.__height = height

    @property
    def display(self) -> pg.Surface:
        return self.__display

    @property
    def width(self) -> float:
        return self.__width
    
    @property
    def height(self) -> float:
        return self.__height