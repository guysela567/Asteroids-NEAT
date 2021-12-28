from NEAT.population import Population
from utils.drawing import ScreenController
from src.menu import MenuScreen
from src.screen import GameScreen
from NEAT.screen import PopulationScreen
from NEAT.demo.screen import DemoScreen
from utils.constants import Constants


class View(ScreenController):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.FPS)

        self.init_screen(GameScreen())
        self.init_screen(PopulationScreen())
        self.init_screen(DemoScreen())
        self.init_screen(MenuScreen())
        self.set_screen(3)