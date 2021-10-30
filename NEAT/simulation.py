from __future__ import annotations

from src.controller import Controller
from NEAT.genome import Genome


class Simulation:
    def __init__(self) -> None:
        ''' Simulates a thinking AI player. '''

        self.__controller = Controller(ai=True)
        self.__fitness = 0

    def update(self, iterations: int = 1) -> None:
        ''' Updates the simulation. '''

        for _ in range(iterations):
            self.__controller.update()
            self.__controller.think()

    def calculate_fitness(self) -> None:
        ''' Calculates score used to determine player's fitness '''

        accuracy = self.__controller.shots_hit / self.__controller.shots_fired \
            if self.__controller.shots_fired != 0 else -.5

        self.__fitness = ((self.__controller.score + 1) * 10 + self.__controller.lifespan * 5) * ((accuracy + 1) ** 2)

    def crossover(self, parent2: Simulation) -> Simulation:
        '''
        Crossovers this simulation with another parent and returns the child,
        while This parent is the fittest.
        '''

        child = Simulation()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generate_phenotype()
        return child

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
    def fitness(self) -> float:
        return self.__fitness

    @property
    def brain(self) -> Genome:
        return self.__controller.brain
    
    @property
    def dead(self) -> bool:
        return self.__controller.dead

    @fitness.setter
    def fitness(self, fitness: float) -> None:
        self.__fitness = fitness

    @brain.setter
    def brain(self, brain: Genome) -> None:
        self.__controller.brain = brain