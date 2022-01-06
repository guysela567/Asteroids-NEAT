from utils.drawing import Screen, Button, Image
from utils.constants import Constants


class MenuScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Asteroids Menu')

        self.set_font(self.load_font('assets/fonts/HyperspaceBold.ttf', 40))
        self.__play_button = Button(self, 50, 100, 250, 100, (255, 255, 255), 'PLAY')
        self.__ai_button = Button(self, 50, 250, 250, 100, (255, 255, 255), 'PLAY AI')
        self.__demo_button = Button(self, 50, 400, 250, 100, (255, 255, 255), 'NEAT DEMO')
        self.__quit_button = Button(self, 50, 650, 250, 100, (255, 255, 255), 'QUIT')

        self.__animation_step = 0
        self.__background_animation = [Image(f'assets/sprites/menu/{i}.gif') for i in range(81)]
    
    def draw(self) -> None:
        self.background(0)
        self.image(self.__background_animation[self.__animation_step], 300, 50, 800, 800)
        
        self.__play_button.draw()
        self.__ai_button.draw()
        self.__demo_button.draw()
        self.__quit_button.draw()

        self.__animation_step += 1
        if self.__animation_step == len(self.__background_animation):
            self.__animation_step = 0

    def on_mouse_down(self) -> None:
        if self.__quit_button.mouse_hover():
            self.quit()

        elif self.__play_button.mouse_hover():
            self.set_screen('game')

        elif self.__ai_button.mouse_hover():
            self.set_screen('ai')

        elif self.__demo_button.mouse_hover():
            self.set_screen('demo')
