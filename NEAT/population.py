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
            # Start with 10 connections and one extra mutation
            for _ in range(10): sim.brain.add_connection(self.__innovation_history)
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
        
        self.__generation += 1
        self.speciate() # Seperate into species
        self.calculate_fitness() # Calculate fitness for each simulation
        self.sort_species() # Sort from best to worst, based on fitness
        self.cull_species() # Kill genomes that have not survived
        self.kill_stale_species(15) # Kill species which have not improved for a while
        self.kill_bad_species() # Kill species which cannot reproduce
        
        print(f'new generation: {self.__generation}')
        print(f'number of mutations: {len(self.__innovation_history)}')
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
                    s.add(sim)
                    species_found = True
                    break
            
            # If none were similar enough or species list is empty
            # then create a new species based on this player
            if not species_found:
                self.__species.append(Species(sim))
            
    def calculate_fitness(self) -> None:
        ''' Calculates the fitness of all of the simulations. '''
        
        for sim in self.__players:
            sim.calculate_fitness()

    def sort_species(self) -> None:
        '''
        Sorts the players within each species 
        and sorts the species based their fitness,
        from the highest to the lowest
        '''

        # Sort players in each species
        for s in self.__species:
            s.sort_species()

        # Sort species list
        self.__species.sort(key=lambda s: s.best_fitness, reverse=True)

    def kill_stale_species(self, generations: float) -> None:
        '''
        Kills all species which have not seen an improvement 
        in the past given generations amount.
        '''

        # Start from index 2 in order to protect the two best species
        # while also promoting innovation by having multiple species
        for i in range(len(self.__species) - 1, 1, -1): # Iterate backwards
            if self.__species[i].staleness >= generations:
                self.__species.pop(i)
    
    def kill_bad_species(self) -> None:
        ''' Removes the species which cannot reproduce. '''

        avg_sum = self.get_avg_fitness_sum()

        # Skip best species
        for i in range(len(self.__species) - 1, 0, -1): # Iterate backwards
            # Compare this species with the rest of the species
            if (self.__species[i].avg_fitness / avg_sum) * len(self.__players) < 1:
                # Kill it if it far worse than the rest
                self.__species.pop(i)

    def cull_species(self) -> None:
        ''' Kills the bottom half of simulations for each species '''

        for s in self.__species:
            # As a result of re-speciating, some sepcies
            # may be kept without any players
            if len(s.players) > 0:
                s.cull()
                # Apply fitness sharing and set average fitness 
                # for the updated amount of simulations
                s.apply_fitness_sharing()
                s.set_avg_fitness()

    def get_avg_fitness_sum(self) -> float:
        ''' Returns the average fitness sum of all species in the population. '''

        return sum(s.avg_fitness for s in self.__species)

    @property
    def players(self) -> list[Simulation]:
        return self.__players
    
    @property
    def controllers(self) -> list[Controller]:
        return [sim.controller for sim in self.__players]

    @property
    def all_dead(self) -> bool:
        return all(sim.dead for sim in self.__players)

    @property
    def generation(self) -> int:
        return self.__generation