from NEAT.population import Population
from utils.drawing import ScreenController
from src.view import View
from NEAT.view import PopulationView
from NEAT.demo.view import DemoView
from utils.constants import Constants


class MasterView(ScreenController):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.FPS)

        self.init_screen(View())
        self.init_screen(PopulationView())
        self.init_screen(DemoView())
        self.set_screen(2)