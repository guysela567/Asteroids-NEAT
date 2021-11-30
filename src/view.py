from __future__ import annotations

from utils.constants import Constants
from utils.sprite import Sprite
from utils.geometry.raycasting import RaySet
from utils.drawing import Screen

from components.player import Player
from components.asteroid import Asteroid

from src.controller import Controller

from random import uniform


class View(Screen):
    def __init__(self, controller: Controller = None) -> None:
        super().__init__(Constants.WINDOW_WIDTH, 
                         Constants.WINDOW_HEIGHT, 
                         Constants.WINDOW_TITLE, 
                         Constants.FPS)

        self.__controller = Controller() if controller is None else controller

        # Graphical setup
        # Generate stars for background
        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         uniform(7, 10)) for _ in range(50)]

    def draw(self) -> None:
        # Update graphics
        self.draw_background()
        self.draw_sprites(self.__controller.player, self.__controller.asteroids)
        self.draw_score(self.__controller.score, self.__controller.high_score)

        if self.__controller.paused:
            self.draw_paused()

        self.draw_rays(self.__controller.player.ray_set)

        for asteroid in self.__controller.asteroids:
            self.draw_poly(asteroid.sprite.rect_verts)

    def update(self) -> None:
        self.__controller.update()

    def on_key_down(self, key: int) -> None:
        if key == self.keys['p']:
            self.__controller.toggle_pause()

        elif key == self.keys['UP']:
            self.__controller.start_boost()

        elif key == self.keys['RIGHT']:
            self.__controller.start_rotate(1)

        elif key == self.keys['LEFT']:
            self.__controller.start_rotate(-1)

        elif key == self.keys['SPACE']:
            self.__controller.shoot()

    def on_key_up(self, key: int) -> None:
        if key == self.keys['UP']:
            self.__controller.stop_boost()

        elif key == self.keys['RIGHT'] and self.__controller.player.rotate_dir == 1 \
                or key == self.keys['LEFT'] and self.__controller.player.rotate_dir == -1:
            self.__controller.stop_rotate()

    def draw_background(self) -> None:
        self.background(0)  # Clear screen to background color

        # Draw stars
        self.fill(255)
        for x, y, size in self.__stars:
            self.circle(x, y, size)

    def draw_sprites(self, player: Player, asteroids: list[Asteroid]) -> None:
        self.draw_sprite(player.sprite)  # Draw player

        # Draw asteroids
        for asteroid in asteroids:
            self.draw_sprite(asteroid.sprite)

        # Draw projectiles
        for projectile in player.projectiles:
            self.draw_sprite(projectile.sprite)

    def draw_score(self, score: int, high_score: int) -> None:
        self.font_size(36)

        # Draw score
        self.text(f'SCORE: {score}', 25, 100)

        # Draw high score
        self.text(f'HIGH SCORE: {high_score}', 25, 25)

    def draw_paused(self) -> None:
        self.fill(255, 0, 0)
        self.font_size(100)
        self.text('GAME PAUSED',
                        Constants.WINDOW_WIDTH * .5,
                        Constants.WINDOW_HEIGHT * .5,
                        center=True)

    def draw_sprite(self, sprite: Sprite) -> None:
        self.image(sprite.image, *sprite.rect)

    def draw_rays(self, ray_set: RaySet) -> None:
        self.fill(0, 255, 0)
        for ray in ray_set:
            self.line(*ray, 5)

    def draw_poly(self, verts: list[Sprite]) -> None:
        self.fill(0, 255, 0)
        for i in range(len(verts)):
            pos1 = verts[i]
            pos2 = verts[i + 1] if i < len(verts) - 1 else verts[0]
            self.line(*pos1, *pos2, 5)

    @property
    def controller(self) -> Controller:
        return self.__controller

    @controller.setter
    def controller(self, controller: Controller) -> None:
        self.__controller = controller