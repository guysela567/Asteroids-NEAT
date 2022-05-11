from __future__ import annotations

from src.controller import Controller


class Simulation(Controller):
    '''Simulates a thinking AI player'''
    def __init__(self) -> None:
        super().__init__(ai=True)
        self.__fitness = 0

    def update(self, iterations: int = 1) -> None:
        '''Updates the simulation
        :param iterations: the number of iterations to update by
        '''

        for _ in range(iterations):
            super().update()
            self.think()

    def calculate_fitness(self) -> None:
        '''Calculates score used to determine player's survival in next generations'''
        accuracy = self.shots_hit / self.shots_fired
        self.__fitness = (self.score + 1) * 100
        self.__fitness += self.lifespan * 50
        self.__fitness *= accuracy ** 2
    
    def crossover(self, parent2: Simulation) -> Simulation:
        '''Crossovers this simulation with another parent and returns the child,
        while This parent is the fittest
        :param parent2: the other parent to crossover with
        '''

        child = Simulation()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generate_phenotype()
        return child

    def clone(self) -> Simulation:
        '''Returns a copy of this simulation with the same genome brain'''
        copy = Simulation()
        # Copy brain
        copy.brain = self.brain.clone()
        copy.brain.generate_phenotype()
        # Copy score and fitness values
        copy.score = self.score
        copy.fitness = self.fitness
        return copy
    
    @property
    def fitness(self) -> float:
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness: float) -> None:
        self.__fitness = fitness