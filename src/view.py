from NEAT.population import Population
from utils.drawing import ScreenController
from src.menu import MenuScreen
from src.game import GameScreen
from NEAT.screen import PopulationScreen
from NEAT.demo.screen import DemoScreen
from utils.constants import Constants


class View(ScreenController):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.FPS)

        self.init_screen(GameScreen(), 'game')
        self.init_screen(PopulationScreen(), 'ai')
        self.init_screen(DemoScreen(), 'demo')
        self.init_screen(MenuScreen(), 'menu')
        self.set_screen('menu')