from __future__ import annotations

from utils.drawing import Screen
from utils.constants import Constants
from NEAT.demo.controller import DemoController
from NEAT.genome import Genome
from NEAT.node import Node

import numpy as np


class DemoScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'NEAT Demo')
        self.__controller = DemoController()

    def update(self) -> None:
        self.__controller.update()

    def draw_network(self, network: Genome, x: float, y: float, w: float, h: float, r: float) -> None:
        nodes_by_layers: list[list[Node]] = []
        node_poses: list[tuple[int, int]] = []
        node_numbers: list[int] = []

        for layer in range(network.layers):
            nodes_by_layers.append(list(filter(lambda node: node.layer == layer, network.nodes)))

        for layer in range(network.layers):
            node_x = x + ((layer + 1) * w) / (network.layers + 1)
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
                # if to_pos[0] == 780:
                #     print('yes', gene.to_node.layer, network.layers, gene.to_node.number)
                self.line(*from_pos, *to_pos, weight)

        self.stroke(0)
        self.stroke_weight(1)
        self.font_size(20)
        for pos, num in zip(node_poses, node_numbers):
            # if pos.x == 780:
            #     print('yes')
            self.fill(255)
            self.circle(*pos, r)
            self.fill(0)
            self.text(str(num), *pos, center=True)
            

    def draw(self) -> None:
        self.background(180)
        self.draw_network(self.__controller.network, 0, 0, self.width, self.height, 30)
    
    def on_key_down(self, key: int) -> None:
        if key == self.keys['UP']:
            self.__controller.add_connection()

        elif key == self.keys['DOWN']:
            self.__controller.add_node()

        elif key == self.keys['SPACE']:
            self.__controller.mutate_weights()

        elif key == self.keys['ESCAPE']:
            self.redirect('menu')