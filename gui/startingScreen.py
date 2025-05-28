import arcade
from arcade.gui import UIManager, UIBoxLayout, UIFlatButton, UIAnchorLayout
from utils.displayScreen import displayScreen

class StaringScreen(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.manager = UIManager()
        self.manager.enable()


        anchor = UIAnchorLayout()


        self.vbox = UIBoxLayout(vertical=True, space_between=20)


        login_button = UIFlatButton(text="Login", width=200)
        self.vbox.add(login_button)
        @login_button.event("on_click")
        def on_click_login(event):
            print("Logged in")
            from loginScreen import LoginScreen
            displayScreen(self.window, self.manager, LoginScreen())



        register_button = UIFlatButton(text="Register", width=200)
        @register_button.event("on_click")
        def on_click_register(event):
            print("Registered")
            from registerScreen import RegisterScreen
            displayScreen(self.window, self.manager, RegisterScreen())

        self.vbox.add(register_button)


        exit_button = UIFlatButton(text="Exit", width=200)
        @exit_button.event("on_click")
        def on_click_exit(event):
            print("Exiting...")
            arcade.close_window()
            arcade.close_window()
        self.vbox.add(exit_button)


        anchor.add(child=self.vbox, anchor_x="center", anchor_y="center")


        self.manager.add(anchor)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

    def on_show_view(self):
        self.manager.enable()
