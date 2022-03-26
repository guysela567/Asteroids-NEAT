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

    def set_network(self, inputs: int, outputs: int) -> None:
        self.__model.set_network(inputs, outputs)

    def toggle_index(self) -> None:
        self.__model.toggle_index()

    def crossover(self) -> None:
        self.__model.crossover()

    def reset_network(self) -> None:
        self.__model.reset_network()

    def reset(self) -> None:
        self.__model.reset()

    @property
    def network(self) -> Genome:
        return self.__model.network

    @property
    def index(self) -> int:
        return self.__model.index

    @property
    def crossed(self) -> bool:
        return self.__model.crossed