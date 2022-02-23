from __future__ import annotations
from NEAT.genome import Genome
from NEAT.node import Node


class DemoModel:
    def __init__(self) -> None:
        self.__default_network: Genome = None
        self.__networks: list[Genome] = []
        self.__innovation_history = []
        self.__index = 0

        self.__crossed = False
        self.__child: Genome = None
    
    def nodes_in_layer(self, layer: int) -> int:
        return sum(1 for node in self.network.nodes if node.layer == layer)

    def get_first_number_in_layer(self, layer: int) -> Node:
        nodes = filter(lambda node: node.layer == layer, self.network.nodes)
        return min(nodes, key=lambda node: node.number).number

    def mutate_weights(self) -> None:
        for gene in self.network.genes:
            gene.mutate_weight()

    def add_connection(self) -> None:
        self.network.add_connection(self.__innovation_history)

    def add_node(self) -> None:
        self.network.add_node(self.__innovation_history)

    def set_network(self, inputs: int, outputs: int) -> None:
        self.__default_network = Genome(inputs, outputs)
        self.__default_network.fully_connect(self.__innovation_history)

        self.__networks = []
        for _ in range(2):
            self.__networks.append(self.__default_network.clone())

    def toggle_index(self) -> None:
        self.__index = 1 - self.__index

    def crossover(self) -> None:
        self.__crossed = True
        self.__child = self.__networks[0].crossover(self.__networks[1])

    def reset_network(self) -> None:
        self.__networks[self.__index] = self.__default_network.clone()

    def reset(self) -> None:
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