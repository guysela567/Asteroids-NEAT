from src.model import Model
from utils.constants import Constants

import arcade
from arcade import color
from random import uniform


class View():
    def __init__(self, model: Model) -> None:
        ''' Graphical setup '''

        self.__model = model

        arcade.set_background_color(color.BLACK)

        # Generate stars for background
        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         uniform(1, 2)) for _ in range(50)]

        # Load retro font
        arcade.load_font('assets/fonts/HyperspaceBold.ttf')

    def draw(self) -> None:
        ''' Renders the screen. '''

        arcade.start_render()  # Clear screen to background color

        # Draw stars
        for x, y, size in self.__stars:
            arcade.draw_point(x, y, color.WHITE, size)

        # Draw player
        self.__model.player.sprite.draw()

        # Draw asteroids
        for asteroid in self.__model.asteroids:
            asteroid.sprite.draw()

        # Draw player's projectiles
        for projectile in self.__model.player.projectiles:
            projectile.sprite.draw()

        # Draw score
        arcade.draw_text(f'SCORE: {self.__model.score}', 25,
                         100, font_size=36, font_name='Hyperspace')

        # Draw high score
        arcade.draw_text(f'HIGH SCORE: {self.__model.high_score}', 25,
                         25, font_size=36, font_name='Hyperspace')

        arcade.finish_render()  # Draw frame

        # TODO Add a sprite list
        # TODO Change Sprites
