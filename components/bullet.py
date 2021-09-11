from arcade import Sprite

from utils.constants import Constants


class Bullet:
    def __init__(self, x: float, y: float, angle: float) -> None:
        self.__x = x
        self.__y = y
        self.__angle = angle

        self.__sprite = Sprite('assets/sprites/bullet.png',
                               Constants.ASTEROID_SPRITE_SCALE)

    def update(self) -> None:
        pass
