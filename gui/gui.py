import arcade
from startingScreen import StaringScreen

def main():
    window = arcade.Window(800, 600, "Gra")
    menu_view = StaringScreen()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()