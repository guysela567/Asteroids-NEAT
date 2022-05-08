from __future__ import annotations

from utils.constants import Constants
from src.model import Model

from NEAT.genome import Genome

from components.asteroid import Asteroid
from components.player import Player


class Controller:
    '''Connects between the game screen (the view) and the model holding the game data
    :param ai: whether to use AI for the player agent
    '''

    def __init__(self, ai: bool = False) -> None:
        self.__model = Model(ai=ai)

    def update(self) -> None:
        '''Updates the game model'''
        if not self.__model.paused:
            self.__model.update(1 / Constants.FPS)

    def toggle_pause(self) -> None:
        '''Toggles between play/pause'''
        self.__model.toggle_pause()

    def start_boost(self) -> None:
        '''Starts boosting the player'''
        self.__model.player.start_boost()

    def stop_boost(self) -> None:
        '''Stops boosting the player'''
        self.__model.player.stop_boost()

    def start_rotate(self, dir: int) -> None:
        '''Starts rotating the player
        :param dir: the direction of the player (1 for anti-clockwize, 1 for clockwize)'''
        self.__model.player.start_rotate(dir)

    def stop_rotate(self) -> None:
        '''Stops rotating the player'''
        self.__model.player.stop_rotate()
    
    def shoot(self) -> None:
        '''Fires a projectile from the player'''
        self.__model.player.shoot()

    def think(self) -> None:
        '''Makes the vision list and acts according to the neural network predictions'''
        self.__model.think()

    def dump_highscore(self) -> None:
        '''Saves the model's highscore to a file'''
        self.__model.dump_highscore()

    def reset(self) -> None:
        '''Resets the model'''
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

    @property
    def seed(self) -> int:
        return self.__model.seed
    
    @property
    def ai_playing(self) -> bool:
        return self.__model.ai_playing

    @property
    def ai_training(self) -> bool:
        return self.__model.ai_training

    @property
    def game_over(self) -> bool:
        return self.__model.game_over
    
    @property
    def lives(self) -> int:
        return self.__model.lives

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__model.brain = brain

    @seed.setter
    def seed(self, seed: int) -> None:
        self.__model.seed = seed

    @ai_playing.setter
    def ai_playing(self, ai) -> None:
        self.__model.ai_playing = ai
        