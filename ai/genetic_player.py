from utils.constants import Constants
from src.controller import Controller

from _thread import start_new_thread
from time import time, sleep


class GeneticPlayer:
    def __init__(self) -> None:
       self.__controller = Controller()
       self.__fitness = 0
    
    def start(self) -> None:
        start_new_thread(self.start_controller, (self.__controller,))

    def start_controller(self, controller: Controller) -> None:
        while True:
            if controller.dead: 
                return

            controller.update()
            controller.think()
            sleep(1 / Constants.FPS)

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def score(self) -> int:
        ''' Calculate score used to determine player's fitness '''
        hit_rate = self.__controller.shots_hit / self.__controller.shots_fired \
            if self.__controller.shots_fired != 0 else 0.5

        return (self.__controller.score + 1) * 10 * self.__controller.lifespan * (hit_rate ** 2)

    @property
    def fitness(self) -> float:
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness: float) -> None:
        self.__fitness = fitness