from utils.drawing import Screen, Image
from utils.constants import Constants


class InstructionsScreen(Screen):
    def __init__(self) -> None:
        super().__init__(Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT, 'Instructions')

        # Setup
        self.__title_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 150)
        self.__regular_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 40)
        self.__key_font = self.load_font('assets/fonts/HyperspaceBold.ttf', 23)

        self.__up_arrow = Image.load_by_scale('assets/sprites/controls/up_arrow.png', 3)
        self.__side_arrows = Image.load_by_scale('assets/sprites/controls/side_arrows.png', 3)
        self.__empty_key = Image.load_by_scale('assets/sprites/controls/empty_key.png', 4)

        self.__key_off_x = self.__empty_key.size[0] * .5
        self.__key_off_y = self.__empty_key.size[1] * .5

        self.__back_image = Image('assets/sprites/back.png')

        # Draw once
        self.draw_text()

    def draw_text(self) -> None:
        drawing_y = self.height * .5 - 125
        drawing_gap = 100
        drawing_x = 100

        self.background(0)

        # Title
        self.fill(255)
        self.set_font(self.__title_font)
        self.text('asteroids', self.width * .5, 120, center=True)

        self.fill(Constants.TEXT_COLOR)

        # Enter key
        self.image(self.__empty_key, drawing_x, drawing_y)
        self.set_font(self.__key_font)
        self.text('enter', drawing_x + self.__key_off_x, drawing_y + self.__key_off_y, center=True)
        self.set_font(self.__regular_font)
        self.text('start', drawing_x + 125, drawing_y)

        drawing_y += drawing_gap

        # Up arrow key
        self.image(self.__up_arrow, drawing_x, drawing_y)
        self.text('thrust', drawing_x + 65, drawing_y)

        drawing_y += drawing_gap
        
        # Side arrow keys
        self.image(self.__side_arrows, drawing_x, drawing_y)
        self.text('turn', drawing_x + 130, drawing_y)

        drawing_y += drawing_gap

        # Space key
        self.image(self.__empty_key, drawing_x, drawing_y)
        self.set_font(self.__key_font)
        self.text('space', drawing_x + self.__key_off_x, drawing_y + self.__key_off_y, center=True)
        self.set_font(self.__regular_font)
        self.text('fire', drawing_x + 125, drawing_y)

        drawing_y += drawing_gap
        
        # Escape key
        self.image(self.__empty_key, drawing_x, drawing_y)
        self.set_font(self.__key_font)
        self.text('escape', drawing_x + self.__key_off_x, drawing_y + self.__key_off_y, center=True)
        self.set_font(self.__regular_font)
        self.text('return to menu', drawing_x + 125, drawing_y)

        # Back image
        self.image(self.__back_image, *Constants.BACK_RECT)

    def on_key_down(self, key: int) -> None:
        if key == self.keys['RETURN']:
            self.redirect('game')
        
        elif key == self.keys['ESCAPE']:
            self.redirect('menu')

    def on_mouse_down(self) -> None:
        x, y, w, h = Constants.BACK_RECT
        if x < self.mouse_pos[0] < x + w and y < self.mouse_pos[1] < y + h:
            self.redirect('menu')