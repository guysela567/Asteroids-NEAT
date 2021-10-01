import pygame as pg

import math

# My 'homemade' wrapper on PyGame to make it more like the processing.org environment combined with HTML Canvas tools


class CTX:
    def __init__(self, surface: pg.Surface) -> None:
        self.__screen = surface

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

        self.__screen.fill((r, g, b))

    def fill(self, r: int, g: int = None, b: int = None) -> None:
        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__filling = True
        self.__fill_color = (r, g, b)

    def no_fill(self) -> None:
        self.__filling = False

    def no_stroke(self) -> None:
        self.__stroking = False

    def stroke(self, r: int, g: int = None, b: int = None) -> None:
        # R, G, B are all the same
        g = r if g is None else g
        b = r if b is None else b

        self.__stroking = True
        self.__stroke_color = (r, g, b)

    def stroke_weight(self, weight) -> None:
        self.__weight = weight

    def circle(self, x: float, y: float, r: float) -> None:
        if self.__filling:
            pg.draw.circle(self.__screen, self.__fill_color, (x, y), r)

        if self.__stroking:
            pg.draw.circle(self.__screen, self.__stroke_color,
                           (x, y), r, self.__weight)

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        if self.__filling:
            pg.draw.rect(self.__screen, self.__fill_color, (x, y, w, h))

        if self.__stroking:
            pg.draw.rect(self.__screen, self.__stroke_color,
                         (x, y, w, h), self.__weight)

    def load_image(path: str) -> pg.Surface:
        return pg.image.load(path)

    def image(self, image: pg.Surface, x: float, y: float, w: float, h: float) -> None:
        self.__screen.blit(pg.transform.scale(image, (w, h)), (x, y))

    def text(self, text: str, x: float, y: float, center: bool = False) -> None:
        text_surface = self.__font.render(text, True, self.__fill_color)

        if center:
            self.__screen.blit(text_surface,
                               text_surface.get_rect(center=(x, y)))
        else:
            self.__screen.blit(text_surface,
                               text_surface.get_rect(topleft=(x, y)))

    def line(self, x1: float, y1: float, x2: float, y2: float, weight: float) -> None:
        pg.draw.line(self.__screen, self.__fill_color,
                     (x1, y1), (x2, y2), weight)

    def font_size(self, size: float) -> None:
        self.__font_size = size
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)

    def font_family(self, name: str) -> None:
        self.__font_family = name
        self.__font = pg.font.SysFont(self.__font_family, self.__font_size)
