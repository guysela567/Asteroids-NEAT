from ai.genetic_player import GeneticPlayer
from ai.neural_network import NeuralNetwork
from src.controller import Controller

from typing import List
from random import random


class Population:
    def __init__(self, size: int) -> None:
        self.__size = size
        self.__players = [GeneticPlayer() for _ in range(self.__size)]
        self.__gen_no = 0

    def start(self) -> None:
        for player in self.__players:
            player.start()

    def next_gen(self) -> None:
        self.__gen_no += 1
        self.calculate_fitness()
        
        for player in self.__players:
            player.controller.brain = self.pool_selection()
            player.controller.reset()
            player.start()

    def calculate_fitness(self) -> None:
        score_sum = sum(p.score for p in self.__players)

        for player in self.__players:
            player.fitness = player.score / score_sum

    def pool_selection(self) -> NeuralNetwork:
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

        chosen = self.controllers[index].brain.copy()
        chosen.mutate(0.1)
        return chosen


    @property
    def players(self) -> List[GeneticPlayer]:
        return self.__players
    
    @property
    def controllers(self) -> List[Controller]:
        return [p.controller for p in self.__players]

    @property
    def all_dead(self) -> bool:
        return all(c.dead for c in self.controllers)

    @property
    def gen_no(self) -> int:
        return self.__gen_no