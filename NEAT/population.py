from src.controller import Controller

from NEAT.simulation import Simulation
from NEAT.genome import Genome

from typing import List
from random import random


class Population:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__players = [Simulation() for _ in range(self.__size)]
        self.__generation = 1

    def start(self) -> None:
        for player in self.__players:
            player.start()

    def next_gen(self) -> None:
        self.__generation += 1
        self.calculate_fitness()
        
        for player in self.__players:
            player.controller.brain = self.pool_selection()
            player.controller.reset()

    def calculate_fitness(self) -> None:
        score_sum = sum(p.score for p in self.__players)

        for player in self.__players:
            player.fitness = player.score / score_sum

    def pool_selection(self) -> Genome:
        # TODO: Add crossover
        
        index = 0
        # Pick a random number between 0 and 1
        # This allows weaker players to continue to next generation
        # While still letting the majority of the strong players in
        r = random()
        while r > 0:
            # reduce by fitness untill value is smaller than zero
            r -= self.__players[index].fitness
            index += 1
        # Go back once
        index -= 1

        chosen = self.controllers[index].brain.clone()
        # chosen.mutate(0.01)
        return chosen

    @property
    def players(self) -> List[Simulation]:
        return self.__players
    
    @property
    def controllers(self) -> List[Controller]:
        return [p.controller for p in self.__players]

    @property
    def all_dead(self) -> bool:
        return all(c.dead for c in self.controllers)

    @property
    def generation(self) -> int:
        return self.__generation