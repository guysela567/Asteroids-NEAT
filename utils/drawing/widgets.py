from __future__ import annotations
import pygame as pg

from utils.drawing import Screen


class Button:
    '''Clickable stylized button
    :param screen: the screen of the button
    :param x: the X coordinate of the top left corner of the button
    :param y: the Y coordinate of the top left corner of the button
    :param w: the width of the button
    :param h: the height of the button
    :param color: the color of the button in (RGB tuple format)
    :param caption: the caption of the button
    '''

    def __init__(self, screen: Screen, x: float, y: float, w: float, h: float, color: tuple, caption: str) -> None:
        self.__screen = screen
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__color = color
        self.__caption = caption

    def draw(self) -> None:
        '''Draws the button on the screen'''
        self.__screen.stroke(0)

        if self.mouse_hover():
            self.__screen.fill(150)
        else: 
            self.__screen.fill(self.__color)

        self.__screen.rect(self.__x, self.__y, self.__w, self.__h, round=20)
        self.__screen.fill(0)
        self.__screen.text(self.__caption, self.__x + self.__w * .5, self.__y + self.__h * .5, center=True)
        self.__screen.no_stroke()

    def mouse_hover(self) -> None:
        '''Returns whether the mouse is hovering over the button'''
        x, y = pg.mouse.get_pos()
        
        return self.__x < x < self.__x + self.__w \
            and self.__y < y < self.__y + self.__h

    @property
    def caption(self) -> str:
        return self.__caption

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def color(self) -> tuple:
        return self.__color

    @caption.setter
    def caption(self, caption: str) -> None:
        self.__caption = caption

    @x.setter
    def x(self, x: float) -> None:
        self.__x = x

    @y.setter
    def y(self, y: float) -> None:
        self.__y = y

    @color.setter
    def color(self, color: tuple) -> None:
        self.__color = color

class TextBox:
    '''Iteractable stylized text box
    :param screen: the screen of the text box
    :param x: the X coordinate of the top left corner of the text box
    :param y: the Y coordinate of the top left corner of the text box
    :param w: the width of the text box
    :param h: the height of the text box
    :param text: default text in the text box
    '''

    def __init__(self, screen: Screen, x: float, y: float, w: float, h: float, text: str = '') -> None:
        self.__defult_width = w
        self.__screen = screen
        self.__rect = pg.Rect(x, y, w, h)
        self.__color = (0, 0, 0)
        self.__text = text
        self.__txt_surface = pg.font.SysFont('monospace', self.__defult_width).render(self.__text, True, self.__color)
        self.__active = False
        self.__padding = 10

    def handle_mousedown(self, mouse_pos: tuple[int, int]) -> None:
        '''Handles the on_mouse_down event
        :param mouse_pos: the position of the mouse
        '''

        if self.__rect.collidepoint(mouse_pos):
            self.__active = not self.__active
        else:
            self.__active = False
        self.__color = (150, 150, 150) if self.__active else (0, 0, 0)

    def handle_keydown(self, key: int, unicode: str) -> None:
        '''Handles the on_key_down event
        "param key: the pressed key
        :param unicode: the unicode of the pressed key
        '''

        if self.__active:
            if key == pg.K_BACKSPACE:
                self.__text = self.__text[:-1]

            else:
                if unicode.isdigit() and int(self.__text + unicode) < 10:
                    self.__text += unicode

            self.__txt_surface = pg.font.SysFont('monospace', self.__defult_width).render(self.__text, True, self.__color)
            self.__rect.w = max(self.__defult_width, self.__txt_surface.get_width() + self.__padding * 2)

    def draw(self):
        '''Draws the button on the screen'''
        pg.draw.rect(self.__screen.surface, (255, 255, 255), self.__rect, border_radius=10)
        self.__screen.surface.blit(self.__txt_surface, (self.__rect.x + self.__padding, self.__rect.y))
        pg.draw.rect(self.__screen.surface, self.__color, self.__rect, 5, border_radius=10)

    def clear(self) -> None:
        '''Clears all the text in the text box'''
        self.__active = False
        self.__text = ''
        self.__txt_surface = pg.font.SysFont('monospace', self.__defult_width).render(self.__text, True, self.__color)
        self.__rect.w = max(self.__defult_width, self.__txt_surface.get_width() + self.__padding * 2)

    @property
    def value(self) -> str:
        return self.__text