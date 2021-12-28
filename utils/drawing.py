from __future__ import annotations

import pygame as pg
from pygame.event import Event
from pygame.time import Clock

from functools import lru_cache


# My wrapper on PyGame to make it more like the processing.org 
# environment combined with HTML Canvas tools 


class Image:
    def __init__(self, image: str | pg.Surface) -> None:
        base_image = image if isinstance(image, pg.Surface) else pg.image.load(image) # Load image
        self.__surface = base_image.convert_alpha() # The surface used for viewing

    @staticmethod
    # @lru_cache
    def resize(image: Image, width: int, height: int) -> Image:
        new_surf = pg.transform.smoothscale(image.surface, (width, height)).convert_alpha()
        return Image(new_surf)

    @staticmethod
    # @lru_cache
    def rotate(image: Image, angle: int) -> Image:
        new_surf = pg.transform.rotate(image.surface, angle)
        return Image(new_surf)

    def get_rect(self, point: tuple[float, float]) -> tuple[int, int, int, int]:
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
    def __init__(self, width: int, height: int, title: str) -> None:
        self.__display = pg.Surface((width, height)).convert()
        self.__width = width
        self.__height = height
        self.__title = title

    @property
    def display(self) -> pg.Surface:
        return self.__display

    @property
    def width(self) -> float:
        return self.__width
    
    @property
    def height(self) -> float:
        return self.__height
    
    @property
    def title(self) -> float:
        return self.__title

class Context:
    def __init__(self, canvas: Canvas) -> None:
        pg.init()

        self.__display = canvas.display

        self.__fill_color = (255, 255, 255)
        self.__stroke_color = (0, 0, 0)
        self.__weight = 5

        self.__filling = True
        self.__stroking = True

        self.__font_family = 'sans serif'
        self.__font_size = 100
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def background(self, r: int, g: int = None, b: int = None) -> None:
        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__display.fill((r, g, b))

    def fill(self, r: int | tuple, g: int = None, b: int = None) -> None:
        if type(r) == tuple:
            self.__fill_color = r
            return

        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__filling = True
        self.__fill_color = (r, g, b)

    def no_fill(self) -> None:
        self.__filling = False

    def no_stroke(self) -> None:
        self.__stroking = False

    def stroke(self, r: int or tuple, g: int = None, b: int = None) -> None:
        if type(r) == tuple:
            self.__stroke_color = r
            return

        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__stroking = True
        self.__stroke_color = (r, g, b)

    def stroke_weight(self, weight) -> None:
        self.__weight = weight

    def circle(self, x: float, y: float, r: float) -> None:
        if self.__filling:
            pg.draw.circle(self.__display, self.__fill_color, (x, y), r)

        if self.__stroking:
            pg.draw.circle(self.__display, self.__stroke_color,
                           (x, y), r, self.__weight)

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        if self.__filling:
            pg.draw.rect(self.__display, self.__fill_color, (x, y, w, h))

        if self.__stroking:
            pg.draw.rect(self.__display, self.__stroke_color,
                         (x, y, w, h), self.__weight)

    def image(self, image: Image, x: float, y: float, w: float, h: float, alpha: float = None) -> None:
        if alpha is None:
            self.__display.blit(pg.transform.scale(image.surface, (w, h)), (x, y))
        else:
            temp = image.__surface.copy()
            temp.set_alpha(alpha)
            self.__display.blit(pg.transform.scale(temp, (w, h)), (x, y))

    def text(self, text: str, x: float, y: float, center: bool = False) -> None:
        text_surface = self.__font.render(text, True, self.__fill_color)

        if center:
            self.__display.blit(text_surface,
                                text_surface.get_rect(center=(x, y)))
        else:
            self.__display.blit(text_surface,
                                text_surface.get_rect(topleft=(x, y)))

    def line(self, x1: float, y1: float, x2: float, y2: float, weight: float) -> None:
        pg.draw.line(self.__display, self.__fill_color,
                     (x1, y1), (x2, y2), weight)

    def font_size(self, size: float) -> None:
        self.__font_size = size
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def font_family(self, name: str) -> None:
        self.__font_family = name
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

