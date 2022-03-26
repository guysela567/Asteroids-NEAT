from __future__ import annotations

import pygame as pg
from pygame.event import Event

from utils.drawing.canvas import Canvas
from utils.drawing.image import Image


class Screen:
    '''Screen consisting of canvas, drawing methods and event handlers.
    :param width: the width of the screen
    :param height: the height of the screen
    :param title: the caption of the screen
    :param fps: the framee rate in which the screen is being updated
    '''

    def __init__(self, width: float, height: float, title: str) -> None:
        # Canvas and keys
        self.__title = title
        self.__canvas = Canvas(width, height)
        
        self.__keys = {k[2:]: v for k, v in pg.constants.__dict__.items() if k.startswith('K_')}

        # Drawing functions
        self.__display = self.__canvas.display

        self.__fill_color = (255, 255, 255)
        self.__stroke_color = (0, 0, 0)
        self.__weight = 5

        self.__filling = True
        self.__stroking = True

        self.__font_family = 'sans serif'
        self.__font_size = 100
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def blur(self, alpha: int = 100) -> None:
        '''Darkens the screen by a given alpha value
        :param alpha: the opacity of the darkness efect, measured from 0 to 255
        '''

        surf = pg.Surface((self.width, self.height))
        surf.fill((0, 0, 0))
        surf.set_alpha(alpha)
        self.__display.blit(surf, (0, 0))

    def background(self, r: int, g: int = None, b: int = None) -> None:
        '''Draws a solid background on top of the previous drawings
        :param r: red value of the background color
        :param g: green value of the background color
        :param b: blue value of the background color
        '''

        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__display.fill((r, g, b))

    def fill(self, r: int | tuple, g: int = None, b: int = None) -> None:
        '''Sets the fill color for drawing
        :param r: red value of the fill color
        :param g: green value of the fill color
        :param b: blue value of the fill color
        '''

        if type(r) == tuple:
            self.__fill_color = r
            return

        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__filling = True
        self.__fill_color = (r, g, b)

    def no_fill(self) -> None:
        '''Removes the fill color for drawing'''
        self.__filling = False

    def no_stroke(self) -> None:
        '''Removes the stroke for drawing'''
        self.__stroking = False

    def stroke(self, r: int or tuple, g: int = None, b: int = None) -> None:
        '''Sets the stroke color for drawing
        :param r: red value of the stroke color
        :param g: green value of the stroke color
        :param b: blue value of the stroke color
        '''

        if type(r) == tuple:
            self.__stroke_color = r
            return

        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__stroking = True
        self.__stroke_color = (r, g, b)

    def stroke_weight(self, weight) -> None:
        '''Sets the stroke weight for drawing'''
        self.__weight = weight

    def circle(self, x: float, y: float, r: float) -> None:
        '''Draws a circle on the screen
        :param x: the center X coordinate of the circle
        :param y: the center Y coordinate of the circle
        :param r: the radius of the circle'''

        if self.__filling:
            pg.draw.circle(self.__display, self.__fill_color, (x, y), r)

        if self.__stroking:
            pg.draw.circle(self.__display, self.__stroke_color,
                           (x, y), r, self.__weight)

    def rect(self, x: float, y: float, w: float, h: float, round: int = 0) -> None:
        '''Draws a rectangle on the screen
        :param x: the X coordinate of the top left corner of the rectangle
        :param y: the Y coordinate of the top left corner of the rectangle
        :param w: the width of the rectangle
        :param h: the height of the rectangle
        :param round: the border radius of the rectangle's corners
        '''

        if self.__filling:
            pg.draw.rect(self.__display, self.__fill_color, (x, y, w, h), border_radius=round)

        if self.__stroking:
            pg.draw.rect(self.__display, self.__stroke_color,
                         (x, y, w, h), self.__weight, border_radius=round)

    def image(self, image: Image, x: float, y: float, w: float = None, h: float = None, alpha: float = None, center: bool = False) -> None:
        '''Draws a given image on the screen
        :param image: the image to draw
        :param x: the X coordinate of the top left corner of the image
        :param y: the Y coordinate of the top left corner of the image
        :param w: the width of the image
        :param h: the height of the image
        :param alpha: the alpha value in which the image is drawn
        :param center: whether or not to draw the image in respect
        to it's center point instead of the top left corner of the image
        '''
        
        scale = (w, h) if w and h else image.size
        
        if alpha is None:
            self.__display.blit(pg.transform.scale(image.surface, scale), (x, y))
        else:
            temp = image.__surface.copy()
            temp.set_alpha(alpha)
            self.__display.blit(pg.transform.scale(temp, scale), (x, y))

    def text(self, text: str, x: float, y: float, center: bool = False) -> None:
        '''Draws the given text on the screen
        :param text: the text to draw
        :param x: the X coordinate for the top left corner of the text rectangle
        :param y: the Y coordinate for the top left corner of the text rectangle
        :param center: whether the text should be drawn in respect to it's center
        point instead of the top left corner of the text rectangle
        '''

        text_surface = self.__font.render(text, True, self.__fill_color)

        if center:
            self.__display.blit(text_surface,
                                text_surface.get_rect(center=(x, y)))
        else:
            self.__display.blit(text_surface,
                                text_surface.get_rect(topleft=(x, y)))

    def line(self, x1: float, y1: float, x2: float, y2: float, weight: float) -> None:
        '''Draws a line segment on the screen
        :param x1: the X coordinate for the beginning of the line
        :param y1: the Y coordinate for the beginning of the line
        :param x2: the X coordinate for the end of the line
        :param y2: the Y coordinate for the end of the line
        '''

        pg.draw.line(self.__display, self.__fill_color,
                     (x1, y1), (x2, y2), weight)

    def font_size(self, size: float) -> None:
        '''Sets the size of the font used to drawing text
        :param size: the new size of the font
        '''

        self.__font_size = size
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def font_family(self, name: str) -> None:
        '''Sets the font family used to drawing text
        :param name: the new font family name
        '''

        self.__font_family = name
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def load_font(self, path: str, size: int) -> pg.font.Font:
        '''Loads a font file with a given font size,
        using the pygame.font module
        :param path: the path to the font file
        :param size: the size of the font'''
        return pg.font.Font(path, size)

    def set_font(self, font: pg.font.Font) -> None:
        '''Sets the font used to draw text
        :param font: the new font'''
        self.__font = font

    def quit(self) -> None:
        '''Quits pygame and exits application'''

        pg.quit()
        exit()
    
    def handle_event(self, event: Event) -> None:
        '''Handles all events registered by pygame,
        using the pygame.event module
        :param event: the event to be handled'''

        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        elif event.type == pg.KEYDOWN and hasattr(self, 'on_key_down'):
            self.on_key_down(event.key, event.unicode)

        elif event.type == pg.KEYUP and hasattr(self, 'on_key_up'):
            self.on_key_up(event.key)
        
        elif event.type == pg.MOUSEBUTTONDOWN and hasattr(self, 'on_mouse_down'):
            self.on_mouse_down()

        elif event.type == pg.MOUSEBUTTONUP and hasattr(self, 'on_mouse_up'):
            self.on_mouse_up()

    def redirect(self, name: str, data: dict = {}) -> None:
        '''Posts a pygame event to the screen manager which
        redirects the user to a different screen
        :param name: the name of the screen to redirect to
        :param data: dictionary containing POST data to the screen manager'''
        pg.event.post(Event(pg.USEREVENT, screen=name, data=data))

    @property
    def mouse_pos(self) -> tuple[int, int]:
        return pg.mouse.get_pos()

    @property
    def title(self) -> str:
        return self.__title

    @property
    def surface(self) -> pg.Surface:
        return self.__canvas.display

    @property
    def width(self) -> int:
        return self.__canvas.width
    
    @property
    def height(self) -> int:
        return self.__canvas.height

    @property
    def keys(self) -> dict[str, str]:
        return self.__keys