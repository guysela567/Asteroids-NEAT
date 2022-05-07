from __future__ import annotations

from utils.drawing import Button, Screen, Image
from utils.constants import Constants
from NEAT.demo.controller import DemoController
from NEAT.genome import Genome
from NEAT.node import Node

import numpy as np


class DemoScreen(Screen):
    '''Graphical screen for simulating topology changes and crossover in the NEAT algorithm'''

    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'NEAT Demo')
        self.__controller = DemoController()
        self.__back_image = Image('assets/sprites/back.png')

        self.__title_font = self.load_font('assets/fonts/HyperSpaceBold.ttf', 60)
        self.__button_font = self.load_font('assets/fonts/HyperSpaceBold.ttf', 20)

        self.__node_button = Button(self, 30, 350, 200, 80, (255, 255, 255), 'Add Node')
        self.__connection_button = Button(self, 30, self.height - 125, 200, 80, (255, 255, 255), 'Add Connection')
        self.__mutate_button = Button(self, self.width - 230, 350, 200, 80, (255, 255, 255), 'Mutate Weights')
        self.__reset_network_button = Button(self, self.width - 230, self.height - 125, 200, 80, (255, 255, 255), 'Reset Network')

        self.__toggle_button = Button(self, 30, 200, 200, 80, (255, 255, 255), 'Toggle Genomes')
        self.__crossover_button = Button(self, self.width - 230, 200, 200, 80, (255, 255, 255), 'Apply Crossover')
        self.__reset_button = Button(self, self.width * .5 - 50, 200, 150, 80, (255, 255, 255), 'Reset')

    def draw(self) -> None:
        '''Updates graphics'''

        self.background(200)
        
        self.set_font(self.__title_font)
        self.text('Configure Topology', self.width * .5, 50, center=True)
        self.text('Child' if self.__controller.crossed else f'For Genome No. {self.__controller.index + 1}', self.width * .5, 110, center=True)

        self.fill(0)
        self.line(0, 300, self.width, 300, 5)
        self.fill(150)
        self.rect(0, 300, self.width, self.height)
        self.draw_network(self.__controller.network, 200, 300, self.width - 400, self.height - 300, 30)
        
        self.set_font(self.__button_font)
        self.__node_button.draw()
        self.__connection_button.draw()
        self.__mutate_button.draw()
        self.__reset_network_button.draw()
        self.__toggle_button.draw()
        self.__crossover_button.draw()
        self.__reset_button.draw()
        self.image(self.__back_image, 10, 10, 65, 65)

    def draw_network(self, network: Genome, x: float, y: float, w: float, h: float, r: float) -> None:
        '''Draws a neural network on the screen
        :param network: genome of the network
        :param x: X coordinate for the top left corner of the drawing
        :param y: Y coordinate for the top left corner of the drawing
        :param w: maximum width of the drawing
        :param h: maximum height of the drawing
        :param r: radius for neurons in the drawing
        '''

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
            self.stroke_weight(3)
            if num == self.__controller.network.bias_node:
                self.stroke(0, 255, 0)
            else: self.stroke(0)
            self.circle(*pos, r)

            self.fill(0)
            self.no_stroke()
            self.font_size(50)
            self.text(str(num + 1), *pos, center=True)     
    
    def on_key_down(self, key: int, unicode: str) -> None:
        '''Handles key down events
        :param key: id of the pressed key
        :param unicode: unicode of the pressed key
        '''

        if key == self.keys['ESCAPE']:
            self.redirect('demo-config')

    def on_mouse_down(self) -> None:
        x, y, w, h = Constants.BACK_RECT
        if x < self.mouse_pos[0] < x + w and y < self.mouse_pos[1] < y + h:
            self.redirect('menu')

        elif self.__node_button.mouse_hover() and self.__controller.network.layers < 5:
            self.__controller.add_node()

        elif self.__connection_button.mouse_hover():
            self.__controller.add_connection()

        elif self.__mutate_button.mouse_hover():
            self.__controller.mutate_weights()

        elif self.__reset_network_button.mouse_hover():
            self.__controller.reset_network()

        elif self.__toggle_button.mouse_hover():
            self.__controller.toggle_index()

        elif self.__crossover_button.mouse_hover():
            self.__controller.crossover()

        elif self.__reset_button.mouse_hover():
            self.__controller.reset()

    def recieve_data(self, data: dict) -> None:
        '''Handles data sent by other screens and sets the base network'''
        self.__controller.set_network(data['inputs'], data['outputs'])