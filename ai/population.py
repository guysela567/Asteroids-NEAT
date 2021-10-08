from ai.genetic_player import GeneticPlayer
from src.controller import Controller

from typing import List


class Population:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__players = [GeneticPlayer() for _ in range(self.__size)]

    def start(self) -> None:
        for player in self.__players:
            player.start()

    @property
    def players(self) -> List[GeneticPlayer]:
        return self.__players
    
    @property
    def controllers(self) -> List[Controller]:
        return [player.controller for player in self.__players]