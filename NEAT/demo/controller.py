from NEAT.demo.model import DemoModel
from NEAT.genome import Genome
from NEAT.node import Node


class DemoController:
    def __init__(self) -> None:
        self.__model = DemoModel()
    
    def update(self) -> None:
        pass

    def nodes_in_layer(self, layer: int) -> int:
        return self.__model.nodes_in_layer(layer)

    def get_first_number_in_layer(self, layer: int) -> Node:
        return self.__model.get_first_number_in_layer(layer)

    def mutate_weights(self) -> None:
        self.__model.mutate_weights()
        
    def add_connection(self) -> None:
        self.__model.add_connection()

    def add_node(self) -> None:
        self.__model.add_node()

    @property
    def network(self) -> Genome:
        return self.__model.network

    @network.setter
    def network(self, network: Genome) -> None:
        self.__model.network = network