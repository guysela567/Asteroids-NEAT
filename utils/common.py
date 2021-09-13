from utils.constants import Constants

from typing import Tuple
from arcade import Sprite


class Common:
    def handle_offscreen(x: float, y: float, sprite: Sprite) -> Tuple[float, float]:
        # left to right
        if x + sprite.width * .5 < 0:
            return Constants.WINDOW_WIDTH + sprite.width * .5, y

        # right to left
        if x - sprite.width * .5 > Constants.WINDOW_WIDTH:
            return -sprite.width * .5, y

        # bottom to top
        if y + sprite.height * .5 < 0:
            return x, Constants.WINDOW_HEIGHT + sprite.height * .5

        # top to bottom
        if y - sprite.height * .5 > Constants.WINDOW_HEIGHT:
            return x, -sprite.height * .5

        return x, y  # Not offscreen
