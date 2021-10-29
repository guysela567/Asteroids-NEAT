from __future__ import annotations

from src.controller import Controller

from NEAT.simulation import Simulation
from NEAT.genome import Genome
from NEAT.connection_history import ConnectionHistory
from NEAT.species import Species


class Population:
    def __init__(self, size: int) -> None:
        '''
        The population of all thinking beings.
        Applies the principles of natural selection for each simulation.
        '''

        self.__size = size
        self.__generation = 1

        # TODO: ADD:
        # self.__best_player: Simulation = None
        # self.__best_score = 0
        # self.__gen_players: list[Simulation] = []
        # self.__mass_extinction_event = False
        
        self.species: list[Species] = []

        # Record of all mutations in this population
        self.__innovation_history: list[ConnectionHistory] = []

        # Populate with simulations
        self.__players = [Simulation() for _ in range(self.__size)]
        for sim in self.__players:
            sim.brain.mutate(self.__innovation_history)
            sim.brain.generate_phenotype()

    def update(self, iterations: int = 1) -> None:
        ''' Updates the population. '''

        self.update_alive(iterations=iterations)

    def update_alive(self, iterations: int = 1) -> None:
        ''' Updates all alive simulations. '''

        for sim in self.__players:
            if not sim.dead:
                sim.update(iterations=iterations)


    def next_gen(self) -> None:
        ''' Deprecated. '''

        self.__generation += 1
        self.calculate_fitness()
        
        for player in self.__players:
            player.controller.brain = self.pool_selection()
            player.controller.reset()

    @property
    def players(self) -> list[Simulation]:
        return self.__players
    
    @property
    def controllers(self) -> list[Controller]:
        return [p.controller for p in self.__players]

    @property
    def all_dead(self) -> bool:
        return all(c.dead for c in self.controllers)

    @property
    def generation(self) -> int:
        return self.__generation