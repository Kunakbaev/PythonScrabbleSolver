import setup
from app import MainApp

if __name__ == '__main__':
    setup.loadNouns()
    app = MainApp()
    app.run()
