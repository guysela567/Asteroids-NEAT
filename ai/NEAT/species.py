from ai.simulation import Simulation
from ai.NEAT.genome import Genome

import math


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

    def same_species(self, genome: Genome) -> bool:
        ''' Returns whether the given genome belonds to this species. '''

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

        self.__players.sort(key=lambda sim: sim.fitness, reverse=True) # Sort list

        # No players
        if len(self.__players) == 0:
            self.__staleness = 200
            return
        
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
        