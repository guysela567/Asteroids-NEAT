from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from ai.genetic_view import GeneticView


def main() -> None:
    ''' Main method '''
    # controller = Controller()
    # controller.start()
    game = GeneticView(7)
    game.start()


if __name__ == '__main__':
    main()
