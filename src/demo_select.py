from utils.drawing import Button, Screen, Image
from utils.constants import Constants


class DemoSelectScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Select Demo')

        self.__title_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 100)
        self.__button_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 40)

        self.__topology_button = Button(self, 0, 400, 400, 100, (255, 255, 255), 'Topology Demo')
        self.__population_button = Button(self, 0, 600, 400, 100, (255, 255, 255), 'Training Demo')

        self.__back_image = Image('assets/sprites/back.png')

        self.__animations: dict[str, int] = {}
        self.reset_animations()

    def reset_animations(self) -> None:
        self.__animations = {
            'title': -200,
            'buttons': -800,
        }

    def apply_animations(self) -> None:
        if self.__animations['title'] < 200:
            self.__animations['title'] += 50
        if self.__animations['buttons'] < self.width * .5 - 200:
            self.__animations['buttons'] += 50

    def draw(self) -> None:
        self.background(0)
        self.apply_animations()

        self.fill(255)
        self.set_font(self.__title_font)
        self.text('Choose Demo', self.width * .5, self.__animations['title'], center=True)
        
        self.set_font(self.__button_font)
        self.__topology_button.x = self.__animations['buttons']
        self.__population_button.x = self.__animations['buttons']
        self.__topology_button.draw()
        self.__population_button.draw()
        self.image(self.__back_image, *Constants.BACK_RECT)

    def on_mouse_down(self) -> None:
        if self.__topology_button.mouse_hover():
            self.redirect('demo-config')

        if self.__population_button.mouse_hover():
            self.redirect('population-demo')

        x, y, w, h = Constants.BACK_RECT
        if x < self.mouse_pos[0] < x + w and y < self.mouse_pos[1] < y + h:
            self.redirect('menu')

    def on_key_down(self, key: int, unicode: str) -> None:
        if key == self.keys['ESCAPE']:
            self.redirect('menu')

    def switch_reset(self) -> None:
        self.reset_animations()