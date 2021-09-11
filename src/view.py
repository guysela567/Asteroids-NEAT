from src.model import Model
from utils.constants import Constants

import arcade
from arcade import color
from random import uniform, randint


class View():
    def __init__(self, model: Model) -> None:
        ''' Graphical setup '''

        self.__model = model

        arcade.set_background_color(color.BLACK)

        self.__stars = [(uniform(0, Constants.WINDOW_WIDTH),
                         uniform(0, Constants.WINDOW_HEIGHT),
                         randint(1, 2)) for _ in range(100)]

    def draw(self) -> None:
        ''' Renders the screen. '''

        arcade.start_render()  # Clear screen to background color

        # Draw stars
        for x, y, size in self.__stars:
            arcade.draw_point(x, y, color.WHITE, size)

        # Draw player
        self.__model.player.sprite.draw()
        self.__model.player.sprite.draw_hit_box(color.AERO_BLUE)

        # Draw asteroids
        for asteroid in self.__model.asteroids:
            asteroid.sprite.draw()
            asteroid.sprite.draw_hit_box(color.AERO_BLUE)

        arcade.finish_render()  # Draw frame
