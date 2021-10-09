from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from ai.pop_view import PopulationView


def main() -> None:
    ''' Main method '''
    # controller = Controller()
    # controller.start()
    game = PopulationView(80)
    game.start()


if __name__ == '__main__':
    main()
