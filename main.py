from game.game import Game
from game.settings import Settings

if __name__ == '__main__':
    settings_obj = Settings()

    while True:
        game = Game(settings_obj)
        game.run()
