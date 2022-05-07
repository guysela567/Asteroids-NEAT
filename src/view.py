from utils.drawing import ScreenManager
from utils.constants import Constants

from src.screens.menu import MenuScreen
from src.screens.game import GameScreen
from src.screens.instructions import InstructionsScreen
from src.screens.demo_select import DemoSelectScreen

from NEAT.demo.demo_config import DemoConfigScreen
from NEAT.screen import PopulationScreen
from NEAT.demo.screen import DemoScreen



class View(ScreenManager):
    '''The view inherits from the screen manager and handles all of the screens in the app'''

    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.FPS)

        self.init_screen(GameScreen(), 'game')
        self.init_screen(InstructionsScreen(), 'instructions')
        self.init_screen(PopulationScreen(), 'population-demo')
        self.init_screen(DemoScreen(), 'topology-demo')
        self.init_screen(MenuScreen(), 'menu')
        self.init_screen(DemoSelectScreen(), 'demo-select')
        self.init_screen(DemoConfigScreen(), 'demo-config')

        self.set_screen('menu')