from components.player import Player
from components.asteroid import Asteroid

from utils.constants import Constants

from typing import List
from random import uniform


class Model:
    def __init__(self) -> None:
        self.__player = Player(Constants.WINDOW_WIDTH *
                               0.5, Constants.WINDOW_HEIGHT * 0.5)

        self.__asteroids = [Asteroid(uniform(0, Constants.WINDOW_WIDTH),
                                     uniform(0, Constants.WINDOW_HEIGHT)) for _ in range(4)]

    def update(self) -> None:
        self.__player.update()

        for asteroid in self.__asteroids:
            asteroid.update()

    @property
    def player(self) -> Player:
        return self.__player

    @property
    def asteroids(self) -> List[Asteroid]:
        return self.__asteroids
