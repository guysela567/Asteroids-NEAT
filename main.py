from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from NEAT.population_view import PopulationView


def main() -> None:
    ''' Main method '''

    game = PopulationView(50)
    game.start()


if __name__ == '__main__':
    main()
