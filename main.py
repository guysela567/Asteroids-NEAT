from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from NEAT.population_view import PopulationView
from src.view import View


def main() -> None:
    ''' Main method '''

    game = PopulationView(30)
    game.start()


if __name__ == '__main__':
    main()
