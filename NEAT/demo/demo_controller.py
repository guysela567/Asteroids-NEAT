from NEAT.demo.demo_model import DemoModel
from NEAT.genome import Genome
from NEAT.node import Node


class DemoController:
    '''The controller connects between the view of the demo screen and the model holding the data'''
    
    def __init__(self) -> None:
        self.__model = DemoModel()

    def nodes_in_layer(self, layer: int) -> int:
        '''Returns the amount of nodes in a given layer
        :param layer: the layer in the genome, starting count from 0'''
        return self.__model.nodes_in_layer(layer)

    def get_first_number_in_layer(self, layer: int) -> Node:
        '''Returns the smallest node number in a given layer
        :param layer: the layer in the genome, starting count from 0'''
        return self.__model.get_first_number_in_layer(layer)

    def mutate_weights(self) -> None:
        '''Mutates weights randomly in active genome'''
        self.__model.mutate_weights()
        
    def add_connection(self) -> None:
        '''Adds a random gene connection in active genome'''
        self.__model.add_connection()

    def add_node(self) -> None:
        '''Adds a random neuron in active genome'''
        self.__model.add_node()

    def set_network(self, inputs: int, outputs: int) -> None:
        '''Sets the base neural network given the shape
        :param inputs: number of selected inputs in the neural network
        :param outputs: number of selected outputs in the neural network'''
        self.__model.set_network(inputs, outputs)

    def toggle_index(self) -> None:
        '''Toggles between the two genomes'''
        self.__model.toggle_index()

    def crossover(self) -> None:
        '''Applies crossover on the two genomes'''
        self.__model.crossover()

    def reset_network(self) -> None:
        '''Resets the active genome to default'''
        self.__model.reset_network()

    def reset(self) -> None:
        '''Resets the model'''
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