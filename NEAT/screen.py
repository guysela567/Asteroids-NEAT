from utils.constants import Constants
from NEAT.population import Population
from NEAT.genome import Genome
from NEAT.node import Node
from src.screens.game import GameScreen

import numpy as np


class PopulationScreen(GameScreen):
    '''Graphical screen used for viewing the training process
    :param population_size: size of the genetic algorithm population
    '''

    def __init__(self, population_size: int = Constants.POPULATION_SIZE) -> None:
        super().__init__()

        self.__population = Population(population_size)
        self.controller = self.__population.batch[0]
        self.__index = 0

        self.__gen_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 25)

    def update(self) -> None:
        '''Updates the controller and master game logic'''

        if not self.__population.done():
            self.__population.update(iterations=Constants.ITERATIONS)

            if self.controller.dead:
                self.next_player()
        else:
            self.__population.natural_selection()
            self.controller = self.__population.batch[0]
            self.__index = 0
    
    def on_key_down(self, key: int, unicode: str) -> None:
        '''handles key press events
        :param key: the key of the event
        :param unicode: the unicode value of the key
        '''

        if key == self.keys['SPACE']:
            self.next_player()

        elif key == self.keys['ESCAPE']:
            self.redirect('menu')

    def draw_network(self, network: Genome, x: float, y: float, w: float, h: float, r: float, show_labels: bool = True) -> None:
        '''Draws the neural network on the screen
        :param genome: the genotype of the network to draw
        :param x: the X coordinate for the top left corner of the drawing
        :param y: the Y coordinate for the top left corner of the drawing
        :param w: the maximum width of the drawing
        :param h: the maximum height of the drawing,
        :param r: the radius of the neurons in the drawing
        :param show_labels: whether or not to draw the node numbers
        '''

        nodes_by_layers: list[list[Node]] = []
        node_poses: list[tuple[int, int]] = []
        node_numbers: list[int] = []

        for layer in range(network.layers):
            nodes_by_layers.append(list(filter(lambda node: node.layer == layer, network.nodes)))

        for layer in range(network.layers):
            node_x = x + r + (w - 2 * r) * (layer / (network.layers - 1))
            for i, node in enumerate(nodes_by_layers[layer]):
                node_y = y + ((i + 1) * h) / (len(nodes_by_layers[layer]) + 1)
                node_poses.append((node_x, node_y))
                node_numbers.append(node.number)

        for gene in network.genes:
            if gene.enabled:
                if gene.weight > 0:
                    self.fill(255, 0, 0)
                else: 
                    self.fill(0, 0, 255)

                weight = int(np.interp(abs(gene.weight), [0, 1], [1, 5]))

                from_pos = node_poses[node_numbers.index(gene.from_node.number)]
                to_pos = node_poses[node_numbers.index(gene.to_node.number)]
                self.line(*from_pos, *to_pos, weight)

        for pos, num in zip(node_poses, node_numbers):
            self.fill(255, 255, 0)
            self.circle(*pos, r)
            if show_labels:
                self.fill(0)
                self.text(str(num), *pos, center=True)

    def draw(self) -> None:
        '''Updates graphics'''

        self.draw_background()

        # AI Guidelines
        self.draw_rays(self.controller.player.ray_set)

        self.fill(255, 150, 150)
        for asteroid in self.controller.asteroids:
            self.draw_poly(asteroid.hitbox.rect_verts)

        self.fill(255)
        self.draw_sprites(self.controller.player, self.controller.asteroids)
        self.draw_score(self.controller.score)

        if self.controller.paused:
            self.draw_paused()
        
        self.fill(255)
        self.set_font(self.__gen_font)
        self.text(f'Generation No. {self.__population.generation}', self.width - 150, 50, center=True)
        self.text(f'Batch No. {self.__population.batch_index + 1}', self.width - 150, 100, center=True)
        self.text(f'of {self.__population.batch_amount}', self.width - 150, 125, center=True)
        self.text(f'Player No. {self.__index + 1}', self.width - 150, 175, center=True)
        self.text(f'of {Constants.BATCH_SIZE}',  self.width - 150, 200, center=True)
        self.draw_network(self.controller.brain, 0, self.height - 300, 400, 300, 5, show_labels=False)

    def next_index(self) -> None:
        '''Proceeds to next index of simulation in current batch'''
        
        self.__index += 1

        if self.__index >= Constants.BATCH_SIZE:
            self.__index = 0

        self.controller = self.__population.batch[self.__index]

    def next_player(self) -> None:
        '''Proceeds to the next simulation in the current batch,
        assuming that at least one player is alive
        '''

        if self.__population.current_batch_done() \
            or len(self.__population.players) < 2:
            return

        self.next_index()
        while self.controller.dead:
            self.next_index()