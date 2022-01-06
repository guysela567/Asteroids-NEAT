from utils.drawing import Screen
from utils.constants import Constants


class InstructionsScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Instructions')

        self.__title_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 150)
        self.__regular_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 50)

    def draw(self) -> None:
        self.background(0)
        self.set_font(self.__title_font)
        self.text('Asteroids', self.width * .5, 100, center=True)
        self.set_font(self.__regular_font)
        self.text('<UP ARROW> THRUST', 100, self.height * .5)
        self.text('<SIDE ARROWS> Turn', 100, self.height * .5 + 100)
        self.text('<SPACE> FIRE', 100, self.height * .5 + 200)