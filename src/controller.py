import arcade
from utils.constants import Constants
from src.model import Model
from src.view import View


class Controller(arcade.Window):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH,
                         Constants.WINDOW_HEIGHT, Constants.WINDOW_TITLE)

        self.__model = Model()
        self.__view = View(self.__model)

    def start(self):
        arcade.run()

    def on_draw(self) -> None:
        self.__view.draw()

    def on_update(self, delta_time: float) -> None:
        ''' Game logic goes here. '''
        if not self.__model.paused:
            self.__model.update(delta_time)

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.P:
            self.__model.toggle_pause()

        elif key == arcade.key.UP:
            self.__model.player.start_boost()

        elif key == arcade.key.RIGHT:
            self.__model.player.start_rotate(-1)

        elif key == arcade.key.LEFT:
            self.__model.player.start_rotate(1)

        elif key == arcade.key.SPACE:
            if self.__model.player.can_shoot:
                self.__model.play_sound('fire')

            self.__model.player.shoot()

    def on_key_release(self, key: int, modifiers: int) -> None:
        if key == arcade.key.UP:
            self.__model.player.stop_boost()

        elif key == arcade.key.RIGHT and self.__model.player.rotate_dir == -1 \
                or key == arcade.key.LEFT and self.__model.player.rotate_dir == 1:
            self.__model.player.stop_rotate()
