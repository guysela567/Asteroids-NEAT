''' My wrapper on PyGame which resembels the user-friendly processing.org IDE. '''

from __future__ import annotations

import pygame as pg
from pygame.event import Event
from pygame.time import Clock
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

class ScreenManager:
    '''The Screen manager is used to manage and navigate between the various screens
    by recieving user events and redirecting them to the appropriate screen
    :param width: the default width of the screen to start the application with
    :param height: the default height of the screen to start the application with
    :param fps: the framee rate in which the screen is being updated
    '''

    def __init__(self, width: int, height: int, fps: int) -> None:
        pg.init()

        self.__display = pg.display.set_mode((width, height))
        self.__clock = Clock()
        self.__screens: dict[str, Screen] = dict()
        self.__screen: str = 0
        self.__fps = fps

    def init_screen(self, screen: Screen, name: str) -> None:
        '''Initializes a new Screen and stores it in a dictionary
        :param screen: screen to be initialized
        :param name: the name of the screen to be recognized with'''
        self.__screens[name] = screen

    def set_screen(self, name: str, data: dict = {}) -> None:
        '''Sets the current active screen
        :param name: the name of the screen
        :param data: the data associated with the POST body of the redirect event
        '''

        self.__screen = name
        screen = self.__screens[self.__screen]

        if hasattr(screen, 'switch_reset'): screen.switch_reset()
        if hasattr(screen, 'recieve_data'): screen.recieve_data(data)

        pg.display.set_mode((screen.width, screen.height))
        pg.display.set_caption(screen.title)


    def start(self) -> None:
        '''Starts the application
        :raises Exception: the application cannot be started without an initialized screen
        '''

        if len(self.__screens) == 0:
            raise Exception('A screen needs to be initialized before starting the screen manager.')

        while True:
            self.update()

    def update(self) -> None:
        '''Updates and forwards events to the current active screen'''

        screen = self.__screens[self.__screen]
        
        # Update active screen
        if hasattr(screen, 'update'):
            screen.update()

        if hasattr(screen, 'draw'):
            screen.draw()
    
        for event in pg.event.get():
            # Handle event for active screen
            screen.handle_event(event)

            # Handle custom redirect events
            if event.type == pg.USEREVENT:
                self.set_screen(event.screen, event.data)

        self.__display.blit(screen.surface, (0, 0))

        pg.display.flip()
        self.__clock.tick(self.__fps)

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