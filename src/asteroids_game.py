from utils.drawing import ScreenManager
from utils.constants import Constants

from src.screens.menu import MenuScreen
from src.screens.game import GameScreen
from src.screens.instructions import InstructionsScreen
from src.screens.demo_select import DemoSelectScreen

from NEAT.demo.demo_config import DemoConfigScreen
from NEAT.pop_screen import PopulationScreen
from NEAT.demo.demo_screen import DemoScreen


class AsteroidsGame:
    '''The view inherits from the screen manager and handles all of the screens in the app'''

    def __init__(self) -> None:
        # Create the screen manager
        self.__view = ScreenManager(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, Constants.FPS)
        # Initialize the screens
        self.__view.init_screen(GameScreen(), 'game')
        self.__view.init_screen(InstructionsScreen(), 'instructions')
        self.__view.init_screen(PopulationScreen(), 'population-demo')
        self.__view.init_screen(DemoScreen(), 'topology-demo')
        self.__view.init_screen(MenuScreen(), 'menu')
        self.__view.init_screen(DemoSelectScreen(), 'demo-select')
        self.__view.init_screen(DemoConfigScreen(), 'demo-config')
        # Set the menu screen as default
        self.__view.set_screen('menu')

    def start(self) -> None:
        self.__view.start()