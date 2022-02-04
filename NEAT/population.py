from __future__ import annotations
from NEAT.genome import Genome

from NEAT.simulation import Simulation
from NEAT.connection_history import ConnectionHistory
from NEAT.species import Species
from utils.constants import Constants

import math


class Population:
    def __init__(self, size: int) -> None:
        '''
        The population of all thinking beings.
        Applies the principles of natural selection for each simulation.
        '''

        self.__size = size
        self.__generation = 1
        
        self.__batch_amount = math.ceil(self.__size / Constants.BATCH_SIZE)

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
            if Constants.TRAINING:
                for _ in range(Constants.STARTING_CONNECTIONS):
                    sim.brain.add_connection(self.__innovation_history)
                sim.brain.mutate(self.__innovation_history)
                sim.brain.generate_phenotype()
            else:
                sim.brain = Genome.load(f'data/gen{Constants.GEN_TAKEN}_spec{Constants.SPEC_TAKEN}.json')

        self.__batch_index = 0
        self.__batch = self.get_current_batch()
        print(len(self.__batch))

    def update(self, iterations: int = 1) -> None:
        ''' Updates the population. '''

        if self.current_batch_done():
            self.next_batch()
        self.update_current_batch(iterations=iterations)

    def update_alive(self, iterations: int = 1) -> None:
        ''' Updates all alive simulations. '''
        
        for sim in self.__players:
            if not sim.dead:
                sim.update(iterations=iterations)

    def update_current_batch(self, iterations: int = 1) -> None:
        ''' Update all alive simulations in batch. '''

        for sim in self.__batch:
            if not sim.dead:
                sim.update(iterations=iterations)

    def done(self) -> None:
        ''' Returns whether all player simulations are dead. '''

        for sim in self.__players:
            if not sim.dead:
                return False
        return True

    def current_batch_done(self) -> bool:
        for sim in self.__batch:
            if not sim.dead:
                return False
        return True
    
    def get_current_batch(self) -> list[Simulation]:
        start = Constants.BATCH_SIZE * self.__batch_index
        end = start + Constants.BATCH_SIZE
        if end > len(self.__players):
            end = len(self.__players)
        return self.__players[start:end]

    def next_batch(self) -> None:
        self.__batch_index += 1
        self.__batch = self.get_current_batch()

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

        if Constants.TRAINING:
            for s in range(4): # Save best genome of 4 best species to file
                self.__species[0].champion.brain.save(f'data/gen{self.__generation - 1}_spec{s + 1}.json')
        
        print(f'new generation: {self.__generation}')
        print(f'number of mutations: {len(self.__innovation_history)}')
        print(f'number of species: {len(self.__species)}')
        print(f'best fitness: {self.__species[0].best_fitness}')
        print('------------------------------------------------------')

        # Repopulate with new simulations
        avg_sum = self.get_avg_fitness_sum()
        children: list[Simulation] = []
        for s in self.__species:
            # Clone the champion without mutations
            children.append(s.champion.clone())
            # -1 since champion was already added
            children_number = math.floor((s.avg_fitness / avg_sum) * self.__size) - 1
            for _ in range(children_number): # Add children
                children.append(s.get_child(self.__innovation_history))
        
        # Sometimes resulted children amount will not be enough
        # due to flooring the number of children for each species
        while len(children) < self.__size:
            # Get more children from the best species untill the number of children gets big enough
            children.append(self.__species[0].get_child(self.__innovation_history))

        # Copy children to new players
        self.__players = children.copy()
        for sim in self.__players:
            sim.brain.generate_phenotype() # Generate neural network for each child
            sim.seed = self.__generation - 1
            sim.reset()

        # Set current batch
        self.__batch_index = 0
        self.__batch = self.get_current_batch()
        
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
        Sorts the species and the players within each species
        based on their fitness, in descending order.
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
            # Kill empty species
            # this is caused by emptying each species
            # in the speciate function
            if len(self.__species[i].players) == 0:
                self.__species.pop(i)

            # Compare this species with the rest of the species
            if (self.__species[i].avg_fitness / avg_sum) * self.__size < 1:
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
    def all_dead(self) -> bool:
        return all(sim.dead for sim in self.__players)

    @property
    def generation(self) -> int:
        return self.__generation

    @property
    def batch_index(self) -> int:
        return self.__batch_index

    @property
    def batch(self) -> list[Simulation]:
        return self.__batch

    @property
    def batch_amount(self) -> int:
        return self.__batch_amount