from source import tools, setup

if __name__ == '__main__':
    game = tools.Game(setup.STATE_DICT, 'menu')
    game.run()
