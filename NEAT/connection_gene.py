from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from NEAT.node import Node

import random


class ConnectionGene:
    def __init__(self, from_node: Node, to_node: Node, weight: float, innovation_number: int) -> None:
        ''' Connects between two nodes in the neural network. '''
        
        self.__from_node = from_node
        self.__to_node = to_node
        self.__weight = weight
        self.__enabled = True
        self.__innovation_number = innovation_number # Unique number used to compare gemomes

    def mutate_weight(self) -> None:
        '''
        Changes/tweaks the node's weight based on probability.
        Each mutation of this type has a:
        10% chance of completely changing the weight.
        90% chance of slightly changing the weight.
        '''

        rand = random.random()
        if rand < 0.1: # Completely change the weight
            self.__weight = random.uniform(-1, 1)
        else: # Change it by a small amount
            self.__weight += random.gauss(0, 1) / 100

            # Keep the weight between it's -1 to 1 bounds
            self.__weight = min(1, max(-1, self.__weight))

    def clone(self, from_node: Node, to_node: Node) -> ConnectionGene:
        ''' Returns a copy of this connection gene. '''

        clone = ConnectionGene(from_node, to_node, self.__weight, self.__innovation_number)
        clone.enabled = self.__enabled
        return clone

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