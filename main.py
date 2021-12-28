from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from src.master_view import MasterView


def main() -> None:
    ''' Main method '''

    game = MasterView()
    game.start()


if __name__ == '__main__':
    main()
