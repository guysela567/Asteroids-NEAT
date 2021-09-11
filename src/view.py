import arcade
from arcade import color
from src.model import Model


class View():
    def __init__(self, model: Model) -> None:
        ''' Graphical setup '''

        self.__model = model

        arcade.set_background_color(color.BLACK)

    def draw(self) -> None:
        ''' Renders the screen. '''

        arcade.start_render()  # Clear screen to background color

        # Draw player
        self.__model.player.sprite.draw()
        self.__model.player.sprite.draw_hit_box(color.AERO_BLUE)

        # Draw asteroids
        for asteroid in self.__model.asteroids:
            asteroid.sprite.draw()
            asteroid.sprite.draw_hit_box(color.AERO_BLUE)

        arcade.finish_render()  # Draw frame
