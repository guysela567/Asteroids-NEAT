from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from NEAT.view import PopulationView
from src.view import View
from NEAT.demo.view import DemoView


def main() -> None:
    ''' Main method '''

    game = PopulationView()
    game.start()


if __name__ == '__main__':
    main()
