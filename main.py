from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from ai.pop_view import PopulationView


def main() -> None:
    ''' Main method '''
    game = PopulationView(85)
    game.start()


if __name__ == '__main__':
    main()
