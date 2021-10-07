from utils.constants import Constants
from utils.sprite import Sprite
from utils.geometry.raycasting import RaySet
from utils.drawing import Context, Screen

from components.player import Player
from components.asteroid import Asteroid

from src.controller import Controller

from typing import List

from random import uniform

import pygame as pg
from pygame.event import Event


class View():
    def __init__(self, cnt: Controller = None) -> None:
        self.__controller = Controller() if cnt is None else cnt

        # Graphical setup
        pg.init()

        self.__screen = Screen(Constants.WINDOW_WIDTH,
                               Constants.WINDOW_HEIGHT,
                               Constants.WINDOW_TITLE)

        self.__ctx = Context(self.__screen)

        # Generate stars for background
        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         uniform(7, 10)) for _ in range(50)]

        self.__clock = pg.time.Clock()

    def start(self) -> None:
        while True:
            self.update()
            self.__controller.update()

    def update(self) -> None:
        # Handle user input
        for event in pg.event.get():
            self.handle_event(event)

        # Update graphics
        self.draw_background()
        self.draw_sprites(self.__controller.player, self.__controller.asteroids)
        self.draw_score(self.__controller.score, self.__controller.high_score)

        if self.__controller.paused:
            self.draw_paused()

        self.draw_rays(self.__controller.player.ray_set)

        for asteroid in self.__controller.asteroids:
            self.draw_poly(asteroid.sprite.rect_verts)

        self.finish_render()

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
            self.__controller.toggle_pause()

        elif key == pg.K_UP:
            self.__controller.start_boost()

        elif key == pg.K_RIGHT:
            self.__controller.start_rotate(1)

        elif key == pg.K_LEFT:
            self.__controller.start_rotate(-1)

        elif key == pg.K_SPACE:
            self.__controller.shoot()

    def on_key_release(self, key: int) -> None:
        if key == pg.K_UP:
            self.__controller.stop_boost()

        elif key == pg.K_RIGHT and self.__controller.player.rotate_dir == 1 \
                or key == pg.K_LEFT and self.__controller.player.rotate_dir == -1:
            self.__controller.stop_rotate()

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
        self.__ctx.image(sprite.image, *sprite.rect)

    def draw_rays(self, ray_set: RaySet) -> None:
        self.__ctx.fill(0, 255, 0)
        for ray in ray_set:
            self.__ctx.line(*ray, 5)

    def draw_poly(self, verts: List[Sprite]) -> None:
        self.__ctx.fill(0, 255, 0)
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]
            self.__ctx.line(*pos1, *pos2, 5)

    @property
    def controller(self) -> Controller:
        return self.__controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        self.__controller = controller