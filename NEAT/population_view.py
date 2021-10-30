from utils.constants import Constants
from src.view import View
from NEAT.population import Population

import pygame as pg
from pygame.event import Event


class PopulationView(View):
    def __init__(self, population_size: int = 50) -> None:
        self.__population = Population(population_size)
        super().__init__(self.__population.controllers[0])
        self.__population_size = population_size
        self.__index = 0

    def start(self) -> None:
        while True:
            if not self.__population.done():
                self.__population.update(iterations=1)
                if self.controller.dead:
                    self.next_player()
            else:
                self.__population.natural_selection()
                self.controller = self.__population.controllers[0]
                self.__index = 0

            self.update()
    
    def handle_event(self, event: Event) -> None:
        # Block user input
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.next_player()

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
        
        self.ctx.fill(255)
        self.ctx.text(f'Generation No. {self.__population.generation}', 
                      Constants.WINDOW_WIDTH - 150, 50, center=True)
        self.ctx.text(f'Player No. {self.__index}', 
                      Constants.WINDOW_WIDTH - 150, 100, center=True)

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