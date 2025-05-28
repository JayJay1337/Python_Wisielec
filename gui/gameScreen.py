import arcade
from arcade.gui import UIManager


class GameScreen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        arcade.manager = UIManager()
        self.manager.enable()


