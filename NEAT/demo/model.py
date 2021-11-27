from __future__ import annotations
from NEAT.genome import Genome
from NEAT.node import Node


class DemoModel:
    def __init__(self, inputs: int, outputs: int) -> None:
        self.__network = Genome(inputs, outputs)
        self.__innovation_history = []
    
    def nodes_in_layer(self, layer: int) -> int:
        return sum(1 for node in self.__network.nodes if node.layer == layer)

    def get_first_number_in_layer(self, layer: int) -> Node:
        nodes = filter(lambda node: node.layer == layer, self.__network.nodes)
        return min(nodes, key=lambda node: node.number).number

    def mutate_weights(self) -> None:
        for gene in self.__network.genes:
            gene.mutate_weight()

    def add_connection(self) -> None:
        self.__network.add_connection(self.__innovation_history)

    def add_node(self) -> None:
        self.__network.add_node(self.__innovation_history)

    @property
    def network(self) -> Genome:
        return self.__network