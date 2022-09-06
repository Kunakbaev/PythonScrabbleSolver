import setup
import game


if __name__ == '__main__':
    setup.loadNouns()
    gameObj = game.Game()
    gameObj.app.gameObj = gameObj     # very strange line of code
    gameObj.app.run()

