from utils.constants import Constants
from src.controller import Controller

from _thread import start_new_thread
from time import sleep


class GeneticPlayer:
    def __init__(self) -> None:
       self.__controller = Controller()
       self.__fitness = 0
    
    def start(self) -> None:
        start_new_thread(self.start_controller, (self.__controller,))

    def start_controller(self, controller) -> None:
        while True:
            controller.update()
            sleep(1 / Constants.FPS)

    @property
    def controller(self) -> Controller:
        return self.__controller

    @property
    def score(self) -> int:
        return self.__controller.score

    @property
    def fitness(self) -> float:
        return self.__fitness

    @fitness.setter
    def fitness(self, fitness: int) -> None:
        self.__fitness = fitness