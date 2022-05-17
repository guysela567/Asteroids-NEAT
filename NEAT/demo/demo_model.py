from __future__ import annotations
from NEAT.genome import Genome
from NEAT.node import Node


class DemoModel:
    '''Holds data for the topology demo simulation, consists of the tested genomes'''

    def __init__(self) -> None:
        self.__default_network: Genome = None
        self.__networks: list[Genome] = []
        self.__innovation_history = []
        self.__index = 0

        self.__crossed = False
        self.__child: Genome = None
    
    def nodes_in_layer(self, layer: int) -> int:
        '''Returns the amount of nodes in a given layer
        :param layer: the layer in the genome, starting count from 0'''
        return sum(1 for node in self.network.nodes if node.layer == layer)

    def get_first_number_in_layer(self, layer: int) -> Node:
        '''Returns the smallest node number in a given layer
        :param layer: the layer in the genome, starting count from 0'''
        nodes = filter(lambda node: node.layer == layer, self.network.nodes)
        return min(nodes, key=lambda node: node.number).number

    def mutate_weights(self) -> None:
        '''Mutates weights randomly in active genome'''
        for gene in self.network.genes:
            gene.mutate_weight()

    def add_connection(self) -> None:
        '''Adds a random gene connection in active genome'''
        self.network.add_connection(self.__innovation_history)

    def add_node(self) -> None:
        '''Adds a random neuron in active genome'''
        self.network.add_node(self.__innovation_history)

    def set_network(self, inputs: int, outputs: int) -> None:
        '''Sets the base neural network given the shape
        :param inputs: number of selected inputs in the neural network
        :param outputs: number of selected outputs in the neural network'''
        self.__default_network = Genome(inputs, outputs)

        self.__networks = []
        for _ in range(2):
            self.__networks.append(self.__default_network.clone())

    def toggle_index(self) -> None:
        '''Toggles between the two genomes'''
        self.__index = 1 - self.__index

    def crossover(self) -> None:
        '''Applies crossover on the two genomes'''
        self.__crossed = True
        self.__child = self.__networks[0].crossover(self.__networks[1])

    def reset_network(self) -> None:
        '''Resets the active genome to default'''
        self.__networks[self.__index] = self.__default_network.clone()

    def reset(self) -> None:
        '''Resets all of the data to default'''
        self.__index = 0
        self.__crossed = False
        self.__child = None
        
        self.__networks = []
        for _ in range(2):
            self.__networks.append(self.__default_network.clone())

    @property
    def network(self) -> Genome:
        if self.__crossed:
            return self.__child
        return self.__networks[self.__index]

    @property
    def index(self) -> int:
        return self.__index

    @property
    def crossed(self) -> bool:
        return self.__crossed