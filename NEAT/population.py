from __future__ import annotations
from NEAT.genome import Genome

from NEAT.simulation import Simulation
from NEAT.connection_history import ConnectionHistory
from NEAT.species import Species
from utils.constants import Constants

import math
import os


class Population:
    '''The population of all thinking beings (Genomes),
    Applies the genetic algorithm for each simulation
    :param size: the size of the population
    '''

    def __init__(self, size: int) -> None:
        self.__size = size
        self.__generation = 0
        
        self.__batch_amount = math.ceil(self.__size / Constants.BATCH_SIZE)
        self.__species: list[Species] = []

        # Record of all mutations in this population
        self.__innovation_history: list[ConnectionHistory] = []

        # Create file saving Directory if it does not exist
        if Constants.TRAINING:
            if not os.path.exists('data'):
                os.mkdir('data')
            if not os.path.exists('data/model'):
                os.mkdir('data/model')

        # Populate with simulations
        self.__players = [Simulation() for _ in range(self.__size)]
        for sim in self.__players:
            # Start with an extra mutation for variaty
            sim.brain.mutate(self.__innovation_history)
            sim.brain.generate_phenotype()

        self.__best_player: Simulation = self.__players[0].clone()
        self.__best_fitness = 0

        self.__batch_index = 0
        self.__batch = self.get_current_batch()

        # Create/clear logs file
        if Constants.TRAINING:
            with open('data/logs.txt', 'w') as f:
                f.write('')

    def update(self, iterations: int = 1) -> None:
        '''Updates the population
        :param iterations: the number of iterations to update by
        '''

        if self.current_batch_done():
            self.next_batch()
        self.update_current_batch(iterations=iterations)

    def set_best_player(self) -> None:
        '''Sets the best player and best score ever seen in this generation'''
        best = self.__species[0].players[0]
        if best.fitness > self.__best_fitness:
            self.__best_fitness = best.fitness
            self.__best_player = best.clone()

    def update_alive(self, iterations: int = 1) -> None:
        '''Updates all alive simulations
        :param iterations: the number of iterations to update by
        '''
        
        for sim in self.__players:
            if not sim.dead:
                sim.update(iterations=iterations)

    def update_current_batch(self, iterations: int = 1) -> None:
        '''Updates all alive simulations in batch
        :param iterations: the number of iterations to update by
        '''

        for sim in self.__batch:
            if not sim.dead:
                sim.update(iterations=iterations)

    def done(self) -> None:
        '''Returns whether all player simulations are dead'''
        for sim in self.__players:
            if not sim.dead:
                return False
        return True

    def current_batch_done(self) -> bool:
        '''Returns whether the current batch is done (all simulations in the batch are dead)'''
        for sim in self.__batch:
            if not sim.dead:
                return False
        return True
    
    def get_current_batch(self) -> list[Simulation]:
        '''Returns the current batch of simulations'''
        start = Constants.BATCH_SIZE * self.__batch_index
        end = start + Constants.BATCH_SIZE
        if end > len(self.__players):
            end = len(self.__players)
        return self.__players[start:end]

    def next_batch(self) -> None:
        '''Proceeds to next batch of the generation'''
        self.__batch_index += 1
        self.__batch = self.get_current_batch()

    def natural_selection(self) -> None:
        '''Simulates nature's natural selection process,
        called at the end of each generation
        '''
        
        self.__generation += 1
        self.speciate() # Seperate into species
        self.calculate_fitness() # Calculate fitness for each simulation
        self.sort_species() # Sort from best to worst, based on fitness
        self.cull_species() # Kill genomes that have not survived
        self.kill_stale_species(15) # Kill species which have not improved for a while
        self.kill_bad_species() # Kill species which cannot reproduce
        self.set_best_player() # Update best player and best score ever

        if Constants.TRAINING:
            for s in range(5): # Save best genome of 5 best species to file
                if len(self.__species) >= s + 1:
                    self.__species[s].champion.brain.save(f'data/model/gen{self.__generation - 1}_spec{s + 1}.json')
            # Save/update best ever genome
            self.__best_player.brain.save('data/best.json')

            # Log results
            with open('data/logs.txt', 'a') as f:
                f.write(f'new generation: {self.__generation}\n')
                f.write(f'number of mutations: {len(self.__innovation_history)}\n')
                f.write(f'number of species: {len(self.__species)}\n')
                f.write(f'best fitness: {self.__best_fitness}\n')
                f.write(f'best score: {self.__best_player.score}\n')
                f.write('------------------------------------------------------\n')

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
                if s.same_species(sim.brain):
                    s.add(sim)
                    species_found = True
                    break
            
            # If none were similar enough or species list is empty
            # then create a new species based on this player
            if not species_found:
                self.__species.append(Species(sim))
            
    def calculate_fitness(self) -> None:
        '''Calculates the fitness of all of the simulations'''
        for sim in self.__players:
            sim.calculate_fitness()

    def sort_species(self) -> None:
        '''Sorts the species and the players within each species
        based on their fitness, sorted in descending order
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
        '''Removes the species which cannot reproduce (fitness is too low)'''
        avg_sum = self.get_avg_fitness_sum()

        # Skip best species
        for i in range(len(self.__species) - 1, 0, -1): # Iterate backwards
            # Compare this species with the rest of the species
            if len(self.__species[i].players) == 0 or \
                (self.__species[i].avg_fitness / avg_sum) * self.__size < 1:
                # Kill it if it is far worse than the rest
                self.__species.pop(i)

    def cull_species(self) -> None:
        '''Kills the bottom half of simulations for each species'''
        for s in self.__species:
            if len(s.players) > 0:
                s.cull()
                # Apply fitness sharing and set average fitness 
                # for the updated amount of simulations
                s.apply_fitness_sharing()
                s.set_avg_fitness()

    def get_avg_fitness_sum(self) -> float:
        '''Returns the average fitness sum of all species in the population'''
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