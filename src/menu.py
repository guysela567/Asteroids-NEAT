from utils.drawing import Screen, Button, Image
from utils.constants import Constants


class MenuScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Asteroids Menu')


        self.font_size(40)
        self.__start_button = Button(self, 100, 100, 250, 100, (255, 255, 255), 'START')
        self.__instructions_button = Button(self, 100, 350, 250, 100, (255, 255, 255), 'INSTRUCTIONS')
        self.__quit_button = Button(self, 100, 600, 250, 100, (255, 255, 255), 'QUIT')
        self.background(100)
    
    def draw(self) -> None:
        self.__start_button.draw()
        self.__instructions_button.draw()
        self.__quit_button.draw()
        self.image(Image('assets/sprites/asteroid1.png'), 425, 150, 500, 500)