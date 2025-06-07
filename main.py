import arcade
from models.init_db import init_db


def main():
    init_db()
    window = arcade.Window(800, 600, "Gra")
    from gui.startingScreen import StartingScreen
    starting_screen = StartingScreen()
    window.show_view(starting_screen)
    arcade.run()

if __name__ == "__main__":
    main()