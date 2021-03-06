from __future__ import annotations

from NEAT.connection_history import ConnectionHistory
from NEAT.connection_gene import ConnectionGene
from NEAT.node import Node
from NEAT.innovation import Innovation

import random
import json


class Genome:
    '''Genotype for the neural network.
    This class consists of genes and nodes used in the phenotype network,
    and acts as a "brain" for each player in the simulation
    :param inputs: number of inputs for the neural network
    :param outputs: number of outputs for the neural network
    :param crossover: whether this genome is a child made by crossover
    '''

    def __init__(self, inputs: int, outputs: int, crossover: bool = False) -> None:
        self.__local_next_innovation_number = 0
        self.__inputs = inputs
        self.__outputs = outputs
        self.__layers = 2
        self.__next_node = 0

        self.__genes: list[ConnectionGene] = []
        self.__nodes: list[Node] = []
        self.__phenotype: list[Node] = []

        if crossover:
            return

        # Add input nodes
        for i in range(self.__inputs):
            self.__nodes.append(Node(i))
            self.__next_node += 1
        

        # Add output nodes
        for i in range(self.__outputs):
            self.__nodes.append(Node(i + self.__inputs))
            self.__nodes[-1].layer = 1
            self.__next_node += 1

        # Add bias node
        self.__bias_node = self.__next_node
        self.__nodes.append(Node(self.__bias_node))
        self.__next_node += 1

        # Fully connect nodes
        for i in range(inputs):
            for j in range(outputs):
                self.__genes.append(ConnectionGene(self.__nodes[i], 
                                    self.__nodes[inputs + j], 
                                    random.uniform(-1, 1), 
                                    self.__local_next_innovation_number))
                self.__local_next_innovation_number += 1

        # Connect the bias
        for i in range(outputs):
            self.__genes.append(ConnectionGene(self.__nodes[self.__bias_node], 
                                self.__nodes[inputs + i], 
                                random.uniform(-1, 1), 
                                self.__local_next_innovation_number))
            self.__local_next_innovation_number += 1
        
    def get_node(self, number: int) -> Node:
        '''Returns the node with a matching number
        :param number: the node number
        '''

        for node in self.__nodes:
            if node.number == number:
                return node

        return None

    def connect_nodes(self) -> None:
        '''Adds the output connections to nodes according to the genes list.
        This allows each node to access its next node during feed forward
        '''
        
        # Clear all existing connections
        for node in self.__nodes:
            node.output_connections = []

        # Add new connections
        for gene in self.__genes:
            gene.from_node.output_connections.append(gene)

    def feed_forward(self, inputs: list[float]) -> list[float]:
        '''Feeds in input values through the neural network and returns the output list
        :param inputs: list of inputs to feed 
        '''

        # Set the outputs for the inputs
        for i in range(self.__inputs):
            self.__nodes[i].output_value = inputs[i]

        # Set output of 1 to bias node
        self.__nodes[self.__bias_node].output_value = 1

        # Engage each node in phenotype
        for node in self.__phenotype:
            node.engage()

        # Save outputs in a list
        outputs = []
        for i in range(self.__outputs):
            outputs.append(self.__nodes[self.__inputs + i].output_value)

        # Reset all nodes' inputs
        for node in self.__nodes:
            node.input_sum = 0
            
        return outputs

    def generate_phenotype(self) -> None:
        '''Generates the neural network as a list of the nodes
        in correct order to be engaged during feed forward
        '''

        self.connect_nodes()
        self.__phenotype = []

        # For each layer add its nodes
        for layer in range(self.__layers):
            for node in self.__nodes:
                if (node.layer == layer):
                    self.__phenotype.append(node)

    def add_node(self, innovation_history: list[ConnectionHistory]) -> None:
        '''Mutates the neural network by adding a new node between two random nodes
        :param innovation_history: global list of all previous mutations
        '''

        # If nothing is connected add a new connection instead
        if len(self.__genes) == 0:
            self.add_connection(innovation_history)
            return

        # Pick a random connection to add a node between
        random_connection = random.choice(self.__genes)

        # Disconnect bias only if it's the only connection
        while random_connection.from_node == self.__nodes[self.__bias_node] and len(self.__genes) > 1:
            random_connection = random.choice(self.__genes)
            
        # Disable original connection
        random_connection.enabled = False

        # Create a new node
        new_node = Node(self.__next_node)
        self.__nodes.append(new_node)
        self.__next_node += 1

        # Add the connection to the new node with a weight of 1
        innovation_number = self.get_innovation_number(innovation_history, random_connection.from_node, new_node)
        self.__genes.append(ConnectionGene(random_connection.from_node, new_node, 1, innovation_number))

        # Add the connection from the node with the original connection's weight
        innovation_number = self.get_innovation_number(innovation_history, new_node, random_connection.to_node)
        self.__genes.append(ConnectionGene(new_node, random_connection.to_node, random_connection.weight, innovation_number))

        # New node's layer is one past the origin node's layer
        new_node.layer = random_connection.from_node.layer + 1

        # Connect new node to bias with a weight of 0, if it's not already connected
        if random_connection.from_node != self.__nodes[self.__bias_node]:
            innovation_number = self.get_innovation_number(innovation_history, self.__nodes[self.__bias_node], new_node)
            self.__genes.append(ConnectionGene(self.__nodes[self.__bias_node], new_node, 0, innovation_number))
        
        # If the new node's layer is the same as the original connection's out node's layer
        # incriment all layers starting from the new node's layer
        if new_node.layer == random_connection.to_node.layer:
            for i in range(0, len(self.__nodes) - 1): # Skip newest node
                if self.__nodes[i].layer >= new_node.layer:
                    self.__nodes[i].layer += 1
        
            # Add 1 to the genome layers
            self.__layers += 1
        
        # Finally reconnect all nodes
        self.connect_nodes()

    def add_connection(self, innovation_history: list[ConnectionHistory]) -> None:
        '''Mutates the neural network by connecting two random nodes
        :param innovation_history: global list of all previous mutations
        '''

        # Cannot add a connection to a fully connected network
        if self.fully_connected():
            return
        
        # Get two random nodes
        n1 = random.choice(self.__nodes)
        n2 = random.choice(self.__nodes)

        # Get new ones untill the two nodes are valid
        while n1.layer == n2.layer or n1.is_connected_to(n2):
            n1 = random.choice(self.__nodes)
            n2 = random.choice(self.__nodes)

        # If the first node is after the second then switch
        if n1.layer > n2.layer:
            n1, n2 = n2, n1

        # Add the connection
        innovation_number = self.get_innovation_number(innovation_history, n1, n2)
        self.__genes.append(ConnectionGene(n1, n2, random.uniform(-1, 1), innovation_number))

        # Connect nodes
        self.connect_nodes()

    def get_innovation_number(self, innovation_history: list[ConnectionHistory], from_node: Node, to_node: Node) -> int:
        '''Returns the innovation number for the new mutation.
        If the mutation has never occured before then a new 
        unique innovation number will be given. However, if
        the mutation matches a previous mutation then it will
        be given the same innovation number as the previous one's
        :param innovation_history: global list of all previous mutations
        :from_node: the start node of the gene
        :to_node: the target node of the gene
        '''

        is_new = True
        innovation_number = Innovation.next_innovation_number

        for history in innovation_history:
            if history.matches(self, from_node, to_node):
                # If a match was found, then it's not a new mutation   
                is_new = False
                # Set the innovation number to the innovation number of the match
                innovation_number = history.innovation_number
                break # Stop searching for a match

        if is_new:
            # If it is a new mutation, add it to the innovation history list
            prior_innovations = [gene.innovation_number for gene in self.__genes]
            innovation_history.append(ConnectionHistory(from_node.number, to_node, innovation_number, prior_innovations))
            Innovation.next_innovation_number += 1

        return innovation_number
    
    def fully_connected(self) -> bool:
        '''Returns whether the neural network is fully connected'''

        max_connections = 0
        nodes_in_layers = [0 for _ in range(self.__layers)]

        for node in self.__nodes:
            nodes_in_layers[node.layer] += 1

        # The maximum amount of connections for each layer is the number of the layer's nodes 
        # multiplied by the number of nodes in the next layer
        for i in range(self.__layers - 1):
            nodes_in_next_layer = 0
            for j in range(i + 1, self.__layers):
                nodes_in_next_layer += nodes_in_layers[j]
            
            max_connections += nodes_in_layers[i] * nodes_in_next_layer

        return max_connections == len(self.__genes)
        
    def mutate(self, innovation_history: list[ConnectionHistory]) -> None:
        '''Mutates the genome in one or more of the three options:
        - Mutate weights (80% chance)
        - Add a new connection (5% chance)
        - Add a new node (3% chance)
        :param innovation_history: global list of all previous mutations
        '''

        # Add a new connection for first mutation
        if len(self.__genes) == 0:
            self.add_connection(innovation_history)

        # 80% chance of mutating weights
        if random.random() < 0.8:
            for gene in self.genes:
                gene.mutate_weight()

        # 5% chance of adding a new connection
        if random.random() < 0.05:
            self.add_connection(innovation_history)

        # 3% chance of adding a new node
        if random.random() < 0.03:
            self.add_node(innovation_history)

    def matching_gene_index(self, innovation_number: int) -> int:
        '''Returns the index of the gene matching the given innovation number,
        Returns -1 if no gene was found
        :param innovation_number: the innovation number of the gene
        '''

        for i, gene in enumerate(self.__genes):
            if gene.innovation_number == innovation_number:
                return i
        return -1

    def crossover(self, parent2: Genome) -> Genome:
        '''Applies crossover of this genome as first parent and given genome as second parent,
        when this genome is the fittest. This will combine the two genomes to one
        genome inheriting from both of them, using the connections' innovation numbers.
        Genes that don't match are called disjoint and access genes,
        These genes are inherited to the child from this genome
        :param parent2: the secon parent for the crossover process
        '''

        # Copy attributes to child
        child = Genome(self.__inputs, self.__outputs, crossover=True)
        child.layers = self.__layers
        child.next_node = self.__next_node
        child.bias_node = self.bias_node

        # Start setting up child's genes
        child_genes: list[ConnectionGene] = []
        genes_enabled: list[bool] = [] # For each genes, set if it's enabled

        for gene in self.__genes:
            set_enabled = True # node is enabled by default
            # Get matching gene with the same innovation number
            second_parent_gene = parent2.matching_gene_index(gene.innovation_number)

            if second_parent_gene != -1: # There is a match
                # if at least one of the parents does not have the gene enabled
                # then disable child's gene 75% of the time
                if not gene.enabled or not parent2.genes[second_parent_gene].enabled:
                    if random.random() < 0.75:
                        set_enabled = False

                if random.random() < 0.5: # Get gene from this genome 50% of the time
                    child_genes.append(gene)
                else: # Else get gene from second parent
                    child_genes.append(parent2.genes[second_parent_gene])

            else: # Second parent does not have a matching gene
                child_genes.append(gene) # Add disjoint or access gene of the fittest

            # Add is_enabled to enabled genes list
            genes_enabled.append(set_enabled) 

        # Copy nodes from this genome to child
        # The child's nodes list is the same as this genome's since it's the fittest
        for node in self.__nodes:
            child.nodes.append(node.clone())

        # Copy connections to child's genes
        for i, gene in enumerate(child_genes):
            from_node = child.get_node(gene.from_node.number)
            to_node = child.get_node(gene.to_node.number)
            child.genes.append(gene.clone(from_node, to_node))
            child.genes[i].enabled = genes_enabled[i] # disable gene if needed

        # Finally connect child's nodes
        child.connect_nodes()
        return child
    
    def clone(self) -> Genome:
        '''Returns a copy of this genome'''

        clone = Genome(self.__inputs, self.__outputs, crossover=True)

        for node in self.__nodes: # Copy nodes
            clone.nodes.append(node.clone())

        for gene in self.__genes: # Copy genes
            from_node = clone.get_node(gene.from_node.number)
            to_node = clone.get_node(gene.to_node.number)
            clone.genes.append(gene.clone(from_node, to_node))

        # Copy attributes
        clone.layers = self.__layers
        clone.next_node = self.__next_node
        clone.bias_node = self.__bias_node
        
        clone.connect_nodes()
        return clone
    
    def to_json(self) -> dict:
        '''Returns a dictionary containing useful information, used for storing the genome in a file'''
        return {
            'inputs': self.__inputs,
            'outputs': self.__outputs,
            'genes': [gene.to_json() for gene in self.__genes],
            'nodes': [node.to_json() for node in self.__nodes],
            'layers': self.__layers,
            'next_node': self.__next_node,
            'bias_node': self.__bias_node,
        }

    def save(self, filename: str) -> None:
        '''Saves this genome to a json file
        :filename: path of the file
        '''

        with open(filename, 'w') as f:
            f.write(json.dumps(self.to_json(), indent=2))

    @classmethod
    def load(cls, filename: str) -> Genome:
        '''Loads a new Genome from json file
        :param filename: path of the file
        '''
        
        with open(filename, 'r') as f:
            data = json.load(f)

            genome = cls(data['inputs'], data['outputs'])
            genome.nodes = [Node.load(node) for node in data['nodes']]
            genome.genes = [ConnectionGene.load(genome, gene) for gene in data['genes']]

            genome.layers = data['layers']
            genome.next_node = data['next_node']
            genome.bias_node = data['bias_node']

            genome.generate_phenotype()
            return genome

    
    @property
    def genes(self) -> list[ConnectionGene]:
        return self.__genes

    @property
    def nodes(self) -> list[Node]:
        return self.__nodes
        
    @property
    def layers(self) -> int:
        return self.__layers

    @property
    def next_node(self) -> int:
        return self.__next_node

    @property
    def bias_node(self) -> int:
        return self.__bias_node

    @layers.setter
    def layers(self, layers: int) -> None:
        self.__layers = layers

    @next_node.setter
    def next_node(self, next_node: int) -> None:
        self.__next_node = next_node

    @bias_node.setter
    def bias_node(self, bias_node: int) -> None:
        self.__bias_node = bias_node

    @genes.setter
    def genes(self, genes: list[ConnectionGene]) -> None:
        self.__genes = genes

    @nodes.setter
    def nodes(self, nodes: list[Node]) -> None:
        self.__nodes = nodes
