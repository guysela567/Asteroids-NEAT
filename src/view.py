from utils.constants import Constants

from components.player import Player
from components.asteroid import Asteroid

from typing import List

import arcade
from arcade import color
from random import uniform


class View():
    def __init__(self) -> None:
        ''' Graphical setup '''
        arcade.set_background_color(color.BLACK)

        # Generate stars for background
        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         uniform(1, 2)) for _ in range(50)]

        # Load retro font
        arcade.load_font('assets/fonts/HyperspaceBold.ttf')

    def draw_background(self) -> None:
        arcade.start_render()  # Clear screen to background color

        # Draw stars
        for x, y, size in self.__stars:
            arcade.draw_point(x, y, color.WHITE, size)

    def finish_render(self) -> None:
        arcade.finish_render()

    def draw_sprites(self, player: Player, asteroids: List[Asteroid]) -> None:
        player.sprite.draw()  # Draw player

        # Draw asteroids
        for asteroid in asteroids:
            asteroid.sprite.draw()

        # Draw projectiles
        for projectile in player.projectiles:
            projectile.sprite.draw()

    def draw_score(self, score: int, high_score: int) -> None:
        # Draw score
        arcade.draw_text(f'SCORE: {score}', 25,
                         100, font_size=36, font_name='Hyperspace')
        # Draw high score
        arcade.draw_text(f'HIGH SCORE: {high_score}', 25,
                         25, font_size=36, font_name='Hyperspace')

    def draw_paused(self) -> None:
        arcade.draw_text('GAME PAUSED',
                         Constants.WINDOW_WIDTH * .5,
                         Constants.WINDOW_HEIGHT * .5,
                         font_name='Hyperspace',
                         anchor_x='center',
                         anchor_y='center',
                         color=color.RED,
                         font_size=100)
