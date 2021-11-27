from pygame.constants import K_SPACE
from utils.drawing import Context, Screen
from NEAT.demo.controller import DemoController
from NEAT.genome import Genome
from NEAT.node import Node
from utils.vector import PositionalVector

import pygame as pg
from pygame.event import Event
from pygame.time import Clock

import numpy as np


class DemoView:
    def __init__(self) -> None:
        self.__controller = DemoController()

        pg.init()
        self.__screen = Screen(800, 600, 'NEAT Demo')
        self.__ctx = Context(self.__screen)
        self.__clock = Clock()

    def start(self) -> None:
        while True:
            self.update()
            self.__controller.update()

    def draw_network(self, network: Genome, x: float, y: float, w: float, h: float, r: float) -> None:
        nodes_by_layers: list[Node] = []
        node_poses: list[PositionalVector] = []
        node_numbers: list[int] = []

        for layer in range(network.layers):
            nodes_by_layers.append(list(filter(lambda node: node.layer == layer, network.nodes)))

        for layer in range(network.layers):
            node_x = x + ((layer + 1) * w) / ((network.layers + 1))
            for i, node in enumerate(nodes_by_layers[layer]):
                node_y = y + ((i + 1) * h) / (len(nodes_by_layers[layer]) + 1)
                node_poses.append(PositionalVector(node_x, node_y))
                node_numbers.append(node.number)

        for gene in network.genes:
            if gene.enabled:
                if gene.weight > 0:
                    self.__ctx.fill(255, 0, 0)
                else: 
                    self.__ctx.fill(0, 0, 255)
            else: 
                self.__ctx.fill(0)

            weight = int(np.interp(abs(gene.weight), [0, 1], [0, 5]))

            from_pos = node_poses[node_numbers.index(gene.from_node.number)]
            to_pos = node_poses[node_numbers.index(gene.to_node.number)]
            self.__ctx.line(*from_pos, *to_pos, weight)

        self.__ctx.stroke(0)
        self.__ctx.stroke_weight(1)
        self.__ctx.font_size(20)
        for pos, num in zip(node_poses, node_numbers):
            self.__ctx.fill(255)
            self.__ctx.circle(*pos, r)
            self.__ctx.fill(0)
            self.__ctx.text(str(num), *pos, center=True)
            

    def draw(self) -> None:
        self.__ctx.background(180)
        self.draw_network(self.__controller.network, 0, 0, 800, 600, 20)

    def finish_render(self) -> None:
        pg.display.flip()
        self.__clock.tick(60)
    
    def update(self) -> None:
        # Handle user input
        for event in pg.event.get():
            self.handle_event(event)

        self.draw()
        self.finish_render()
    
    def handle_event(self, event: Event) -> None:
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.__controller.add_connection()
            elif event.key == pg.K_DOWN:
                self.__controller.add_node()
            elif event.key == pg.K_SPACE:
                self.__controller.mutate_weights()