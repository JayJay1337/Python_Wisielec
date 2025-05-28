import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout, UILabel
from utils.displayScreen import displayScreen

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()
        anchor = UIAnchorLayout()

        self.vbox = UIBoxLayout(vertical=True, space_between=20)

        self.vbox.add(UILabel(text="USTAWIENIA", font_size=40, text_color=arcade.color.CYAN))

        anchor.add(child = self.vbox, anchor_x="center", anchor_y="center")

        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
