from __future__ import annotations

import pygame as pg
from pygame.time import Clock

from utils.drawing.screen import Screen


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