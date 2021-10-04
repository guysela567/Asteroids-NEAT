from utils.constants import Constants
from src.model import Model
from src.view import View

import pygame as pg
from pygame.event import Event

import random


class Controller:
    def __init__(self) -> None:
        self.__view = View()
        self.__model = Model()

    def start(self):
        while True:
            # Handle user input
            for event in pg.event.get():
                self.handle_event(event)

            # AI
            self.__model.think([random.random() for _ in range(8)])

            # Update model
            if not self.__model.paused:
                self.__model.update(1 / Constants.FPS)

            # Update view
            self.__view.draw_background()
            self.__view.draw_sprites(self.__model.player, self.__model.asteroids)
            self.__view.draw_score(self.__model.score, self.__model.high_score)

            if self.__model.paused:
                self.__view.draw_paused()

            self.__view.finish_render()


    def handle_event(self, event: Event) -> None:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        elif event.type == pg.KEYDOWN:
            self.on_key_press(event.key)

        elif event.type == pg.KEYUP:
            self.on_key_release(event.key)

    def on_key_press(self, key: int) -> None:
        if key == pg.K_p:
            self.__model.toggle_pause()

        elif key == pg.K_UP:
            self.__model.player.start_boost()

        elif key == pg.K_RIGHT:
            self.__model.player.start_rotate(1)

        elif key == pg.K_LEFT:
            self.__model.player.start_rotate(-1)

        elif key == pg.K_SPACE:
            self.__model.player.shoot()

    def on_key_release(self, key: int) -> None:
        if key == pg.K_UP:
            self.__model.player.stop_boost()

        elif key == pg.K_RIGHT and self.__model.player.rotate_dir == 1 \
                or key == pg.K_LEFT and self.__model.player.rotate_dir == -1:
            self.__model.player.stop_rotate()