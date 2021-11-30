from utils.constants import Constants
from NEAT.population import Population
from NEAT.genome import Genome
from NEAT.node import Node
from src.view import View

import numpy as np


class PopulationView(View):
    def __init__(self, population_size: int = 50) -> None:
        self.__population = Population(population_size)
        super().__init__(self.__population.controllers[0])
        self.__population_size = population_size
        self.__index = 0

    def update(self) -> None:
        if not self.__population.done():
            self.__population.update(iterations=1)
            if self.controller.dead:
                self.next_player()
        else:
            self.__population.natural_selection()
            self.controller = self.__population.controllers[0]
            self.__index = 0
    
    def on_key_down(self, key: int) -> None:
        return

    def on_key_up(self, key: int) -> None:
        if key == self.keys['SPACE']:
            self.next_player()

    def draw_network(self, network: Genome, x: float, y: float, w: float, h: float, r: float, show_labels: bool = True) -> None:
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

        self.font_size(20)
        for pos, num in zip(node_poses, node_numbers):
            self.fill(255, 255, 0)
            self.circle(*pos, r)
            if show_labels:
                self.fill(0)
                self.text(str(num), *pos, center=True)

    def draw(self) -> None:
        # Update graphics
        self.draw_background()
        self.draw_sprites(self.controller.player, self.controller.asteroids)
        self.draw_score(self.controller.score, self.controller.high_score)

        if self.controller.paused:
            self.draw_paused()

        self.draw_rays(self.controller.player.ray_set)

        for asteroid in self.controller.asteroids:
            self.draw_poly(asteroid.sprite.rect_verts)
        
        self.fill(255)
        self.text(f'Generation No. {self.__population.generation}', 
                      Constants.WINDOW_WIDTH - 150, 50, center=True)
        self.text(f'Player No. {self.__index + 1} of {self.__population_size}', 
                      Constants.WINDOW_WIDTH - 150, 100, center=True)
        self.draw_network(self.controller.brain, 0, Constants.WINDOW_HEIGHT - 300, 400, 300, 5, show_labels=False)

    def next_index(self) -> None:
        self.__index += 1
        if self.__index == self.__population_size:
            self.__index = 0

        self.controller = self.__population.controllers[self.__index]

    def next_player(self) -> None:
        ''' Assume that at least one player is alive. '''

        if self.__population.done():
            return

        self.next_index()
        while self.controller.dead:
            self.next_index()