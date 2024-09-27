import sys
from pygame import init, quit
from src.App import App

if __name__ == '__main__':
    init()
    app = App()
    app.run()
    quit()
    sys.exit()
