from __future__ import annotations

from utils.constants import Constants
from src.model import Model

from NEAT.genome import Genome

from components.asteroid import Asteroid
from components.player import Player


class Controller:
    def __init__(self, ai: bool = False) -> None:
        self.__model = Model(ai=ai)

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

    def reset(self) -> None:
        self.__model.reset()
    
    @property
    def player(self) -> Player:
        return self.__model.player

    @property
    def asteroids(self) -> list[Asteroid]:
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
    
    @property
    def shots_fired(self) -> float:
        return self.__model.shots_fired
    
    @property
    def shots_hit(self) -> float:
        return self.__model.shots_hit
    
    @property
    def lifespan(self) -> int:
        return self.__model.lifespan
    
    @property
    def dead(self) -> bool:
        return self.__model.dead

    @property
    def brain(self) -> Genome:
        return self.__model.brain

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__model.brain = brain
        