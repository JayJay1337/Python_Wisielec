import arcade
from gui.startingScreen import StartingScreen
from models.init_db import init_db


def main():
    init_db()
    window = arcade.Window(800, 600, "Gra")
    menu_view = StartingScreen()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()