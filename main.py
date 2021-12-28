from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


from src.view import View


def main() -> None:
    ''' Main method '''

    game = View()
    game.start()


if __name__ == '__main__':
    main()
