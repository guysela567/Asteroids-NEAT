from __future__ import annotations
from utils.constants import Constants
from src.controller import Controller
from NEAT.genome import Genome

from _thread import start_new_thread

import time


class Simulation:
    def __init__(self) -> None:
       self.__controller = Controller(ai=True)
       self.__fitness = 0

    def start(self) -> None:
        start_new_thread(self.start_controller, (self.__controller,))

    def start_controller(self, controller: Controller) -> None:
        while True:
            if controller.dead: 
                return

            self.__controller.update()
            self.__controller.think()
            time.sleep(1 / (Constants.FPS * 10))

    def update(self) -> None:
            self.__controller.update()
            self.__controller.think()

    def clone(self) -> Simulation:
        ''' Returns a copy of this simulation with the same genome brain. '''

        copy = Simulation()
        copy.brain = self.brain
        copy.brain.generate_phenotype()
        copy.fitness = self.__fitness

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def score(self) -> int:
        ''' Calculate score used to determine player's fitness '''

        accuracy = self.__controller.shots_hit / self.__controller.shots_fired \
            if self.__controller.shots_fired != 0 else -.5

        return ((self.__controller.score + 1) * 10 + self.__controller.lifespan * 5) * ((accuracy + 1) ** 2)
    
    @property
    def fitness(self) -> float:
        return self.__fitness

    @property
    def brain(self) -> Genome:
        return self.__controller.brain

    @fitness.setter
    def fitness(self, fitness: float) -> None:
        self.__fitness = fitness

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__controller.brain = brain