from __future__ import annotations

from utils.drawing import Screen, Image, TextBox
from utils.constants import Constants
from NEAT.demo.controller import DemoController
from NEAT.genome import Genome
from NEAT.node import Node

import numpy as np


class DemoScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'NEAT Demo')
        self.__controller = DemoController()
        self.__back_image = Image('assets/sprites/back.png')

    def update(self) -> None:
        self.__controller.update()  

    def draw(self) -> None:
        self.background(180)
        self.draw_network(self.__controller.network, 0, 0, self.width, self.height, 30)
        self.image(self.__back_image, 10, 10, 65, 65)

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
                self.line(*from_pos, *to_pos, weight)

        self.stroke(0)
        self.stroke_weight(1)
        self.font_size(20)
        for pos, num in zip(node_poses, node_numbers):
           
            self.fill(255)
            if num == self.__controller.network.bias_node:
                self.stroke(0, 255, 0)
                self.stroke_weight(5)
            else: self.no_stroke()
            self.circle(*pos, r)

            self.fill(0)
            self.font_size(50)
            self.text(str(num), *pos, center=True)     
    
    def on_key_down(self, key: int, unicode: str) -> None:
        if key == self.keys['UP']:
            self.__controller.add_connection()

        elif key == self.keys['DOWN']:
            self.__controller.add_node()

        elif key == self.keys['SPACE']:
            self.__controller.mutate_weights()

        elif key == self.keys['ESCAPE']:
            self.redirect('demo-config')

    def on_mouse_down(self) -> None:
        x, y, w, h = Constants.BACK_RECT
        if x < self.mouse_pos[0] < x + w and y < self.mouse_pos[1] < y + h:
            self.redirect('menu')

    def recieve_data(self, data: dict) -> None:
        self.__controller.network = Genome(data['inputs'], data['outputs'])