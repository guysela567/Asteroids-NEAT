from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 


from ai.population import Population


def main() -> None:
    ''' Main method '''
    # controller = Controller()
    # controller.start()
    pop = Population(10)
    pop.start()


if __name__ == '__main__':
    main()
