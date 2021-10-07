from src.controller import Controller
from src.view import View

from time import sleep

class Population:
    def __init__(self, size) -> None:
        self.__view = View()

        self.__size = size
        self.__controllers = [Controller() for _ in range(self.__size)]

    def start(self) -> None:
        self.__view.start()