class Screen(Context):
    def __init__(self, width: float, height: float, title: str) -> None:
        '''
        Screen consisting of canvas, drawing methods and event handlers.

        Args:
            width (float): Width of the screen.
            height (float): Height of the screen.
            title (str): Caption of the screen.
            fps (int): Frame rate in which the screen updates.
        '''

        self.__canvas = Canvas(width, height, title)
        super().__init__(self.__canvas)
        
        self.__keys = {k[2:]: v for k, v in pg.constants.__dict__.items() if k.startswith('K_')}
    
    def update_all(self) -> None:
        if hasattr(self, 'update'):
            self.update()

        if hasattr(self, 'draw'):
            self.draw()
    
        for event in pg.event.get():
            self.handle_event(event)

    @property
    def surface(self) -> pg.Surface:
        return self.__canvas.display
    
    def handle_event(self, event: Event) -> None:
        ''' Handles all events registered by pygame. '''

        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        elif event.type == pg.KEYDOWN and hasattr(self, 'on_key_down'):
            self.on_key_down(event.key)

        elif event.type == pg.KEYUP and hasattr(self, 'on_key_up'):
            self.on_key_up(event.key)
        
        elif event.type == pg.MOUSEBUTTONDOWN and hasattr(self, 'on_mouse_down'):
            self.on_mouse_down()

        elif event.type == pg.MOUSEBUTTONUP and hasattr(self, 'on_mouse_up'):
            self.on_mouse_up()

    @property
    def width(self) -> int:
        return self.__canvas.width
    
    @property
    def height(self) -> int:
        return self.__canvas.height

    @property
    def keys(self) -> dict[str, str]:
        return self.__keys

class ScreenController:
    def __init__(self, width: int, height: int, fps: int) -> None:
        self.__display = pg.display.set_mode((width, height))
        self.__clock = Clock()
        self.__screens: list[Screen] = []
        self.__screen: int = 0
        self.__fps = fps

    def init_screen(self, screen: Screen) -> None:
        self.__screens.append(screen)

    def set_screen(self, index: int) -> None:
        self.__screen = index

    def start(self) -> None:
        if len(self.__screens) == 0:
            raise Exception('A screen needs to be initialized before starting the view.')

        while True:
            self.update()

    def update(self) -> None:
        screen = self.__screens[self.__screen]
        screen.update_all()
        self.__display.blit(screen.surface, (0, 0))

        pg.display.flip()
        self.__clock.tick(self.__fps)

class Button:
    def __init__(self, ctx: Context, x: float, y: float, w: float, h: float, color: tuple, caption: str) -> None:
        self.__ctx = ctx
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__color = color
        self.__caption = caption

    def draw(self) -> None:
        self.__ctx.stroke(0)
        self.__ctx.fill(self.__color)
        self.__ctx.rect(self.__x, self.__y, self.__w, self.__h)
        self.__ctx.fill(0)
        self.__ctx.text(self.__caption, self.__x + self.__w * .5, self.__y + self.__h * .5, center=True)
        self.__ctx.no_stroke()

    def mouse_hover(self) -> None:
        x, y = pg.mouse.get_pos()
        
        return self.__x < x < self.__x + self.__w \
            and self.__y < y < self.__y + self.__h

    @property
    def caption(self) -> str:
        return self.__caption

    @caption.setter
    def caption(self, caption: str) -> None:
        self.__caption = caption


    def __init__(self, width: float, height: float, title: str, fps: int) -> None:
        '''
        Screen consisting of canvas, drawing methods and event handlers.

        Args:
            width (float): Width of the screen.
            height (float): Height of the screen.
            title (str): Caption of the screen.
            fps (int): Frame rate in which the screen updates.
        '''

        self.__canvas = Canvas(width, height, title, fps)
        super().__init__(self.__canvas)
        
        self.__keys = {k[2:]: v for k, v in pg.constants.__dict__.items() if k.startswith('K_')}
    
    def start(self) -> None:
        ''' Starts the main loop. '''

        while True:
            self.update()

    def update(self) -> None:
        ''' Gets called in each frame. handles events in the main loop. '''

        if hasattr(self, 'draw'):
            self.draw()
        
        for event in pg.event.get():
            self.handle_event(event)
        
        self.__canvas.update()
    
    def handle_event(self, event: Event) -> None:
        ''' Handles all events registered by pygame. '''

        if event.type == pg.QUIT:
            pg.quit()
            exit()
        
        elif event.type == pg.KEYDOWN and hasattr(self, 'on_keydown'):
            self.on_keydown(event.key)

        elif event.type == pg.KEYUP and hasattr(self, 'on_keyup'):
            self.on_keyup(event.key)
        
        elif event.type == pg.MOUSEBUTTONDOWN and hasattr(self, 'on_mousedown'):
            self.on_mousedown()

        elif event.type == pg.MOUSEBUTTONUP and hasattr(self, 'on_mouseup'):
            self.on_mouseup()

    @property
    def ctx(self) -> Context:
        return self.__ctx

    @property
    def width(self) -> int:
        return self.__canvas.width
    
    @property
    def height(self) -> int:
        return self.__canvas.height

    @property
    def keys(self) -> dict[str, str]:
        return self.__keys