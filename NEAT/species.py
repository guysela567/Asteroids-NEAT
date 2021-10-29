from __future__ import annotations

from NEAT.simulation import Simulation
from NEAT.genome import Genome
from NEAT.connection_history import ConnectionHistory

import math
import random


class Species:
    def __init__(self, sim: Simulation) -> None:
        '''
        A group of similar simulations, containing game state and genetic information.
        Since NEAT encourages innovation,
        each genome competes against other genomes in it's species.
        '''

        self.__players: list[Simulation] = []
        self.__best_fitness = 0
        self.__avg_fitness = 0
        self.__staleness = 0 # Number of generations the species has gone without any improvements

        self.__players.append(sim)
        self.__best_fitness = sim.fitness # Only genome so it's the best
        self.__rep = sim.brain.clone() # Best player's brain to compare new genomes to

        # Compatability
        self.__EXCESS_COEFFICIENT = 1
        self.__WEIGHT_DIFFERENCE_COEFFICIENT = 0.5
        self.__COMPATABILITY_THREASHOLD = 3

    def __contains__(self, genome: Genome) -> bool:
        return self.same_species(genome)

    def same_species(self, genome: Genome) -> bool:
        ''' Returns whether the given genome belongs to this species. '''

        excess_and_disjoint = Species.get_excess_disjoint(genome, self.__rep)
        avg_weight_diff = Species.get_avg_weight_diff(genome, self.__rep)

        # Normalizes the delta function for large genomes
        normalizer = len(genome.genes) - 20
        if normalizer > 1: # Constrain to 1
            normalizer = 1

        # The delta function itself
        compatability = (self.__EXCESS_COEFFICIENT * excess_and_disjoint) / normalizer \
            + self.__WEIGHT_DIFFERENCE_COEFFICIENT * avg_weight_diff
            
        return self.__COMPATABILITY_THREASHOLD > compatability

    def add_to_species(self, sim: Simulation) -> None:
        self.__players.append(sim)

    @staticmethod
    def get_excess_disjoint(brain1: Genome, brain2: Genome) -> int:
        ''' Returns the number excess and disjoint genes (genes that do not match) between two given genomes. '''
        
        matching_count = 0
        for g1 in brain1.genes:
            for g2 in brain2.genes:
                if g1.innovation_number == g2.innovation_number:
                    matching_count += 2

        gene_num = len(brain1.genes) + len(brain2.genes) # Exclude biases
        return gene_num - matching_count

    @staticmethod
    def avg_weight_difference(brain1: Genome, brain2: Genome) -> float:
        ''' Returns the average weight difference between two given genomes. '''

        # No weights to compare
        if len(brain1.genes) == 0 or len(brain2.genes) == 0:
            return 0

        matching_count = 0
        total_diff = 0
        
        for g1 in brain1.genes:
            for g2 in brain2.genes:
                if g1.innovation_number == g2.innovation_number:
                    matching_count += 1
                    total_diff += math.abs(g1.weight - g2.weight)
                    break # Only two genes of two genomes can match

        if matching_count == 0: # Divide by 0 error
            return 100

        return total_diff / matching_count # Return average

    def sort_species(self) -> None:
        ''' Sorts the species' simulations by fitness in descending order. '''

        # No players
        if len(self.__players) == 0:
            self.__staleness = 200
            return

        # Sort list by fitness
        self.__players.sort(key=lambda sim: sim.fitness, reverse=True)
        
        # New best was found
        best = self.__players[0]
        if best.fitness > self.__best_fitness:
            self.__best_fitness = best.fitness
            self.__rep = best.brain.clone()
            self.__staleness = 0
        else: # No improvements
            self.__staleness += 1

    def set_avg_fitness(self) -> None:
        ''' Sets average fitness of this species' simulations. '''

        self.__avg_fitness = sum(sim.fitness for sim in self.__players) / len(self.__players)
        
    def get_child(self, innovation_history: list[ConnectionHistory]) -> Simulation:
        ''' Gets a child from two players in this species. '''

        baby = None
        # 25% chance to skip crossover
        if random.random() < 0.25:
            baby = self.select_player().clone()
        else: # Do crossover of two random parents
            parent1 = self.select_player()
            parent2 = self.select_player()

            # Crossover the best parent with the second parent
            baby = parent1.crossover(parent2) \
                if parent1.fitness > parent2.fitness \
                    else parent2.crossover(parent1)

        # Mutate child's brain
        baby.brain.mutate(innovation_history)
        return baby
    
    def select_player(self) -> Simulation:
        '''
        Gets a player based on its fitness.
        Better players will have a higher chance of getting picked,
        while worse players will still have a small chance of being picked.
        '''

        # Get a number between 0 and fitness sum of all players
        fitness_sum = sum(sim.fitness for sim in self.__players)
        random_value = random.uniform(0, fitness_sum)

        # The closer the accumalating sum gets to the random value,
        # the easier for worse players to get chosen
        accumalating_sum = 0
        for sim in self.__players:
            accumalating_sum += sim.fitness
            if accumalating_sum > random_value:
                return sim

        return self.__players[0] # If by any chance this didn't work

    def cull(self):
        '''
        As a part of the natural selection process, 
        this method kills the bottom half of the species' players
        That didn't make it to the next generation.
        '''

        if len(self.__players > 2): # If length is greater than or equals to 2 keep all players
            self.__players = self.__players[len(self.__players) // 2:]

    def apply_fitness_sharing(self) -> None:
        '''
        In order to protect innovative and unique players, the fitness of each player
        is divided by the number of the players in its species.
        '''

        for sim in self.__players:
            sim.fitness /= len(self.__players)

    @property
    def avg_fitness(self) -> float:
        return self.__avg_fitness