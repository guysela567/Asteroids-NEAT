from utils.constants import Constants
from src.model import Model

from components.asteroid import Asteroid
from components.player import Player

from typing import List
from time import sleep


class Controller:
    def __init__(self) -> None:
        self.__model = Model()

    def update(self) -> None:
        # Update model
        if not self.__model.paused:
            self.__model.update(1 / Constants.FPS)

    def toggle_pause(self) -> None:
        self.__model.toggle_pause()

    def start_boost(self) -> None:
        self.__model.player.start_boost()

    def stop_boost(self) -> None:
        self.__model.player.stop_boost()

    def start_rotate(self, dir: int) -> None:
        self.__model.player.start_rotate(dir)

    def stop_rotate(self) -> None:
        self.__model.player.stop_rotate()
    
    def shoot(self) -> None:
        self.__model.player.shoot()

    def think(self) -> None:
        self.__model.think()

    @property
    def model(self) -> Model:
        return self.__model
    
    @property
    def player(self) -> Player:
        return self.__model.player

    @property
    def asteroids(self) -> List[Asteroid]:
        return self.__model.asteroids

    @property
    def score(self) -> int:
        return self.__model.score

    @property
    def high_score(self) -> int:
        return self.__model.high_score

    @property
    def paused(self) -> bool:
        return self.__model.paused