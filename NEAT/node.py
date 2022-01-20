from __future__ import annotations

from NEAT.connection_gene import ConnectionGene

import math


class Node:
    def __init__(self, number: int) -> None:
        ''' Represents a neuron in the neural network. '''

        self.__number = number
        self.__input_sum = 0
        self.__output_value = 0
        self.__output_connections: list[ConnectionGene] = []
        self.__layer = 0

    def engage(self) -> None:
        ''' Sends its output to the inputs of the nodes its connected to. '''

        if self.__layer != 0: # No activation for inputs and bias
            self.__output_value = Node.sigmoid(self.__input_sum)
            
        # For each connection, add the weighted output to the sum of inputs of the connected node
        for connection in self.__output_connections:
            if connection.enabled:
                connection.to_node.input_sum += connection.weight * self.__output_value

    @staticmethod
    def sigmoid(x: float) -> float:
        ''' Sigmoid activation function.  '''
        
        return 1 / (1 + math.exp(-4.9 * x))

    def is_connected_to(self, node: Node) -> bool:
        ''' 
        Returns whether this node is connected to the given node.
        This is used when adding a new connection.
        '''

        # Nodes in the same layer cannot be connected
        if node.layer == self.__layer:
            return False

        if node.layer < self.layer: # The other node connects to this node
            if any(connection.to_node == self for connection in node.output_connections):
                return True
        else: # This node connects to the other node
            return any(connection.to_node == node for connection in self.__output_connections)

    def clone(self) -> Node:
        ''' Returns a copy of this node. '''
        
        clone = Node(self.__number)
        clone.layer = self.__layer
        return clone

    def to_json(self) -> dict:
        connections: list[int] = []
        for connection in self.__output_connections:
            connections.append(connection.from_node.number)
            connections.append(connection.to_node.number)

        return { 
            'number': self.__number,
            'layer': self.__layer,
            'connections': connections,
        }

    @property
    def number(self) -> int:
        return self.__number
    
    @property
    def output_connections(self) -> list[ConnectionGene]:
        return self.__output_connections

    @property
    def input_sum(self) -> float:
        return self.__input_sum

    @property
    def layer(self) -> int:
        return self.__layer

    @property
    def output_value(self) -> float:
        return self.__output_value

    @output_connections.setter
    def output_connections(self, connections: list[ConnectionGene]) -> None:
        self.__output_connections = connections

    @input_sum.setter
    def input_sum(self, input_sum: float) -> None:
        self.__input_sum = input_sum

    @layer.setter
    def layer(self, layer: int) -> None:
        self.__layer = layer

    @output_value.setter
    def output_value(self, output: float) -> None:
        self.__output_value = output