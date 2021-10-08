from src.controller import Controller
from src.view import View

from utils.constants import Constants

from _thread import start_new_thread
from time import sleep

class Population:
    def __init__(self, size) -> None:
        self.__size = size
        self.__controllers = [Controller() for _ in range(self.__size)]
        self.__view = View(self.__controllers[0])

    def start(self) -> None:
        for c in self.__controllers:
            start_new_thread(self.start_controller, (c,))

        print('started')
        self.__view.controller = self.__controllers[1]
        self.__view.start()

    def start_controller(self, controller) -> None:
        while True:
            controller.update()
            sleep(1 / Constants.FPS)