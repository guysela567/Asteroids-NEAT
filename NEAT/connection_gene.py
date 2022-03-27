from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from NEAT.node import Node
    from NEAT.genome import Genome

import random


class ConnectionGene:
    '''Connects between two nodes in the neural network
    :param from_node: the start node of the gene
    :param to_node: the target node of the gene
    :param weight: the weight of the gene
    :innovation_number: the innovation number for the gene
    '''

    def __init__(self, from_node: Node, to_node: Node, weight: float, innovation_number: int) -> None:
        
        self.__from_node = from_node
        self.__to_node = to_node
        self.__weight = weight
        self.__enabled = True
        self.__innovation_number = innovation_number # Unique number used to compare gemomes

    def mutate_weight(self) -> None:
        '''Changes/tweaks the node's weight based on probability.
        Each mutation of this type has a:
        - 10% chance of completely changing the weight
        - 90% chance of slightly changing the weight
        '''

        rand = random.random()
        if rand < 0.1: # Completely change the weight
            self.__weight = random.uniform(-1, 1)
        else: # Change it by a small amount
            self.__weight += random.gauss(0, 1)

            # Keep the weight between it's -1 to 1 bounds
            self.__weight = min(1, max(-1, self.__weight))

    def clone(self, from_node: Node, to_node: Node) -> ConnectionGene:
        '''Returns a copy of this connection gene
        :param from_node: the start node of the clone
        :param to_node: the target node of the clone
        '''

        clone = ConnectionGene(from_node, to_node, self.__weight, self.__innovation_number)
        clone.enabled = self.__enabled
        return clone

    def to_json(self) -> dict:
        '''Returns a dictionary containing useful information of the gene, used to store the gene in a file'''
        return {
            'from_node': self.__from_node.number,
            'to_node': self.__to_node.number,
            'weight': self.__weight,
            'innovation_number': self.__innovation_number,
            'enabled': self.__enabled,
        }

    @classmethod
    def load(cls, genome: Genome, data: dict) -> ConnectionGene:
        '''Loads the gene from a dictionary
        :param genome: the genome of the loaded gene
        :param data: the data of this gene
        '''
        
        from_node = genome.get_node(data['from_node'])
        to_node = genome.get_node(data['to_node'])
        gene = cls(from_node, to_node, data['weight'], data['innovation_number'])
        gene.enabled = data['enabled']
        return gene

    @property
    def from_node(self) -> Node:
        return self.__from_node
    
    @property
    def to_node(self) -> Node:
        return self.__to_node

    @property
    def weight(self) -> float:
        return self.__weight

    @property
    def enabled(self) -> bool:
        return self.__enabled

    @property
    def innovation_number(self) -> int:
        return self.__innovation_number
    
    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self.__enabled = enabled