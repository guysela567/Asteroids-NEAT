from utils.constants import Constants
from utils.sprite import Sprite

from components.player import Player
from components.asteroid import Asteroid

from typing import List

from random import uniform

import pygame as pg
from utils.drawing import CTX


class View():
    def __init__(self) -> None:
        pg.init()

        ''' Graphical setup '''
        self.__screen = pg.display.set_mode([Constants.WINDOW_WIDTH,
                                             Constants.WINDOW_HEIGHT])

        pg.display.set_caption(Constants.WINDOW_TITLE)

        self.__ctx = CTX(self.__screen)

        # Generate stars for background
        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         uniform(1, 2)) for _ in range(50)]

        self.__clock = pg.time.Clock()

    def draw_background(self) -> None:
        self.__ctx.background(0)  # Clear screen to background color

        # Draw stars
        self.__ctx.fill(255)
        for x, y, size in self.__stars:
            self.__ctx.circle(x, y, size)

    def finish_render(self) -> None:
        pg.display.flip()
        self.__clock.tick(Constants.FPS)

    def draw_sprites(self, player: Player, asteroids: List[Asteroid]) -> None:
        self.draw_sprite(player.sprite)  # Draw player

        # Draw asteroids
        for asteroid in asteroids:
            self.draw_sprite(asteroid.sprite)

        # Draw projectiles
        for projectile in player.projectiles:
            self.draw_sprite(projectile.sprite)

    def draw_score(self, score: int, high_score: int) -> None:
        self.__ctx.font_size(36)

        # Draw score
        self.__ctx.text(f'SCORE: {score}', 25, 100)

        # Draw high score
        self.__ctx.text(f'HIGH SCORE: {high_score}', 25, 25)

    def draw_paused(self) -> None:
        self.__ctx.fill(255, 0, 0)
        self.__ctx.font_size(100)
        self.__ctx.text('GAME PAUSED',
                        Constants.WINDOW_WIDTH * .5,
                        Constants.WINDOW_HEIGHT * .5,
                        center=True)

    def draw_sprite(self, sprite: Sprite) -> None:
        self.__screen.blit(sprite.image, sprite.rect)
