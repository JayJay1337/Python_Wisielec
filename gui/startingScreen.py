import arcade
import sys
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout
from loginScreen import LoginScreen
from registerScreen import RegisterScreen

class MainMenuScreen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()

        # Layout środkowy (do kotwiczenia w centrum ekranu)
        anchor = UIAnchorLayout()

        # Layout pionowy wewnątrz anchor layout
        self.vbox = UIBoxLayout(vertical=True, space_between=20)

        # === LOGIN BUTTON ===
        login_button = UIFlatButton(text="Login", width=200)
        self.vbox.add(login_button)
        @login_button.event("on_click")
        def on_click_login(event):
            print("Logged in")
            self.manager.disable()
            self.window.show_view(LoginScreen())


        # === REGISTER BUTTON ===
        register_button = UIFlatButton(text="Register", width=200)
        @register_button.event("on_click")
        def on_click_register(event):
            print("Registered")
            self.manager.disable()
            self.window.show_view((RegisterScreen()))

        self.vbox.add(register_button)

        # === EXIT BUTTON ===
        exit_button = UIFlatButton(text="Exit", width=200)
        @exit_button.event("on_click")
        def on_click_exit(event):
            print("Exiting...")
            arcade.close_window()
            sys.exit()

        self.vbox.add(exit_button)

        # Dodaj VBox do layoutu kotwiczącego
        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")

        # Dodaj anchor do managera
        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
