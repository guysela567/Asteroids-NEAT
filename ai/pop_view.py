from src.view import View

from ai.population import Population

import pygame as pg
from pygame.event import Event


class PopulationView(View):
    def __init__(self, population_size) -> None:
        self.__population = Population(population_size)
        super().__init__(self.__population.controllers[0])
        self.__population_size = population_size
        self.__index = 0

    def start(self) -> None:
        self.__population.start()
        while True:
            self.update()
    
    def handle_event(self, event: Event) -> None:
        # Block user input
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.__index += 1
            if self.__index == self.__population_size:
                self.__index = 0

            self.controller = self.__population.controllers[self.__index]
