from src.controller import Controller


class Population:
    def __init__(self, size):
        self.__size = size
        self.__controllers = [Controller() for _ in range(self.__size)]

    def start(self) -> None:
        for c in self.__controllers:
            c.start()