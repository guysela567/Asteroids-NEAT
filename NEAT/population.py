from __future__ import annotations

from src.controller import Controller

from NEAT.simulation import Simulation
from NEAT.connection_history import ConnectionHistory
from NEAT.species import Species

import math


class Population:
    def __init__(self, size: int) -> None:
        '''
        The population of all thinking beings.
        Applies the principles of natural selection for each simulation.
        '''

        self.__size = size
        self.__generation = 1

        # TODO: ADD the following features:
        # self.__best_player: Simulation = None
        # self.__best_score = 0
        # self.__gen_players: list[Simulation] = []
        # self.__mass_extinction_event = False
        
        self.__species: list[Species] = []

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

    def done(self) -> None:
        ''' Returns whether all player simulations are dead. '''

        for sim in self.__players:
            if not sim.dead:
                return False
        return True

    def natural_selection(self) -> None:
        '''
        Simulates nature's natural selection process,
        called at the end of each generation.
        '''

        self.speciate() # Seperate into species
        self.calculate_fitness() # Calculate fitness for each simulation
        self.sort_species() # Sort from best to worst, based on fitness
        self.cull_species() # Kill genomes that have not survived
        self.kill_stale_species() # Kill species which have not improved for a while
        self.kll_bad_species() # Kill species which cannot reproduce
        
        print(f'new generation: {self.__generation}')
        print(f'number of muatations: {len(self.__innovation_history)}')
        print(f'number of species: {len(self.__species)}')
        print('------------------------------------------------------')

        # Repopulate with new simulations
        avg_sum = self.get_avg_fitness_sum()
        children: list[Simulation] = []
        for s in self.__species:
            # Clone the champion without mutations
            children.append(s.champion.clone())
            # -1 since champion was already added
            children_number = math.floor((s.avg_fitness / avg_sum) * len(self.__players)) - 1
            for _ in range(children_number): # Add children
                children.append(s.get_child(self.__innovation_history))
        
        # Sometimes resulted children amount will not be enough
        # due to flooring the number of children for each specie
        if len(children) < len(self.__players):
            children.append(self.__players[0].clone()) # Clone first player of last generation
            # Due to species list being sorted from best to worst,
            # for each generation excluding the first one, the first 
            # player in the list will always be from the previous best species

        # If number of children is still not enough
        # then add a child of best specie untill the number of children gets big enough
        while len(children) < len(self.__players):
            children.append(self.__species[0].get_child(self.__innovation_history))

        # Copy children to new players
        self.__players = children.copy()
        for sim in self.__players:
            sim.brain.generate_phenotype() # Generate neural network for each child

        self.__generation += 1
        
    def speciate(self) -> None:
        '''
        Seperates the population's players into species based on their similarity 
        to the leaders of each species in the previous generation.
        '''

        # Empty all species
        for s in self.__species:
            s.players = []
        
        # Iterate through each simulation
        for sim in self.__players:
            species_found = False

            # Check for each species if simulation fits
            for s in self.__species:
                if sim.brain in s:
                    s.add_to_species(sim)
                    species_found = True
                    break
            
            # If none were similar enough or species list is empty
            if not species_found: # Create a new species based on this player
                self.__species.add(sim)


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